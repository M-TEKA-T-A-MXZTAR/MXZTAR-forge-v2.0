#!/usr/bin/env python3
"""Verify that run_mxztar_forge.sh launches from its own checkout location."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = PROJECT_ROOT / "run_mxztar_forge.sh"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    launcher_text = LAUNCHER.read_text(encoding="utf-8")
    require("MXZTAR-forge-v2.0" not in launcher_text, "launcher still hard-codes checkout name")
    require("MXZTAR-forge-v2c0" not in launcher_text, "launcher still contains legacy checkout name")
    require('dirname -- "${BASH_SOURCE[0]}"' in launcher_text, "launcher does not derive its own directory")

    with tempfile.TemporaryDirectory(prefix="mxztar-relocated-") as temp_dir:
        checkout = Path(temp_dir) / "arbitrary-checkout-name"
        launcher_copy = checkout / "run_mxztar_forge.sh"
        fake_python = checkout / ".venv" / "bin" / "python"
        expected_entry = checkout / "src" / "mxztar_forge.py"
        capture = checkout / "launcher-capture.txt"

        fake_python.parent.mkdir(parents=True)
        expected_entry.parent.mkdir(parents=True)
        shutil.copy2(LAUNCHER, launcher_copy)
        expected_entry.write_text("# fixture\n", encoding="utf-8")
        fake_python.write_text(
            "#!/usr/bin/env bash\n"
            f"printf '%s\\n%s\\n' \"$PWD\" \"$1\" > \"{capture}\"\n",
            encoding="utf-8",
        )
        launcher_copy.chmod(0o755)
        fake_python.chmod(0o755)

        subprocess.run(
            [str(launcher_copy)],
            cwd=Path(temp_dir),
            check=True,
            env={**os.environ},
        )

        lines = capture.read_text(encoding="utf-8").splitlines()
        require(lines == [str(checkout), str(expected_entry)], "relocated launcher used wrong paths")

    print("PASS: launcher contains no old or canonical checkout-name dependency")
    print("PASS: launcher selects the checkout-local virtual environment")
    print("PASS: launcher changes to its own repository directory")
    print("PASS: launcher uses the absolute checkout-local application entry point")
    print("PASS: relocatable launcher contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
