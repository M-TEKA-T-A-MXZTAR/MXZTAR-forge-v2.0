# MXZTAR Forge v2.0 — Progress Ledger

**Ledger date:** 6 August 2026  
**Repository:** `M-TEKA-T-A-MXZTAR/MXZTAR-forge-v2.0`  
**Active product horizon:** Stage One editable 2D assets and Stage Two reversible 3D blockouts  
**Merged runtime baseline:** `main` through PR #81 at `e8659d5`  
**Current delivery gate:** R1 final-runtime and state-authority mapping before R2 acceptance-harness correction

## 1. Purpose

This ledger records dated implementation and verification chronology.

It does not replace:

- `docs/product/MASTER_BUILD_PLAN.md` for the finished product boundary;
- `docs/product/RECOVERY_AND_COMPLETION_PLAN.md` for the active engineering order;
- `docs/product/CURRENT_CAPABILITY_BOUNDARY.md` for present capability;
- `docs/architecture/FINAL_RUNTIME_AND_STATE_AUTHORITY_MAP.md` for final composition and mutable-state ownership;
- `docs/REGRESSION_AND_DRIFT_REGISTER.md` for causal learning.

Detailed commit and review history remains available in Git and GitHub. Historical implementation narration may be condensed here when its causal learning has been preserved elsewhere.

## 2. Status vocabulary

| Status | Meaning |
|---|---|
| VERIFIED | Applicable automated and recorded T1700 evidence exists for the stated boundary |
| DETERMINISTICALLY VERIFIED | Automated contracts pass; required live, downstream or release acceptance may remain |
| MERGED | Code is on `main`; merge alone does not prove a complete user journey |
| PARTIAL | Useful implementation exists, but the complete workflow does not |
| PLANNED | Required by the active product plan but not implemented |
| BLOCKED | A named dependency or acceptance gate prevents safe progress |
| DEFERRED | Outside the active Stage One–Two delivery sequence |

## 3. Consolidated merged chronology

### Foundation through PR #32

Earlier repository work established the local Qt application, source-art intelligence, project panels, agent workflows, jobs evidence, Shape Library evidence browsing and initial hardware-safe operation. Exact details remain in Git history and prior ledger revisions.

### Project and Editor authority — PR #33 to PR #53

- PR #33 — canonical project manifest, required directories, history and atomic creation.
- PR #34 — one-writer lock and recovery classification.
- PR #35 — project session and Start Here create/open/close authority.
- PR #36 — project-contained source intake and processed lifecycle.
- PRs #39–#41 — asynchronous source intake and Qt lifecycle corrections.
- PR #42 — project-owned model-call evidence.
- PR #44 — guided next action and source handoff.
- PRs #45–#47 — My Library lifecycle and accepted image compatibility.
- PR #48 — Editor-first product reconciliation.
- PR #49 — native shape document and reversible Editor foundation.
- PR #50 — launcher import correction.
- PR #51 — Stage One–Two source-truth reconciliation.
- PR #52 — Purpose-driven Project Birth.
- PR #53 — Start Here routing, Editor menus and five reversible primitives.

### Integrated 2D/3D foundation — PR #54 to PR #65

- PR #54 — project-owned 3D object-scene foundation and CPU-rendered 3D workspace.
- PR #55 — single-object movement isolation, visible placement and immediate 3D synchronization.
- PR #56 — fresh project/document creation, project switching and explicit paired deletion.
- PR #57 — Project Birth guidance restoration and CodeQL protection.
- PR #58 — CodeQL Advanced workflow for Actions and Python.
- PR #59 — documentation and capability reconciliation at that baseline.
- PR #60 — transient positioning guides, measurements, optional snapping and preserved empty-space orbit.
- PR #61 — mouse-wheel page scrolling and explicit 3D zoom modes.
- PR #62 — isolated wheel-verifier settings and Qt background-thread cleanup.
- PR #63 — real wheel-event consumption and active-output reveal.
- PR #64 — asset-generation and modular Construct architecture planning.
- PR #65 — sticky Editor control bar at the visible viewport top.

### Interaction correction and recovery lessons — PR #66 to PR #80

