#!/usr/bin/env python3
"""Recoverable project deletion through an application-owned Project Trash."""

from __future__ import annotations

import json
import os
import stat
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from core.project_access import read_project_lock
from core.project_manifest import fsync_directory
from core.project_session import ProjectSession, ProjectSessionError


PROJECT_TRASH_DIRNAME = ".project-trash"
PROJECT_TRASH_RECEIPT = ".mxztar-forge-trash-receipt.json"
PROJECT_TRASH_SCHEMA = "mxztar_forge_project_trash_receipt"
PROJECT_TRASH_SCHEMA_VERSION = "1.0.0"
MAX_TRASH_NAME_ATTEMPTS = 1000


@dataclass(frozen=True)
class ProjectTrashResult:
    original_project_dir: Path
    trashed_project_dir: Path
    was_active: bool


def _validated_project_target(session: ProjectSession, project_dir: str | Path) -> Path:
    unresolved = Path(project_dir).expanduser()
    if not unresolved.is_absolute():
        unresolved = Path.cwd() / unresolved
    if unresolved.is_symlink():
        raise ProjectSessionError("Project Trash will not move a symbolic-link project path.")
    target = unresolved.resolve()
    if target.parent != session.projects_root:
        raise ProjectSessionError(
            f"Project Trash accepts only direct children of: {session.projects_root}"
        )
    if target.name.startswith("."):
        raise ProjectSessionError("Hidden project directories cannot be moved to Project Trash.")
    try:
        metadata = target.lstat()
    except FileNotFoundError as exc:
        raise ProjectSessionError(f"Selected project does not exist: {target}") from exc
    except OSError as exc:
        raise ProjectSessionError(f"Could not inspect selected project: {exc}") from exc
    if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
        raise ProjectSessionError("Selected project must be a real non-symlink directory.")
    return target


def _prepare_trash_root(session: ProjectSession) -> Path:
    root = session.projects_root / PROJECT_TRASH_DIRNAME
    if root.exists() or root.is_symlink():
        metadata = root.lstat()
        if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
            raise ProjectSessionError("Project Trash path must be a real directory.")
    else:
        try:
            root.mkdir(mode=0o700, parents=False, exist_ok=False)
            fsync_directory(session.projects_root)
        except OSError as exc:
            raise ProjectSessionError(f"Could not create Project Trash: {exc}") from exc
    return root


def _allocate_destination(trash_root: Path, target: Path, moment: datetime) -> Path:
    stem = f"{moment:%Y%m%dT%H%M%SZ}-{target.name}"
    for attempt in range(MAX_TRASH_NAME_ATTEMPTS):
        suffix = "" if attempt == 0 else f"-{attempt + 1}"
        candidate = trash_root / f"{stem}{suffix}"
        if not candidate.exists() and not candidate.is_symlink():
            return candidate
    raise ProjectSessionError(
        f"Could not allocate a unique Project Trash destination after "
        f"{MAX_TRASH_NAME_ATTEMPTS} attempts."
    )


def _write_receipt(
    trashed_project: Path,
    original_project: Path,
    *,
    moved_at: datetime,
    was_active: bool,
) -> None:
    receipt_path = trashed_project / PROJECT_TRASH_RECEIPT
    temporary = trashed_project / f"{PROJECT_TRASH_RECEIPT}.tmp"
    payload = {
        "schema": PROJECT_TRASH_SCHEMA,
        "schema_version": PROJECT_TRASH_SCHEMA_VERSION,
        "moved_at_utc": moved_at.astimezone(timezone.utc).isoformat(),
        "original_project_dir": str(original_project),
        "trashed_project_dir": str(trashed_project),
        "was_active": bool(was_active),
        "recovery_note": (
            "This project was moved out of the canonical projects list. Restore only "
            "after validating the destination name and ensuring no project with the "
            "original name already exists."
        ),
    }
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(temporary, flags, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, receipt_path)
        fsync_directory(trashed_project)
    except Exception:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def _restore_active_session_after_failure(
    session: ProjectSession,
    original_project: Path,
    original_error: Exception,
) -> None:
    try:
        session.open(original_project)
    except Exception as restore_error:
        raise ProjectSessionError(
            f"Project Trash failed: {original_error}. The previously active project "
            f"could not be reopened: {restore_error}"
        ) from original_error
    raise ProjectSessionError(
        f"Project Trash failed: {original_error}. The previously active project was reopened."
    ) from original_error


def move_project_to_trash(
    session: ProjectSession,
    project_dir: str | Path,
    *,
    timestamp: datetime | None = None,
) -> ProjectTrashResult:
    """Move one selected project into recoverable trash without following symlinks."""
    target = _validated_project_target(session, project_dir)
    active = bool(
        session.project_dir is not None
        and session.project_dir.resolve() == target
        and session.state is not None
    )
    moment = timestamp or datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)

    with session.mutation_guard():
        if active:
            close_result = session.close()
            if close_result.warning:
                _restore_active_session_after_failure(
                    session,
                    target,
                    ProjectSessionError(close_result.warning),
                )
        else:
            try:
                lock = read_project_lock(target)
            except Exception as exc:
                raise ProjectSessionError(
                    f"Could not validate the selected project's writer lock: {exc}"
                ) from exc
            if lock is not None:
                raise ProjectSessionError(
                    "Selected project is locked by another writer and cannot be moved to "
                    "Project Trash."
                )

        try:
            trash_root = _prepare_trash_root(session)
            destination = _allocate_destination(trash_root, target, moment)
            target.rename(destination)
            fsync_directory(session.projects_root)
            fsync_directory(trash_root)
        except Exception as exc:
            if active:
                _restore_active_session_after_failure(session, target, exc)
            raise ProjectSessionError(f"Could not move project to Project Trash: {exc}") from exc

        try:
            _write_receipt(
                destination,
                target,
                moved_at=moment,
                was_active=active,
            )
        except Exception as exc:
            rollback_error = None
            try:
                destination.rename(target)
                fsync_directory(session.projects_root)
                fsync_directory(trash_root)
            except Exception as rollback_exc:
                rollback_error = rollback_exc
            if rollback_error is not None:
                raise ProjectSessionError(
                    f"Project moved to {destination}, but its trash receipt failed and "
                    f"automatic rollback also failed: {rollback_error}"
                ) from exc
            if active:
                _restore_active_session_after_failure(session, target, exc)
            raise ProjectSessionError(
                f"Project Trash receipt failed; the project was restored: {exc}"
            ) from exc

    return ProjectTrashResult(
        original_project_dir=target,
        trashed_project_dir=destination,
        was_active=active,
    )
