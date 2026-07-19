#!/usr/bin/env python3
"""Validated project opening and single-writer locking."""

from __future__ import annotations

import json
import os
import socket
import uuid
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from core.project_manifest import (
    PROJECT_DIRS,
    ProjectManifestError,
    fsync_directory,
    load_project_manifest,
    utc_now_iso,
)


LOCK_FILENAME = ".mxztar-forge.lock"
LOCK_SCHEMA = "mxztar_forge_project_lock"
LOCK_SCHEMA_VERSION = "1.0.0"
MAX_LOCK_BYTES = 64 * 1024


class ProjectAccessError(RuntimeError):
    pass


class ProjectLockedError(ProjectAccessError):
    pass


class ProjectAccessStatus(str, Enum):
    WRITABLE = "writable"
    LOCKED = "locked"
    READ_ONLY_RECOVERY = "read_only_recovery"


@dataclass(frozen=True)
class ProjectLockRecord:
    writer_id: str
    process_id: int
    created_at_utc: str
    host: str


@dataclass(frozen=True)
class ProjectLockLease:
    project_dir: Path
    writer_id: str
    process_id: int
    host: str


@dataclass(frozen=True)
class ProjectOpenAssessment:
    status: ProjectAccessStatus
    project_dir: Path
    manifest: dict | None
    lock: ProjectLockRecord | None
    diagnostics: tuple[str, ...]


def _validate_lock(payload: object) -> ProjectLockRecord:
    if not isinstance(payload, dict):
        raise ProjectAccessError("Project lock root must be a JSON object.")
    if payload.get("lock_schema") != LOCK_SCHEMA:
        raise ProjectAccessError("Project lock schema is unsupported.")
    if payload.get("lock_schema_version") != LOCK_SCHEMA_VERSION:
        raise ProjectAccessError("Project lock schema version is unsupported.")
    for key in ("writer_id", "created_at_utc", "host"):
        if not isinstance(payload.get(key), str) or not payload[key]:
            raise ProjectAccessError(f"Project lock requires non-empty string: {key}")
    process_id = payload.get("process_id")
    if not isinstance(process_id, int) or isinstance(process_id, bool) or process_id <= 0:
        raise ProjectAccessError("Project lock process_id must be a positive integer.")
    return ProjectLockRecord(
        writer_id=payload["writer_id"],
        process_id=process_id,
        created_at_utc=payload["created_at_utc"],
        host=payload["host"],
    )


def read_project_lock(project_dir: Path) -> ProjectLockRecord | None:
    lock_path = Path(project_dir).expanduser().resolve() / LOCK_FILENAME
    if not lock_path.exists() and not lock_path.is_symlink():
        return None
    if lock_path.is_symlink():
        raise ProjectAccessError("Project lock must not be a symbolic link.")
    try:
        if lock_path.stat().st_size > MAX_LOCK_BYTES:
            raise ProjectAccessError("Project lock exceeds the safe size limit.")
        payload = json.loads(lock_path.read_text(encoding="utf-8"))
    except ProjectAccessError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ProjectAccessError(f"Could not validate project lock: {exc}") from exc
    return _validate_lock(payload)


