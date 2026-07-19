#!/usr/bin/env python3
"""Rebuildable, bounded thumbnail-cache identity for source art."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable

from core.paths import SOURCE_PREVIEW_CACHE_DIR, ensure_project_dirs


DEFAULT_MAX_CACHE_FILES = 128
DEFAULT_MAX_CACHE_BYTES = 256 * 1024 * 1024


def _source_path_key(source_path: Path) -> str:
    resolved = str(Path(source_path).expanduser().resolve()).encode("utf-8")
    return hashlib.sha256(resolved).hexdigest()[:32]


def source_preview_cache_path(source_path: Path) -> Path:
    """Return a versioned cache path with a stable per-source prefix."""
    source_path = Path(source_path).expanduser().resolve()
    stat = source_path.stat()
    version_identity = f"{stat.st_size}\n{stat.st_mtime_ns}".encode("utf-8")
    version_key = hashlib.sha256(version_identity).hexdigest()[:32]

    ensure_project_dirs()
    return SOURCE_PREVIEW_CACHE_DIR / (
        f"{_source_path_key(source_path)}-{version_key}.png"
    )


def obsolete_source_preview_paths(
    source_path: Path,
    keep_path: Path,
) -> tuple[Path, ...]:
    """Return older cached versions for the same resolved source path."""
    prefix = _source_path_key(source_path)
    return tuple(
        path
        for path in SOURCE_PREVIEW_CACHE_DIR.glob(f"{prefix}-*.png")
        if path != keep_path
    )


def prune_source_preview_cache(
    keep_paths: Iterable[Path] = (),
    max_files: int = DEFAULT_MAX_CACHE_FILES,
    max_bytes: int = DEFAULT_MAX_CACHE_BYTES,
) -> None:
    """Remove oldest rebuildable thumbnails until count and byte bounds hold."""
    keep = {Path(path) for path in keep_paths}
    entries = []

    for path in SOURCE_PREVIEW_CACHE_DIR.glob("*.png"):
        try:
            stat = path.stat()
        except OSError:
            continue
        entries.append((path, stat.st_mtime_ns, stat.st_size))

    total_bytes = sum(size for _, _, size in entries)
    removable = sorted(
        (entry for entry in entries if entry[0] not in keep),
        key=lambda entry: entry[1],
    )

    while removable and (
        len(entries) > max_files or total_bytes > max_bytes
    ):
        path, _, size = removable.pop(0)
        try:
            path.unlink()
        except OSError:
            continue
        total_bytes -= size
        entries = [entry for entry in entries if entry[0] != path]
