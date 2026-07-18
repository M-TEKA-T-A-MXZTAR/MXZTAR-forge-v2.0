#!/usr/bin/env python3
"""Rebuildable thumbnail-cache identity for source art."""

from __future__ import annotations

import hashlib
from pathlib import Path

from core.paths import SOURCE_PREVIEW_CACHE_DIR, ensure_project_dirs


def source_preview_cache_path(source_path: Path) -> Path:
    """Return a cache path invalidated by source path, size, or modification time."""
    source_path = Path(source_path).expanduser().resolve()
    stat = source_path.stat()
    identity = (
        f"{source_path}\n"
        f"{stat.st_size}\n"
        f"{stat.st_mtime_ns}"
    ).encode("utf-8")
    key = hashlib.sha256(identity).hexdigest()

    ensure_project_dirs()
    return SOURCE_PREVIEW_CACHE_DIR / f"{key}.png"
