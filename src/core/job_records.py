#!/usr/bin/env python3
"""Read legacy MXZTAR Forge agent records without creating new project authority."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from core.agent_runner import WORKFLOW_OUTPUT_DIRS


MAX_JOB_RECORDS = 500
MAX_RECORD_BYTES = 2 * 1024 * 1024


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
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return JobRecord(path=path, status="INVALID", error=f"Could not read record: {exc}")


def scan_job_records(
    should_stop: Callable[[], bool] | None = None,
    limit: int = MAX_JOB_RECORDS,
) -> list[JobRecord]:
    """Discover recent legacy records from the runner's existing output directories."""
    stop = should_stop or (lambda: False)
    candidates: list[tuple[int, Path]] = []

    for directory in sorted(set(WORKFLOW_OUTPUT_DIRS.values()), key=str):
        if stop() or not directory.exists():
            continue
        try:
            paths = directory.glob("*.json")
            for path in paths:
                if stop():
                    return []
                try:
                    if path.is_symlink() or not path.is_file():
                        continue
                    candidates.append((path.stat().st_mtime_ns, path))
                except OSError:
                    continue
        except OSError:
            continue

    candidates.sort(key=lambda pair: pair[0], reverse=True)
    records = []
    for _, path in candidates[: max(0, limit)]:
        if stop():
            return []
        records.append(read_job_record(path))
    return records
