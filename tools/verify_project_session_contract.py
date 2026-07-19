#!/usr/bin/env python3
"""Verify the project session and truthful Start Here baseline."""

from __future__ import annotations

import tempfile
import time
from pathlib import Path
from unittest.mock import patch

from PySide6.QtWidgets import QApplication

from core.project_access import LOCK_FILENAME, ProjectAccessStatus
from core import project_session as session_module
from core.project_access import ProjectLockedError, acquire_project_lock, release_project_lock
from core.project_manifest import create_project
from core.project_session import (
    ProjectSession,
    ProjectSessionError,
    discover_project_directories,
)
from qt_app import MXZTARForgeWindow
from qt_panels.start_here_panel import StartHerePanel


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    app = QApplication.instance() or QApplication([])
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        writer_session = ProjectSession(root)
        panel = StartHerePanel(writer_session)
        panel.profile_fields["project_name"].setText("Session Contract")
        panel.profile_fields["primary_goal"].setText("Verify truthful project authority.")
        panel.create_current_project()
        project_dir = root / "session-contract"
        require(writer_session.is_writable, "created project did not acquire a writer lease")
        require((project_dir / LOCK_FILENAME).is_file(), "writer lock was not created")
        require(not panel.create_project_button.isEnabled(), "active session allows another create")
        require(panel.close_project_button.isEnabled(), "active session cannot be closed")
        print("PASS: Start Here creates one canonical writable project session")

        reader_session = ProjectSession(root)
        reader_panel = StartHerePanel(reader_session)
        index = reader_panel.project_selector.findData(str(project_dir))
        require(index >= 0, "created project was not discoverable")
        reader_panel.project_selector.setCurrentIndex(index)
        reader_panel.open_selected_project()
        require(reader_session.state is not None, "locked project was not attached")
        require(not reader_session.is_writable, "second session became a writer")
        require(
            reader_session.state.assessment.status is ProjectAccessStatus.LOCKED,
            "second session did not report the active lock",
        )
        require((project_dir / LOCK_FILENAME).is_file(), "read-only attachment changed the lock")
        reader_panel.close_project()
        require(
            "no writer lease was held or released" in reader_panel.status_label.text(),
            "read-only detach claimed a writer release",
        )
        print("PASS: locked projects attach visibly without writable authority")

        require(panel.close_project(), "writer session did not close")
        require(not (project_dir / LOCK_FILENAME).exists(), "project close leaked its writer lock")
        print("PASS: explicit project close releases the owning writer lease")

        damaged_dir, _ = create_project("Damaged Project", projects_root=root)
        (damaged_dir / "source" / "originals").rmdir()
        damaged_session = ProjectSession(root)
        damaged_state = damaged_session.open(damaged_dir)
        require(not damaged_state.writable, "damaged project opened writable")
        require(
            damaged_state.assessment.status is ProjectAccessStatus.READ_ONLY_RECOVERY,
            "damaged project did not enter recovery",
        )
        require(not (damaged_dir / LOCK_FILENAME).exists(), "recovery attachment created a lock")
        damaged_session.close()
        print("PASS: recovery projects remain attached read-only and unmodified")

        outside_dir, _ = create_project("Outside Root", projects_root=root / "outside")
        try:
            ProjectSession(root).open(outside_dir)
        except ProjectSessionError:
            pass
        else:
            raise AssertionError("out-of-root project was accepted")
        symlink_path = root / "symlink-project"
        symlink_path.symlink_to(outside_dir, target_is_directory=True)
        try:
            ProjectSession(root).open(symlink_path)
        except ProjectSessionError:
            pass
        else:
            raise AssertionError("symlinked project was accepted")
        print("PASS: sessions reject symlinked and out-of-root project paths")

        bounded_paths = [root / f"entry-{index}" for index in range(4)]
        for path in bounded_paths:
            path.mkdir()
        bounded_entries = iter(bounded_paths)
        with patch.object(Path, "iterdir", return_value=bounded_entries):
            require(len(discover_project_directories(root, limit=2)) <= 2, "discovery exceeded limit")
            require(next(bounded_entries).name == "entry-2", "discovery consumed beyond its limit")
        print("PASS: synchronous project discovery bounds directory enumeration")

        discovery_panel = StartHerePanel(ProjectSession(root))
        with patch(
            "qt_panels.start_here_panel.discover_project_directories",
            side_effect=ProjectSessionError("permission denied"),
        ):
            discovery_panel.refresh_projects()
        require(
            "permission denied" in discovery_panel.status_label.text(),
            "project discovery error was hidden",
        )
        print("PASS: project discovery failures remain visible to the user")

        partial_dir, _ = create_project("Partial Release", projects_root=root)
        partial_session = ProjectSession(root)
        partial_session.open(partial_dir)

        def partial_release(lease):
            (lease.project_dir / LOCK_FILENAME).unlink()
            raise OSError("directory fsync failed")

        with patch.object(session_module, "release_project_lock", side_effect=partial_release):
            partial_result = partial_session.close()
        require(partial_session.state is None, "partial release retained writable authority")
        require(partial_result.warning is not None, "partial release durability warning was hidden")
        print("PASS: partial lock release clears authority and reports durability uncertainty")

        race_dir, _ = create_project("Acquisition Race", projects_root=root)
        race_session = ProjectSession(root)
        competing_lease = None

        def lose_race(path):
            nonlocal competing_lease
            competing_lease = acquire_project_lock(path, "writer_competitor")
            raise ProjectLockedError("race lost")

        with patch.object(session_module, "acquire_project_lock", side_effect=lose_race):
            race_state = race_session.open(race_dir)
        require(not race_state.writable, "race loser retained writable authority")
        require(
            race_state.assessment.status is ProjectAccessStatus.LOCKED,
            "race loser did not attach the locked project",
        )
        race_session.close()
        require(competing_lease is not None, "race fixture did not acquire competing lock")
        release_project_lock(competing_lease)
        print("PASS: an acquisition-race loser attaches the project as locked")

        shutdown_dir, _ = create_project("Shutdown Contract", projects_root=root)
        shutdown_session = ProjectSession(root)
        shutdown_session.open(shutdown_dir)
        window = MXZTARForgeWindow(shutdown_session)
        window.show()
        window.close()
        deadline = time.monotonic() + 5
        while window.isVisible() and time.monotonic() < deadline:
            app.processEvents()
        require(not window.isVisible(), "application shutdown did not complete")
        require(shutdown_session.state is None, "application retained its project session")
        require(not (shutdown_dir / LOCK_FILENAME).exists(), "application shutdown leaked the lock")
        print("PASS: application shutdown releases the session-owned writer lease")

        panel.deleteLater()
        reader_panel.deleteLater()
        discovery_panel.deleteLater()
        window.deleteLater()
        app.processEvents()

    print("PASS: project session and Start Here contract verified")


if __name__ == "__main__":
    main()
