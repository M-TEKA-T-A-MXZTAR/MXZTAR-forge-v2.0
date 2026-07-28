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
from core.project_session import ProjectSession  # noqa: E402
from qt_app import SETTINGS_APP, SETTINGS_ORG  # noqa: E402
from qt_editor_app import EDITOR_PAGE_INDEX  # noqa: E402
from qt_live_acceptance_guards import install_live_acceptance_guards  # noqa: E402


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
    install_live_acceptance_guards()

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

            scrollbar = window.page_scroll.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
            window.open_page(EDITOR_PAGE_INDEX)
            process(app)
            require(
                scrollbar.value() == scrollbar.minimum(),
                "entering Editor starts at the top instead of clipping text below the fixed strip",
            )

            panel = window.editor_panel
            first_document_id = panel.document["document_id"]
            panel.create_blank_document()
            process(app)
            second_document_id = panel.document["document_id"]
            panel.add_circle_command()
            process(app)

            labels = [
                panel.document_selector.itemText(index)
                for index in range(panel.document_selector.count())
            ]
            require(
                any(second_document_id[-8:] in label for label in labels)
                and any(first_document_id[-8:] in label for label in labels),
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
                panel.document_selector.findData(first_document_id) >= 0,
                "remaining documents stay available for deliberate reopening",
            )

            remaining_index = panel.document_selector.findData(first_document_id)
            panel.document_selector.setCurrentIndex(remaining_index)
            process(app)
            require(
                panel.document is not None
                and panel.document["document_id"] == first_document_id,
                "a remaining document reopens only after deliberate selection",
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

            original_get_text = authoring_app.QInputDialog.getText
            authoring_app.QInputDialog.getText = staticmethod(
                lambda *_args, **_kwargs: (disposable_project.name, True)
            )
            try:
                require(
                    controller.delete_selected_project(),
                    "Start Here Delete Selected Project completes deliberately",
                )
            finally:
                authoring_app.QInputDialog.getText = original_get_text
            process(app)
            require(
                not disposable_project.exists()
                and start_panel.project_selector.findData(str(disposable_project)) < 0,
                "Start Here deletion removes the project from the active project list",
            )
            require(
                "Removed from active projects" in start_panel.project_status_label.text()
                and "Project Trash" in start_panel.project_status_label.text(),
                "Start Here reports deletion beside the project controls",
            )
        finally:
            close_safely(window, app)
            if session.state is not None:
                session.close()

    print("PASS: visible deletion and unclipped Editor entry contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
