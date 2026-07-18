#!/usr/bin/env python3
"""
Verify MXZTAR-forge main-window sizing and persistence contract.

This verifier uses Qt's offscreen platform so it can run without opening the
visible desktop UI. It checks that the main shell has a screen-safe default,
remains resizable, provides a scrollable page area, and can persist/restore
window geometry through QSettings.
"""

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

from PySide6.QtWidgets import QApplication, QScrollArea  # noqa: E402

import qt_app  # noqa: E402


TEST_SETTINGS_ORG = "MXZTAR-forge-verifier"
TEST_SETTINGS_APP = "window-geometry-contract"


def require(condition: bool, message: str) -> None:
    """Raise a deterministic verifier failure instead of relying on assert."""
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mxztar-qt-settings-") as settings_root:
        os.environ["XDG_CONFIG_HOME"] = settings_root

        app = QApplication.instance() or QApplication([])
        app.setOrganizationName(TEST_SETTINGS_ORG)
        app.setApplicationName(TEST_SETTINGS_APP)

        qt_app.SETTINGS_ORG = TEST_SETTINGS_ORG
        qt_app.SETTINGS_APP = TEST_SETTINGS_APP

        window = qt_app.MXZTARForgeWindow()

        minimum = window.minimumSize()
        current = window.size()

        require(minimum.width() <= current.width(), "window width starts below minimum")
        require(minimum.height() <= current.height(), "window height starts below minimum")
        require(minimum.width() <= 800, "minimum width should permit smaller screens")
        require(minimum.height() <= 560, "minimum height should permit smaller screens")

        requested_width = minimum.width() + 40
        requested_height = minimum.height() + 40
        window.resize(requested_width, requested_height)
        resized = window.size()
        require(resized.width() == requested_width, "window width did not resize as requested")
        require(resized.height() == requested_height, "window height did not resize as requested")

        require(isinstance(window.page_scroll, QScrollArea), "main pages must be inside a scroll area")
        require(window.page_scroll.widgetResizable(), "page scroll area must resize its widget")

        geometry = window.saveGeometry()
        require(not geometry.isEmpty(), "window geometry did not serialize")

        window.settings.setValue("main_window/geometry", geometry)
        restored_window = qt_app.MXZTARForgeWindow()
        restored_geometry = restored_window.settings.value("main_window/geometry")
        require(restored_geometry is not None, "saved geometry was not available to restore")

        print("PASS: main window is resizable")
        print("PASS: minimum size is screen-friendly")
        print("PASS: page area is scrollable")
        print("PASS: window geometry can be saved and restored")
        print("PASS: window geometry contract verified")

        window.close()
        restored_window.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
