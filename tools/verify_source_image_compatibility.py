#!/usr/bin/env python3
"""Verify MXZTAR Forge source-image compatibility and truthful AI gating."""

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

from PIL import Image  # noqa: E402

from core import project_source_intake, source_library  # noqa: E402
from core.source_library import SourceArtItem  # noqa: E402
from qt_panels.agent_panel import AgentPanel  # noqa: E402
from qt_panels.my_library_panel import MyLibraryPanel  # noqa: E402
from source_image_compatibility import (  # noqa: E402
    ACCEPTED_SOURCE_EXTENSIONS,
    MODEL_READY_EXTENSIONS,
    decode_source_preview,
    install_source_image_compatibility,
    source_file_dialog_filter,
    source_is_model_ready,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def make_item(path: Path) -> SourceArtItem:
    return SourceArtItem(
        label=path.name,
        path=path,
        folder_name=path.parent.name,
        suffix=path.suffix.casefold(),
        size_bytes=path.stat().st_size,
    )


class FakeCombo:
    def __init__(self, item) -> None:
        self._item = item

    def currentData(self):
        return self._item


class FakeAgentPanel:
    def __init__(self, item) -> None:
        self.source_combo = FakeCombo(item)
        self.status = ""

    def set_status(self, message: str) -> None:
        self.status = message


def main() -> int:
    install_source_image_compatibility()

    require(
        source_library.SUPPORTED_IMAGE_SUFFIXES == ACCEPTED_SOURCE_EXTENSIONS,
        "source discovery did not receive the authoritative extension set",
    )
    require(
        project_source_intake.SUPPORTED_EXTENSIONS == ACCEPTED_SOURCE_EXTENSIONS,
        "project intake did not receive the authoritative extension set",
    )
    require(
        MODEL_READY_EXTENSIONS == {".png", ".jpg", ".jpeg", ".webp"},
        "model-ready source boundary drifted",
    )

    installed_decode = MyLibraryPanel.decode_bounded_image
    installed_start = AgentPanel.start_selected_workflow
    install_source_image_compatibility()
    require(
        MyLibraryPanel.decode_bounded_image is installed_decode,
        "preview compatibility installation was not idempotent",
    )
    require(
        AgentPanel.start_selected_workflow is installed_start,
        "AI compatibility installation was not idempotent",
    )

    with tempfile.TemporaryDirectory(prefix="mxztar-source-compat-") as raw_temp:
        root = Path(raw_temp)

        portrait_png = root / "portrait-source.png"
        Image.new("RGBA", (1400, 1800), (20, 40, 80, 180)).save(
            portrait_png,
            format="PNG",
        )
        portrait_preview, portrait_error = decode_source_preview(portrait_png)
        require(not portrait_preview.isNull(), f"portrait PNG preview failed: {portrait_error}")
        require(
            portrait_preview.width() <= 1600 and portrait_preview.height() <= 1200,
            "portrait PNG preview exceeded the bounded UI dimensions",
        )

        fixture_specs = {
            ".bmp": "BMP",
            ".tif": "TIFF",
            ".gif": "GIF",
        }
        for extension, image_format in fixture_specs.items():
            source_path = root / f"source{extension}"
            preview_path = root / f"preview-{extension[1:]}.png"
            Image.new("RGB", (320, 240), (80, 120, 160)).save(
                source_path,
                format=image_format,
            )

            width, height, decoded_format = project_source_intake._make_preview(
                source_path,
                preview_path,
                extension,
            )
            require((width, height) == (320, 240), f"{extension} dimensions drifted")
            require(decoded_format == image_format, f"{extension} format identity drifted")
            require(preview_path.is_file(), f"{extension} project preview was not created")

            preview, error = decode_source_preview(source_path)
            require(not preview.isNull(), f"{extension} library preview failed: {error}")
            require(
                source_library.is_supported_source(source_path),
                f"{extension} source discovery rejected an accepted original",
            )

        unsupported = root / "vector.svg"
        unsupported.write_text("<svg/>", encoding="utf-8")
        require(
            not source_library.is_supported_source(unsupported),
            "unsupported SVG was incorrectly classified as accepted raster source art",
        )

        bmp_item = make_item(root / "source.bmp")
        require(not source_is_model_ready(bmp_item), "BMP was incorrectly marked model-ready")
        fake_panel = FakeAgentPanel(bmp_item)
        AgentPanel.start_selected_workflow(fake_panel)
        require(
            "No model call was started" in fake_panel.status,
            "non-model-ready AI execution was not blocked truthfully",
        )

        png_item = make_item(portrait_png)
        require(source_is_model_ready(png_item), "PNG was not marked model-ready")

    file_filter = source_file_dialog_filter()
    for extension in ACCEPTED_SOURCE_EXTENSIONS:
        require(f"*{extension}" in file_filter, f"file picker omitted {extension}")

    print("PASS: portrait PNG renders as a bounded thumbnail")
    print("PASS: BMP, TIFF, and GIF originals create project previews")
    print("PASS: accepted source formats share one discovery and intake contract")
    print("PASS: unsupported SVG remains outside the raster source contract")
    print("PASS: non-model-ready formats are blocked before Ollama execution")
    print("PASS: source image compatibility installation is idempotent")
    print("PASS: broad source image compatibility verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
