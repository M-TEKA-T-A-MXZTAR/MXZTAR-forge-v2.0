# MXZTAR Forge v2.0 — Historical First-Release Plan

> **Historical filename retained to avoid broken links.**
>
> This document is no longer the active release-scope authority. The former “First
> Rentable Release” plan was written when MXZTAR Forge was centred on AI-assisted source
> analysis, concept briefs, prompt packs, and guided production notes. The founder later
> confirmed free-of-charge access and an editor-first Stage One–Two product.
>
> Current authority:
>
> - `docs/product/MASTER_BUILD_PLAN.md`;
> - `docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md`;
> - `docs/PROGRESS_LEDGER.md`.

## 1. Why this file remains

The earlier plan contains useful engineering principles and project history, but its former
release boundary conflicts with the current product.

Git history preserves the complete earlier text. This current file records what was carried
forward and what was superseded so future work does not accidentally reactivate the old
AI-first scope.

---

## 2. Principles carried forward

The following requirements remain active:

### Durable results

A workflow is not complete merely because text appears in the interface. Results and
failures require structured, traceable, recoverable records.

### Truthful job state

A diagnostic may be saved successfully while the job itself failed. The UI must distinguish
storage success from workflow success.

### Review and approval

Raw findings and model output do not become project truth automatically. User approval,
correction, rejection, and supersession require durable records.

### Compatibility gates

A workflow or operation may be READY, CAUTION, BLOCKED, or READ_ONLY. Missing inputs and
unsupported states must be explained before execution.

### Local ownership

Source art and project files remain locally accessible. External upload or network work
requires explicit user action and disclosure.

### Modest hardware

Heavy work remains off the Qt main thread, one heavy local job runs at a time by default,
and no model is downloaded silently.

### Guided next action

Forge should prevent users from becoming lost, but guidance must not silently approve,
merge, delete, switch projects, start heavy work, or export.

---

## 3. Scope that was superseded

The following ideas are no longer the product centre or first-release acceptance boundary:

- source-art intelligence as the required first user workflow;
- four AI workflows operating end to end as the main release gate;
- concept-folder assembly as the primary product output;
- concept briefs and render prompt packs as the central creator value;
- a workflow selector as the main application workspace;
- the implication that “rentable” means a paid entitlement.

These capabilities may remain optional Agent Workflows, but they support the Forge Editor.
They do not replace editable shapes, manual correction, Shape Library authority,
construction history, or validated exports.

---

## 4. Current product boundary

### Stage One — Forge Editor

A creator can:

- create a project from a clear Purpose;
- import source art or start from a blank shape document;
- trace, extract, or draw editable shapes;
- edit paths, nodes, layers, transforms, groups, and explicit 2D geometry operations;
- review, approve, version, supersede, and reuse Shape Library assets;
- export verified SVG, PNG, and Forge Pack outputs;
- close, reopen, and recover editable work.

### Stage Two — Construct

A creator can:

- generate reversible 3D components from approved shapes or primitives;
- edit construction recipes;
- position and assemble components through explicit relationships;
- distinguish group, contact, stitch, join, boolean, separate, and bake;
- export validated GLB/glTF and OBJ blockouts;
- continue work in a named downstream program.

Stage Two is the planned finished-product boundary.

---

## 5. Optional Agent Workflows

The existing prompt contracts remain optional support jobs:

- source-art intelligence;
- shape and structure harvest;
- modular-set perspective;
- prototype imagination;
- concept brief;
- render prompt pack;
- recommend next step.

Their outputs begin as raw evidence or planning material. They may inform an Editor or
Construct decision but cannot become approved geometry automatically.

---

## 6. Access model

Use of the official software is intended to be free of charge. There is no confirmed timed
trial, recurring subscription, or core-feature paywall. Voluntary support must not control
core functionality or access to local files.

A recognised software `LICENSE` remains a separate founder decision and release gate.
Public repository visibility and free-of-charge access do not themselves define permission
to modify or redistribute the source.

---

## 7. Historical interpretation rule

When an older issue, commit, comment, or document refers to the “first rentable release,”
interpret it as historical planning unless the requirement is explicitly carried forward
by the current Master Build Plan.
