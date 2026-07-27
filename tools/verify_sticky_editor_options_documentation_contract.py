#!/usr/bin/env python3
"""Protect sticky geometry, live regression history, and the compact command strip correction."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = PROJECT_ROOT / "docs" / "PROGRESS_LEDGER.md"
CAPABILITY_PATH = PROJECT_ROOT / "docs" / "product" / "CURRENT_CAPABILITY_BOUNDARY.md"
SOURCE_TRUTH_PATH = PROJECT_ROOT / "docs" / "SOURCE_OF_TRUTH.md"
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
    ledger = read(LEDGER_PATH)
    capability = read(CAPABILITY_PATH)
    source_truth = read(SOURCE_TRUTH_PATH)
    correction = read(CORRECTION_PATH)
    runtime = read(RUNTIME_PATH)

    # Preserve the historical evidence explaining why PR #65 and PR #66 existed.
    require_text(
        ledger,
        "did not remain at the top of the currently visible workspace while the page scrolled",
        "Progress Ledger lost the original sticky-control failure",
    )
    require_text(
        ledger,
        "`Editor Options` was still an auto-closing popup",
        "Progress Ledger lost the PR #65 popup-dismissal finding",
    )
    require_text(
        capability,
        "Sticky Editor control bar | DETERMINISTICALLY VERIFIED on merged main",
        "Capability boundary lost the accepted sticky viewport geometry",
    )

    # The founder-directed correction now outranks earlier current-state tree claims.
    require_text(
        source_truth,
        "docs/product/EDITOR_COMMAND_STRIP_CORRECTION.md",
        "Source-of-Truth hierarchy does not promote the live command-strip correction",
    )
    require_text(
        source_truth,
        "superseding earlier current-state claims that required an always-open Editor action tree",
        "Source-of-Truth policy does not resolve the rejected tree contract",
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
            "no more than 48 pixels high",
            "Correction document does not protect Editor workspace height",
        ),
    ):
        require_text(correction, expected, message)

    # Protect the real runtime surface, not merely documentation wording.
    forbid_text(runtime, "QTreeWidget", "Runtime reintroduced a persistent Editor command tree")
    forbid_text(runtime, "options_tree", "Runtime reintroduced the rejected options-tree authority")
    require_text(runtime, "self.bar.setMaximumHeight(48)", "Runtime does not cap the compact strip height")
    require_text(runtime, "self.menu_buttons", "Runtime lacks the compact category-button registry")
    require_text(runtime, "QToolButton.ToolButtonPopupMode.InstantPopup", "Runtime categories do not open standard dropdown menus")
    for title in ("Document", "Shape", "Edit", "Object", "View"):
        require_text(runtime, f'"{title}"', f"Runtime compact strip omits {title}")

    print("PASS: historical sticky and popup failures remain documented")
    print("PASS: Source Truth promotes the founder-directed compact command-strip correction")
    print("PASS: runtime rejects the persistent tree and caps the command strip at 48 pixels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
