#!/usr/bin/env python3
"""Prevent high-impact drift between Forge runtime and product documentation."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

README_PATH = PROJECT_ROOT / "README.md"
SOURCE_TRUTH_PATH = PROJECT_ROOT / "docs" / "SOURCE_OF_TRUTH.md"
LEDGER_PATH = PROJECT_ROOT / "docs" / "PROGRESS_LEDGER.md"
MASTER_PLAN_PATH = PROJECT_ROOT / "docs" / "product" / "MASTER_BUILD_PLAN.md"
CAPABILITY_PATH = PROJECT_ROOT / "docs" / "product" / "CURRENT_CAPABILITY_BOUNDARY.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"Required documentation file is missing: {path.relative_to(PROJECT_ROOT)}")
    return path.read_text(encoding="utf-8")


def require_text(text: str, expected: str, message: str) -> None:
    require(expected in text, message)


def forbid_text(text: str, forbidden: str, message: str) -> None:
    require(forbidden not in text, message)


def main() -> int:
    readme = read(README_PATH)
    source_truth = read(SOURCE_TRUTH_PATH)
    ledger = read(LEDGER_PATH)
    master = read(MASTER_PLAN_PATH)
    capability = read(CAPABILITY_PATH)

    require_text(
        readme,
        "Current Capability Boundary",
        "README does not link to the present-tense capability authority",
    )
    require_text(
        readme,
        "mxztar_forge_object_scene",
        "README does not record the implemented project-owned object scene",
    )
    require_text(
        readme,
        "Ollama assessment is not shape extraction",
        "README does not distinguish AI assessment from editable extraction",
    )

    require_text(ledger, "**Ledger date:** 27 July 2026", "Progress Ledger date is stale")
    for pr_number in range(54, 62):
        require_text(
            ledger,
            f"PR #{pr_number}",
            f"Progress Ledger does not record PR #{pr_number}",
        )
    require_text(
        ledger,
        "PR #61 mouse-wheel page scrolling and pinned Editor options",
        "Progress Ledger does not identify the current interaction correction",
    )
    require_text(
        ledger,
        "DETERMINISTICALLY VERIFIED on the PR #61 branch; T1700 live acceptance pending",
        "Progress Ledger overstates or omits the PR #61 evidence boundary",
    )
    require_text(
        ledger,
        "the 3D output consumed every wheel event as zoom",
        "Progress Ledger does not record the live scrolling defect truthfully",
    )
    forbid_text(
        ledger,
        "Current branch: `agent/smart-positioning-guides`",
        "Progress Ledger reverted to the merged PR #60 branch",
    )

    require_text(
        master,
        "## 5. Current verified runtime baseline — 26 July 2026",
        "Master Plan lacks the current verified runtime baseline",
    )
    require_text(
        master,
        "### Milestone D — Smart guides and manipulation clarity",
        "Master Plan does not preserve the direct-manipulation milestone",
    )
    require_text(
        master,
        "Ollama assessment alone is not extraction",
        "Master Plan does not preserve the AI-versus-geometry authority boundary",
    )
    require_text(
        master,
        "reversible `Insert into Current Document` command",
        "Master Plan does not define reusable library insertion authority",
    )
    forbid_text(
        master,
        "implement Project Birth and the corrected Start Here authority layout",
        "Master Plan reverted to planning already-completed Project Birth work",
    )

    require_text(
        capability,
        "Turn native shapes into 3D objects | DETERMINISTICALLY VERIFIED foundation",
        "Capability boundary does not record the implemented five-primitive 3D foundation",
    )
    require_text(
        capability,
        "Smart positioning guides | DETERMINISTICALLY VERIFIED on merged main",
        "Capability boundary does not record the merged PR #60 guide implementation",
    )
    require_text(
        capability,
        "Optional snapping | DETERMINISTICALLY VERIFIED on merged main",
        "Capability boundary does not record merged optional snapping",
    )
    require_text(
        capability,
        "Mouse-wheel page scrolling | DETERMINISTICALLY VERIFIED on PR #61 branch",
        "Capability boundary does not record the PR #61 scrolling correction",
    )
    require_text(
        capability,
        "Pinned Editor options | DETERMINISTICALLY VERIFIED on PR #61 branch",
        "Capability boundary does not preserve always-visible Editor options",
    )
    require_text(
        capability,
        "`Scroll page` is the default",
        "Capability boundary does not preserve page scrolling as the default wheel mode",
    )
    require_text(
        capability,
        "Scroll page; Ctrl+wheel zoom",
        "Capability boundary does not preserve the modifier zoom option",
    )
    require_text(
        capability,
        "Document, Shape, Edit, Object and View actions remain available after scrolling to the bottom",
        "Capability boundary does not preserve the pinned options tree requirement",
    )
    require_text(
        capability,
        "Guides appear only while moving one selected object",
        "Capability boundary does not preserve transient guide lifetime",
    )
    require_text(
        capability,
        "Turning guides off also disables snapping",
        "Capability boundary permits invisible forced snapping",
    )
    require_text(
        capability,
        "bounded from 1 to 50 scene units",
        "Capability boundary does not preserve bounded guide tolerance",
    )
    require_text(
        capability,
        "Extract shapes from a 2D image by tracing | PLANNED",
        "Capability boundary incorrectly claims tracing exists",
    )
    require_text(
        capability,
        "Insert Shape Library assets into a document | PLANNED",
        "Capability boundary does not state that library insertion is unimplemented",
    )
    require_text(
        capability,
        "Stitch, weld, join mesh or boolean merge | PLANNED",
        "Capability boundary does not state that merge operations are unimplemented",
    )

    require_text(
        source_truth,
        "docs/product/CURRENT_CAPABILITY_BOUNDARY.md",
        "Source-of-Truth hierarchy does not include current capability authority",
    )
    require_text(
        source_truth,
        "## 8. Documentation drift contract",
        "Source-of-Truth policy does not define documentation drift prevention",
    )

    print("PASS: README reflects the verified merged shape/object runtime boundary")
    print("PASS: Progress Ledger records PRs #54-#61 and the current interaction gate")
    print("PASS: capability authority records merged guides and PR61 wheel routing truthfully")
    print("PASS: pinned options, tracing, Ollama, library insertion, and merge boundaries remain truthful")
    print("PASS: Source Truth protects the present-tense capability authority")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
