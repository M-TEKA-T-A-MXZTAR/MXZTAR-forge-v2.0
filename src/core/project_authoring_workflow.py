#!/usr/bin/env python3
"""Safe project switching and fresh Editor project creation."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from core.project_session import ProjectSession, ProjectSessionError, ProjectSessionState


FRESH_PROJECT_PREFIX = "Fresh Forge Project"
FRESH_PROJECT_PURPOSE = "Fresh Editor document"
MAX_FRESH_NAME_ATTEMPTS = 100


def switch_project(session: ProjectSession, project_dir: str | Path) -> ProjectSessionState:
    """Close the current authority, then open one selected canonical project."""
    target = Path(project_dir).expanduser().resolve()
    if session.project_dir is not None and session.project_dir.resolve() == target:
        if session.state is None:
            raise ProjectSessionError("The current project state is unavailable.")
        return session.state

    if session.state is not None:
        session.close()
    return session.open(target)


def create_fresh_project(
    session: ProjectSession,
    *,
    timestamp: datetime | None = None,
) -> ProjectSessionState:
    """Create one uniquely named project after safely closing current authority."""
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

    raise ProjectSessionError(
        f"Could not allocate a unique fresh project after {MAX_FRESH_NAME_ATTEMPTS} attempts."
    ) from last_error
