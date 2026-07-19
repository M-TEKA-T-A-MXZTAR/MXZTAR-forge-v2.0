#!/usr/bin/env python3
"""Verify the visible My Library grid and exact AgentPanel handoff."""

from __future__ import annotations

import hashlib
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PySide6.QtGui import QImage  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

import qt_app  # noqa: E402
from core.source_library import SourceArtItem  # noqa: E402
from qt_panels import my_library_panel as library_module  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_sources(temp_dir: str) -> list[SourceArtItem]:
    items = []
    for index in range(6):
        path = Path(temp_dir) / f"source-{index + 1}.png"
        image = QImage(80 + index, 60 + index, QImage.Format.Format_RGB32)
        image.fill(0x223344 + index)
        require(image.save(str(path)), f"could not create fixture {index + 1}")
        items.append(
            SourceArtItem(
                label=f"input / {path.name}",
                path=path,
                folder_name="input",
                suffix=".png",
                size_bytes=path.stat().st_size,
            )
        )
    return items


def main() -> int:
    app = QApplication.instance() or QApplication([])
    original_scan = library_module.scan_source_art

    try:
        with tempfile.TemporaryDirectory(prefix="mxztar-library-") as temp_dir:
            items = make_sources(temp_dir)
            before = {item.path: digest(item.path) for item in items}
            library_module.scan_source_art = lambda: items

            panel = library_module.MyLibraryPanel()
            app.processEvents()

            require(panel.source_grid.count() == 6, "library did not show all six sources")
            for index in range(panel.source_grid.count()):
                card = panel.source_grid.item(index)
                require(not card.icon().isNull(), f"source card {index + 1} has no thumbnail")
            require(panel.selected_source() == items[0], "library did not select first source")
            require(panel.preview_label.maximumHeight() <= 220, "selected preview is too tall")

            panel.source_grid.setCurrentRow(4)
            require(panel.selected_source() == items[4], "grid selection did not change source")

            emitted = []
            panel.source_selected.connect(emitted.append)
            panel.use_in_agent_workflows()
            require(emitted == [items[4]], "library did not emit exact selected SourceArtItem")

            window = qt_app.MXZTARForgeWindow()
            window.library_panel.source_grid.setCurrentRow(2)
            window.library_panel.use_in_agent_workflows()
            app.processEvents()

            selected = window.agent_panel.source_combo.currentData()
            require(isinstance(selected, SourceArtItem), "AgentPanel received no source item")
            require(selected.path == items[2].path, "AgentPanel received a different source")
            require(window.pages.currentIndex() == 2, "handoff did not navigate to Agent Workflows")
            require(window.sidebar.currentRow() == 2, "sidebar did not follow navigation")

            window.agent_panel._job_active = True
            require(
                window.agent_panel.select_source_item(items[0]) is False,
                "active job allowed source replacement",
            )
            window.agent_panel._job_active = False
            window.close()

            for item in items:
                require(digest(item.path) == before[item.path], "library modified source bytes")

            library_module.scan_source_art = lambda: []
            empty_panel = library_module.MyLibraryPanel()
            require(not empty_panel.use_button.isEnabled(), "empty library enabled handoff")
            require(
                "No source art found" in empty_panel.status_label.text(),
                "empty library did not explain the Desktop input action",
            )

            print("PASS: all six source images appear as visible cards")
            print("PASS: every source card has a thumbnail")
            print("PASS: selected preview height is compact")
            print("PASS: grid selection emits the exact SourceArtItem")
            print("PASS: handoff navigates to Agent Workflows")
            print("PASS: active AI job rejects source replacement")
            print("PASS: discovery and handoff leave all source bytes unchanged")
            print("PASS: visible My Library grid verified")
    finally:
        library_module.scan_source_art = original_scan

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
