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
from PySide6.QtGui import QImage, QImageIOHandler  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from core import source_preview_cache as cache_module  # noqa: E402
from core.source_library import SourceArtItem  # noqa: E402
from qt_panels import my_library_panel as library_module  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


class FakeLargeImageReader:
    requested_scaled_size = QSize()
    read_calls = 0
    source_size = QSize(50000, 40000)
    supports_scaled_decode = True

    def __init__(self, path: str):
        self.path = path

    def setAutoTransform(self, enabled: bool) -> None:
        require(enabled, "preview reader did not enable image orientation")

    def size(self) -> QSize:
        return type(self).source_size

    def supportsOption(self, option) -> bool:
        require(
            option == QImageIOHandler.ImageOption.ScaledSize,
            "panel checked the wrong decoder capability",
        )
        return type(self).supports_scaled_decode

    def setScaledSize(self, size: QSize) -> None:
        type(self).requested_scaled_size = size

    def read(self) -> QImage:
        type(self).read_calls += 1
        size = type(self).requested_scaled_size
        if not size.isValid():
            size = type(self).source_size
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
    original_cache_dir = cache_module.SOURCE_PREVIEW_CACHE_DIR

    try:
        with tempfile.TemporaryDirectory(prefix="mxztar-large-preview-") as temp_dir:
            cache_module.SOURCE_PREVIEW_CACHE_DIR = Path(temp_dir) / "preview-cache"
            cache_module.SOURCE_PREVIEW_CACHE_DIR.mkdir()

            source_path = Path(temp_dir) / "very-large-source.png"
            source_path.write_bytes(b"untouched-large-source-fixture")
            before = digest(source_path)

            identity_fixture = Path(temp_dir) / "cache-identity.png"
            identity_fixture.write_bytes(b"version-one")
            first_cache_identity = original_cache_path(identity_fixture)
            identity_fixture.write_bytes(b"version-two-with-new-size")
            second_cache_identity = original_cache_path(identity_fixture)
            require(
                first_cache_identity != second_cache_identity,
                "source change did not invalidate thumbnail cache identity",
            )

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

            thumbnail_path.unlink()
            FakeLargeImageReader.supports_scaled_decode = False
            reads_before_unsafe = FakeLargeImageReader.read_calls
            unsafe_panel = library_module.MyLibraryPanel()
            app.processEvents()
            require(
                FakeLargeImageReader.read_calls == reads_before_unsafe,
                "unsupported large format was decoded",
            )
            require(
                "cannot prove a memory-bounded" in unsafe_panel.preview_label.text(),
                "unsafe decoder did not explain the preview boundary",
            )

            FakeLargeImageReader.supports_scaled_decode = True
            FakeLargeImageReader.source_size = QSize(800, 600)
            FakeLargeImageReader.requested_scaled_size = QSize()
            small_thumbnail = Path(temp_dir) / "small-preview.png"
            library_module.source_preview_cache_path = lambda _: small_thumbnail
            small_panel = library_module.MyLibraryPanel()
            app.processEvents()
            require(
                not FakeLargeImageReader.requested_scaled_size.isValid(),
                "small source was unnecessarily upscaled",
            )
            require(
                small_panel._preview_image.size() == QSize(800, 600),
                "small source dimensions were not preserved",
            )

            print("PASS: 50000x40000 source requests a bounded preview decode")
            print(
                f"PASS: preview decode bound = {requested.width()}x{requested.height()}"
            )
            print("PASS: unsupported large decoder is rejected before read")
            print("PASS: small source is not upscaled")
            print("PASS: bounded thumbnail is cached and reused")
            print("PASS: source changes invalidate thumbnail cache identity")
            print("PASS: resize rendering uses the cached bounded preview")
            print("PASS: original large source bytes remain unchanged")
            print("PASS: large-source preview contract verified")
    finally:
        library_module.QImageReader = original_reader
        library_module.scan_source_art = original_scan
        library_module.source_preview_cache_path = original_cache_path
        cache_module.SOURCE_PREVIEW_CACHE_DIR = original_cache_dir

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
