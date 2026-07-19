#!/usr/bin/env python3
"""Save truthful local-model run evidence inside the active Forge project."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from pathlib import Path

from brain.service import DEFAULT_MODEL, AgentResult, run_vision_workflow
from core.project_manifest import APPLICATION_VERSION, atomic_write_text, utc_now_iso
from core.project_session import ProjectSession, ProjectSessionError
from core.project_source_intake import scan_project_source_art
from core.source_library import SourceArtItem


RUN_EVIDENCE_SCHEMA = "mxztar_forge_workflow_run_evidence"
RUN_EVIDENCE_VERSION = "1.0.0"


class ProjectWorkflowRunError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProjectWorkflowRunResult:
    agent_result: AgentResult
    evidence_path: Path


def _validated_project_source(
    session: ProjectSession, source: SourceArtItem
) -> SourceArtItem:
    if not session.is_writable or session.state is None or session.project_dir is None:
        raise ProjectSessionError("A writable project session is required.")
    project_id = session.state.assessment.manifest["project_id"]
    if (
        source.authority != "active_project"
        or not source.asset_id
        or source.project_id != project_id
    ):
        raise ProjectWorkflowRunError(
            "Workflow source must belong to the active writable project."
        )
    for canonical in scan_project_source_art(session):
        if canonical.asset_id == source.asset_id and canonical.path == source.path:
            return canonical
    raise ProjectWorkflowRunError(
        "Selected source is not a canonical source of the active project."
    )


def run_project_agent_job(
    session: ProjectSession,
    source: SourceArtItem,
    workflow_key: str,
    user_notes: str = "",
    model: str = DEFAULT_MODEL,
) -> ProjectWorkflowRunResult:
    """Run the model, then save unvalidated evidence without claiming project truth."""
    canonical = _validated_project_source(session, source)
    project_dir = session.project_dir
    project_id = session.state.assessment.manifest["project_id"]
    started_at = utc_now_iso()

    result = run_vision_workflow(
        source_path=canonical.path,
        workflow_key=workflow_key,
        user_notes=user_notes,
        model=model,
    )

    if (
        not session.is_writable
        or session.state is None
        or session.project_dir != project_dir
        or session.state.assessment.manifest["project_id"] != project_id
    ):
        raise ProjectWorkflowRunError(
            "Project authority changed during the model run; no evidence was saved."
        )

    completed_at = utc_now_iso()
    run_id = f"run_{uuid.uuid4().hex}"
    status = "model_call_succeeded" if result.ok else "failed"
    directory = project_dir / ("logs" if result.ok else "diagnostics")
    evidence_path = directory / f"{run_id}.workflow-run.json"
    evidence = {
        "schema_name": RUN_EVIDENCE_SCHEMA,
        "schema_version": RUN_EVIDENCE_VERSION,
        "run_id": run_id,
        "project_id": project_id,
        "workflow_key": workflow_key,
        "status": status,
        "workflow_complete": False,
        "approval_state": "not_applicable",
        "started_at_utc": started_at,
        "completed_at_utc": completed_at,
        "application_version": APPLICATION_VERSION,
        "execution": {
            "model_provider": "ollama",
            "model_name": model,
            "host_mode": "local",
            "parallel_limit": 1,
            "triggered_by": "user",
            "worker_type": "qt_thread_worker",
        },
        "provenance": {
            "source_asset_id": canonical.asset_id,
            "source_project_id": canonical.project_id,
            "source_path": canonical.path.relative_to(project_dir).as_posix(),
        },
        "raw_model_output": result.output_text,
        "error": result.error or None,
        "validation": {
            "structured_findings_validated": False,
            "note": (
                "This record is model-run evidence only. It is not an approved finding, "
                "shape, brief, recommendation, or completed workflow artifact."
            ),
        },
    }
    atomic_write_text(
        evidence_path,
        json.dumps(evidence, indent=2, ensure_ascii=False) + "\n",
    )
    return ProjectWorkflowRunResult(result, evidence_path)
