#!/usr/bin/env python3
"""Verify current relationships among Forge governing documentation."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

AGENTS_PATH = PROJECT_ROOT / "AGENTS.md"
README_PATH = PROJECT_ROOT / "README.md"
SOURCE_TRUTH_PATH = PROJECT_ROOT / "docs" / "SOURCE_OF_TRUTH.md"
LEDGER_PATH = PROJECT_ROOT / "docs" / "PROGRESS_LEDGER.md"
REGISTER_PATH = PROJECT_ROOT / "docs" / "REGRESSION_AND_DRIFT_REGISTER.md"
MASTER_PLAN_PATH = PROJECT_ROOT / "docs" / "product" / "MASTER_BUILD_PLAN.md"
RECOVERY_PLAN_PATH = PROJECT_ROOT / "docs" / "product" / "RECOVERY_AND_COMPLETION_PLAN.md"
ARCHITECTURE_PATH = (
    PROJECT_ROOT / "docs" / "product" / "ASSET_GENERATION_AND_CONSTRUCT_ARCHITECTURE.md"
)
CAPABILITY_PATH = PROJECT_ROOT / "docs" / "product" / "CURRENT_CAPABILITY_BOUNDARY.md"

MINIMUM_RUNTIME_BASELINE_PR = 80


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


def parse_date(text: str, label: str, document_name: str) -> datetime:
    match = re.search(rf"\*\*{re.escape(label)}:\*\*\s+(\d{{1,2}} [A-Za-z]+ \d{{4}})", text)
    require(match is not None, f"{document_name} does not declare {label}")
    try:
        return datetime.strptime(match.group(1), "%d %B %Y")
    except ValueError as exc:
        raise AssertionError(f"{document_name} has an invalid {label}") from exc


def parse_runtime_baseline(text: str, document_name: str) -> tuple[int, str]:
    match = re.search(
        r"\*\*Merged runtime baseline:\*\*\s+`main` through PR #(\d+) at `([0-9a-f]{7,40})`",
        text,
    )
    require(match is not None, f"{document_name} does not declare a parseable merged runtime baseline")
    return int(match.group(1)), match.group(2)


def main() -> int:
    agents = read(AGENTS_PATH)
    readme = read(README_PATH)
    source_truth = read(SOURCE_TRUTH_PATH)
    ledger = read(LEDGER_PATH)
    register = read(REGISTER_PATH)
    master = read(MASTER_PLAN_PATH)
    recovery = read(RECOVERY_PLAN_PATH)
    architecture = read(ARCHITECTURE_PATH)
    capability = read(CAPABILITY_PATH)

    # Governing authority must be explicit and finite.
    for path in (
        "docs/product/MASTER_BUILD_PLAN.md",
        "docs/product/RECOVERY_AND_COMPLETION_PLAN.md",
        "docs/product/CURRENT_CAPABILITY_BOUNDARY.md",
        "docs/PROGRESS_LEDGER.md",
        "docs/REGRESSION_AND_DRIFT_REGISTER.md",
        "docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md",
        "docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md",
        "docs/product/OUTPUT_ARTIFACT_CONTRACTS.md",
        "README.md",
    ):
        require_text(
            source_truth,
            path,
            f"Source-of-Truth hierarchy omits governing document: {path}",
        )
    require_text(
        source_truth,
        "must not remain permanent competing sources of current instruction",
        "Source Truth does not prevent correction notes from becoming competing authority",
    )
    require_text(
        source_truth,
        "must not fossilise old state through exact historical dates, PR numbers or obsolete phrases",
        "Source Truth still permits frozen snapshot assertions",
    )
    require_text(
        source_truth,
        "The official launcher and all installed runtime corrections are part of the tested system",
        "Source Truth does not require final composed-runtime evidence",
    )

    # Current Capability and the Ledger must agree on the merged runtime baseline.
    parse_date(capability, "Snapshot date", "Current Capability Boundary")
    parse_date(ledger, "Ledger date", "Progress Ledger")
    capability_pr, capability_sha = parse_runtime_baseline(
        capability, "Current Capability Boundary"
    )
    ledger_pr, ledger_sha = parse_runtime_baseline(ledger, "Progress Ledger")
    require(
        capability_pr >= MINIMUM_RUNTIME_BASELINE_PR,
        f"Current Capability baseline regressed below PR #{MINIMUM_RUNTIME_BASELINE_PR}",
    )
    require(
        (capability_pr, capability_sha) == (ledger_pr, ledger_sha),
        "Current Capability and Progress Ledger disagree on the merged runtime baseline",
    )

    # Known stale snapshots must not return.
    for stale in (
        "**Snapshot date:** 27 July 2026",
        "`main` through PR #66",
        "Active branch evidence:** PR #67",
        "Current branch: `agent/persistent-editor-options-and-project-trash`",
        "Pinned Editor options | DETERMINISTICALLY VERIFIED on merged main",
        "Persistent Editor action tree | DETERMINISTICALLY VERIFIED",
    ):
        forbid_text(
            capability + "\n" + ledger,
            stale,
            f"Current-state documentation reverted to stale authority: {stale}",
        )

    # The recovery sequence must be finite and must precede broad feature work.
    for phase in range(7):
        require_text(
            recovery,
            f"Phase R{phase}",
            f"Recovery Plan omits Phase R{phase}",
        )
    for requirement in (
        "final-runtime map",
        "official final runtime",
        "real mouse and wheel events",
        "save, close and reopen",
        "T1700 live acceptance",
        "No new broad feature family should begin",
    ):
        require_text(
            recovery,
            requirement,
            f"Recovery Plan omits required recovery control: {requirement}",
        )

    # Causal learning must be durable, not merely described in a PR.
    for entry in range(1, 9):
        require_text(
            register,
            f"RD-{entry:03d}",
            f"Regression and Drift Register omits RD-{entry:03d}",
        )
    for requirement in (
        "Incorrect assumption:",
        "Architectural condition:",
        "Verification gap:",
        "Prevention rule:",
        "final composed runtime",
        "pointer lock",
        "Current-capability documentation fossilised",
        "Manual verifier inventory allowed omission",
    ):
        require_text(
            register,
            requirement,
            f"Regression register omits causal field or known mechanism: {requirement}",
        )

    # Agent rules must control complete user actions and preserved state.
    for requirement in (
        "complete user action",
        "preserved invariants",
        "official launcher",
        "final composed runtime",
        "authoritative state owner",
        "real Qt",
        "REGRESSION_AND_DRIFT_REGISTER.md",
    ):
        require_text(
            agents,
            requirement,
            f"AGENTS.md omits required operating rule: {requirement}",
        )

    # Product authority remains Stage One plus Stage Two, with AI kept subordinate.
    for requirement in (
        "Stage One — Forge Editor",
        "Stage Two — Construct",
        "Stage One and Stage Two together",
        "Ollama assessment alone is not extraction",
        "reversible `Insert into Current Document` command",
    ):
        require_text(
            master,
            requirement,
            f"Master Build Plan omits product boundary: {requirement}",
        )
    require_text(
        architecture,
        "editable path authority",
        "Supporting architecture omits editable-geometry authority",
    )
    require_text(
        architecture,
        "copied into a user project before the user edits them",
        "Supporting architecture permits bundled assets to be edited in place",
    )
    require_text(
        architecture,
        "Merely placing objects around a central point must never trigger F–J automatically",
        "Supporting architecture permits placement to become destructive geometry",
    )

    # Present capability must include the latest accepted interaction foundation.
    for requirement in (
        "Select and direct 2D movement",
        "Direct 2D resize",
        "Safe Editor re-entry",
        "Compact command strip",
        "Stable Design View",
        "Pointer-following precision",
        "Source Truth verification | PARTIAL governance gate",
        "manual tracing into editable paths",
        "approval, rejection, supersession and reusable Shape Library authority",
        "validated GLB/glTF or OBJ continuation profiles",
        "The official launcher currently composes behaviour through multiple subclasses",
        "final-runtime mapping and regression-contract consolidation",
    ):
        require_text(
            capability,
            requirement,
            f"Current Capability omits present truth or limitation: {requirement}",
        )

    # README is a public surface and must point to governing truth without overstating release state.
    for requirement in (
        "Current Capability Boundary",
        "Recovery and Completion Plan",
        "Regression and Drift Register",
        "Ollama assessment is not shape extraction",
        "mxztar_forge_object_scene",
        "not yet a finished end-user release",
        "recognised software `LICENSE`",
    ):
        require_text(
            readme,
            requirement,
            f"README omits required public boundary: {requirement}",
        )
    forbid_text(
        readme,
        "The next planned runtime gate is transient smart positioning guidance",
        "README still presents already-implemented smart guides as the next milestone",
    )

    print(
        f"PASS: Current Capability and Progress Ledger agree on PR #{capability_pr} at {capability_sha}"
    )
    print("PASS: governing documents form one finite authority chain")
    print("PASS: recovery phases and causal regression records are present")
    print("PASS: final-runtime, real-event, persistence and live-acceptance rules are protected")
    print("PASS: README and Current Capability retain truthful Stage One–Two limits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
