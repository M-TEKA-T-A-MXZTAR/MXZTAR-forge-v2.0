# MXZTAR Forge v2.0 — Progress Ledger

**Ledger date:** 27 July 2026  
**Repository:** `M-TEKA-T-A-MXZTAR/MXZTAR-forge-v2.0`  
**Active product horizon:** integrated shape/object CAD, Stage One and Stage Two  
**Merged runtime baseline:** `61ab6c4` through PR #59  
**Current delivery gate:** PR #60 transient smart positioning guides and measurements  
**Current branch:** `agent/smart-positioning-guides`

This ledger records current product truth and priority changes. Detailed commit history remains available in Git.

---

## 1. Status vocabulary

| Status | Meaning |
|---|---|
| VERIFIED | Required automated and recorded T1700 evidence exists for the stated boundary |
| DETERMINISTICALLY VERIFIED | Automated contracts pass; required visual or downstream acceptance may remain |
| MERGED | Code is on `main`; merge alone does not prove the complete product gate |
| PARTIAL | Useful implementation exists, but the complete user workflow does not |
| PLANNED | Required but not implemented |
| BLOCKED | A named dependency or founder decision prevents safe progress |
| DEFERRED | Outside the active product horizon |

---

## 2. Founder product direction

Forge is developing as a sophisticated but approachable local CAD workbench based on shapes and objects.

```text
Purpose
→ project
→ source image or blank document
→ editable shape
→ real 3D object
→ direct manipulation and positioning guidance
→ composition and construction
→ review and reusable library
→ portable outputs
```

This direction does not authorise fake perspective effects, unsupported automatic reconstruction, manufacturing claims, or a vague one-button merge operation.

---

## 3. Confirmed merged foundation

- PR #33 — canonical project manifest, required directories, history, atomic creation.
- PR #34 — one-writer lock and recovery classification.
- PR #35 — project session and Start Here create/open/close authority.
- PR #36 — project-contained source intake and processed lifecycle.
- PRs #39–#41 — asynchronous source intake and UI lifecycle corrections.
- PR #42 — project-owned model-call evidence.
- PR #44 — guided Next workflow and exact source handoff.
- PRs #45–#47 — stable My Library lifecycle and accepted image compatibility.
- PR #48 — Editor-first product reconciliation.
- PR #49 — native shape document and minimum reversible Editor.
- PR #50 — launcher import correction.
- PR #51 — Stage One–Two source-truth reconciliation.
- PR #52 — Purpose-driven Project Birth.
- PR #53 — Start Here default launch, project routing, Editor menus, and five reversible primitives.
- PR #54 — project-owned 3D object-scene foundation and CPU-rendered 3D workspace.
- PR #55 — single-object movement isolation, visible placement, immediate 3D synchronization, and stable layout.
- PR #56 — fresh project/document creation, project switching, and explicit paired deletion.
- PR #57 — restored Project Birth blank-document guidance and protected CodeQL Advanced.
- PR #58 — GitHub-generated CodeQL Advanced workflow for Actions and Python.
- PR #59 — reconciled README, Master Build Plan, Progress Ledger, capability boundary, and documentation-drift verification.

---

## 4. Recorded T1700 evidence

### PR #57 and PR #59 merged-main verification

Status: **VERIFIED for the deterministic repository boundary**.

Recorded evidence includes:

- Project Birth focused verifier exit code `0`;
- complete Source Truth verification exit code `0`;
- required documentation files present;
- documentation runtime-state contract passes;
- listed Python files compile;
- CodeQL Advanced contract passes;
- launcher import contract passes;
- Project Birth and routing pass;
- native shape document and primitive commands pass;
- 3D object CAD contract passes;
- single-object usability contract passes;
- Editor project authoring and paired deletion pass;
- all seven optional prompt contracts build.

No downstream export, production mesh, manufacturing, tracing, approved library, or advanced assembly acceptance is implied.

---

## 5. Current workspace truth

| Workspace | Current truth |
|---|---|
| Start Here | Purpose-driven Project Birth, discovery, open/switch, close, and guided blank-document path are implemented |
| Editor | Primary integrated 2D shape and 3D object workspace; PR #60 adds transient movement guidance on its branch |
| My Library | Verified bounded source intake, previews, exact handoff, and guarded lifecycle |
| Shape Library | Evidence browser only; approved editable lifecycle and insertion are not implemented |
| Agent Workflows | Optional local-AI assessment and planning foundation; not geometry authority |
| Jobs | Verified read-only evidence browser |
| Construct | Advanced construction and assembly workspace is not yet a complete exposed workflow |
| Review | Planned |
| Export | Verified SVG, PNG, GLB/glTF, and OBJ adapters are not implemented |

---

## 6. Implemented shape and object boundary

### Native 2D shape creation

Status: **PARTIAL / DETERMINISTICALLY VERIFIED**.

Implemented shapes:

- Rectangle;
- Square;
- Circle;
- Ellipse;
- Star.

Implemented authority:

- native versioned shape document;
- durable command replay;
- Undo and Redo;
- autosave and canonical save;
- transaction rollback;
- reopen and recovery;
- explicit deletion requiring a valid selection.

