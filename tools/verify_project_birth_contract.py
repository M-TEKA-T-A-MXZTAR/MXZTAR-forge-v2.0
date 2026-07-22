#!/usr/bin/env python3
"""Verify Purpose-driven Project Birth and official project-to-Editor routing."""

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
from core.shape_document import create_blank_shape_document  # noqa: E402
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
        require(
            [action.text() for action in panel.open_project_menu.actions()]
            == ["Open Project", "Go to Project"],
            "Open Selected does not expose the two real project-routing choices",
        )
        require(not panel.create_project_button.isEnabled(), "blank Purpose enabled creation")
        require(not panel.close_project_button.isEnabled(), "detached panel enabled close")
        print("PASS: Start Here exposes Project Birth and project-routing controls")

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
        panel.open_project_action.trigger()
        require(panel.purpose_edit.text() == purpose, "reopen did not display project Purpose")
        require(not panel.purpose_edit.isEnabled(), "reopened project allowed Purpose editing")
        require(panel.close_project(), "reopened project did not close")
        print("PASS: Open Project attaches authority without leaving Start Here")

        long_purpose = "Design a modular propulsion housing system " + ("with service panels " * 8)
        long_name = project_name_from_purpose(long_purpose)
        require(
            len(long_name) <= MAX_PROJECT_DISPLAY_NAME_CHARS,
            "derived display name exceeded its contract bound",
        )
        require(project_slug(long_name), "bounded display name did not produce a safe slug")
        print("PASS: long Purpose text derives a bounded display name and safe slug")

        profile_state = {
            "project_name": "MXZTAR Forge v2.0",
            "project_role": "Local creative-concept engineering forge",
            "creator_name": "",
            "brand_presence": "",
            "primary_goal": "Keep this optional profile note once.",
            "workflow_focus": "Reusable shape editing",
            "updated_utc": "",
        }

        def fake_load_profile() -> dict[str, str]:
            return dict(profile_state)

        def fake_save_profile(profile: dict[str, str]) -> dict[str, str]:
            for key in tuple(profile_state):
                profile_state[key] = str(profile.get(key, profile_state[key])).strip()
            return dict(profile_state)

        with (
            patch("qt_panels.start_here_panel.load_profile", side_effect=fake_load_profile),
            patch("qt_panels.start_here_panel.save_profile", side_effect=fake_save_profile),
            patch("qt_panels.start_here_panel.load_settings_notes", return_value=""),
        ):
            profile_panel = StartHerePanel(ProjectSession(Path(temporary) / "profile-projects"))
            require(
                profile_panel.notes_edit.toPlainText() == profile_state["primary_goal"],
                "optional profile notes were decorated with UI labels on load",
            )
            profile_panel.save_fields()
            profile_panel.load_all()
            profile_panel.save_fields()
            require(
                profile_state["primary_goal"] == "Keep this optional profile note once.",
                "repeated profile saves compounded labels or workflow context",
            )
            profile_panel.deleteLater()
        print("PASS: optional profile notes remain stable across repeated load/save cycles")

        guided_root = Path(temporary) / "guided-projects"
        guided_session = ProjectSession(guided_root)
        with patch.object(library_module, "scan_source_art", return_value=[]):
            window = EditorForgeWindow(guided_session)
            require(
                window.sidebar.currentRow() == 1
                and window.pages.currentWidget() is window.start_here_panel,
                "official launcher did not begin on Start Here",
            )
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
                window._guided_target is window.editor_panel.document_button,
                "blank-document guidance did not target the Document menu",
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

        navigation_root = Path(temporary) / "navigation-projects"
        seed_session = ProjectSession(navigation_root)
        seed_state = seed_session.create_and_open(
            "Existing Project Build", "Open the current project build in Editor"
        )
        create_blank_shape_document(seed_session, title="Existing Build Document")
        seed_dir = seed_state.assessment.project_dir
        seed_session.close()

        navigation_session = ProjectSession(navigation_root)
        with patch.object(library_module, "scan_source_art", return_value=[]):
            navigation_window = EditorForgeWindow(navigation_session)
            project_index = navigation_window.start_here_panel.project_selector.findData(
                str(seed_dir)
            )
            require(project_index >= 0, "existing project was not available in Start Here")
            navigation_window.start_here_panel.project_selector.setCurrentIndex(project_index)
            navigation_window.start_here_panel.go_to_project_action.trigger()
            app.processEvents()
            require(navigation_session.is_writable, "Go to Project did not acquire project authority")
            require(
                navigation_window.pages.currentWidget() is navigation_window.editor_panel,
                "Go to Project did not navigate to Editor",
            )
            require(
                navigation_window.editor_panel.document is not None
                and navigation_window.editor_panel.document["title"] == "Existing Build Document",
                "Editor did not display the selected project's current build",
            )
            navigation_session.close()
            navigation_window.deleteLater()
        print("PASS: Go to Project opens Editor and displays the current project build")

        panel.deleteLater()
        app.processEvents()

    print("PASS: Purpose-driven Project Birth and routing contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
