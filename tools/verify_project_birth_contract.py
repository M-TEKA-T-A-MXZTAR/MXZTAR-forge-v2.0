#!/usr/bin/env python3
"""Verify Purpose-driven Project Birth and its official Editor handoff."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PySide6.QtWidgets import QApplication  # noqa: E402

from core.project_manifest import (  # noqa: E402
    MAX_PROJECT_DISPLAY_NAME_CHARS,
    load_project_manifest,
    project_name_from_purpose,
    project_slug,
)
from core.project_session import ProjectSession  # noqa: E402
from qt_editor_app import EditorForgeWindow  # noqa: E402
from qt_panels import my_library_panel as library_module  # noqa: E402
from qt_panels.start_here_panel import StartHerePanel  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    app = QApplication.instance() or QApplication([])

    with tempfile.TemporaryDirectory(prefix="mxztar-project-birth-") as temporary:
        root = Path(temporary) / "projects"
        session = ProjectSession(root)
        panel = StartHerePanel(session)

        require(
            panel.project_actions_layout.itemAt(0).widget() is panel.purpose_label,
            "Purpose label is not first on the lower project-authority row",
        )
        require(
            panel.project_actions_layout.itemAt(1).widget() is panel.purpose_edit,
            "Purpose input is not in the moved project-action position",
        )
        require(
            panel.project_actions_layout.itemAt(2).widget() is panel.create_project_button,
            "Create Project is not positioned to the right of Purpose",
        )
        require(
            panel.project_actions_layout.itemAt(3).widget() is panel.close_project_button,
            "Close Project is not positioned to the right of Create Project",
        )
        require(not panel.create_project_button.isEnabled(), "blank Purpose enabled creation")
        require(not panel.close_project_button.isEnabled(), "detached panel enabled close")
        print("PASS: Start Here exposes the required two-row Project Authority layout")

        panel.purpose_edit.setText("---")
        require(
            not panel.create_project_button.isEnabled(),
            "non-identifying punctuation enabled project creation",
        )

        purpose = "Build reusable engine-panel shapes from this source art"
        expected_name = project_name_from_purpose(purpose)
        expected_dir = root / project_slug(expected_name)
        panel.purpose_edit.setText(purpose)
        require(panel.create_project_button.isEnabled(), "valid Purpose did not enable creation")
        panel.create_current_project()

        require(session.is_writable, "Project Birth did not acquire writable authority")
        require(session.project_dir == expected_dir, "Project Birth derived an unexpected slug")
        manifest = load_project_manifest(expected_dir)
        require(manifest["project_name"] == expected_name, "derived display name was not stored")
        require(manifest["primary_goal"] == purpose, "exact Purpose was not stored in project.json")

        history_lines = (expected_dir / manifest["history_path"]).read_text(
            encoding="utf-8"
        ).splitlines()
        require(len(history_lines) == 1, "Project Birth did not create exactly one first event")
        first_event = json.loads(history_lines[0])
        require(first_event["event"] == "project_created", "first event is not project_created")
        require(first_event["purpose"] == purpose, "first event did not preserve Purpose")
        require(
            f"Purpose: {purpose}" in (expected_dir / "README.md").read_text(encoding="utf-8"),
            "project README did not expose the stored Purpose",
        )
        require(not panel.purpose_edit.isEnabled(), "attached project allowed Purpose editing")
        require(not panel.create_project_button.isEnabled(), "attached project allowed another create")
        require(panel.close_project_button.isEnabled(), "attached project cannot be closed")
        print("PASS: Project Birth preserves Purpose, derives identity, and records first history")

        require(panel.close_project(), "Project Birth session did not close")
        require(panel.purpose_edit.isEnabled(), "detached panel did not re-enable Purpose")
        require(panel.purpose_edit.text() == "", "closing a project left stale Purpose text")

        panel.refresh_projects()
        index = panel.project_selector.findData(str(expected_dir))
        require(index >= 0, "created project was not discoverable after close")
        panel.project_selector.setCurrentIndex(index)
        panel.open_selected_project()
        require(panel.purpose_edit.text() == purpose, "reopen did not display project Purpose")
        require(not panel.purpose_edit.isEnabled(), "reopened project allowed Purpose editing")
        require(panel.close_project(), "reopened project did not close")
        print("PASS: closing clears fresh input and reopening restores project Purpose")

        long_purpose = "Design a modular propulsion housing system " + ("with service panels " * 8)
        long_name = project_name_from_purpose(long_purpose)
        require(
            len(long_name) <= MAX_PROJECT_DISPLAY_NAME_CHARS,
            "derived display name exceeded its contract bound",
        )
        require(project_slug(long_name), "bounded display name did not produce a safe slug")
        print("PASS: long Purpose text derives a bounded display name and safe slug")

        guided_root = Path(temporary) / "guided-projects"
        guided_session = ProjectSession(guided_root)
        with patch.object(library_module, "scan_source_art", return_value=[]):
            window = EditorForgeWindow(guided_session)
            window.start_here_panel.purpose_edit.setText("Create a reusable panel shape")
            window.refresh_guided_next_step()
            require(
                window.next_step_button.text() == "Next: Create project",
                "official guidance did not identify Project Birth",
            )
            require(
                window._guided_target is window.start_here_panel.create_project_button,
                "official guidance did not target Create Project",
            )
            window.perform_guided_next_step()
            require(guided_session.is_writable, "guided Project Birth did not open writable")
            require(
                window.next_step_button.text() == "Next: New blank document",
                "Project Birth did not offer the blank Editor path",
            )
            require(
                window._guided_target is window.editor_panel.new_button,
                "blank-document guidance did not target the Editor control",
            )
            window.perform_guided_next_step()
            require(window.editor_panel.has_open_document(), "guided blank document was not created")
            require(
                window.pages.currentWidget() is window.editor_panel,
                "guided blank document did not navigate to Editor",
            )
            guided_session.close()
            window.deleteLater()
        print("PASS: official guided flow moves from Purpose to project to blank Editor document")

        panel.deleteLater()
        app.processEvents()

    print("PASS: Purpose-driven Project Birth contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
