#!/usr/bin/env python3
"""
Source-art discovery for MXZTAR Forge v2.0.

Scans the known source folders used by the rebuilt forge:
- workspace/input
- workspace/imports
- workspace/test_inputs
"""

from dataclasses import dataclass
from pathlib import Path
from collections.abc import Callable
from typing import List

from core.paths import INPUT_DIR, IMPORTS_DIR, TEST_INPUTS_DIR, ensure_project_dirs


SUPPORTED_IMAGE_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff",
}


@dataclass(frozen=True)
class SourceArtItem:
    label: str
    path: Path
    folder_name: str
    suffix: str
    size_bytes: int
    preview_path: Path | None = None
    asset_id: str | None = None
    project_id: str | None = None
    authority: str = "legacy_workspace"
    sha256: str | None = None


def known_source_dirs() -> List[Path]:
    ensure_project_dirs()
    return [INPUT_DIR, IMPORTS_DIR, TEST_INPUTS_DIR]


def is_supported_source(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in SUPPORTED_IMAGE_SUFFIXES


def scan_source_art(interrupted: Callable[[], bool] | None = None) -> List[SourceArtItem]:
    ensure_project_dirs()

    items: List[SourceArtItem] = []

    for folder in known_source_dirs():
        if interrupted is not None and interrupted():
            break
        if not folder.exists():
            continue

        for path in folder.iterdir():
            if interrupted is not None and interrupted():
                return items
            if not is_supported_source(path):
                continue

            try:
                size_bytes = path.stat().st_size
            except OSError:
                size_bytes = 0

            label = f"{folder.name} / {path.name}"

            items.append(
                SourceArtItem(
                    label=label,
                    path=path,
                    folder_name=folder.name,
                    suffix=path.suffix.lower(),
                    size_bytes=size_bytes,
                )
            )

    return sorted(items, key=lambda item: item.label.casefold())


def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"

    kb = size_bytes / 1024
    if kb < 1024:
        return f"{kb:.1f} KB"

    mb = kb / 1024
    if mb < 1024:
        return f"{mb:.2f} MB"

    gb = mb / 1024
    return f"{gb:.2f} GB"
