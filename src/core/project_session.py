#!/usr/bin/env python3
"""Application-owned project session boundary."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from core.paths import PROJECTS_DIR
from core.project_access import (
    ProjectAccessStatus,
    ProjectLockLease,
    ProjectOpenAssessment,
    acquire_project_lock,
    assess_project_open,
    release_project_lock,
)
from core.project_manifest import create_project


class ProjectSessionError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProjectSessionState:
    assessment: ProjectOpenAssessment
    writable: bool


def discover_project_directories(
    projects_root: Path = PROJECTS_DIR, limit: int = 200
) -> tuple[Path, ...]:
    """Return a bounded list of direct, non-symlink project directories."""
    root = Path(projects_root).expanduser().resolve()
    if not root.is_dir() or limit <= 0:
        return ()
    try:
        candidates = tuple(root.iterdir())
    except OSError:
        return ()
    projects = (
        path
        for path in candidates
        if path.is_dir() and not path.is_symlink() and not path.name.startswith(".")
    )
    return tuple(sorted(projects, key=lambda path: path.name.casefold())[:limit])


class ProjectSession:
    """Own at most one attached project and at most one writer lease."""

    def __init__(self, projects_root: Path = PROJECTS_DIR):
        self.projects_root = Path(projects_root).expanduser().resolve()
        self._state: ProjectSessionState | None = None
        self._lease: ProjectLockLease | None = None

    @property
    def state(self) -> ProjectSessionState | None:
        return self._state

    @property
    def project_dir(self) -> Path | None:
        return self._state.assessment.project_dir if self._state else None

    @property
    def is_writable(self) -> bool:
        return self._state is not None and self._state.writable

    def create_and_open(self, project_name: str, primary_goal: str = "") -> ProjectSessionState:
        self._require_detached()
        project_dir, _manifest = create_project(
            project_name,
            primary_goal=primary_goal,
            projects_root=self.projects_root,
        )
        return self.open(project_dir)

    def open(self, project_dir: Path) -> ProjectSessionState:
        self._require_detached()
        assessment = assess_project_open(project_dir)
        if assessment.status is ProjectAccessStatus.WRITABLE:
            lease = acquire_project_lock(assessment.project_dir)
            self._lease = lease
            self._state = ProjectSessionState(assessment=assessment, writable=True)
        else:
            self._state = ProjectSessionState(assessment=assessment, writable=False)
        return self._state

    def close(self) -> None:
        if self._lease is not None:
            release_project_lock(self._lease)
        self._lease = None
        self._state = None

    def _require_detached(self) -> None:
        if self._state is not None or self._lease is not None:
            raise ProjectSessionError("Close the current project before opening another one.")
