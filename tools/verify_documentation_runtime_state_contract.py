#!/usr/bin/env python3
"""Verify current Forge documentation authority without fossilising an old PR era."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PATHS = {
    "baseline": PROJECT_ROOT / "docs" / "CURRENT_BASELINE.json",
    "agents": PROJECT_ROOT / "AGENTS.md",
    "readme": PROJECT_ROOT / "README.md",
    "source_truth": PROJECT_ROOT / "docs" / "SOURCE_OF_TRUTH.md",
    "ledger": PROJECT_ROOT / "docs" / "PROGRESS_LEDGER.md",
    "master": PROJECT_ROOT / "docs" / "product" / "MASTER_BUILD_PLAN.md",
    "capability": PROJECT_ROOT / "docs" / "product" / "CURRENT_CAPABILITY_BOUNDARY.md",
    "active": PROJECT_ROOT / "docs" / "product" / "ACTIVE_ENGINEERING_PLAN.md",
    "runtime": PROJECT_ROOT / "docs" / "architecture" / "FINAL_RUNTIME_COMPOSITION.md",
    "regression": PROJECT_ROOT
    / "docs"
    / "architecture"
    / "REGRESSION_AND_DRIFT_PREVENTION.md",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_text(name: str) -> str:
    path = PATHS[name]
    require(path.is_file(), f"Required current authority is missing: {path.relative_to(PROJECT_ROOT)}")
    return path.read_text(encoding="utf-8")


def require_text(text: str, expected: str, message: str) -> None:
    require(expected in text, message)


def forbid_text(text: str, forbidden: str, message: str) -> None:
    require(forbidden not in text, message)


def load_baseline() -> dict:
    path = PATHS["baseline"]
    require(path.is_file(), "docs/CURRENT_BASELINE.json is missing")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AssertionError(f"CURRENT_BASELINE.json is invalid JSON: {exc}") from exc

    require(isinstance(value, dict), "CURRENT_BASELINE.json must contain one object")
    require(
        value.get("schema") == "mxztar_forge_repository_baseline",
        "CURRENT_BASELINE.json has the wrong schema",
    )
    require(value.get("schema_version") == "1.0.0", "Unsupported baseline schema version")
    require(isinstance(value.get("baseline_pr"), int), "baseline_pr must be an integer")
    require(value.get("baseline_pr", 0) > 0, "baseline_pr must be positive")
    for field in (
        "snapshot_date",
        "baseline_branch",
        "active_gate",
        "active_gate_name",
        "next_gate",
        "next_gate_name",
        "next_feature_gate",
        "next_feature_gate_name",
    ):
        require(
            isinstance(value.get(field), str) and value[field].strip(),
            f"Baseline field {field!r} must be a non-empty string",
        )
    return value


def main() -> int:
    baseline = load_baseline()
    agents = read_text("agents")
    readme = read_text("readme")
    source_truth = read_text("source_truth")
    ledger = read_text("ledger")
    master = read_text("master")
    capability = read_text("capability")
    active = read_text("active")
    runtime = read_text("runtime")
    regression = read_text("regression")

    baseline_pr = baseline["baseline_pr"]
    pr_token = f"PR #{baseline_pr}"
    date_iso = baseline["snapshot_date"]
    date_words = "6 August 2026" if date_iso == "2026-08-06" else date_iso

    # Current authority must share one baseline instead of drifting independently.
    for name, text in (
        ("README", readme),
        ("Current Capability Boundary", capability),
        ("Active Engineering Plan", active),
        ("Progress Ledger", ledger),
        ("Final Runtime Composition", runtime),
    ):
        require_text(text, pr_token, f"{name} does not identify the assessed {pr_token} baseline")

    for name, text in (
        ("Current Capability Boundary", capability),
        ("Active Engineering Plan", active),
        ("Progress Ledger", ledger),
    ):
        require_text(text, date_words, f"{name} does not identify the current snapshot date")

    # The stable plan must remain stable rather than becoming another progress ledger.
    require_text(
        master,
        "It deliberately does **not** contain current PR history",
        "Master Plan does not state its stable responsibility",
    )
    forbid_text(master, "PR #", "Master Plan contains current or historical PR tracking")
    forbid_text(master, "Current branch:", "Master Plan contains temporary branch state")
    forbid_text(
        master,
        "Current verified runtime baseline",
        "Master Plan contains a dated runtime snapshot",
    )
    require_text(master, "The 18 first-class workflow families", "Master Plan lost the finite workflow taxonomy")
    require_text(master, "Stage One and Stage Two together define MXZTAR Forge v2.0", "Master Plan lost the active product boundary")
    require_text(master, "Omission and archival rule", "Master Plan lacks authority-de-duplication rules")

    # Source Truth must assign one role to every current document.
    for required in (
        "docs/CURRENT_BASELINE.json",
        "docs/product/MASTER_BUILD_PLAN.md",
        "docs/product/CURRENT_CAPABILITY_BOUNDARY.md",
        "docs/product/ACTIVE_ENGINEERING_PLAN.md",
        "docs/architecture/FINAL_RUNTIME_COMPOSITION.md",
        "docs/architecture/REGRESSION_AND_DRIFT_PREVENTION.md",
        "docs/PROGRESS_LEDGER.md",
    ):
        require_text(source_truth, required, f"Source Truth hierarchy omits {required}")
    require_text(
        source_truth,
        "Historical evidence and deferred vision",
        "Source Truth does not de-authorise historical correction documents",
    )
    require_text(
        source_truth,
        "does not prove the official application",
        "Source Truth does not protect final-runtime verification",
    )
    require_text(
        source_truth,
        "without fossilising one historical PR era",
        "Source Truth does not prohibit stale phrase preservation",
    )

    # Agent instructions must direct agents to the recovered governance and runtime maps.
    for required in (
        "ACTIVE_ENGINEERING_PLAN.md",
        "FINAL_RUNTIME_COMPOSITION.md",
        "REGRESSION_AND_DRIFT_PREVENTION.md",
        "Test the **official final composed runtime**",
        "Silence is not approval",
    ):
        require_text(agents, required, f"AGENTS.md omits required operating rule: {required}")

    # Active sequence must match machine-readable gate metadata.
    require_text(
        active,
        f"Gate {baseline['active_gate']} — {baseline['active_gate_name']}",
        "Active Engineering Plan does not match active baseline gate",
    )
    require_text(
        active,
        f"Gate {baseline['next_gate']} — {baseline['next_gate_name']}",
        "Active Engineering Plan does not match next baseline gate",
    )
    require_text(
        active,
        f"Gate {baseline['next_feature_gate']} — {baseline['next_feature_gate_name']}",
        "Active Engineering Plan does not match next feature gate",
    )
    require_text(active, "Status:** ACTIVE", "Active Engineering Plan does not identify one active gate")
    require_text(active, "T1700 live interaction acceptance", "Active plan omits live acceptance before new geometry")

    # Present capability must include recent restored interactions and preserve planned boundaries.
    for required in (
        "Direct 2D selection and movement",
        "Direct 2D resize",
        "Front orthographic 3D Design View",
        "Direct 3D movement",
        "Final-runtime real-event verification",
        "T1700 consolidated acceptance through PR #80",
    ):
        require_text(capability, required, f"Capability Boundary omits current capability/evidence: {required}")
    for planned in (
        "Freeform paths, nodes, and handles | PLANNED",
        "Source-region manual tracing | PLANNED",
        "Approved Shape Library insertion | PLANNED",
        "Object groups and recoverable assemblies | PLANNED",
        "Verified GLB/glTF or OBJ continuation | PLANNED",
    ):
        require_text(capability, planned, f"Capability Boundary overstates or omits planned boundary: {planned}")
    forbid_text(
        capability,
        "PR #63 branch",
        "Capability Boundary reverted to the obsolete PR #63-era snapshot",
    )
    forbid_text(
        capability,
        "PR #67 branch",
        "Capability Boundary reverted to the obsolete PR #67-era snapshot",
    )

    # Runtime map must reflect the official launcher composition.
    for required in (
        "run_mxztar_forge.sh",
        "src/mxztar_forge.py",
        "install_source_image_compatibility()",
        "install_my_library_refresh_guard()",
        "install_live_acceptance_guards()",
        "install_project_menu_and_rename()",
        "install_project_menu_review_fixes()",
        "install_direct_2d_resize()",
        "AuthoringEditorForgeWindow",
        "GuardedProjectAwareEditorPanel",
        "one official application shell",
    ):
        require_text(runtime, required, f"Final Runtime Composition omits: {required}")

    # Regression doctrine must capture the causal classes that repeatedly produced repair work.
    for required in (
        "Final-runtime mismatch",
        "Assertion-to-experience gap",
        "Competing state ownership",
        "Patch-order dependency",
        "Fragmented user-story delivery",
        "Verification-environment mismatch",
        "Documentation fossilisation",
        "Merge-before-acceptance",
        "Recoup:",
        "Regroup:",
        "Proceed:",
    ):
        require_text(regression, required, f"Regression doctrine omits causal control: {required}")

    # Public README must link current authorities and remain within capability truth.
    for required in (
        "Current Capability Boundary",
        "Active Engineering Plan",
        "Final Runtime Composition",
        "Regression and Drift Prevention",
        "Ollama assessment is not shape extraction",
        "not yet a finished end-user release",
    ):
        require_text(readme, required, f"README omits current public truth: {required}")
    forbid_text(
        readme,
        "The next planned runtime gate is transient smart positioning guidance",
        "README reverted to the pre-PR #60 next milestone",
    )

    # Ledger must record current recovery rather than duplicate every old PR detail.
    require_text(ledger, "Governance-recovery finding — 6 August 2026", "Ledger omits the current drift diagnosis")
    require_text(ledger, "Phase F — Transform separation and direct-manipulation restoration", "Ledger omits PR #74-#80 causal phase")
    require_text(ledger, "Fresh consolidated T1700 acceptance", "Ledger omits the next acceptance boundary")

    print(f"PASS: current baseline metadata is valid ({date_iso}, main through {pr_token})")
    print("PASS: current documents have distinct authority responsibilities")
    print("PASS: Master Plan contains stable product scope rather than PR history")
    print("PASS: capability and active sequence include the PR #80 interaction baseline")
    print("PASS: final runtime composition and regression controls are documented")
    print("PASS: planned geometry, library, assembly, and export work remains unclaimed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
