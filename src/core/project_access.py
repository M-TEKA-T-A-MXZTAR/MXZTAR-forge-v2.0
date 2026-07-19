#!/usr/bin/env python3
"""Validated project opening and single-writer locking."""

from __future__ import annotations

import json
import os
import socket
import stat
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
    acquisition_id: str
    boot_id: str | None
    process_start_id: str | None


@dataclass(frozen=True)
class ProjectLockLease:
    project_dir: Path
    writer_id: str
    process_id: int
    host: str
    acquisition_id: str


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
    for key in ("writer_id", "created_at_utc", "host", "acquisition_id"):
        if not isinstance(payload.get(key), str) or not payload[key]:
            raise ProjectAccessError(f"Project lock requires non-empty string: {key}")
    process_id = payload.get("process_id")
    if not isinstance(process_id, int) or isinstance(process_id, bool) or process_id <= 0:
        raise ProjectAccessError("Project lock process_id must be a positive integer.")
    for key in ("boot_id", "process_start_id"):
        value = payload.get(key, object())
        if value is not None and (not isinstance(value, str) or not value):
            raise ProjectAccessError(f"Project lock {key} must be null or a non-empty string.")
    return ProjectLockRecord(
        writer_id=payload["writer_id"],
        process_id=process_id,
        created_at_utc=payload["created_at_utc"],
        host=payload["host"],
        acquisition_id=payload["acquisition_id"],
        boot_id=payload["boot_id"],
        process_start_id=payload["process_start_id"],
    )


def read_project_lock(project_dir: Path) -> ProjectLockRecord | None:
    lock_path = Path(project_dir).expanduser().resolve() / LOCK_FILENAME
    if not lock_path.exists() and not lock_path.is_symlink():
        return None
    try:
        metadata = lock_path.lstat()
        if not stat.S_ISREG(metadata.st_mode):
            raise ProjectAccessError("Project lock must be a regular file.")
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(lock_path, flags)
        with os.fdopen(descriptor, "r", encoding="utf-8") as handle:
            opened_metadata = os.fstat(handle.fileno())
            if not stat.S_ISREG(opened_metadata.st_mode):
                raise ProjectAccessError("Project lock must be a regular file.")
            if opened_metadata.st_size > MAX_LOCK_BYTES:
                raise ProjectAccessError("Project lock exceeds the safe size limit.")
            text = handle.read(MAX_LOCK_BYTES + 1)
        if len(text.encode("utf-8")) > MAX_LOCK_BYTES:
            raise ProjectAccessError("Project lock exceeds the safe size limit.")
        payload = json.loads(text)
    except ProjectAccessError:
        raise
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
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


def process_identity(process_id: int) -> tuple[str, str] | None:
    """Return Linux boot and process-start identities, or None when unverifiable."""
    try:
        boot_id = Path("/proc/sys/kernel/random/boot_id").read_text(encoding="ascii").strip()
        stat_path = (
            Path("/proc/self/stat")
            if process_id == os.getpid()
            else Path(f"/proc/{process_id}/stat")
        )
        stat_text = stat_path.read_text(encoding="ascii")
        process_fields_after_name = stat_text[stat_text.rindex(")") + 2 :].split()
        process_start_id = process_fields_after_name[19]
    except (OSError, UnicodeError, IndexError):
        return None
    if not boot_id or not process_start_id:
        return None
    return boot_id, process_start_id


def _validate_project_structure(project_dir: Path, manifest: dict) -> list[str]:
    diagnostics = []
    required_paths = [Path(relative) for relative in PROJECT_DIRS]
    required_paths.extend((Path("README.md"), Path(manifest["history_path"])))
    for relative in required_paths:
        candidate = project_dir / relative
        components = tuple(relative.parents)[::-1][1:] + (relative,)
        symlink = next(
            (component for component in components if (project_dir / component).is_symlink()),
            None,
        )
        if symlink is not None:
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
    manifest_path = project_path / "project.json"
    if manifest_path.is_symlink():
        return ProjectOpenAssessment(
            ProjectAccessStatus.READ_ONLY_RECOVERY,
            project_path,
            None,
            None,
            ("Canonical project path must not be a symbolic link: project.json",),
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
        live_identity = process_identity(lock.process_id)
        recorded_identity = (lock.boot_id, lock.process_start_id)
        if live_identity is None or None in recorded_identity:
            return ProjectOpenAssessment(
                ProjectAccessStatus.READ_ONLY_RECOVERY,
                project_path,
                manifest,
                lock,
                ("Project lock owner identity could not be verified. The lock was preserved.",),
            )
        if live_identity != recorded_identity:
            return ProjectOpenAssessment(
                ProjectAccessStatus.READ_ONLY_RECOVERY,
                project_path,
                manifest,
                lock,
                ("Project lock PID was reused or its boot identity changed. The stale lock was preserved.",),
            )
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
    if len(writer.encode("utf-8")) > 256:
        raise ProjectAccessError("Writer ID exceeds the 256-byte limit.")
    identity = process_identity(os.getpid())
    boot_id, process_start_id = identity if identity is not None else (None, None)
    acquisition_id = f"lock_{uuid.uuid4().hex}"
    record = {
        "lock_schema": LOCK_SCHEMA,
        "lock_schema_version": LOCK_SCHEMA_VERSION,
        "writer_id": writer,
        "process_id": os.getpid(),
        "created_at_utc": utc_now_iso(),
        "host": socket.gethostname(),
        "acquisition_id": acquisition_id,
        "boot_id": boot_id,
        "process_start_id": process_start_id,
    }
    serialized = json.dumps(record, indent=2) + "\n"
    if len(serialized.encode("utf-8")) > MAX_LOCK_BYTES:
        raise ProjectAccessError("Serialized project lock exceeds the safe size limit.")
    lock_path = assessment.project_dir / LOCK_FILENAME
    created_identity: tuple[int, int] | None = None
    try:
        with lock_path.open("x", encoding="utf-8", newline="\n") as handle:
            created = os.fstat(handle.fileno())
            created_identity = (created.st_dev, created.st_ino)
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        fsync_directory(assessment.project_dir)
    except FileExistsError as exc:
        raise ProjectLockedError("Another writer acquired the project lock first.") from exc
    except Exception:
        if created_identity is not None:
            try:
                current = lock_path.lstat()
                if (current.st_dev, current.st_ino) == created_identity:
                    lock_path.unlink()
                    fsync_directory(assessment.project_dir)
            except OSError:
                # Best-effort cleanup must not mask the original acquisition failure.
                pass
        raise
    return ProjectLockLease(
        assessment.project_dir,
        writer,
        os.getpid(),
        socket.gethostname(),
        acquisition_id,
    )


def release_project_lock(lease: ProjectLockLease) -> None:
    lock_path = lease.project_dir / LOCK_FILENAME
    record = read_project_lock(lease.project_dir)
    if record is None:
        raise ProjectAccessError("Project lock no longer exists.")
    if os.getpid() != lease.process_id or socket.gethostname() != lease.host:
        raise ProjectAccessError("Only the lease-owning process may release its project lock.")
    if (
        record.writer_id != lease.writer_id
        or record.process_id != lease.process_id
        or record.host != lease.host
        or record.acquisition_id != lease.acquisition_id
    ):
        raise ProjectAccessError("Refusing to release a project lock owned by another writer.")
    lock_path.unlink()
    fsync_directory(lease.project_dir)
