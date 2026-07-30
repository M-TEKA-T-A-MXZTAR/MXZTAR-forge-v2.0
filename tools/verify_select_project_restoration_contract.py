#!/usr/bin/env python3
"""Verify that the unified Project menu preserves explicit project selection."""

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

from PySide6.QtCore import QSettings  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

import qt_editor_authoring_app as authoring_app  # noqa: E402
import qt_live_acceptance_guards as live_guards  # noqa: E402
import qt_project_menu_and_rename as project_ui  # noqa: E402
import qt_project_menu_review_fixes as review_fixes  # noqa: E402
from core.project_session import ProjectSession  # noqa: E402
from qt_app import SETTINGS_APP, SETTINGS_ORG  # noqa: E402


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


def action_labels(menu) -> list[str]:
    return [action.text() for action in menu.actions() if not action.isSeparator()]


def main() -> int:
    live_guards.install_live_acceptance_guards()
    project_ui.install_project_menu_and_rename()
    review_fixes.install_project_menu_review_fixes()

    with tempfile.TemporaryDirectory(prefix="mxztar-select-project-") as temporary:
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
        alpha_state = session.create_and_open("Alpha Project", "Verify selected authority")
        alpha_path = alpha_state.assessment.project_dir

        beta_session = ProjectSession(projects_root)
        beta_state = beta_session.create_and_open("Beta Project", "Verify alternate selection")
        beta_path = beta_state.assessment.project_dir
        beta_session.close()

        window = None
        try:
            window = authoring_app.AuthoringEditorForgeWindow(session)
            window.resize(980, 760)
            window.show()
            process(app)

            start_panel = window.start_here_panel
            editor_panel = window.editor_panel

            require(
                action_labels(start_panel.project_menu)[0] == "Select Project…"
                and action_labels(editor_panel.project_menu)[0] == "Select Project…",
                "Select Project remains the first action in both unified Project menus",
            )
            require(
                start_panel.project_select_action.isEnabled()
                and editor_panel.project_select_action.isEnabled(),
                "Select Project is enabled when canonical projects exist",
            )
            require(
                start_panel.project_selector.isEnabled()
                and editor_panel.project_selector.isEnabled(),
                "project selectors remain usable while a project is attached",
            )

            beta_start_index = start_panel.project_selector.findData(str(beta_path))
            beta_editor_index = editor_panel.project_selector.findData(str(beta_path))
            require(
                beta_start_index >= 0 and beta_editor_index >= 0,
                "the alternate canonical project is available on both surfaces",
            )
            start_panel.project_selector.setCurrentIndex(beta_start_index)
            editor_panel.project_selector.setCurrentIndex(beta_editor_index)
            process(app)
            require(
                start_panel.project_switch_action.isEnabled()
                and editor_panel.project_switch_action.isEnabled(),
                "selecting another project enables the existing switch action",
            )
            require(
                session.project_dir == alpha_path,
                "selection alone does not silently switch or mutate project authority",
            )
        finally:
            close_safely(window, app)
            if session.state is not None:
                session.close()

    print("PASS: explicit Select Project path restored without authority changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
