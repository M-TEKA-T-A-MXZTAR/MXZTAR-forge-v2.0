#!/usr/bin/env python3
"""Recoverable project deletion through an application-owned Project Trash."""

from __future__ import annotations

import json
import os
import stat
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path

from core.project_access import (
    ProjectLockLease,
    acquire_project_lock,
    release_project_lock,
)
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
            # Cleanup is best-effort; preserve the original receipt-write failure.
            pass
        raise


def _remove_installed_receipt(project_dir: Path) -> None:
    """Remove a receipt durably before a moved project is rolled back."""
    receipt_path = project_dir / PROJECT_TRASH_RECEIPT
    if not receipt_path.exists() and not receipt_path.is_symlink():
        return
    metadata = receipt_path.lstat()
    if not stat.S_ISREG(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
        raise ProjectSessionError(
            "Project Trash rollback found an unsafe recovery-receipt path."
        )
    receipt_path.unlink()
    fsync_directory(project_dir)


def _lease_at(lease: ProjectLockLease, project_dir: Path) -> ProjectLockLease:
    """Point the same owned lease at the directory after an atomic rename."""
    return replace(lease, project_dir=project_dir)


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
    """Move one selected project into recoverable trash under an exclusive lease."""
    target = _validated_project_target(session, project_dir)
    moment = timestamp or datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)

    with session.mutation_guard():
        state = session.state
        active = bool(
            session.project_dir is not None
            and session.project_dir.resolve() == target
            and state is not None
        )
        if active and not state.writable:
            raise ProjectSessionError(
                "The active project is attached read-only or locked by another writer and "
                "cannot be moved to Project Trash."
            )

        if active:
            close_result = session.close()
            if close_result.warning:
                _restore_active_session_after_failure(
                    session,
                    target,
                    ProjectSessionError(close_result.warning),
                )

        try:
            deletion_lease = acquire_project_lock(
                target,
                writer_id=f"project_trash_{os.getpid()}",
            )
        except Exception as exc:
            error = ProjectSessionError(
                f"Could not acquire exclusive Project Trash authority: {exc}"
            )
            if active:
                _restore_active_session_after_failure(session, target, error)
            raise error from exc

        lease_location = target
        trash_root: Path | None = None
        destination: Path | None = None
        moved = False
        try:
            trash_root = _prepare_trash_root(session)
            destination = _allocate_destination(trash_root, target, moment)
            target.rename(destination)
            moved = True
            lease_location = destination
            fsync_directory(session.projects_root)
            fsync_directory(trash_root)

            _write_receipt(
                destination,
                target,
                moved_at=moment,
                was_active=active,
            )
            release_project_lock(_lease_at(deletion_lease, destination))
        except Exception as exc:
            rollback_error: Exception | None = None
            release_error: Exception | None = None

            if moved and destination is not None and trash_root is not None:
                try:
                    _remove_installed_receipt(destination)
                    destination.rename(target)
                    lease_location = target
                    fsync_directory(session.projects_root)
                    fsync_directory(trash_root)
                except Exception as rollback_exc:
                    rollback_error = rollback_exc

            try:
                release_project_lock(_lease_at(deletion_lease, lease_location))
            except Exception as cleanup_exc:
                release_error = cleanup_exc

            if rollback_error is not None:
                suffix = (
                    f" The deletion lease also could not be released: {release_error}."
                    if release_error is not None
                    else ""
                )
                raise ProjectSessionError(
                    f"Project moved toward Project Trash, but automatic rollback failed: "
                    f"{rollback_error}.{suffix}"
                ) from exc

            if release_error is not None:
                raise ProjectSessionError(
                    f"Project Trash failed and the project was restored, but its deletion "
                    f"lease could not be released: {release_error}"
                ) from exc

            if active:
                _restore_active_session_after_failure(session, target, exc)
            raise ProjectSessionError(
                f"Project Trash failed; the project remained or was restored at its "
                f"canonical path: {exc}"
            ) from exc

    if destination is None:
        raise ProjectSessionError("Project Trash completed without a destination path.")
    return ProjectTrashResult(
        original_project_dir=target,
        trashed_project_dir=destination,
        was_active=active,
    )
