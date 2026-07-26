#!/usr/bin/env python3
"""Verify page scrolling, live 3D zoom delivery, and pinned Editor options."""

from __future__ import annotations

import copy
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

from PySide6.QtCore import QEvent, QPoint, QPointF, QSettings, Qt  # noqa: E402
from PySide6.QtGui import QWheelEvent  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from core.project_session import ProjectSession  # noqa: E402
from qt_app import SETTINGS_APP, SETTINGS_ORG  # noqa: E402
from qt_editor_app import EDITOR_PAGE_INDEX, START_HERE_PAGE_INDEX  # noqa: E402
from qt_editor_authoring_app import AuthoringEditorForgeWindow  # noqa: E402
from qt_panels.editor_wheel_controls import (  # noqa: E402
    WHEEL_MODE_SCROLL,
    WHEEL_MODE_SCROLL_CTRL_ZOOM,
    WHEEL_MODE_SETTING,
    WHEEL_MODE_ZOOM,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def make_wheel_event(
    target,
    angle_y: int,
    *,
    modifiers: Qt.KeyboardModifier = Qt.KeyboardModifier.NoModifier,
    pixel_y: int = 0,
) -> QWheelEvent:
    """Create a real Qt wheel event positioned over the requested widget."""
    local_center = target.rect().center()
    global_center = target.mapToGlobal(local_center)
    event = QWheelEvent(
        QPointF(local_center),
        QPointF(global_center),
        QPoint(0, pixel_y),
        QPoint(0, angle_y),
        Qt.MouseButton.NoButton,
        modifiers,
        Qt.ScrollPhase.ScrollUpdate,
        False,
    )
    event.setAccepted(False)
    return event


def deliver_wheel(app: QApplication, target, event: QWheelEvent) -> None:
    QApplication.sendEvent(target, event)
    app.processEvents()


def process_deferred(app: QApplication) -> None:
    """Run queued single-shot layout and scroll corrections."""
    app.processEvents()
    app.processEvents()


def close_window_safely(window, app: QApplication) -> None:
    """Exercise the production deferred-close path and drain its Qt threads."""
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


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mxztar-wheel-routing-") as temporary:
        settings_root = Path(temporary) / "settings"
        settings_root.mkdir(parents=True, exist_ok=True)

        # QSettings routing must be established before QApplication and before any
        # production window constructs its settings object. This prevents a focused
        # verifier run from reading or changing the user's real wheel preference.
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        QSettings.setPath(
            QSettings.Format.IniFormat,
            QSettings.Scope.UserScope,
            str(settings_root),
        )

        app = QApplication.instance() or QApplication([])
        app.setOrganizationName(SETTINGS_ORG)
        app.setApplicationName(SETTINGS_APP)

        isolated_settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
        isolated_settings.clear()
        isolated_settings.sync()
        require(
            isolated_settings.value(WHEEL_MODE_SETTING) is None,
            "wheel verifier starts from a clean isolated settings namespace",
        )

        session = ProjectSession(Path(temporary) / "projects")
        window = None
        try:
            state = session.create_and_open(
                "Mouse Wheel Routing",
                "Verify page scrolling and explicit viewport zoom modes",
            )
            require(state.writable, "mouse-wheel test project opens with writable authority")

            window = AuthoringEditorForgeWindow(session)
            window.resize(900, 620)
            window.show()
            window.open_page(EDITOR_PAGE_INDEX)
            panel = window.editor_panel
            if not panel.has_open_document():
                panel.create_blank_document()
            panel.add_rectangle_command()
            panel.add_square_command()
            process_deferred(app)

            controller = window.editor_mouse_wheel_controller
            require(
                controller.current_mode() == WHEEL_MODE_SCROLL,
                "page scrolling is the first-run default mouse-wheel mode",
            )
            require(
                controller.bar.isVisible()
                and not window.page_scroll.isAncestorOf(controller.bar),
                "Editor interaction controls stay visible outside the scrolling page",
            )
            menu_titles = {
                action.menu().title()
                for action in controller.options_menu.actions()
                if action.menu() is not None
            }
            require(
                menu_titles == {"Document", "Shape", "Edit", "Object", "View"},
                "pinned Editor Options exposes the complete implemented action tree",
            )

            window.pages.setMinimumHeight(window.page_scroll.viewport().height() + 900)
            window.pages.updateGeometry()
            process_deferred(app)
            scrollbar = window.page_scroll.verticalScrollBar()
            require(scrollbar.maximum() > 0, "Editor page exposes a real vertical scroll range")

            # Reproduce the live transition: start at the top in 2D, then request 3D.
            panel.show_2d_view()
            process_deferred(app)
            scrollbar.setValue(0)
            panel.show_3d_view()
            process_deferred(app)
            output_top = panel.object_viewport.mapTo(
                window.page_scroll.viewport(), QPoint(0, 0)
            ).y()
            require(
                scrollbar.value() > 0
                and 0 <= output_top < window.page_scroll.viewport().height(),
                "switching to 3D brings the newly active output into visible page range",
            )

            scrollbar.setValue(min(100, max(0, scrollbar.maximum() - 100)))
            scroll_before = scrollbar.value()
            zoom_before = panel.object_viewport.scene_data["view"]["zoom"]
            scroll_event = make_wheel_event(panel.object_viewport, -120)
            deliver_wheel(app, panel.object_viewport, scroll_event)
            require(
                scroll_event.isAccepted()
                and scrollbar.value() > scroll_before
                and panel.object_viewport.scene_data["view"]["zoom"] == zoom_before,
                "real wheel delivery over 3D scrolls the page without zoom by default",
            )

            panel.show_2d_view()
            process_deferred(app)
            scrollbar.setValue(0)
            canvas_event = make_wheel_event(panel.canvas.viewport(), -120)
            deliver_wheel(app, panel.canvas.viewport(), canvas_event)
            require(
                canvas_event.isAccepted() and scrollbar.value() > 0,
                "real wheel delivery over 2D also scrolls the outer page",
            )
            sidebar_event = make_wheel_event(window.sidebar, -120)
            require(
                not controller.eventFilter(window.sidebar, sidebar_event),
                "wheel routing does not interfere with sidebar navigation",
            )

            panel.show_3d_view()
            process_deferred(app)
            controller.set_mode(WHEEL_MODE_ZOOM, announce=False)
            scroll_before = scrollbar.value()
            zoom_before = panel.object_viewport.scene_data["view"]["zoom"]
            zoom_event = make_wheel_event(panel.object_viewport, 120)
            deliver_wheel(app, panel.object_viewport, zoom_event)
            require(
                zoom_event.isAccepted()
                and panel.object_viewport.scene_data["view"]["zoom"] > zoom_before
                and scrollbar.value() == scroll_before,
                "real wheel delivery in 3D zoom mode zooms without scrolling the page",
            )

            panel.show_2d_view()
            process_deferred(app)
            scrollbar.setValue(0)
            zoom_mode_canvas_event = make_wheel_event(panel.canvas.viewport(), -120)
            deliver_wheel(app, panel.canvas.viewport(), zoom_mode_canvas_event)
            require(
                zoom_mode_canvas_event.isAccepted() and scrollbar.value() > 0,
                "3D zoom mode still scrolls the page when the wheel is over 2D output",
            )

            panel.show_3d_view()
            process_deferred(app)
            controller.set_mode(WHEEL_MODE_SCROLL_CTRL_ZOOM, announce=False)
            scrollbar.setValue(min(100, max(0, scrollbar.maximum() - 100)))
            scroll_before = scrollbar.value()
            ctrl_mode_scroll = make_wheel_event(panel.object_viewport, -120)
            deliver_wheel(app, panel.object_viewport, ctrl_mode_scroll)
            require(
                ctrl_mode_scroll.isAccepted() and scrollbar.value() > scroll_before,
                "modifier mode scrolls the page when Ctrl is not held",
            )

            scroll_before = scrollbar.value()
            zoom_before = panel.object_viewport.scene_data["view"]["zoom"]
            ctrl_zoom_event = make_wheel_event(
                panel.object_viewport,
                120,
                modifiers=Qt.KeyboardModifier.ControlModifier,
            )
            deliver_wheel(app, panel.object_viewport, ctrl_zoom_event)
            require(
                ctrl_zoom_event.isAccepted()
                and panel.object_viewport.scene_data["view"]["zoom"] > zoom_before
                and scrollbar.value() == scroll_before,
                "Ctrl+wheel performs 3D zoom without leaking into page scrolling",
            )

            window.settings.sync()
            restarted_settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
            restarted_settings.sync()
            require(
                str(restarted_settings.value(WHEEL_MODE_SETTING))
                == WHEEL_MODE_SCROLL_CTRL_ZOOM,
                "a fresh settings reader restores the selected mouse-wheel mode",
            )

            scrollbar.setValue(scrollbar.maximum())
            app.processEvents()
            require(
                controller.bar.isVisible(),
                "pinned Editor options remain visible after scrolling to the bottom",
            )
            window.pages.setCurrentIndex(START_HERE_PAGE_INDEX)
            app.processEvents()
            require(
                controller.bar.isHidden(),
                "Editor-only interaction controls stay out of unrelated pages",
            )
            window.pages.setCurrentIndex(EDITOR_PAGE_INDEX)
            process_deferred(app)
            require(
                controller.bar.isVisible(),
                "pinned interaction controls return whenever Editor is active",
            )

            scene_before_cleanup = copy.deepcopy(panel.object_viewport.scene_data)
            require(
                scene_before_cleanup is not None,
                "wheel routing leaves the project-owned object scene available",
            )
        finally:
            close_window_safely(window, app)
            if session.state is not None:
                session.close()

    print("PASS: Editor mouse-wheel scrolling and pinned-options contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
