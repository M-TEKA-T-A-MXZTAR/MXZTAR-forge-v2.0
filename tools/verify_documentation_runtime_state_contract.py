#!/usr/bin/env python3
"""Prevent high-impact drift between Forge runtime and product documentation."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

README_PATH = PROJECT_ROOT / "README.md"
SOURCE_TRUTH_PATH = PROJECT_ROOT / "docs" / "SOURCE_OF_TRUTH.md"
LEDGER_PATH = PROJECT_ROOT / "docs" / "PROGRESS_LEDGER.md"
MASTER_PLAN_PATH = PROJECT_ROOT / "docs" / "product" / "MASTER_BUILD_PLAN.md"
ARCHITECTURE_PATH = (
    PROJECT_ROOT / "docs" / "product" / "ASSET_GENERATION_AND_CONSTRUCT_ARCHITECTURE.md"
)
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
    architecture = read(ARCHITECTURE_PATH)
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
    for pr_number in range(54, 64):
        require_text(
            ledger,
            f"PR #{pr_number}",
            f"Progress Ledger does not record PR #{pr_number}",
        )
    require_text(
        ledger,
        "PR #63 live 3D output reveal and wheel-event routing",
        "Progress Ledger does not identify the current live interaction correction",
    )
    require_text(
        ledger,
        "DETERMINISTICALLY VERIFIED on the PR #63 branch; T1700 live acceptance pending",
        "Progress Ledger overstates or omits the PR #63 evidence boundary",
    )
    require_text(
        ledger,
        "left the object viewport below the current visible page range",
        "Progress Ledger does not record the live output-visibility defect",
    )
    require_text(
        ledger,
        "still allowed the real wheel event to scroll the outer page",
        "Progress Ledger does not record the live wheel-propagation defect",
    )
    require_text(
        ledger,
        "real `QWheelEvent` objects are sent through Qt",
        "Progress Ledger does not preserve real-event verification",
    )
    forbid_text(
        ledger,
        "Current branch: `agent/restore-mouse-wheel-scrolling`",
        "Progress Ledger reverted to the merged PR #61 branch",
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
        source_truth,
        "docs/product/ASSET_GENERATION_AND_CONSTRUCT_ARCHITECTURE.md",
        "Source-of-Truth hierarchy does not promote the active asset-generation addendum",
    )
    require_text(
        source_truth,
        "Where its nearer engineering sequence conflicts with an older immediate-sequence list, this addendum wins",
        "Source-of-Truth policy does not resolve active sequencing conflicts",
    )
    require_text(
        source_truth,
        "a versioned shipped starter source-asset pack",
        "Source-of-Truth policy does not preserve the brought-forward starter asset decision",
    )
    require_text(
        source_truth,
        "object groups, recoverable assemblies, visual seams, mesh stitch or weld, join mesh, booleans, separate, and bake",
        "Source-of-Truth policy collapses distinct Construct operations",
    )

    require_text(
        architecture,
        "founder-authorised active Stage One–Two sequencing addendum",
        "Asset-generation architecture lacks active founder-authorised status",
    )
    require_text(
        architecture,
        "editable path authority",
        "Asset-generation architecture does not begin with editable geometry authority",
    )
    require_text(
        architecture,
        "shipped starter source assets",
        "Asset-generation architecture does not bring bundled assets forward",
    )
    require_text(
        architecture,
        "assets/\n  starter_pack/\n    manifest.json",
        "Asset-generation architecture lacks a bounded installed starter-pack layout",
    )
    require_text(
        architecture,
        "copied into a user project before the user edits them",
        "Bundled starter assets may be mutated in place",
    )
    require_text(
        architecture,
        "Area or surface subset",
        "Construct architecture lacks stable area or surface-subset authority",
    )
    require_text(
        architecture,
        "Primary Focus Surface",
        "Construct architecture lacks primary focus-surface interaction",
    )
    require_text(
        architecture,
        "Effect stack",
        "Construct architecture lacks ordered reversible effect authority",
    )
    for effect_name in (
        "Greebling",
        "Roughness",
        "Distortion",
        "Bend",
        "Logic wiring",
        "Brushed Titanium",
        "Polished Chrome",
        "Anodized Aluminium",
        "Oxidized Copper",
        "Iridescent Nickel",
    ):
        require_text(
            architecture,
            effect_name,
            f"Asset-generation architecture omits required effect/profile: {effect_name}",
        )
    require_text(
        architecture,
        "Randomized",
        "Logic-wiring architecture lacks seeded randomized routing",
    )
    require_text(
        architecture,
        "Symbiotic",
        "Logic-wiring architecture lacks feature-aware symbiotic routing",
    )
    require_text(
        architecture,
        "Aligned",
        "Logic-wiring architecture lacks axis/grid-aligned routing",
    )
    require_text(
        architecture,
        "Merely placing objects around a central point must never trigger F–J automatically",
        "Construct architecture permits placement to silently become destructive geometry",
    )
    require_text(
        architecture,
        "The next runtime milestone is **Freeform Path Authority**",
        "Active architecture does not identify the next common geometry foundation",
    )
    require_text(
        architecture,
        "No dead interface controls",
        "Active architecture permits unimplemented context-menu promises",
    )
    require_text(
        architecture,
        "This architecture does not claim that Forge currently provides",
        "Active architecture does not separate planning from runtime capability",
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
        "Mouse-wheel page scrolling | DETERMINISTICALLY VERIFIED on merged main",
        "Capability boundary does not record the merged default scrolling correction",
    )
    require_text(
        capability,
        "Explicit 3D wheel zoom | DETERMINISTICALLY VERIFIED on PR #63 branch",
        "Capability boundary does not record real-event 3D zoom authority",
    )
    require_text(
        capability,
        "Active output reveal | DETERMINISTICALLY VERIFIED on PR #63 branch",
        "Capability boundary does not record active output visibility",
    )
    require_text(
        capability,
        "Pinned Editor options | DETERMINISTICALLY VERIFIED on merged main",
        "Capability boundary does not preserve always-visible Editor options",
    )
    require_text(
        capability,
        "`Scroll page` is the first-run default",
        "Capability boundary does not preserve page scrolling as the default wheel mode",
    )
    require_text(
        capability,
        "An authorised 3D zoom event is delivered once, accepted, and consumed before page propagation",
        "Capability boundary permits zoom events to leak into page scrolling",
    )
    require_text(
        capability,
        "Selecting 2D or 3D brings the active output into visible page range after layout settles",
        "Capability boundary does not preserve active-output reveal",
    )
    require_text(
        capability,
        "Document, Shape, Edit, Object and View actions remain available after scrolling to the bottom",
        "Capability boundary does not preserve the pinned options tree requirement",
    )
    require_text(
        capability,
        "Deterministic verification now uses real `QWheelEvent` delivery through Qt",
        "Capability boundary relies on fake direct handler verification",
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
    print("PASS: Progress Ledger records PRs #54-#63 and the current live interaction gate")
    print("PASS: capability authority records real wheel delivery and active-output reveal truthfully")
    print("PASS: active asset-generation, starter-pack, surface, assembly, and effect architecture is protected")
    print("PASS: Source Truth separates the brought-forward plan from current runtime claims")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
