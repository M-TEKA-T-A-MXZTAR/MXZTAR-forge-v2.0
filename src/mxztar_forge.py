#!/usr/bin/env python3
"""
MXZTAR Forge v2.0 launcher entry point.

Local creative-concept engineering forge.
Default AI resource policy:
- OLLAMA_NUM_THREAD=2
- OLLAMA_NUM_PARALLEL=1
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("OLLAMA_NUM_THREAD", "2")
os.environ.setdefault("OLLAMA_NUM_PARALLEL", "1")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from source_image_compatibility import install_source_image_compatibility
from qt_startup_guards import install_my_library_refresh_guard

install_source_image_compatibility()
install_my_library_refresh_guard()

from qt_editor_app import main


if __name__ == "__main__":
    raise SystemExit(main())
