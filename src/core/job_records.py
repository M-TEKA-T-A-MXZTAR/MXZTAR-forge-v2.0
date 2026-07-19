#!/usr/bin/env python3
"""Read legacy MXZTAR Forge agent records without creating new project authority."""

from __future__ import annotations

import json
import heapq
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from core.agent_runner import WORKFLOW_OUTPUT_DIRS
from core.project_workflow_run import RUN_EVIDENCE_SCHEMA, RUN_EVIDENCE_VERSION


MAX_JOB_RECORDS = 500
MAX_RECORD_BYTES = 2 * 1024 * 1024
MAX_AGGREGATE_RECORD_BYTES = 16 * 1024 * 1024
MAX_SCAN_DIAGNOSTICS = 20


@dataclass(frozen=True)
class JobRecord:
    path: Path
    status: str
    created_utc: str = ""
    workflow_key: str = ""
    model: str = ""
    source_path: str = ""
    output_text: str = ""
    error: str = ""


@dataclass(frozen=True)
class JobScanResult:
    records: tuple[JobRecord, ...]
    diagnostics: tuple[str, ...] = ()
    omitted_for_byte_budget: int = 0


def _text(value: object) -> str:
    return value if isinstance(value, str) else ""


def read_job_record(path: Path) -> JobRecord:
    """Return a truthful view of one saved record, including malformed records."""
    try:
        size = path.stat().st_size
        if size > MAX_RECORD_BYTES:
            return JobRecord(path=path, status="INVALID", error="Record exceeds the 2 MiB UI read limit.")

        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("record root is not a JSON object")

        if payload.get("schema_name") == RUN_EVIDENCE_SCHEMA:
            if payload.get("schema_version") != RUN_EVIDENCE_VERSION:
                return JobRecord(path=path, status="INVALID", error="Unsupported run-evidence schema version.")
            evidence_status = payload.get("status")
            if evidence_status == "model_call_succeeded":
                status = "MODEL_OK"
            elif evidence_status == "failed":
                status = "FAILED"
            else:
                return JobRecord(path=path, status="INVALID", error="Run evidence has an invalid status.")
            execution = payload.get("execution")
            provenance = payload.get("provenance")
            if not isinstance(execution, dict) or not isinstance(provenance, dict):
                return JobRecord(path=path, status="INVALID", error="Run evidence metadata is incomplete.")
            return JobRecord(
                path=path,
                status=status,
                created_utc=_text(payload.get("completed_at_utc") or payload.get("started_at_utc")),
                workflow_key=_text(payload.get("workflow_key")),
                model=_text(execution.get("model_name")),
                source_path=_text(provenance.get("source_path")),
                output_text=_text(payload.get("raw_model_output")),
                error=_text(payload.get("error")),
            )

        ok = payload.get("ok")
        if ok is True:
            status = "SUCCESS"
        elif ok is False:
            status = "FAILED"
        else:
            return JobRecord(path=path, status="INVALID", error="Record has no boolean 'ok' field.")

        return JobRecord(
            path=path,
            status=status,
            created_utc=_text(payload.get("created_utc")),
            workflow_key=_text(payload.get("workflow_key")),
            model=_text(payload.get("model")),
            source_path=_text(payload.get("source_path")),
            output_text=_text(payload.get("output_text")),
            error=_text(payload.get("error")),
        )
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError, ValueError) as exc:
        return JobRecord(path=path, status="INVALID", error=f"Could not read record: {exc}")


def scan_job_records(
    should_stop: Callable[[], bool] | None = None,
    limit: int = MAX_JOB_RECORDS,
    path_filter: Callable[[Path], bool] | None = None,
    project_dir: Path | None = None,
) -> JobScanResult:
    """Discover recent legacy and active-project run-evidence records."""
    stop = should_stop or (lambda: False)
    candidate_heap: list[tuple[int, str, int, Path]] = []
    diagnostics: list[str] = []

    def note(message: str) -> None:
        if len(diagnostics) < MAX_SCAN_DIAGNOSTICS:
            diagnostics.append(message)

    directories = set(WORKFLOW_OUTPUT_DIRS.values())
    if project_dir is not None:
        project_root = Path(project_dir).resolve()
        for name in ("logs", "diagnostics"):
            directory = project_root / name
            if (
                directory.is_dir()
                and not directory.is_symlink()
                and directory.resolve().parent == project_root
            ):
                directories.add(directory)

    for directory in sorted(directories, key=str):
        if stop() or not directory.exists():
            continue
        try:
            paths = directory.iterdir()
            for path in paths:
                if stop():
                    return JobScanResult(())
                try:
                    if (
                        path.suffix.lower() != ".json"
                        or (path_filter is not None and not path_filter(path))
                        or path.is_symlink()
                        or not path.is_file()
                    ):
                        continue
                    stat = path.stat()
                    entry = (stat.st_mtime_ns, str(path), stat.st_size, path)
                    if len(candidate_heap) < max(0, limit):
                        heapq.heappush(candidate_heap, entry)
                    elif candidate_heap and entry > candidate_heap[0]:
                        heapq.heapreplace(candidate_heap, entry)
                except OSError as exc:
                    note(f"Could not inspect job record {path}: {exc}")
                    continue
        except OSError as exc:
            note(f"Could not scan job directory {directory}: {exc}")
            continue

    candidates = sorted(candidate_heap, reverse=True)
    records = []
    decoded_bytes = 0
    omitted = 0
    for _, _, size, path in candidates:
        if stop():
            return JobScanResult(())
        if decoded_bytes + min(size, MAX_RECORD_BYTES) > MAX_AGGREGATE_RECORD_BYTES:
            omitted += 1
            continue
        records.append(read_job_record(path))
        decoded_bytes += min(size, MAX_RECORD_BYTES)
    return JobScanResult(tuple(records), tuple(diagnostics), omitted)
