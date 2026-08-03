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
from core.project_authoring_workflow import (  # noqa: E402
    create_fresh_project,
    switch_project,
)
from core.project_session import ProjectSession, ProjectSessionError  # noqa: E402
from core.shape_document import load_shape_document  # noqa: E402
from qt_editor_app import EDITOR_PAGE_INDEX  # noqa: E402
from qt_editor_authoring_app import AuthoringEditorForgeWindow  # noqa: E402
import qt_project_menu_and_rename as project_ui  # noqa: E402
import qt_project_menu_review_fixes as project_review_fixes  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def select_combo_data(combo, value: str) -> None:
    index = combo.findData(value)
    require(index >= 0, f"project chooser contains {Path(value).name}")
    combo.setCurrentIndex(index)


def main() -> int:
    project_ui.install_project_menu_and_rename()
    project_review_fixes.install_project_menu_review_fixes()
    QApplication.instance() or QApplication([])
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
        window.editor_panel.select_cad_object(None)
        require(
            not window.editor_panel.delete_selected_action.isEnabled()
            and not window.editor_panel.delete_selected_shape_object(confirm=False)
            and len(window.editor_panel.document["objects"]) == 2
            and len(window.editor_panel.object_scene["objects"]) == 2,
            "direct deletion requires an explicit selection and never targets the last shape",
        )
        selected_object = window.editor_panel.object_scene["objects"][-1]
        window.editor_panel.select_cad_object(selected_object["object_id"])
        deleted_source_id = selected_object["source_shape_id"]
        require(
            window.editor_panel.delete_selected_action.isEnabled(),
            "direct deletion enables after one valid shape/object is selected",
        )
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

        invalid_target = projects_root.parent / "outside-canonical-projects"
        try:
            switch_project(session, invalid_target)
        except ProjectSessionError as exc:
            require(
                session.project_dir == first_project
                and session.state is not None
                and "restored" in str(exc).lower(),
                "failed project switching restores the previously open project authority",
            )
        else:
            raise AssertionError("invalid project switch unexpectedly succeeded")

        second_session = ProjectSession(projects_root)
        second_state = second_session.create_and_open(
            "Second Authoring Project",
            "Verify project switching",
        )
        second_project = second_state.assessment.project_dir
        second_session.close()

        window.start_here_panel.refresh_projects()
        window.editor_panel.refresh_project_choices()
        select_combo_data(window.start_here_panel.project_selector, str(second_project))
        require(
            window.editor_panel.project_selector.currentData() == str(second_project)
            and session.project_dir == first_project,
            "Start Here selection is shared with Editor without switching authority",
        )
        require(
            window.start_here_panel.project_switch_action.isEnabled(),
            "Start Here enables Switch Project for the shared target",
        )
        window.start_here_panel.project_switch_action.trigger()
        require(
            session.project_dir == second_project,
            "Start Here Switch Project menu action changes authority to the shared target",
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
        window.start_here_panel.refresh_projects()
        select_combo_data(window.editor_panel.project_selector, str(first_project))
        require(
            window.start_here_panel.project_selector.currentData() == str(first_project)
            and session.project_dir == second_project,
            "Editor selection is shared with Start Here without switching authority",
        )
        require(
            window.editor_panel.project_switch_action.isEnabled(),
            "Editor enables Switch Project for the shared target",
        )
        window.editor_panel.project_switch_action.trigger()
        require(
            session.project_dir == first_project,
            "Editor Switch Project menu action changes authority back to the shared target",
        )
        require(
            window.editor_panel.document is not None
            and window.editor_panel.document["document_id"] == first_document_id,
            "Editor project switching reloads that project's document chooser and document",
        )

        original_create_and_open = session.create_and_open

        def fail_create_and_open(_project_name: str, _primary_goal: str = ""):
            raise OSError("simulated fresh-project storage failure")

        session.create_and_open = fail_create_and_open
        try:
            create_fresh_project(session)
        except ProjectSessionError as exc:
            require(
                session.project_dir == first_project
                and session.state is not None
                and "restored" in str(exc).lower(),
                "failed fresh-project creation restores the previously open project authority",
            )
        else:
            raise AssertionError("simulated fresh-project failure unexpectedly succeeded")
        finally:
            session.create_and_open = original_create_and_open

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
