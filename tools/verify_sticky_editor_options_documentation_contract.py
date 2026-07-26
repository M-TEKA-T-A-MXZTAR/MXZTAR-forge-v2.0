#!/usr/bin/env python3
"""Protect PR #65 sticky geometry and PR #66 persistent Editor actions."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = PROJECT_ROOT / "docs" / "PROGRESS_LEDGER.md"
CAPABILITY_PATH = PROJECT_ROOT / "docs" / "product" / "CURRENT_CAPABILITY_BOUNDARY.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"Required documentation file is missing: {path.relative_to(PROJECT_ROOT)}")
    return path.read_text(encoding="utf-8")


def require_text(text: str, expected: str, message: str) -> None:
    require(expected in text, message)


def main() -> int:
    ledger = read(LEDGER_PATH)
    capability = read(CAPABILITY_PATH)

    for expected, message in (
        (
            "PR #66 persistent Editor action tree and recoverable Project Trash",
            "Progress Ledger does not identify the current persistent-control gate",
        ),
        (
            "did not remain at the top of the currently visible workspace while the page scrolled",
            "Progress Ledger does not retain the original live sticky-control failure",
        ),
        (
            "DETERMINISTICALLY VERIFIED on the PR #65 branch; T1700 live acceptance pending",
            "Progress Ledger overstates or omits the historical PR #65 evidence boundary",
        ),
        (
            "the bar is outside the scrollable content and directly above its visible viewport",
            "Progress Ledger does not preserve the PR #65 viewport-column correction",
        ),
        (
            "the verifier requires the bar to remain at the exact same top coordinate",
            "Progress Ledger does not preserve PR #65 geometric position verification",
        ),
        (
            "Editor Options was still an auto-closing popup",
            "Progress Ledger does not record the PR #65 live popup-dismissal defect",
        ),
        (
            "the popup-only Editor Options control is replaced by an always-open `QTreeWidget`",
            "Progress Ledger does not preserve the PR #66 persistent-tree correction",
        ),
        (
            "clicking a real tree item triggers the existing action without dismissing the tree",
            "Progress Ledger does not preserve real persistent-tree action delivery",
        ),
    ):
        require_text(ledger, expected, message)

    for expected, message in (
        (
            "Sticky Editor control bar | DETERMINISTICALLY VERIFIED on merged main",
            "Capability boundary does not record merged PR #65 sticky geometry",
        ),
        (
            "Persistent Editor action tree | DETERMINISTICALLY VERIFIED on PR #66 branch",
            "Capability boundary does not record the PR #66 persistent action tree",
        ),
        (
            "The Editor controls occupy a dedicated row directly above `page_scroll`, outside the scrolling content.",
            "Capability boundary does not require a dedicated viewport-top control row",
        ),
        (
            "The control bar retains the same window-relative top coordinate while the Editor page scrolls from top to maximum.",
            "Capability boundary does not protect sticky geometry through maximum scroll",
        ),
        (
            "The row hides on unrelated pages and returns to the same viewport-top position in Editor.",
            "Capability boundary does not protect page-specific sticky-control visibility",
        ),
        (
            "Document, Shape, Edit, Object and View are visible as a persistent action tree, not merely available behind a popup button.",
            "Capability boundary permits the Editor action tree to collapse behind a popup",
        ),
        (
            "Selecting a tree action cannot close the tree",
            "Capability boundary does not preserve continuous mouse reachability after action selection",
        ),
        (
            "PR #66 manual live acceptance remains the gate before new asset-generation runtime work.",
            "Capability boundary advances runtime work before PR #66 live acceptance",
        ),
    ):
        require_text(capability, expected, message)

    print("PASS: Progress Ledger retains PR #65 sticky geometry and records the PR #66 popup defect")
    print("PASS: Current Capability Boundary requires a continuously visible persistent action tree")
    print("PASS: sticky and persistent Editor-options documentation contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