- PR #66 — introduced a persistent always-open Editor action tree and recoverable Project Trash. Deterministic checks passed, but the tree failed T1700 live usability because it consumed excessive workspace.
- PR #67 — restored a compact fixed command strip with temporary dropdown menus while preserving Project Trash and wheel routing.
- PR #68 — removed the pulsing Next Action behaviour and added explicit document lifecycle handling.
- PR #69 — corrected deletion visibility and clipping.
- PR #70 — simplified deletion interaction while preserving recoverability.
- PR #71 — unified project menu and rename authority.
- PR #72 — restored project and document selectors lost during menu unification.
- PR #73 — corrected shared project-switch target authority.
- PR #74 — separated object transforms from camera navigation.
- PR #75 — restored direct object resize and Save Project access.
- PR #76 — restored direct object movement.
- PR #77 — restored safe Editor re-entry to Select.
- PR #78 — corrected precise direct 2D and 3D movement and pointer-following behaviour.
- PR #79 — restored stable front orthographic Design View as the editing default.
- PR #80 — added direct durable 2D resize for all five primitives with minimum-geometry validation.

### Governance reset — PR #81

- PR #81 — replaced competing governance addenda with one finite authority chain; added the Recovery and Completion Plan and Regression and Drift Register; refreshed Current Capability and README truth; replaced fossilised documentation assertions with semantic relationship checks; restored full Source Truth success.

PR #81 changed governance and verification contracts, not runtime behaviour.

## 4. Current merged evidence boundary

Status: **DETERMINISTICALLY VERIFIED foundation and governance baseline through PR #81**, with live and final-event limitations recorded separately.

The merged repository includes focused contracts for:

- project birth, switching, recovery and Project Trash;
- native shape-document creation and command replay;
- project-owned 3D object scenes;
- direct selection, movement, resize and deletion;
- paired 2D/3D membership;
- safe Editor re-entry;
- stable Design View and object/camera separation;
- positioning guides and optional snapping;
- real wheel-event routing and active-output reveal;
- compact Editor command controls;
- launcher import and prompt contracts;
- one coherent governance hierarchy and causal regression register;
- CodeQL configuration.

Important evidence boundary:

- deterministic success does not automatically prove live workspace usability;
- isolated component success does not prove the official final composed runtime;
- interaction-heavy changes require explicit T1700 live acceptance status;
- save, close and reopen must be included when durable state changes;
- downstream export and release claims require separate continuation or clean-install evidence.

## 5. Current R1 work — final runtime and state authority

Status: **ACTIVE BRANCH / NOT MERGED** until review and required checks complete.

The R1 change:

- maps `run_mxztar_forge.sh` through `src/mxztar_forge.py` into the final authoring window;
- records the six startup installers and their order;
- records the final window hierarchy and successive Editor-panel replacements;
- identifies `DirectResizeProjectAwareEditorPanel` as the final installed Editor binding;
- names the authoritative owner of project, document, scene, camera, selection, source, worker and window state;
- records why each compatibility layer exists and the conditions required before retirement;
- adds an executable final-runtime composition contract;
- promotes the map into Source Truth and required-document verification.

No visible UI, persistence schema or runtime behaviour is changed by R1 mapping.

## 6. Current recovery sequence

1. review and merge the R1 map only after Source Truth, compile, security and composition checks pass;
2. begin R2 acceptance harness correction against the mapped official runtime;
3. convert PR #66–#80 lessons into official-launcher contracts;
4. deliver real mouse and wheel events through the final composition;
5. confirm geometry, visibility, pointer/object lock, save, close and reopen;
6. complete applicable T1700 interaction acceptance;
7. begin R3 consolidation only after the R2 evidence boundary is stable;
8. begin Stage One freeform path and manual trace work only after the recovery gate closes.

## 7. Current product boundary

Forge currently has a meaningful integrated primitive-based 2D and 3D blockout foundation.

Forge does not yet have a complete:

- source-image-to-approved-reusable-asset workflow;
- Shape Library approval and insertion workflow;
- validated 2D export workflow;
- reviewed shape-to-component recipe system;
- recoverable assembly workflow;
- validated 3D continuation profile;
- end-user release installation path.

The Current Capability Boundary is the present-tense authority for these limits.
