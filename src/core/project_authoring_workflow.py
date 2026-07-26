#!/usr/bin/env python3
"""Safe project switching and fresh Editor project creation."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import NoReturn

from core.project_session import ProjectSession, ProjectSessionError, ProjectSessionState


FRESH_PROJECT_PREFIX = "Fresh Forge Project"
FRESH_PROJECT_PURPOSE = "Fresh Editor document"
MAX_FRESH_NAME_ATTEMPTS = 100


def _restore_previous_project(
    session: ProjectSession,
    previous_project: Path | None,
    original_error: Exception,
    action: str,
) -> NoReturn:
    """Best-effort restore the previous authority before reporting an authoring failure."""
    if previous_project is None:
        raise ProjectSessionError(f"{action} failed: {original_error}") from original_error

    try:
        restored = session.open(previous_project)
    except Exception as restore_error:
        raise ProjectSessionError(
            f"{action} failed: {original_error}. The previous project could not be restored: "
            f"{restore_error}"
        ) from original_error

    status = "writable" if restored.writable else "read-only"
    raise ProjectSessionError(
        f"{action} failed: {original_error}. The previous project was restored {status}."
    ) from original_error


def switch_project(session: ProjectSession, project_dir: str | Path) -> ProjectSessionState:
    """Close current authority, open the target, and restore current authority on failure."""
    target = Path(project_dir).expanduser().resolve()
    if session.project_dir is not None and session.project_dir.resolve() == target:
        if session.state is None:
            raise ProjectSessionError("The current project state is unavailable.")
        return session.state

    previous_project = session.project_dir.resolve() if session.project_dir is not None else None
    if session.state is not None:
        session.close()
    try:
        return session.open(target)
    except Exception as exc:
        _restore_previous_project(session, previous_project, exc, "Project switch")


def create_fresh_project(
    session: ProjectSession,
    *,
    timestamp: datetime | None = None,
) -> ProjectSessionState:
    """Create a uniquely named project and restore current authority on failure."""
    previous_project = session.project_dir.resolve() if session.project_dir is not None else None
    if session.state is not None:
        session.close()

    moment = timestamp or datetime.now()
    stem = f"{FRESH_PROJECT_PREFIX} {moment:%Y-%m-%d %H-%M-%S}"
    last_error: Exception | None = None
    for attempt in range(1, MAX_FRESH_NAME_ATTEMPTS + 1):
        name = stem if attempt == 1 else f"{stem} {attempt}"
        try:
            return session.create_and_open(name, FRESH_PROJECT_PURPOSE)
        except FileExistsError as exc:
            last_error = exc
            continue
        except Exception as exc:
            _restore_previous_project(session, previous_project, exc, "Fresh project creation")

    allocation_error = ProjectSessionError(
        f"Could not allocate a unique fresh project after {MAX_FRESH_NAME_ATTEMPTS} attempts."
    )
    if last_error is not None:
        allocation_error.__cause__ = last_error
    _restore_previous_project(
        session,
        previous_project,
        allocation_error,
        "Fresh project creation",
    )
