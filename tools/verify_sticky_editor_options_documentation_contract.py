#!/usr/bin/env python3
"""Protect the accepted compact Editor command strip and its causal history."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_PATH = PROJECT_ROOT / "docs" / "product" / "CURRENT_CAPABILITY_BOUNDARY.md"
REGISTER_PATH = PROJECT_ROOT / "docs" / "REGRESSION_AND_DRIFT_REGISTER.md"
CORRECTION_PATH = PROJECT_ROOT / "docs" / "product" / "EDITOR_COMMAND_STRIP_CORRECTION.md"
RUNTIME_PATH = PROJECT_ROOT / "src" / "qt_panels" / "editor_wheel_controls.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"Required file is missing: {path.relative_to(PROJECT_ROOT)}")
    return path.read_text(encoding="utf-8")


def require_text(text: str, expected: str, message: str) -> None:
    require(expected in text, message)


def forbid_text(text: str, forbidden: str, message: str) -> None:
    require(forbidden not in text, message)


def main() -> int:
    capability = read(CAPABILITY_PATH)
    register = read(REGISTER_PATH)
    correction = read(CORRECTION_PATH)
    runtime = read(RUNTIME_PATH)

    # Present truth describes the accepted compact interaction, not an old branch gate.
    require_text(
        capability,
        "Compact command strip | DETERMINISTICALLY VERIFIED foundation",
        "Current Capability does not preserve the compact Editor command strip",
    )
    require_text(
        capability,
        "Continuously visible interaction controls | DETERMINISTICALLY VERIFIED foundation",
        "Current Capability does not preserve continuously visible Editor controls",
    )
    require_text(
        capability,
        "historical always-open tree was rejected after live usability failure",
        "Current Capability omits the rejected always-open-tree boundary",
    )
    for stale in (
        "Active branch evidence:** PR #67",
        "Compact Editor command strip | DETERMINISTICALLY VERIFIED on PR #67 branch",
        "Persistent Editor action tree | DETERMINISTICALLY VERIFIED",
        "PR #67 manual live acceptance remains the gate",
    ):
        forbid_text(
            capability,
            stale,
            f"Current Capability reverted to stale command-strip authority: {stale}",
        )

    # Historical detail remains supporting evidence and causal learning, not current authority.
    require_text(
        register,
        "RD-001 — Deterministic visibility did not prove usable layout",
        "Regression register lost the command-layout causal entry",
    )
    require_text(
        register,
        "visible and persistent controls were equivalent to usable placement",
        "Regression register lost the incorrect layout assumption",
    )
    require_text(
        register,
        "retained task workspace in the official runtime",
        "Regression register does not protect usable workspace",
    )
    for expected, message in (
        (
            "PR #66 failed T1700 live acceptance",
            "Correction document does not record the live acceptance failure",
        ),
        (
            "Document, Shape, Edit, Object, View, and the mouse-wheel selector",
            "Correction document does not define the complete compact row",
        ),
        (
            "temporary dropdown that closes after selection",
            "Correction document does not restore normal menu dismissal",
        ),
        (
            "original in-page category buttons must be hidden",
            "Correction document permits a duplicate scrolling command row",
        ),
        (
            "no more than 48 pixels high",
            "Correction document does not protect Editor workspace height",
        ),
        (
            "supported 760-pixel minimum window width",
            "Correction document does not protect the supported minimum width",
        ),
    ):
        require_text(correction, expected, message)

    # Protect the real runtime surface, not merely documentation wording.
    forbid_text(runtime, "QTreeWidget", "Runtime reintroduced a persistent Editor command tree")
    forbid_text(runtime, "options_tree", "Runtime reintroduced the rejected options-tree authority")
    require_text(runtime, "self.bar.setMaximumHeight(48)", "Runtime does not cap the compact strip height")
    require_text(runtime, "self.menu_buttons", "Runtime lacks the compact category-button registry")
    require_text(
        runtime,
        "QToolButton.ToolButtonPopupMode.InstantPopup",
        "Runtime categories do not open standard dropdown menus",
    )
    require_text(
        runtime,
        "self._hide_in_page_menu_buttons()",
        "Runtime does not hide duplicate in-page command buttons",
    )
    require_text(runtime, 'self.mode_label = QLabel("Wheel:"', "Runtime wheel label is not compact")
    require_text(
        runtime,
        'self.mode_combo.addItem("Ctrl+wheel zoom"',
        "Runtime wheel selector retains overlong copy",
    )
    require_text(
        runtime,
        "QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon",
        "Runtime does not bound the wheel selector at minimum width",
    )
    for title in ("Document", "Shape", "Edit", "Object", "View"):
        require_text(runtime, f'"{title}"', f"Runtime compact strip omits {title}")

    print("PASS: current capability protects the accepted compact Editor interaction")
    print("PASS: rejected layout history remains in the causal register and supporting correction")
    print("PASS: runtime rejects duplicate/tree controls and protects minimum-width layout")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
