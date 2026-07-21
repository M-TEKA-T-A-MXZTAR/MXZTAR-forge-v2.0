#!/usr/bin/env python3
"""Verify live-launch My Library refresh serialization."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from qt_panels.my_library_panel import MyLibraryPanel  # noqa: E402
from qt_startup_guards import (  # noqa: E402
    defer_refresh_for_existing_worker,
    install_my_library_refresh_guard,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


class FakeThread:
    def __init__(self) -> None:
        self.interruptions = 0

    def requestInterruption(self) -> None:
        self.interruptions += 1


class FakePanel:
    def __init__(self) -> None:
        self._discovery_thread = None
        self._thumbnail_loader = None
        self._refresh_pending = False
        self._intake_active = False
        self.status = ""

    def has_active_intake(self) -> bool:
        return self._intake_active

    def set_status(self, message: str) -> None:
        self.status = message


def main() -> int:
    discovery_panel = FakePanel()
    discovery = FakeThread()
    discovery_panel._discovery_thread = discovery
    require(
        defer_refresh_for_existing_worker(discovery_panel),
        "owned discovery worker did not serialize refresh",
    )
    require(discovery_panel._refresh_pending, "discovery refresh was not queued")
    require(discovery.interruptions == 1, "discovery interruption was not requested")

    thumbnail_panel = FakePanel()
    thumbnail = FakeThread()
    thumbnail_panel._thumbnail_loader = thumbnail
    require(
        defer_refresh_for_existing_worker(thumbnail_panel),
        "owned thumbnail worker did not serialize refresh",
    )
    require(thumbnail_panel._refresh_pending, "thumbnail refresh was not queued")
    require(thumbnail.interruptions == 1, "thumbnail interruption was not requested")

    idle_panel = FakePanel()
    require(
        not defer_refresh_for_existing_worker(idle_panel),
        "idle panel incorrectly deferred refresh",
    )

    intake_panel = FakePanel()
    intake_panel._intake_active = True
    intake_panel._discovery_thread = FakeThread()
    require(
        not defer_refresh_for_existing_worker(intake_panel),
        "intake handling did not remain with the original refresh contract",
    )

    original = MyLibraryPanel.refresh_library
    try:
        calls = []

        def baseline(panel):
            calls.append(panel)
            return "baseline"

        MyLibraryPanel.refresh_library = baseline
        install_my_library_refresh_guard()
        installed = MyLibraryPanel.refresh_library
        install_my_library_refresh_guard()
        require(
            MyLibraryPanel.refresh_library is installed,
            "startup guard installation was not idempotent",
        )
        result = installed(idle_panel)
        require(result == "baseline", "idle refresh did not reach original implementation")
        require(calls == [idle_panel], "original refresh was called unexpectedly")
    finally:
        MyLibraryPanel.refresh_library = original

    print("PASS: owned discovery worker serializes duplicate refresh")
    print("PASS: owned thumbnail worker serializes duplicate refresh")
    print("PASS: idle refresh reaches the original implementation")
    print("PASS: intake remains governed by the original refresh contract")
    print("PASS: startup guard installation is idempotent")
    print("PASS: live startup refresh guard verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
