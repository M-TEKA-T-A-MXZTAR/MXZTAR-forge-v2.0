#!/usr/bin/env python3
"""Verify supported Forge import orders in fresh Python processes."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"


def run_case(name: str, code: str) -> None:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(SRC_ROOT)
    environment.setdefault("QT_QPA_PLATFORM", "offscreen")
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=PROJECT_ROOT,
        env=environment,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    if completed.returncode != 0:
        details = "\n".join(
            part for part in (completed.stdout.strip(), completed.stderr.strip()) if part
        )
        raise RuntimeError(f"{name} failed with exit {completed.returncode}:\n{details}")
    print(f"PASS: {name}")


def main() -> int:
    run_case(
        "qt_panels package import remains side-effect free",
        """
import sys
import qt_panels
assert 'qt_startup_guards' not in sys.modules
assert 'source_image_compatibility' not in sys.modules
assert callable(qt_panels.install_panel_runtime_contracts)
""",
    )
    run_case(
        "startup guard imports before panel package without a cycle",
        """
import qt_startup_guards
from qt_panels.my_library_panel import MyLibraryPanel
assert callable(qt_startup_guards.install_my_library_refresh_guard)
assert MyLibraryPanel is not None
""",
    )
    run_case(
        "panel import can explicitly install runtime contracts",
        """
from qt_panels.my_library_panel import MyLibraryPanel
from qt_panels import install_panel_runtime_contracts
install_panel_runtime_contracts()
assert getattr(MyLibraryPanel.refresh_library, '_mxztar_worker_ownership_guard', False)
assert getattr(MyLibraryPanel.decode_bounded_image, '_mxztar_source_compatibility', False)
""",
    )
    run_case(
        "official launcher import installs contracts without a cycle",
        """
import mxztar_forge
from qt_panels.my_library_panel import MyLibraryPanel
assert getattr(MyLibraryPanel.refresh_library, '_mxztar_worker_ownership_guard', False)
assert getattr(MyLibraryPanel.decode_bounded_image, '_mxztar_source_compatibility', False)
assert callable(mxztar_forge.main)
""",
    )
    print("PASS: Forge launcher import contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
