#!/usr/bin/env python3
"""Verify the project session and truthful Start Here baseline."""

from __future__ import annotations

import tempfile
import time
from pathlib import Path

from PySide6.QtWidgets import QApplication

from core.project_access import LOCK_FILENAME, ProjectAccessStatus
from core.project_manifest import create_project
from core.project_session import ProjectSession
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
        window.deleteLater()
        app.processEvents()

    print("PASS: project session and Start Here contract verified")


if __name__ == "__main__":
    main()
