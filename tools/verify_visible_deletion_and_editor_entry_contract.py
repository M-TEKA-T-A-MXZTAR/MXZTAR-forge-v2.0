#!/usr/bin/env python3
"""Verify conclusive deletion feedback and unclipped Editor entry."""

from __future__ import annotations

import os
import sys
import tempfile
import time
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PySide6.QtCore import QPoint, QSettings  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

import qt_editor_authoring_app as authoring_app  # noqa: E402
import qt_live_acceptance_guards as live_guards  # noqa: E402
from core.project_session import ProjectSession  # noqa: E402
from core.shape_document import create_blank_shape_document  # noqa: E402
from qt_app import SETTINGS_APP, SETTINGS_ORG  # noqa: E402
from qt_editor_app import EDITOR_PAGE_INDEX, START_HERE_PAGE_INDEX  # noqa: E402


SHAPE_DIR = Path("structures/shape-documents")
SCENE_DIR = Path("structures/object-scenes")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def process(app: QApplication) -> None:
    app.processEvents()
    app.processEvents()


def close_safely(window, app: QApplication) -> None:
    if window is None:
        return
    window.close()
    deadline = time.monotonic() + 10.0
    while window.isVisible() and time.monotonic() < deadline:
        process(app)
        time.sleep(0.01)
    if window.isVisible():
        window.jobs_panel.request_scan_shutdown()
        window.library_panel.request_thumbnail_shutdown()
        window.shape_panel.request_scan_shutdown()
        deadline = time.monotonic() + 10.0
        while (
            window.jobs_panel.has_active_scan()
            or window.library_panel.has_active_thumbnail_loading()
            or window.shape_panel.has_active_scan()
        ) and time.monotonic() < deadline:
            process(app)
            time.sleep(0.01)
        window.close()
        process(app)
    window.deleteLater()
    process(app)