Not implemented:

- pen or Bezier paths;
- freehand drawing;
- node and handle editing;
- layers, groups, locking, visibility, arrays, mirrors, 2D snapping, or 2D booleans.

### Project-owned 3D object scene

Status: **DETERMINISTICALLY VERIFIED foundation**.

Implemented on merged `main`:

- five native shapes become real extruded 3D objects;
- source shape and object membership remain linked;
- XYZ position;
- width, height, and depth;
- X/Y/Z rotation;
- colour and opacity;
- object selection;
- drag movement and resize;
- numeric Object Inspector;
- empty-space orbit and wheel zoom;
- perspective, grid, line, camera, and zoom persistence;
- reversible object edits;
- paired membership during Undo, Redo, and deletion;
- atomic save, rollback, and restart restoration;
- moving one selected object leaves nonselected objects unchanged.

### PR #60 smart positioning gate

Status: **DETERMINISTICALLY VERIFIED on the PR branch; T1700 live acceptance pending merge**.

Implemented on the branch:

- transient X/Y alignment lines while moving one selected object;
- centre and axis-aligned edge comparison against scene centre and neighbouring objects;
- live centre delta values for X, Y, and Z;
- nearest-object centre distance, surface distance, and Z difference;
- separate `Position Guides` and `Snap to Guides` controls;
- snapping off by default;
- bounded configurable tolerance from 1 to 50 scene units;
- disabling guides also disables snapping so movement is never invisibly forced;
- guide state disappears immediately on release;
- final freely moved or explicitly snapped position uses the existing reversible object command;
- empty-space drag remains perspective orbit and shows no movement guides.

Not included in PR #60:

- equal-gap distribution guidance;
- transform gizmos;
- anchors, connectors, hierarchy, or assemblies;
- stitch, weld, join mesh, 3D booleans, separate, or bake;
- revolve, sweep, loft, shell, relief, bevel, vertex/face editing, or sculpting;
- verified 3D export.

---

## 7. Source-image and Ollama boundary

Status: **PARTIAL evidence foundation**.

Implemented:

- project-owned source copy;
- source identity and hash;
- bounded preview;
- supported source intake;
- optional Ollama assessment and raw findings.

Not implemented:

- source-region geometry selection;
- manual tracing into editable paths;
- deterministic contour, threshold, mask, or silhouette extraction;
- model-generated editable geometry;
- review and approval of extracted candidates.

Ollama findings remain evidence or guidance. They do not become editable or approved geometry automatically.

---

## 8. Shape Library boundary

Status: **PARTIAL evidence browser**.

The current Shape Library does not provide:

- approved editable shape records;
- approval, rejection, correction, versioning, or supersession;
- `Insert into Current Document`;
- reversible library insertion;
- compatibility validation against the current document;
- reusable component or assembly insertion.

---

## 9. Security and repository controls

Current PR #60 evidence:

- Python Compile Check: passing;
- Security & Code Scan: passing;
- Source Truth Check: passing, including the positioning-guide verifier;
- CodeQL Advanced: required before ready-for-review status.

The repository source-truth gate now compiles the guide calculation and viewport modules and executes the full interaction contract.

---

## 10. Next permitted engineering sequence

After PR #60 review, merge, T1700 synchronization, and live acceptance:

1. freeform editable paths, nodes, and handles;
2. source-region selection and manual tracing;
3. bounded deterministic contour and mask candidates;
4. Ollama-assisted candidate assessment through the same editable path;
5. review, approval, versioning, and real Shape Library insertion;
6. 2D composition, alignment, groups, arrays, and explicit booleans;
7. advanced reversible 3D construction recipes;
8. assemblies, anchors, connectors, hierarchy, and distinct merge operations;
9. verified SVG, PNG, GLB/glTF, and OBJ output profiles;
10. release installation, migration, backup, recovery, licence, and documentation gates.

```text
focused branch
→ deterministic verifier
→ Source Truth
→ review comments
→ merge confirmation
→ T1700 sync
→ applicable live acceptance
→ ledger and capability-boundary update
```

---

## 11. Current non-claims

Forge does not currently claim:

- a completed CAD release;
- editable tracing from arbitrary source images;
- automatic production-ready reconstruction;
- approved Shape Library insertion;
- advanced assembly or constraint solving;
- equal-gap or distribution guides;
- engineering-grade dimensions or tolerances;
- manufacturing safety;
- watertight or repaired meshes;
- stitch, weld, join mesh, booleans, topology repair, rigging, UVs, LODs, collision, or production materials;
- verified SVG, PNG, GLB/glTF, or OBJ continuation;
- universal downstream compatibility;
- an open-source licence.

---

## 12. Verification rule

No capability becomes VERIFIED solely because code was committed or merged.

Evidence may include:

- compile and fresh-process import checks;
- schema and command-replay validation;
- project authority and integrity tests;
- interruption and rollback tests;
- Qt lifecycle and offscreen rendering tests;
- manual T1700 interaction tests;
- downstream continuation tests.

The environment that ran each verification must be identified truthfully.
