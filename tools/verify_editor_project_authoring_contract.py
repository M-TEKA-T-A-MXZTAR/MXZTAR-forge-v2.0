#!/usr/bin/env python3
"""Verify fresh Editor startup, project switching, and direct paired deletion."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PySide6.QtWidgets import QApplication  # noqa: E402

from core.object_scene import load_object_scene  # noqa: E402
from core.project_session import ProjectSession  # noqa: E402
from core.shape_document import load_shape_document  # noqa: E402
from qt_editor_app import EDITOR_PAGE_INDEX  # noqa: E402
from qt_editor_authoring_app import AuthoringEditorForgeWindow  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def select_combo_data(combo, value: str) -> None:
    index = combo.findData(value)
    require(index >= 0, f"project chooser contains {Path(value).name}")
    combo.setCurrentIndex(index)


def main() -> int:
    app = QApplication.instance() or QApplication([])
    with tempfile.TemporaryDirectory(prefix="mxztar-editor-authoring-") as temporary:
        projects_root = Path(temporary) / "projects"
        session = ProjectSession(projects_root)
        window = AuthoringEditorForgeWindow(session)

        require(session.state is None, "Forge starts detached when no project was selected")
        window.open_page(EDITOR_PAGE_INDEX)
        require(
            session.state is not None and session.is_writable,
            "entering Editor with no project creates writable fresh project authority",
        )
        require(
            window.editor_panel.document is not None,
            "entering Editor with no project opens a fresh blank document",
        )
        first_project = session.project_dir
        first_document_id = window.editor_panel.document["document_id"]
        require(
            window.start_here_panel.project_selector.isEnabled()
            and window.start_here_panel.new_project_document_button.isEnabled(),
            "Start Here keeps project switching and fresh-project controls available",
        )
        require(
            window.editor_panel.project_selector.count() >= 1
            and window.editor_panel.document_selector.count() >= 1,
            "Editor exposes both project and document choosers",
        )

        window.editor_panel.add_rectangle_command()
        window.editor_panel.add_square_command()
        require(
            len(window.editor_panel.document["objects"]) == 2
            and len(window.editor_panel.object_scene["objects"]) == 2,
            "two created shapes are synchronized into paired 3D objects",
        )
        deleted_source_id = window.editor_panel._selected_source_shape_id()
        require(
            window.editor_panel.delete_selected_shape_object(confirm=False),
            "Delete Selected Shape/Object succeeds without using Undo",
        )
        require(
            len(window.editor_panel.document["objects"]) == 1
            and len(window.editor_panel.object_scene["objects"]) == 1,
            "direct deletion removes the selected item from both 2D and 3D",
        )
        require(
            deleted_source_id
            not in {item["object_id"] for item in window.editor_panel.document["objects"]},
            "deleted source shape is absent from active document state",
        )
        reloaded_document = load_shape_document(session, first_document_id).document
        reloaded_scene = load_object_scene(session, first_document_id)
        require(
            len(reloaded_document["objects"]) == 1
            and len(reloaded_scene["objects"]) == 1,
            "paired deletion persists across document and scene reload",
        )

        second_session = ProjectSession(projects_root)
        second_state = second_session.create_and_open(
            "Second Authoring Project",
            "Verify project switching",
        )
        second_project = second_state.assessment.project_dir
        second_session.close()

        window.start_here_panel.refresh_projects()
        select_combo_data(window.start_here_panel.project_selector, str(second_project))
        switched = window.start_here_panel.open_selected_project()
        require(
            switched is not None and session.project_dir == second_project,
            "Start Here switches safely from an attached project to another project",
        )
        require(
            window.start_here_panel.project_selector.isEnabled(),
            "Start Here project chooser remains available after switching",
        )

        window.open_page(EDITOR_PAGE_INDEX)
        require(
            window.editor_panel.document is not None,
            "Editor creates a blank document when the switched project has none",
        )
        window.editor_panel.refresh_project_choices()
        select_combo_data(window.editor_panel.project_selector, str(first_project))
        switched_back = window.editor_panel.switch_selected_project()
        require(
            switched_back is not None and session.project_dir == first_project,
            "Editor project chooser switches authority back to the first project",
        )
        require(
            window.editor_panel.document is not None
            and window.editor_panel.document["document_id"] == first_document_id,
            "Editor project switching reloads that project's document chooser and document",
        )

        fresh_state = window.start_here_project_controller.create_fresh_project_document()
        require(
            fresh_state is not None
            and session.project_dir not in {first_project, second_project}
            and window.editor_panel.document is not None,
            "New Project + Document creates and opens a distinct fresh authoring project",
        )

        window.editor_panel.add_circle_command()
        window.editor_panel.set_project_mutation_active(True, "contract work")
        require(
            not window.editor_panel.switch_project_button.isEnabled()
            and not window.editor_panel.new_project_document_button.isEnabled()
            and not window.editor_panel.delete_selected_action.isEnabled(),
            "active work blocks Editor project switching, fresh creation, and deletion",
        )
        window.editor_panel.set_project_mutation_active(False, "contract work")
        require(
            window.editor_panel.new_project_document_button.isEnabled()
            and window.editor_panel.delete_selected_action.isEnabled(),
            "Editor authoring controls restore after active work finishes",
        )

        window.deleteLater()
        if session.state is not None:
            session.close()

    print("PASS: Editor project authoring contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
