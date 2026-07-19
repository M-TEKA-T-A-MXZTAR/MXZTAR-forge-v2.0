#!/usr/bin/env python3
"""Verify installation of My Apps and Desktop launchers in an isolated home."""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = PROJECT_ROOT / "tools" / "install_desktop_launchers.sh"
ICON_SOURCE = PROJECT_ROOT / "assets" / "icons" / "mxztar-forge-star.svg"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def expected_fields(checkout: Path) -> dict[str, str]:
    return {
        "Type": "Application",
        "Name": "MXZTAR Forge v2.0",
        "Exec": str(checkout / "run_mxztar_forge.sh"),
        "Path": str(checkout),
        "Icon": str(checkout / "assets" / "icons" / "mxztar-forge-star.svg"),
        "Terminal": "false",
    }


def parse_desktop_entry(path: Path) -> dict[str, str]:
    fields = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            fields[key] = value
    return fields


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mxztar-launchers-") as temp_dir:
        root = Path(temp_dir)
        home = root / "home"
        checkout = root / "MXZTAR-forge-v2.0"
        runner = checkout / "run_mxztar_forge.sh"
        icon = checkout / "assets" / "icons" / "mxztar-forge-star.svg"

        home.mkdir()
        icon.parent.mkdir(parents=True)
        runner.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
        runner.chmod(0o755)
        icon.write_text(ICON_SOURCE.read_text(encoding="utf-8"), encoding="utf-8")

        env = {
            **os.environ,
            "MXZTAR_HOME": str(home),
            "MXZTAR_CHECKOUT": str(checkout),
        }

        subprocess.run(["bash", str(INSTALLER)], env=env, check=True)

        launchers = (
            home / ".local" / "share" / "applications" / "mxztar-forge-v2.desktop",
            home / "Desktop" / "MXZTAR-Forge-v2.0.desktop",
        )
        expected = expected_fields(checkout)
        input_dir = checkout / "workspace" / "input"
        input_link = home / "Desktop" / "MXZTAR-Forge-Input"

        require(input_dir.is_dir(), "authoritative workspace/input was not created")
        require(input_link.is_symlink(), "Desktop input folder-link was not created")
        require(
            input_link.resolve() == input_dir.resolve(),
            "Desktop input folder-link targets the wrong directory",
        )

        for launcher in launchers:
            require(launcher.exists(), f"launcher was not installed: {launcher}")
            require(os.access(launcher, os.X_OK), f"launcher is not executable: {launcher}")
            fields = parse_desktop_entry(launcher)
            for key, value in expected.items():
                require(fields.get(key) == value, f"{launcher}: incorrect {key}")

        subprocess.run(["bash", str(INSTALLER)], env=env, check=True)

        for launcher in launchers:
            backups = tuple(launcher.parent.glob(f"{launcher.name}.before-v2.0-*"))
            require(len(backups) == 1, f"existing launcher was not backed up: {launcher}")

        print("PASS: My Apps launcher installed")
        print("PASS: Desktop launcher installed")
        print("PASS: both launchers are executable")
        print("PASS: both launchers target the canonical checkout runner")
        print("PASS: both launchers use the repository-owned star icon")
        print("PASS: Desktop input folder-link targets workspace/input")
        print("PASS: reinstall backs up existing launcher files")
        print("PASS: desktop launcher installation contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
