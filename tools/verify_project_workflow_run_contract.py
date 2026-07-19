#!/usr/bin/env python3
"""Verify project-owned model-run evidence without calling Ollama."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PIL import Image  # noqa: E402

from brain.service import AgentResult  # noqa: E402
from core.project_session import ProjectSession  # noqa: E402
from core.project_source_intake import import_source_copy, scan_project_source_art  # noqa: E402
from core import project_workflow_run as workflow_module  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def fake_result(source, workflow, ok=True, error=""):
    return AgentResult(
        ok=ok,
        model="fixture-model",
        workflow_key=workflow,
        source_path=str(source),
        output_text='{"fixture": true}' if ok else "",
        error=error,
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mxztar-project-workflow-") as temporary:
        root = Path(temporary)
        projects = root / "projects"
        external = root / "source.png"
        Image.new("RGB", (64, 48), (12, 34, 56)).save(external)

        session = ProjectSession(projects)
        session.create_and_open("Workflow Evidence")
        imported = import_source_copy(session, external)
        source = scan_project_source_art(session)[0]
        project_dir = session.project_dir

        expected_image_bytes = source.path.read_bytes()
        observed_image_bytes = []

        def successful_model_call(source_path, workflow_key, image_bytes, **_):
            observed_image_bytes.append(image_bytes)
            return fake_result(source_path, workflow_key)

        with patch.object(
            workflow_module,
            "run_vision_workflow",
            side_effect=successful_model_call,
        ):
            success = workflow_module.run_project_agent_job(
                session, source, "source_art_intelligence"
            )
        require(
            observed_image_bytes == [expected_image_bytes],
            "model did not receive the exact verified source bytes",
        )

        record = json.loads(success.evidence_path.read_text(encoding="utf-8"))
        require(success.evidence_path.parent == project_dir / "logs", "success evidence escaped logs")
        require(record["status"] == "model_call_succeeded", "model-call status drifted")
        require(record["workflow_complete"] is False, "unvalidated output became completed workflow")
        require(record["approval_state"] == "not_applicable", "run evidence gained approval")
        require(record["provenance"]["source_asset_id"] == imported.record["asset_id"], "source provenance drifted")
        require(record["provenance"]["source_sha256"] == imported.record["sha256"], "source hash provenance drifted")
        require(record["validation"]["structured_findings_validated"] is False, "raw text became validated")
        require(not session.state.assessment.manifest["current_artifact_ids"], "run evidence entered project truth")
        print("PASS: successful model call saves unvalidated project-owned evidence without approval")
        print("PASS: model input bytes exactly match recorded source provenance")

        with patch.object(
            workflow_module,
            "run_vision_workflow",
            side_effect=lambda source_path, workflow_key, **_: fake_result(
                source_path, workflow_key, ok=False, error="fixture Ollama failure"
            ),
        ):
            failure = workflow_module.run_project_agent_job(
                session, source, "source_art_intelligence"
            )
        failed_record = json.loads(failure.evidence_path.read_text(encoding="utf-8"))
        require(failure.evidence_path.parent == project_dir / "diagnostics", "failure escaped diagnostics")
        require(failed_record["status"] == "failed", "failure status drifted")
        require(failed_record["error"] == "fixture Ollama failure", "failure diagnostic was lost")
        print("PASS: failed model call remains a project diagnostic")

        before = set((project_dir / "logs").glob("*.workflow-run.json"))
        def revoke_then_return(source_path, workflow_key, **_):
            session.revoke_writable_authority("fixture authority change")
            return fake_result(source_path, workflow_key)

        with patch.object(workflow_module, "run_vision_workflow", side_effect=revoke_then_return):
            try:
                workflow_module.run_project_agent_job(
                    session, source, "source_art_intelligence"
                )
            except workflow_module.ProjectWorkflowRunError:
                pass
            else:
                raise RuntimeError("authority change did not block evidence save")
        after = set((project_dir / "logs").glob("*.workflow-run.json"))
        require(after == before, "authority change created new evidence")
        print("PASS: authority change during model work blocks the project write")

        session.close()

    print("PASS: project-owned workflow evidence contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
