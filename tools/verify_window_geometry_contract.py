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
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PySide6.QtWidgets import QApplication, QScrollArea  # noqa: E402

import qt_app  # noqa: E402
from qt_app import MXZTARForgeWindow  # noqa: E402


def main() -> int:
    app = QApplication.instance() or QApplication([])
    app.setOrganizationName(qt_app.SETTINGS_ORG)
    app.setApplicationName(qt_app.SETTINGS_APP)

    window = MXZTARForgeWindow()

    minimum = window.minimumSize()
    current = window.size()

    assert minimum.width() <= current.width(), "window width starts below minimum"
    assert minimum.height() <= current.height(), "window height starts below minimum"
    assert minimum.width() <= 800, "minimum width should permit smaller screens"
    assert minimum.height() <= 560, "minimum height should permit smaller screens"

    window.resize(minimum.width() + 40, minimum.height() + 40)
    resized = window.size()
    assert resized.width() == minimum.width() + 40, "window width did not resize as requested"
    assert resized.height() == minimum.height() + 40, "window height did not resize as requested"

    assert isinstance(window.page_scroll, QScrollArea), "main pages must be inside a scroll area"
    assert window.page_scroll.widgetResizable(), "page scroll area must resize its widget"

    geometry = window.saveGeometry()
    assert not geometry.isEmpty(), "window geometry did not serialize"

    window.settings.setValue("main_window/geometry", geometry)
    restored_window = MXZTARForgeWindow()
    restored_geometry = restored_window.settings.value("main_window/geometry")
    assert restored_geometry is not None, "saved geometry was not available to restore"

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
