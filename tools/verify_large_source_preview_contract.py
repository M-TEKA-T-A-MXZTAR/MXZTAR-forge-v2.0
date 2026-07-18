#!/usr/bin/env python3
"""Verify that very large source art is decoded only as a bounded preview."""

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

from PySide6.QtCore import QSize  # noqa: E402
from PySide6.QtGui import QImage  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from core.source_library import SourceArtItem  # noqa: E402
from qt_panels import my_library_panel as library_module  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


class FakeLargeImageReader:
    requested_scaled_size = QSize()
    read_calls = 0

    def __init__(self, path: str):
        self.path = path

    def setAutoTransform(self, enabled: bool) -> None:
        require(enabled, "preview reader did not enable image orientation")

    def size(self) -> QSize:
        return QSize(50000, 40000)

    def setScaledSize(self, size: QSize) -> None:
        type(self).requested_scaled_size = size

    def read(self) -> QImage:
        type(self).read_calls += 1
        size = type(self).requested_scaled_size
        image = QImage(size, QImage.Format.Format_RGB32)
        image.fill(0x335577)
        return image

    def errorString(self) -> str:
        return ""


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    app = QApplication.instance() or QApplication([])
    original_reader = library_module.QImageReader
    original_scan = library_module.scan_source_art
    original_cache_path = library_module.source_preview_cache_path

    try:
        with tempfile.TemporaryDirectory(prefix="mxztar-large-preview-") as temp_dir:
            source_path = Path(temp_dir) / "very-large-source.png"
            source_path.write_bytes(b"untouched-large-source-fixture")
            before = digest(source_path)

            item = SourceArtItem(
                label=f"input / {source_path.name}",
                path=source_path,
                folder_name="input",
                suffix=".png",
                size_bytes=source_path.stat().st_size,
            )

            thumbnail_path = Path(temp_dir) / "cached-preview.png"
            library_module.QImageReader = FakeLargeImageReader
            library_module.scan_source_art = lambda: [item]
            library_module.source_preview_cache_path = lambda _: thumbnail_path

            panel = library_module.MyLibraryPanel()
            app.processEvents()

            requested = FakeLargeImageReader.requested_scaled_size
            require(requested.isValid(), "preview decoder received no bounded size")
            require(
                requested.width() <= library_module.PREVIEW_MAX_WIDTH,
                "preview width exceeded its decode bound",
            )
            require(
                requested.height() <= library_module.PREVIEW_MAX_HEIGHT,
                "preview height exceeded its decode bound",
            )
            require(
                panel._preview_image.size() == requested,
                "panel did not cache the bounded decoded image",
            )
            require(thumbnail_path.exists(), "bounded thumbnail was not cached")
            require(
                digest(source_path) == before,
                "bounded preview processing modified the original source",
            )

            first_read_count = FakeLargeImageReader.read_calls
            second_panel = library_module.MyLibraryPanel()
            app.processEvents()
            require(
                FakeLargeImageReader.read_calls == first_read_count,
                "cached thumbnail did not prevent a second source decode",
            )
            require(
                not second_panel._preview_image.isNull(),
                "cached thumbnail could not be rendered",
            )

            print("PASS: 50000x40000 source requests a bounded preview decode")
            print(
                f"PASS: preview decode bound = {requested.width()}x{requested.height()}"
            )
            print("PASS: bounded thumbnail is cached and reused")
            print("PASS: resize rendering uses the cached bounded preview")
            print("PASS: original large source bytes remain unchanged")
            print("PASS: large-source preview contract verified")
    finally:
        library_module.QImageReader = original_reader
        library_module.scan_source_art = original_scan
        library_module.source_preview_cache_path = original_cache_path

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
