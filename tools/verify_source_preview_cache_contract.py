#!/usr/bin/env python3
"""Verify source-preview cache invalidation, cleanup, and hard bounds."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from core import source_preview_cache as cache_module


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    original_cache_dir = cache_module.SOURCE_PREVIEW_CACHE_DIR

    try:
        with tempfile.TemporaryDirectory(prefix="mxztar-preview-cache-") as temp_dir:
            cache_dir = Path(temp_dir) / "cache"
            cache_dir.mkdir()
            cache_module.SOURCE_PREVIEW_CACHE_DIR = cache_dir

            source = Path(temp_dir) / "source.png"
            source.write_bytes(b"version-one")
            first_path = cache_module.source_preview_cache_path(source)
            first_path.write_bytes(b"old-thumbnail")

            source.write_bytes(b"version-two-with-different-size")
            second_path = cache_module.source_preview_cache_path(source)
            require(first_path != second_path, "source edit did not change cache version")
            require(
                cache_module.obsolete_source_preview_paths(source, second_path)
                == (first_path,),
                "older version was not identified for replacement",
            )

            second_path.write_bytes(b"current-thumbnail")
            first_path.unlink()

            for index in range(8):
                path = cache_dir / f"unrelated-{index}.png"
                path.write_bytes(bytes(index + 1))
                os.utime(path, ns=(index + 1, index + 1))

            cache_module.prune_source_preview_cache(
                keep_paths=(second_path,),
                max_files=3,
                max_bytes=1024,
            )

            remaining = tuple(cache_dir.glob("*.png"))
            require(len(remaining) <= 3, "cache count bound was not enforced")
            require(second_path in remaining, "current thumbnail was pruned")

            oversized = cache_dir / "oversized.png"
            oversized.write_bytes(b"x" * 2048)
            cache_module.prune_source_preview_cache(
                keep_paths=(second_path,),
                max_files=3,
                max_bytes=1024,
            )
            total_bytes = sum(path.stat().st_size for path in cache_dir.glob("*.png"))
            require(total_bytes <= 1024, "cache byte bound was not enforced")
            require(second_path.exists(), "kept thumbnail was removed by byte pruning")

            print("PASS: source edit creates a new cache version")
            print("PASS: obsolete same-source thumbnail is identified")
            print("PASS: oldest cache files are pruned to a count bound")
            print("PASS: cache is pruned to a byte bound")
            print("PASS: current thumbnail survives pruning")
            print("PASS: source-preview cache contract verified")
    finally:
        cache_module.SOURCE_PREVIEW_CACHE_DIR = original_cache_dir

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
