#!/usr/bin/env python3
"""Verify My Library discovery, preview, and exact AgentPanel handoff."""

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


def main() -> int:
    app = QApplication.instance() or QApplication([])
    original_scan = library_module.scan_source_art

    try:
        with tempfile.TemporaryDirectory(prefix="mxztar-library-") as temp_dir:
            source_path = Path(temp_dir) / "known-source.png"
            image = QImage(48, 32, QImage.Format.Format_RGB32)
            image.fill(0x336699)
            require(image.save(str(source_path)), "could not create preview fixture")

            item = SourceArtItem(
                label=f"input / {source_path.name}",
                path=source_path,
                folder_name="input",
                suffix=".png",
                size_bytes=source_path.stat().st_size,
            )
            before = digest(source_path)
            library_module.scan_source_art = lambda: [item]

            panel = library_module.MyLibraryPanel()
            require(panel.source_combo.count() == 1, "library did not discover fixture")
            require(panel.selected_source() == item, "library did not retain exact SourceArtItem")
            require(panel.preview_label.pixmap() is not None, "library did not create preview")
            require(not panel.preview_label.pixmap().isNull(), "library preview is empty")

            emitted = []
            panel.source_selected.connect(emitted.append)
            panel.use_in_agent_workflows()
            require(emitted == [item], "library did not emit exact selected SourceArtItem")
            require(digest(source_path) == before, "library handoff modified source bytes")

            window = qt_app.MXZTARForgeWindow()
            window.library_panel.source_combo.clear()
            window.library_panel.source_combo.addItem(item.label, item)
            window.library_panel.source_combo.setCurrentIndex(0)
            window.library_panel.update_selection()
            window.library_panel.use_in_agent_workflows()
            app.processEvents()

            selected = window.agent_panel.source_combo.currentData()
            require(isinstance(selected, SourceArtItem), "AgentPanel received no source item")
            require(selected.path == item.path, "AgentPanel received a different source path")
            require(window.pages.currentIndex() == 2, "handoff did not navigate to Agent Workflows")
            require(window.sidebar.currentRow() == 2, "sidebar did not follow Agent Workflows navigation")
            require(digest(source_path) == before, "window handoff modified source bytes")

            window.agent_panel._job_active = True
            require(
                window.agent_panel.select_source_item(item) is False,
                "active job allowed source replacement",
            )
            window.agent_panel._job_active = False
            window.close()

            library_module.scan_source_art = lambda: []
            empty_panel = library_module.MyLibraryPanel()
            require(not empty_panel.use_button.isEnabled(), "empty library enabled source handoff")
            require(
                "No source art found" in empty_panel.status_label.text(),
                "empty library did not explain next action",
            )

            print("PASS: My Library discovers and previews supported source art")
            print("PASS: handoff emits the exact selected SourceArtItem")
            print("PASS: handoff navigates to Agent Workflows")
            print("PASS: active AI job rejects source replacement")
            print("PASS: discovery and handoff leave source bytes unchanged")
            print("PASS: empty library has safe disabled actions")
            print("PASS: My Library source baseline verified")
    finally:
        library_module.scan_source_art = original_scan

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
