#!/usr/bin/env python3
"""Application-owned project session boundary."""

from __future__ import annotations

import itertools
import stat
from dataclasses import dataclass
from pathlib import Path

from core.paths import PROJECTS_DIR
from core.project_access import (
    ProjectAccessStatus,
    ProjectLockedError,
    ProjectLockLease,
    ProjectOpenAssessment,
    acquire_project_lock,
    assess_project_open,
    read_project_lock,
    release_project_lock,
)
from core.project_manifest import create_project


class ProjectSessionError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProjectSessionState:
    assessment: ProjectOpenAssessment
    writable: bool


@dataclass(frozen=True)
class ProjectSessionCloseResult:
    released_writer: bool
    warning: str | None = None


def discover_project_directories(
    projects_root: Path = PROJECTS_DIR, limit: int = 200
) -> tuple[Path, ...]:
    """Return a bounded list of direct, non-symlink project directories."""
    root = Path(projects_root).expanduser().resolve()
    if limit <= 0:
        return ()
    try:
        root_metadata = root.stat()
        if not stat.S_ISDIR(root_metadata.st_mode):
            raise ProjectSessionError(f"Projects root is not a directory: {root}")
        projects = []
        for path in itertools.islice(root.iterdir(), limit):
            metadata = path.lstat()
            if (
                stat.S_ISDIR(metadata.st_mode)
                and not stat.S_ISLNK(metadata.st_mode)
                and not path.name.startswith(".")
            ):
                projects.append(path)
    except FileNotFoundError:
        return ()
    except OSError as exc:
        raise ProjectSessionError(f"Could not discover projects in {root}: {exc}") from exc
    return tuple(sorted(projects, key=lambda path: path.name.casefold()))


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
        project_path = self._validated_direct_child(project_dir)
        assessment = assess_project_open(project_path)
        if assessment.status is ProjectAccessStatus.WRITABLE:
            try:
                lease = acquire_project_lock(assessment.project_dir)
            except ProjectLockedError:
                assessment = assess_project_open(assessment.project_dir)
                if assessment.status is ProjectAccessStatus.WRITABLE:
                    raise
                self._state = ProjectSessionState(assessment=assessment, writable=False)
            else:
                self._lease = lease
                self._state = ProjectSessionState(assessment=assessment, writable=True)
        else:
            self._state = ProjectSessionState(assessment=assessment, writable=False)
        return self._state

    def close(self) -> ProjectSessionCloseResult:
        released_writer = self._lease is not None
        if self._lease is not None:
            try:
                release_project_lock(self._lease)
            except Exception as exc:
                try:
                    lock = read_project_lock(self._lease.project_dir)
                except Exception:
                    raise exc
                if lock is not None:
                    raise exc
                self._lease = None
                self._state = None
                return ProjectSessionCloseResult(
                    released_writer=True,
                    warning=f"Writer lock was removed but directory durability could not be confirmed: {exc}",
                )
        self._lease = None
        self._state = None
        return ProjectSessionCloseResult(released_writer=released_writer)

    def _require_detached(self) -> None:
        if self._state is not None or self._lease is not None:
            raise ProjectSessionError("Close the current project before opening another one.")

    def _validated_direct_child(self, project_dir: Path) -> Path:
        unresolved = Path(project_dir).expanduser()
        if not unresolved.is_absolute():
            unresolved = Path.cwd() / unresolved
        if unresolved.is_symlink():
            raise ProjectSessionError("Project path must not be a symbolic link.")
        if unresolved.parent.resolve() != self.projects_root:
            raise ProjectSessionError(
                f"Project must be a direct child of the canonical projects root: {self.projects_root}"
            )
        return unresolved.resolve()
