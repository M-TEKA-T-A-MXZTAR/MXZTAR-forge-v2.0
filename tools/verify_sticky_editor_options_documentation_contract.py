#!/usr/bin/env python3
"""Protect the PR #65 sticky Editor-options viewport contract."""

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
            "PR #65 sticky Editor controls at the visible viewport top",
            "Progress Ledger does not identify the current sticky-control gate",
        ),
        (
            "did not remain at the top of the currently visible workspace while the page scrolled",
            "Progress Ledger does not record the live sticky-control failure",
        ),
        (
            "DETERMINISTICALLY VERIFIED on the PR #65 branch; T1700 live acceptance pending",
            "Progress Ledger overstates or omits the PR #65 evidence boundary",
        ),
        (
            "the bar is outside the scrollable content and directly above its visible viewport",
            "Progress Ledger does not preserve the sticky viewport-column correction",
        ),
        (
            "the verifier requires the bar to remain at the exact same top coordinate",
            "Progress Ledger does not preserve geometric sticky-position verification",
        ),
    ):
        require_text(ledger, expected, message)

    for expected, message in (
        (
            "Sticky Editor options | DETERMINISTICALLY VERIFIED on PR #65 branch",
            "Capability boundary does not record the PR #65 sticky-control state",
        ),
        (
            "The sticky Editor controls occupy a dedicated row directly above `page_scroll`, outside the scrolling content.",
            "Capability boundary does not require a dedicated viewport-top control row",
        ),
        (
            "The control bar retains the same window-relative top coordinate while the Editor page scrolls from top to maximum.",
            "Capability boundary does not protect sticky geometry through maximum scroll",
        ),
        (
            "The sticky row hides on unrelated pages and returns to the same viewport-top position in Editor.",
            "Capability boundary does not protect page-specific sticky-control visibility",
        ),
        (
            "PR #65 manual live acceptance remains the gate before new asset-generation runtime work.",
            "Capability boundary advances runtime work before PR #65 live acceptance",
        ),
    ):
        require_text(capability, expected, message)

    print("PASS: Progress Ledger records the PR #65 live sticky-control defect and correction")
    print("PASS: Current Capability Boundary requires viewport-top geometry, not nominal visibility")
    print("PASS: sticky Editor-options documentation contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
