#!/usr/bin/env python3
"""Verify asynchronous project intake, discovery, authority, and shutdown gates."""

from __future__ import annotations

import os
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PIL import Image  # noqa: E402
from PySide6.QtCore import QTimer  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from core.project_session import ProjectSession  # noqa: E402
from qt_app import MXZTARForgeWindow  # noqa: E402
from qt_panels import my_library_panel as library_module  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def wait_until(app, predicate, message: str, timeout: float = 10) -> None:
    deadline = time.monotonic() + timeout
    while not predicate() and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()
    require(predicate(), message)


def wait_for_library(app, panel) -> None:
    wait_until(
        app,
        lambda: not panel.has_active_intake() and not panel.has_active_thumbnail_loading(),
        "project intake or library discovery did not finish",
    )


def main() -> int:
    app = QApplication.instance() or QApplication([])
    with tempfile.TemporaryDirectory(prefix="mxztar-project-intake-ui-") as temporary:
        root = Path(temporary)
        projects = root / "projects"
        external = root / "external"
        external.mkdir()
        source = external / "operator-source.png"
        Image.new("RGB", (1800, 900), (18, 42, 84)).save(source)
        source_before = source.read_bytes()

        session = ProjectSession(projects)
        session.create_and_open("Project Intake UI")

        with patch.object(library_module, "scan_source_art", return_value=[]):
            window = MXZTARForgeWindow(session)
            window.show()
            wait_for_library(app, window.library_panel)
            require(
                window.library_panel.import_button.isEnabled(),
                "writable project did not enable intake",
            )

            real_import = library_module.import_source_copy

            def delayed_import(active_session, source_path):
                time.sleep(0.2)
                return real_import(active_session, source_path)

            ticks = []
            timer = QTimer()
            timer.timeout.connect(lambda: ticks.append(time.monotonic()))
            timer.start(10)
            with patch.object(
                library_module, "import_source_copy", side_effect=delayed_import
            ):
                require(
                    window.library_panel.start_project_intake(source),
                    "writable intake did not start",
                )
                app.processEvents()
                require(
                    not window.start_here_panel.close_project_button.isEnabled(),
                    "active intake allowed project close",
                )
                require(
                    window.close() is False,
                    "active intake allowed application shutdown",
                )
                wait_for_library(app, window.library_panel)
            timer.stop()

            require(len(ticks) >= 3, "Qt event loop did not remain responsive during intake")
            require(source.read_bytes() == source_before, "external source bytes changed")
            require(session.is_writable, "successful intake lost writable authority")
            require(window.library_panel.source_grid.count() == 1, "project source was not discovered")
            item = window.library_panel.selected_source()
            require(item is not None, "project source was not selected")
            require(item.authority == "active_project", "project source authority is unclear")
            require(item.path != source, "library still points at the external source")
            require(item.path.read_bytes() == source_before, "project copy bytes drifted")
            require(item.preview_path is not None and item.preview_path.is_file(), "preview missing")
            print("PASS: project intake stays off the Qt main thread and external bytes remain unchanged")

            require(window.library_panel.start_project_intake(source), "duplicate intake did not start")
            wait_for_library(app, window.library_panel)
            require(window.library_panel.source_grid.count() == 1, "duplicate intake created another card")
            require("Already present" in window.library_panel.status_label.text(), "duplicate was not truthful")
            print("PASS: duplicate project intake remains idempotent and visibly classified")

            invalid = external / "invalid.png"
            invalid.write_bytes(b"not an image")
            require(window.library_panel.start_project_intake(invalid), "invalid intake did not start")
            wait_for_library(app, window.library_panel)
            require(
                "failed; no success is claimed" in window.library_panel.status_label.text(),
                "failed intake was not reported truthfully",
            )
            require(window.library_panel.source_grid.count() == 1, "failed intake created project truth")
            print("PASS: failed intake remains failure and creates no project source")

            window.start_here_panel.close_project()
            app.processEvents()
            wait_for_library(app, window.library_panel)
            require(
                not window.library_panel.import_button.isEnabled(),
                "detached session allowed intake",
            )
            require(window.library_panel.source_grid.count() == 0, "detached project source remained visible")
            print("PASS: project discovery follows the active session and detached intake is blocked")

            window.close()
            app.processEvents()

    print("PASS: asynchronous project source intake UI contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
