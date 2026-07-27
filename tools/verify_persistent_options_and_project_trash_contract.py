#!/usr/bin/env python3
"""Verify the compact Editor command strip and recoverable Project Trash."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from pathlib import Path
from unittest import mock

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PySide6.QtCore import QPoint, QSettings, Qt  # noqa: E402
from PySide6.QtTest import QTest  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from core.project_access import read_project_lock  # noqa: E402
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

MENU_TITLES = ("Document", "Shape", "Edit", "Object", "View")


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
        window.close()
        process(app)
    window.deleteLater()
    process(app)


def create_detached(session: ProjectSession, name: str) -> Path:
    path = session.create_and_open(name, f"Verify {name}").assessment.project_dir
    session.close()
    return path


def find_receipt(trash_root: Path, original: Path) -> dict:
    for candidate in trash_root.iterdir():
        receipt = candidate / PROJECT_TRASH_RECEIPT
        if candidate.is_dir() and receipt.is_file():
            payload = json.loads(receipt.read_text(encoding="utf-8"))
            if payload.get("original_project_dir") == str(original):
                return payload
    raise AssertionError(f"No Project Trash receipt for {original}")


def verify_compact_strip(window, panel, app: QApplication) -> None:
    controller = window.editor_mouse_wheel_controller
    central = window.centralWidget()
    bar_top = controller.bar.mapTo(central, QPoint(0, 0)).y()

    require(not hasattr(controller, "options_tree"), "persistent Editor command tree is removed")
    require(tuple(controller.menu_buttons) == MENU_TITLES, "five compact Editor menu categories exist")
    require(controller.bar.isVisible() and controller.bar.height() <= 48, "command strip is at most 48 pixels high")
    require(all(controller.menu_button(name).isVisible() for name in MENU_TITLES), "all categories are directly visible")

    view_button = controller.menu_button("View")
    view_menu = view_button.menu()
    require(view_menu is panel.view_menu, "View button uses the real Editor View menu")
    require(panel.view_3d_action in view_menu.actions(), "View menu exposes the real 3D action")

    view_button.showMenu()
    process(app)
    require(view_menu.isVisible(), "View dropdown opens temporarily")
    action_rect = view_menu.actionGeometry(panel.view_3d_action)
    require(action_rect.isValid(), "3D action has clickable menu geometry")
    QTest.mouseClick(
        view_menu,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
        action_rect.center(),
    )
    process(app)
    require(panel.view_stack.currentWidget() is panel.object_viewport, "dropdown triggers the real 3D command")
    require(not view_menu.isVisible(), "dropdown closes after command selection")

    scrollbar = window.page_scroll.verticalScrollBar()
    scrollbar.setValue(scrollbar.maximum())
    process(app)
    require(
        controller.bar.isVisible()
        and controller.bar.height() <= 48
        and controller.bar.mapTo(central, QPoint(0, 0)).y() == bar_top,
        "compact strip remains fixed while the Editor page scrolls",
    )


def verify_project_trash(window, panel, session, projects_root, current, removable, app) -> None:
    require(
        panel.project_controls_layout.indexOf(panel.delete_project_button)
        == panel.project_controls_layout.indexOf(panel.switch_project_button) + 1,
        "Delete Project remains adjacent to Switch Project",
    )

    other = ProjectSession(projects_root)
    other.open(removable)
    try:
        try:
            move_project_to_trash(session, removable)
        except ProjectSessionError:
            require(removable.is_dir(), "another writer blocks Project Trash")
        else:
            raise AssertionError("Project Trash ignored another writer")
    finally:
        other.close()

    index = panel.project_selector.findData(str(removable))
    require(index >= 0, "delete target is discoverable")
    panel.project_selector.setCurrentIndex(index)
    panel.set_project_mutation_active(True, "verification")
    require(
        not panel.delete_project_button.isEnabled()
        and not panel.delete_selected_project(confirm=False)
        and removable.is_dir(),
        "active work blocks deletion",
    )
    panel.set_project_mutation_active(False, "verification")
    process(app)

    lock_seen: list[bool] = []
    original_rename = Path.rename

    def observe_rename(path: Path, destination: Path):
        if path == removable:
            lock_seen.append(read_project_lock(path) is not None)
        return original_rename(path, destination)

    with mock.patch.object(Path, "rename", new=observe_rename):
        require(panel.delete_selected_project(confirm=False), "selected non-active project moves to Project Trash")
    require(lock_seen == [True], "exclusive writer lease is held across the move")
    require(session.project_dir == current and session.state is not None, "current project authority is preserved")
    require(not removable.exists(), "trashed project leaves canonical discovery")

    payload = find_receipt(projects_root / PROJECT_TRASH_DIRNAME, removable)
    require(
        payload.get("schema") == PROJECT_TRASH_SCHEMA
        and payload.get("was_active") is False,
        "recovery receipt preserves project identity and authority state",
    )

    outside = projects_root.parent / "outside-project"
    outside.mkdir()
    try:
        move_project_to_trash(session, outside)
    except ProjectSessionError:
        require(outside.is_dir(), "out-of-root deletion is rejected")
    else:
        raise AssertionError("Project Trash accepted an out-of-root path")

    current_index = panel.project_selector.findData(str(current))
    panel.project_selector.setCurrentIndex(current_index)
    require(panel.delete_selected_project(confirm=False), "active project can be deliberately moved to Project Trash")
    process(app)
    require(
        session.state is None and session.project_dir is None and not current.exists(),
        "active deletion closes authority and leaves Forge detached",
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mxztar-compact-options-trash-") as temporary:
        root = Path(temporary)
        settings_root = root / "settings"
        settings_root.mkdir()
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope, str(settings_root))

        app = QApplication.instance() or QApplication([])
        app.setOrganizationName(SETTINGS_ORG)
        app.setApplicationName(SETTINGS_APP)
        settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
        settings.clear()
        settings.sync()

        projects_root = root / "projects"
        session = ProjectSession(projects_root)
        current = create_detached(session, "Compact Options Current")
        removable = create_detached(session, "Recoverable Delete Target")
        session.open(current)

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
            process(app)

            verify_compact_strip(window, panel, app)
            verify_project_trash(window, panel, session, projects_root, current, removable, app)
        finally:
            close_safely(window, app)
            if session.state is not None:
                session.close()

    print("PASS: compact Editor command strip and recoverable Project Trash contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