def main() -> int:
    live_guards.install_live_acceptance_guards()

    with tempfile.TemporaryDirectory(prefix="mxztar-visible-deletion-") as temporary:
        root = Path(temporary)
        settings_root = root / "settings"
        settings_root.mkdir()
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        QSettings.setPath(
            QSettings.Format.IniFormat,
            QSettings.Scope.UserScope,
            str(settings_root),
        )

        app = QApplication.instance() or QApplication([])
        app.setOrganizationName(SETTINGS_ORG)
        app.setApplicationName(SETTINGS_APP)
        settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
        settings.clear()
        settings.sync()

        projects_root = root / "projects"
        session = ProjectSession(projects_root)
        session.create_and_open(
            "Visible Deletion Contract",
            "Verify unmistakable deletion and unclipped Editor entry",
        )

        window = None
        try:
            window = authoring_app.AuthoringEditorForgeWindow(session)
            window.resize(980, 760)
            window.show()
            process(app)

            start_panel = window.start_here_panel
            controller = window.start_here_project_controller
            require(
                hasattr(start_panel, "project_management_layout")
                and start_panel.project_management_layout.indexOf(
                    controller.delete_project_button
                )
                >= 0
                and start_panel.project_actions_layout.indexOf(
                    controller.delete_project_button
                )
                < 0,
                "Start Here exposes project deletion in a dedicated management row",
            )
            require(
                hasattr(start_panel, "project_trash_feedback_label"),
                "Start Here exposes separate near-field Project Trash feedback",
            )

            scrollbar = window.page_scroll.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
            window.open_page(EDITOR_PAGE_INDEX)
            process(app)
            require(
                scrollbar.value() == scrollbar.minimum(),
                "entering Editor starts at the top instead of clipping text below the fixed strip",
            )

            panel = window.editor_panel
            require(
                getattr(
                    type(panel).delete_selected_project,
                    "_mxztar_selection_confirmation",
                    False,
                )
                and "yes/cancel" in panel.delete_project_button.toolTip().lower()
                and "typing" not in panel.delete_project_button.toolTip().lower()
                and "yes/cancel"
                in controller.delete_project_button.toolTip().lower()
                and "typing"
                not in controller.delete_project_button.toolTip().lower(),
                "project deletion uses selection plus a simple Yes/Cancel confirmation",
            )

            first_document_id = panel.document["document_id"]
            panel.create_blank_document()
            process(app)
            second_document_id = panel.document["document_id"]
            panel.add_circle_command()
            process(app)

            unopened_result = create_blank_shape_document(session)
            unopened_document_id = unopened_result.document["document_id"]
            unopened_scene_path = (
                session.project_dir
                / SCENE_DIR
                / f"{unopened_document_id}.object-scene.json"
            )
            panel.refresh_documents(second_document_id)
            process(app)
            require(
                panel.document["document_id"] == second_document_id
                and not unopened_scene_path.exists(),
                "a remaining canonical document can exist without a paired scene before deletion",
            )

            labels = [
                panel.document_selector.itemText(index)
                for index in range(panel.document_selector.count())
            ]
            require(
                any(second_document_id[-8:] in label for label in labels)
                and any(first_document_id[-8:] in label for label in labels)
                and any(unopened_document_id[-8:] in label for label in labels),
                "same-title documents display distinct short IDs in the selector",
            )

            second_document_path = (
                session.project_dir
                / SHAPE_DIR
                / f"{second_document_id}.shape.json"
            )
            second_scene_path = (
                session.project_dir
                / SCENE_DIR
                / f"{second_document_id}.object-scene.json"
            )
            before_count = panel.document_selector.count()
            require(
                second_document_path.is_file() and second_scene_path.is_file(),
                "disposable document and paired scene exist before visible deletion",
            )
            require(
                panel.delete_open_document(confirm=False),
                "Delete Document completes through the guarded transaction",
            )
            process(app)
            require(
                panel.document_selector.count() == before_count - 1
                and panel.document is None
                and panel.object_scene is None
                and panel.document_selector.currentIndex() == -1,
                "successful document deletion leaves an unmistakably empty workspace",
            )
            require(
                not second_document_path.exists()
                and not second_scene_path.exists()
                and "no replacement document was opened" in panel.status_label.text(),
                "document and paired scene disappear with explicit near-field confirmation",
            )
            require(
                not unopened_scene_path.exists(),
                "post-delete selector refresh does not create or synchronize an unrelated scene",
            )
            require(
                panel.document_selector.findData(first_document_id) >= 0
                and panel.document_selector.findData(unopened_document_id) >= 0,
                "remaining documents stay available for deliberate reopening",
            )
            require(
                window.next_step_button.text() == "Next: New blank document",
                "guided navigation refreshes after deletion empties the workspace",
            )

            window.open_page(START_HERE_PAGE_INDEX)
            process(app)
            window.open_page(EDITOR_PAGE_INDEX)
            process(app)
            require(
                panel.document is None
                and panel.object_scene is None
                and panel.document_selector.currentIndex() == -1
                and not unopened_scene_path.exists(),
                "the deliberate empty state survives leaving and re-entering Editor",
            )

            unopened_index = panel.document_selector.findData(unopened_document_id)
            panel.document_selector.setCurrentIndex(unopened_index)
            process(app)
            require(
                panel.document is not None
                and panel.document["document_id"] == unopened_document_id
                and unopened_scene_path.is_file(),
                "a remaining document and its scene open only after deliberate selection",
            )

            panel.create_blank_document()
            process(app)
            failing_document_id = panel.document["document_id"]
            original_list_documents = live_guards.list_shape_documents

            def fail_document_discovery(_session):
                raise RuntimeError("malformed remaining canonical document")

            live_guards.list_shape_documents = fail_document_discovery
            try:
                require(
                    panel.delete_open_document(confirm=False),
                    "document deletion remains authoritative when later discovery fails",
                )
            finally:
                live_guards.list_shape_documents = original_list_documents
            process(app)
            require(
                "remaining document discovery failed" in panel.status_label.text()
                and "No remaining-document count is claimed" in panel.status_label.text()
                and "0 documents remain" not in panel.status_label.text(),
                "failed discovery is preserved instead of being reported as a zero count",
            )
            require(
                panel.document is None
                and panel.document_selector.currentIndex() == -1,
                "a failed post-delete discovery leaves no replacement document open",
            )
            panel.refresh_documents(unopened_document_id)
            process(app)
            require(
                panel.document is not None
                and panel.document["document_id"] == unopened_document_id
                and failing_document_id
                not in {
                    panel.document_selector.itemData(index)
                    for index in range(panel.document_selector.count())
                },
                "normal discovery recovers after the injected failure without restoring the deleted document",
            )

            wheel_controller = window.editor_mouse_wheel_controller
            wheel_controller._reveal_active_output()
            process(app)
            target = panel.view_stack.currentWidget()
            content = window.page_scroll.widget()
            target_top = target.mapTo(content, QPoint(0, 0)).y()
            expected = max(scrollbar.minimum(), min(scrollbar.maximum(), target_top))
            require(
                scrollbar.value() == expected,
                "explicit output reveal aligns to the output without leaving clipped text above it",
            )

            disposable_session = ProjectSession(projects_root)
            disposable_state = disposable_session.create_and_open(
                "Disposable Start Here Project",
                "Verify visible Project Trash feedback",
            )
            disposable_project = disposable_state.assessment.project_dir
            disposable_session.close()

            start_panel.refresh_projects()
            disposable_index = start_panel.project_selector.findData(
                str(disposable_project)
            )
            require(
                disposable_index >= 0,
                "Start Here discovers the disposable project selected for deletion",
            )
            start_panel.project_selector.setCurrentIndex(disposable_index)
            process(app)
            authority_before = start_panel.project_status_label.text()

            original_question = live_guards.QMessageBox.question
            original_get_text = authoring_app.QInputDialog.getText

            def reject_exact_name_input(*_args, **_kwargs):
                raise AssertionError(
                    "Exact project-name typing must not be used for deletion confirmation."
                )

            authoring_app.QInputDialog.getText = staticmethod(reject_exact_name_input)
            try:
                live_guards.QMessageBox.question = staticmethod(
                    lambda *_args, **_kwargs: live_guards.QMessageBox.StandardButton.Cancel
                )
                require(
                    not controller.delete_selected_project()
                    and disposable_project.exists(),
                    "Cancel leaves the selected project untouched without requesting typed input",
                )

                live_guards.QMessageBox.question = staticmethod(
                    lambda *_args, **_kwargs: live_guards.QMessageBox.StandardButton.Yes
                )
                require(
                    controller.delete_selected_project(),
                    "Start Here deletes the selected project after one Yes confirmation",
                )
            finally:
                live_guards.QMessageBox.question = original_question
                authoring_app.QInputDialog.getText = original_get_text
            process(app)
            require(
                not disposable_project.exists()
                and start_panel.project_selector.findData(str(disposable_project)) < 0,
                "Start Here deletion removes the project from the active project list",
            )
            require(
                start_panel.project_status_label.text() == authority_before,
                "deleting an inactive project retains the attached-project authority display",
            )
            require(
                "removed" in start_panel.project_trash_feedback_label.text().lower()
                and "Project Trash"
                in start_panel.project_trash_feedback_label.text(),
                "Start Here reports deletion in separate near-field Project Trash feedback",
            )
        finally:
            close_safely(window, app)
            if session.state is not None:
                session.close()

    print("PASS: visible deletion and unclipped Editor entry contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
