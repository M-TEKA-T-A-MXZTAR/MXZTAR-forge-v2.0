#!/usr/bin/env python3
"""Source-image compatibility contract for MXZTAR Forge.

Forge preserves accepted source originals unchanged. My Library creates only
bounded, rebuildable previews. Local vision execution remains fail-closed for
formats that are not explicitly model-ready.
"""

from __future__ import annotations

import io
import warnings
from pathlib import Path

from PIL import Image, UnidentifiedImageError
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QFileDialog

from core import project_source_intake, source_library
from core.source_library import SourceArtItem


ACCEPTED_SOURCE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff",
    ".gif",
}

FORMAT_BY_EXTENSION = {
    ".png": "PNG",
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".webp": "WEBP",
    ".bmp": "BMP",
    ".tif": "TIFF",
    ".tiff": "TIFF",
    ".gif": "GIF",
}

MIME_BY_FORMAT = {
    "PNG": "image/png",
    "JPEG": "image/jpeg",
    "WEBP": "image/webp",
    "BMP": "image/bmp",
    "TIFF": "image/tiff",
    "GIF": "image/gif",
}

MODEL_READY_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
LIBRARY_PREVIEW_MAX_SIZE = (1600, 1200)
MAX_FALLBACK_PREVIEW_PIXELS = 40_000_000


def accepted_source_extensions_text() -> str:
    return ", ".join(sorted(ACCEPTED_SOURCE_EXTENSIONS))


def source_file_dialog_filter() -> str:
    patterns = " ".join(f"*{suffix}" for suffix in sorted(ACCEPTED_SOURCE_EXTENSIONS))
    return f"Supported source images ({patterns})"


def decode_source_preview(path: Path) -> tuple[QImage, str]:
    """Decode one accepted image into a bounded in-memory PNG preview.

    Pillow is used as the compatibility decoder because Qt's PNG handler may
    not advertise scaled decoding. That made valid portrait PNG previews fail
    whenever their height exceeded My Library's display bound.
    """

    source_path = Path(path)
    extension = source_path.suffix.casefold()
    expected_format = FORMAT_BY_EXTENSION.get(extension)
    if expected_format is None:
        return QImage(), f"Unsupported source-image extension: {extension or '(none)'}"

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(source_path) as image:
                decoded_format = image.format
                if decoded_format != expected_format:
                    return (
                        QImage(),
                        f"Image bytes decode as {decoded_format or 'unknown'}, not {extension}.",
                    )

                if getattr(image, "is_animated", False):
                    image.seek(0)

                width, height = image.size
                if width <= 0 or height <= 0:
                    return QImage(), "Image dimensions are unavailable."
                if width * height > MAX_FALLBACK_PREVIEW_PIXELS:
                    return (
                        QImage(),
                        "Image exceeds the bounded 40-megapixel preview limit; "
                        "the original remains accepted and unchanged.",
                    )

                image.thumbnail(
                    LIBRARY_PREVIEW_MAX_SIZE,
                    Image.Resampling.LANCZOS,
                )
                if image.mode != "RGBA":
                    image = image.convert("RGBA")

                payload = io.BytesIO()
                image.save(payload, format="PNG", optimize=True)

        preview = QImage.fromData(payload.getvalue(), "PNG")
        if preview.isNull():
            return QImage(), "Qt could not construct the bounded preview image."
        return preview, ""
    except (
        OSError,
        ValueError,
        UnidentifiedImageError,
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ) as exc:
        return QImage(), f"Could not decode a bounded source preview: {exc}"


def source_is_model_ready(item: SourceArtItem) -> bool:
    return item.suffix.casefold() in MODEL_READY_EXTENSIONS


def install_source_image_compatibility() -> None:
    """Install the format contract once before any panel is constructed."""

    if (
        getattr(install_source_image_compatibility, "_installed", False)
        or getattr(install_source_image_compatibility, "_installing", False)
    ):
        return

    install_source_image_compatibility._installing = True
    try:
        from qt_panels.agent_panel import AgentPanel
        from qt_panels.my_library_panel import MyLibraryPanel

        source_library.SUPPORTED_IMAGE_SUFFIXES = set(ACCEPTED_SOURCE_EXTENSIONS)
        project_source_intake.SUPPORTED_EXTENSIONS = set(ACCEPTED_SOURCE_EXTENSIONS)
        project_source_intake.FORMAT_BY_EXTENSION = dict(FORMAT_BY_EXTENSION)
        project_source_intake.MIME_BY_FORMAT = dict(MIME_BY_FORMAT)

        current_decode = MyLibraryPanel.decode_bounded_image
        if not getattr(current_decode, "_mxztar_source_compatibility", False):

            def compatible_decode(_panel, path):
                return decode_source_preview(Path(path))

            compatible_decode._mxztar_source_compatibility = True
            compatible_decode.__name__ = current_decode.__name__
            compatible_decode.__doc__ = current_decode.__doc__
            MyLibraryPanel.decode_bounded_image = compatible_decode

        current_picker = MyLibraryPanel.choose_project_source
        if not getattr(current_picker, "_mxztar_source_compatibility", False):

            def compatible_picker(panel):
                if not panel.project_session.is_writable:
                    panel.set_status(
                        "Open or create a writable project before importing source art."
                    )
                    return
                path, _selected_filter = QFileDialog.getOpenFileName(
                    panel,
                    "Import Source into Active Project",
                    str(Path.home()),
                    source_file_dialog_filter(),
                )
                if path:
                    panel.start_project_intake(Path(path))

            compatible_picker._mxztar_source_compatibility = True
            compatible_picker.__name__ = current_picker.__name__
            compatible_picker.__doc__ = current_picker.__doc__
            MyLibraryPanel.choose_project_source = compatible_picker

        current_empty_message = AgentPanel.empty_source_message
        if not getattr(current_empty_message, "_mxztar_source_compatibility", False):

            def compatible_empty_message(_panel):
                folders = "\n".join(
                    f"- {path}" for path in source_library.known_source_dirs()
                )
                return (
                    "No supported source art found.\n\n"
                    "Accepted source originals:\n"
                    f"{accepted_source_extensions_text()}\n\n"
                    "PNG, JPEG, and WebP are currently model-ready. BMP, TIFF, and "
                    "GIF are accepted and previewable but require a future normalized "
                    "model-input derivative before AI execution.\n\n"
                    "Known source folders:\n"
                    f"{folders}"
                )

            compatible_empty_message._mxztar_source_compatibility = True
            compatible_empty_message.__name__ = current_empty_message.__name__
            compatible_empty_message.__doc__ = current_empty_message.__doc__
            AgentPanel.empty_source_message = compatible_empty_message

        current_start = AgentPanel.start_selected_workflow
        if not getattr(current_start, "_mxztar_source_compatibility", False):

            def compatible_start(panel):
                item = panel.source_combo.currentData()
                if isinstance(item, SourceArtItem) and not source_is_model_ready(item):
                    panel.set_status(
                        f"{item.suffix.upper()} is accepted as authoritative source art and "
                        "can be previewed, but local AI currently requires PNG, JPEG, or "
                        "WebP. No model call was started."
                    )
                    return None
                current_start(panel)
                return None

            compatible_start._mxztar_source_compatibility = True
            compatible_start.__name__ = current_start.__name__
            compatible_start.__doc__ = current_start.__doc__
            AgentPanel.start_selected_workflow = compatible_start

        install_source_image_compatibility._installed = True
    finally:
        install_source_image_compatibility._installing = False


install_source_image_compatibility._installing = False
install_source_image_compatibility._installed = False
