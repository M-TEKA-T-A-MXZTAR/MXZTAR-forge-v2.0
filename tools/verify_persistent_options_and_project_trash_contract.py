#!/usr/bin/env python3
"""Verify persistent Editor actions and guarded recoverable Project Trash."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PySide6.QtCore import QPoint, QSettings, Qt  # noqa: E402
from PySide6.QtTest import QTest  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from core.project_session import ProjectSession, ProjectSessionError  # noqa: E402
from core.project_trash import (  # noqa: E402
    PROJECT_TRASH_DIRNAME,
    PROJECT_TRASH_RECEIPT,
    PROJECT_TRASH_SCHEMA,
    move_project_to_trash,
)
from qt_app import SETTINGS_APP, SETTINGS_ORG  # noqa: E402
from qt_editor_app import EDITOR_PAGE_INDEX  # noqa: E402
from qt_editor_authoring_app import AuthoringEditorForgeWindow  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def process_deferred(app: QApplication) -> None:
    app.processEvents()
    app.processEvents()


def close_window_safely(window, app: QApplication) -> None:
    if window is None:
        return
    window.close()
    deadline = time.monotonic() + 10.0
    while window.isVisible() and time.monotonic() < deadline:
        app.processEvents()
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
            app.processEvents()
            time.sleep(0.01)
        window.close()
        app.processEvents()
    window.deleteLater()
    app.processEvents()


def receipt_payload(trashed_project: Path) -> dict:
    receipt = trashed_project / PROJECT_TRASH_RECEIPT
    require(receipt.is_file(), "Project Trash writes a recovery receipt inside the moved project")
    return json.loads(receipt.read_text(encoding="utf-8"))


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mxztar-persistent-options-trash-") as temporary:
        temp_root = Path(temporary)
        settings_root = temp_root / "settings"
        settings_root.mkdir(parents=True, exist_ok=True)
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

        projects_root = temp_root / "projects"
        session = ProjectSession(projects_root)
        current_state = session.create_and_open(
            "Persistent Options Current",
            "Verify continuously visible actions",
        )
        current_path = current_state.assessment.project_dir
        session.close()
        removable_state = session.create_and_open(
            "Recoverable Delete Target",
            "Verify Project Trash",
        )
        removable_path = removable_state.assessment.project_dir
        session.close()
        session.open(current_path)

        # A different writer must prevent Project Trash from moving the target.
        other_session = ProjectSession(projects_root)
        other_session.open(removable_path)
        try:
            try:
                move_project_to_trash(session, removable_path)
            except ProjectSessionError as exc:
                require(
                    "locked" in str(exc).lower(),
                    "Project Trash rejects a project held by another writer",
                )
            else:
                raise AssertionError("Project Trash moved a project held by another writer")
        finally:
            other_session.close()

        window = None
        try:
            window = AuthoringEditorForgeWindow(session)
            window.resize(980, 760)
            window.show()
            window.open_page(EDITOR_PAGE_INDEX)
            panel = window.editor_panel
            if not panel.has_open_document():
                panel.create_blank_document()
            panel.add_rectangle_command()
            panel.add_square_command()
            process_deferred(app)

            controller = window.editor_mouse_wheel_controller
            tree = controller.options_tree
            central = window.centralWidget()
            initial_bar_top = controller.bar.mapTo(central, QPoint(0, 0)).y()
            categories = {
                tree.topLevelItem(index).text(0)
                for index in range(tree.topLevelItemCount())
            }
            require(
                tree.isVisible()
                and categories == {"Document", "Shape", "Edit", "Object", "View"},
                "Editor exposes one persistent complete action tree instead of a closing popup",
            )

            view_3d_item = controller.option_item_for_action(panel.view_3d_action)
            require(view_3d_item is not None, "persistent tree mirrors the real 3D View action")
            tree.scrollToItem(view_3d_item)
            process_deferred(app)
            item_rect = tree.visualItemRect(view_3d_item)
            require(
                item_rect.isValid() and tree.viewport().rect().intersects(item_rect),
                "the selected action is inside the persistent tree's mouse viewport",
            )

            scrollbar = window.page_scroll.verticalScrollBar()
            scrollbar.setValue(0)
            QTest.mouseClick(
                tree.viewport(),
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier,
                item_rect.center(),
            )
            process_deferred(app)
            require(
                panel.view_stack.currentWidget() is panel.object_viewport,
                "clicking a persistent-tree action triggers the real Editor command",
            )
            require(
                tree.isVisible()
                and controller.bar.isVisible()
                and tree.currentItem() is view_3d_item
                and controller.bar.mapTo(central, QPoint(0, 0)).y() == initial_bar_top,
                "choosing an option cannot close or move the Editor action tree",
            )

            scrollbar.setValue(scrollbar.maximum())
            process_deferred(app)
            require(
                tree.isVisible()
                and controller.bar.mapTo(central, QPoint(0, 0)).y() == initial_bar_top,
                "page movement never removes the persistent action tree from mouse range",
            )

            require(
                panel.project_controls_layout.indexOf(panel.delete_project_button)
                == panel.project_controls_layout.indexOf(panel.switch_project_button) + 1,
                "Switch Project includes an adjacent Delete Project control",
            )
            require(
                hasattr(window.start_here_panel, "delete_project_button"),
                "Start Here also exposes Delete Selected Project beside switching controls",
            )

            removable_index = panel.project_selector.findData(str(removable_path))
            require(removable_index >= 0, "Editor project selector discovers the delete target")
            panel.project_selector.setCurrentIndex(removable_index)
            process_deferred(app)

            panel.set_project_mutation_active(True, "verification work")
            require(
                not panel.delete_project_button.isEnabled()
                and not panel.delete_selected_project(confirm=False)
                and removable_path.is_dir(),
                "active project work blocks Delete Project without mutating the target",
            )
            panel.set_project_mutation_active(False, "verification work")
            process_deferred(app)
            require(
                panel.delete_project_button.isEnabled(),
                "Delete Project restores only after active work finishes",
            )

            require(
                panel.delete_selected_project(confirm=False),
                "Editor Delete Project moves the exactly selected non-active project",
            )
            require(
                session.project_dir == current_path and session.state is not None,
                "deleting a different project preserves current project authority",
            )
            require(
                not removable_path.exists()
                and panel.project_selector.findData(str(removable_path)) < 0,
                "trashed project disappears from canonical project discovery",
            )

            trash_root = projects_root / PROJECT_TRASH_DIRNAME
            trashed_candidates = tuple(
                path for path in trash_root.iterdir() if path.is_dir()
            )
            require(
                len(trashed_candidates) == 1,
                "Project Trash contains exactly the selected moved project",
            )
            payload = receipt_payload(trashed_candidates[0])
            require(
                payload.get("schema") == PROJECT_TRASH_SCHEMA
                and payload.get("original_project_dir") == str(removable_path)
                and payload.get("was_active") is False,
                "Project Trash receipt preserves original identity and non-active authority",
            )

            outside = temp_root / "outside-project"
            outside.mkdir()
            try:
                move_project_to_trash(session, outside)
            except ProjectSessionError as exc:
                require(
                    "direct children" in str(exc),
                    "Project Trash rejects paths outside the canonical projects root",
                )
            else:
                raise AssertionError("Project Trash accepted an out-of-root path")
        finally:
            close_window_safely(window, app)

        # Active-project deletion is deliberate and leaves the session detached.
        if session.state is None:
            session.open(current_path)
        active_result = move_project_to_trash(
            session,
            current_path,
            timestamp=datetime(2026, 7, 27, 8, 30, tzinfo=timezone.utc),
        )
        require(
            active_result.was_active
            and session.state is None
            and session.project_dir is None
            and not current_path.exists(),
            "moving the active project to Project Trash closes authority and detaches safely",
        )
        active_payload = receipt_payload(active_result.trashed_project_dir)
        require(
            active_payload.get("was_active") is True
            and active_payload.get("original_project_dir") == str(current_path),
            "active-project receipt records the closed authority boundary",
        )

    print("PASS: persistent Editor options and recoverable Project Trash contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