def process_is_alive(process_id: int) -> bool | None:
    """Return True, False, or None when the local process state is unknowable."""
    try:
        os.kill(process_id, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return None
    return True


def _validate_project_structure(project_dir: Path, manifest: dict) -> list[str]:
    diagnostics = []
    required_paths = [Path(relative) for relative in PROJECT_DIRS]
    required_paths.extend((Path("README.md"), Path(manifest["history_path"])))
    for relative in required_paths:
        candidate = project_dir / relative
        if candidate.is_symlink():
            diagnostics.append(f"Canonical project path must not be a symbolic link: {relative}")
        elif relative in (Path("README.md"), Path(manifest["history_path"])):
            if not candidate.is_file():
                diagnostics.append(f"Required project file is missing: {relative}")
        elif not candidate.is_dir():
            diagnostics.append(f"Required project directory is missing: {relative}")
    return diagnostics


def assess_project_open(project_dir: Path) -> ProjectOpenAssessment:
    project_path = Path(project_dir).expanduser().resolve()
    diagnostics: list[str] = []
    manifest = None
    lock = None
    if not project_path.is_dir():
        return ProjectOpenAssessment(
            ProjectAccessStatus.READ_ONLY_RECOVERY,
            project_path,
            None,
            None,
            (f"Project directory does not exist: {project_path}",),
        )
    try:
        manifest = load_project_manifest(project_path)
        diagnostics.extend(_validate_project_structure(project_path, manifest))
    except ProjectManifestError as exc:
        diagnostics.append(str(exc))
    if diagnostics:
        return ProjectOpenAssessment(
            ProjectAccessStatus.READ_ONLY_RECOVERY,
            project_path,
            manifest,
            None,
            tuple(diagnostics),
        )
    try:
        lock = read_project_lock(project_path)
    except ProjectAccessError as exc:
        return ProjectOpenAssessment(
            ProjectAccessStatus.READ_ONLY_RECOVERY,
            project_path,
            manifest,
            None,
            (str(exc), "The uncertain lock was preserved; recovery must be explicit."),
        )
    if lock is None:
        return ProjectOpenAssessment(
            ProjectAccessStatus.WRITABLE, project_path, manifest, None, ()
        )
    if lock.host != socket.gethostname():
        return ProjectOpenAssessment(
            ProjectAccessStatus.LOCKED,
            project_path,
            manifest,
            lock,
            ("Project is locked by a writer on another host or host identity.",),
        )
    alive = process_is_alive(lock.process_id)
    if alive is True:
        return ProjectOpenAssessment(
            ProjectAccessStatus.LOCKED,
            project_path,
            manifest,
            lock,
            ("Project is locked by an active local writer.",),
        )
    reason = (
        "Project lock owner is no longer running. The stale lock was preserved."
        if alive is False
        else "Project lock owner could not be verified. The lock was preserved."
    )
    return ProjectOpenAssessment(
        ProjectAccessStatus.READ_ONLY_RECOVERY,
        project_path,
        manifest,
        lock,
        (reason,),
    )


def acquire_project_lock(project_dir: Path, writer_id: str | None = None) -> ProjectLockLease:
    assessment = assess_project_open(project_dir)
    if assessment.status is not ProjectAccessStatus.WRITABLE:
        raise ProjectLockedError("Project is not available for writable access: " + "; ".join(assessment.diagnostics))
    writer = writer_id or f"writer_{uuid.uuid4().hex}"
    if not isinstance(writer, str) or not writer.strip():
        raise ProjectAccessError("Writer ID must be a non-empty string.")
    record = {
        "lock_schema": LOCK_SCHEMA,
        "lock_schema_version": LOCK_SCHEMA_VERSION,
        "writer_id": writer,
        "process_id": os.getpid(),
        "created_at_utc": utc_now_iso(),
        "host": socket.gethostname(),
    }
    lock_path = assessment.project_dir / LOCK_FILENAME
    try:
        with lock_path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(record, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        fsync_directory(assessment.project_dir)
    except FileExistsError as exc:
        raise ProjectLockedError("Another writer acquired the project lock first.") from exc
    return ProjectLockLease(
        assessment.project_dir, writer, os.getpid(), socket.gethostname()
    )


def release_project_lock(lease: ProjectLockLease) -> None:
    lock_path = lease.project_dir / LOCK_FILENAME
    record = read_project_lock(lease.project_dir)
    if record is None:
        raise ProjectAccessError("Project lock no longer exists.")
    if (
        record.writer_id != lease.writer_id
        or record.process_id != lease.process_id
        or record.host != lease.host
    ):
        raise ProjectAccessError("Refusing to release a project lock owned by another writer.")
    lock_path.unlink()
    fsync_directory(lease.project_dir)
