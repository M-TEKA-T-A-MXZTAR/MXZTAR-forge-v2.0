# MXZTAR Forge v2.0 — Progress Ledger

**Ledger date:** 22 July 2026  
**Repository:** `M-TEKA-T-A-MXZTAR/MXZTAR-forge-v2.0`  
**Active product horizon:** Stage One and Stage Two  
**Current next gate:** Project Birth and Start Here authority layout

This ledger records current product truth. Detailed historical versions remain available in Git history.

---

## 1. Status vocabulary

| Status | Meaning |
|---|---|
| VERIFIED | Required deterministic and live evidence for the stated gate is recorded |
| DETERMINISTICALLY VERIFIED | Automated contract passed, but required live or downstream acceptance remains |
| MERGED | Code or documentation is on `main`; merge alone does not prove the full product gate |
| PARTIAL | Some useful implementation exists, but the workflow or acceptance boundary is incomplete |
| PLANNED | Required by the active Stage One–Two product but not implemented |
| BLOCKED | Cannot safely proceed until a named dependency or decision is resolved |
| DEFERRED | Outside the active Stage One–Two product horizon |
| HISTORICAL | Retained for provenance but no longer active authority |

---

## 2. Current product spine

MXZTAR Forge is a local-first, human-governed creative construction workbench.

```text
project purpose
→ source image or blank canvas
→ trace, extract, or draw an editable shape
→ correct and combine shapes
→ approve reusable Shape Library assets
→ generate reversible 3D components
→ assemble recoverable structures
→ export through verified downstream profiles
```

The product is organised into:

- 4 shared platform workflow families;
- 8 Stage One workflow families;
- 6 Stage Two workflow families.

Stage One and Stage Two together define the planned finished product. Future Product Levels Three and Four remain deferred.

---

## 3. Product-stage ledger

| Product stage | Status | Current boundary | Activation/exit gate |
|---|---|---|---|
| Stage One — Forge Editor and portable 2D assets | ACTIVE / PARTIAL FOUNDATION | Project authority, source intake, previews, guided navigation, Jobs, evidence paths, native shape document, and minimum Editor command foundation exist | Complete Project Birth, live Editor acceptance, full manual editing, extraction, Shape Library lifecycle, SVG/PNG/Forge Pack, and release engineering |
| Stage Two — Construct and portable 3D blockouts | PLANNED | Product contract and workflow families are defined; no production Construct workspace, component schema, assembly authority, or verified 3D export is claimed | Verified Stage One release and approved reusable shape authority |
| Future Product Level Three | DEFERRED | Infrastructure relationships, regional state, distributed deltas, and advanced system-scale construction are future-only | Separate founder decision after Stage Two |
| Future Product Level Four | DEFERRED | Cross-device platform, operator jobs, collaboration, immersive clients, economy, persistent regions, and world simulation are future-only | Separate founder decision after preceding levels |

---

## 4. Shared platform workflow state

### P1. Project lifecycle

**Status:** VERIFIED CORE / UX CORRECTION REQUIRED

Present:

- canonical project manifest and self-contained directory;
- atomic creation and collision refusal;
- one-writer lock;
- writable, locked, and recovery classification;
- create/open/close session methods;
- writer-lease release and guarded close;
- project discovery bounded outside the Qt main thread where required.

Observed gap:

- Start Here technically contains Create Project and Close Project controls, but the current layout and dependence on the broader onboarding profile do not present a clear usable Project Birth journey.
- The founder requires a dedicated `PURPOSE:` input as the first project event.
- Create Project and Close Project must move to the right beneath Refresh Projects and Open Selected.

Next gate:

- Project Birth PR with Purpose storage, safe slug derivation, project-created history event, corrected control states, and focused Qt contract.

### P2. Source lifecycle

**Status:** VERIFIED FOUNDATION

Present:

- project-owned source copy;
- source identity and hash;
- bounded preview generation;
- unchanged external source bytes;
- duplicate identity handling;
- explicit project-copy processing action;
- supported intake for PNG, JPEG, WebP, BMP, TIFF, and GIF first-frame preview.

Current model-ready boundary:

- PNG, JPEG, and WebP are model-ready;
- BMP, TIFF, and GIF remain blocked from model execution pending a provenance-preserving normalized derivative.

Next gate:

- source overlay and exact region selection in the Editor.

### P3. Job lifecycle

**Status:** VERIFIED FOUNDATION

Present:

- asynchronous Qt worker patterns;
- one-active-heavy-job guard;
- elapsed time and heartbeat patterns;
- success/failure distinction;
- saved diagnostic does not imply successful workflow;
- safe cooperative worker shutdown;
- read-only Jobs evidence browser.

Next gate:

- reuse for algorithmic extraction, AI proposals, validation, and export packaging.

### P4. Recovery, migration, and integrity

**Status:** VERIFIED FOUNDATION / EXPANSION REQUIRED

Present:

- atomic project creation;
- lock and recovery classification;
- shape-document transaction marker;
- canonical rollback;
- autosave recovery;
- stale temporary-file containment;
- read-only recovery on interrupted editor transaction;
- source-truth and fresh-process launcher import checks.

Next gate:

- versioned migrations for every new Stage One and Stage Two artifact schema.

---

## 5. Stage One workflow state

### S1. Blank Shape Creation

**Status:** MERGED / DETERMINISTICALLY VERIFIED

PR #49 established:

- native `mxztar_forge_shape_document` schema version `1.0.0`;
- project-owned `structures/shape-documents/` storage;
- lazy directory creation only after writable authority;
- blank-document creation and manifest registration;
- bounded document size and command history;
- content integrity;
- autosave separate from canonical truth;
- save, reopen, rollback, and interrupted-transaction recovery.

Live status:

- full merged-main create/save/reopen acceptance remains pending because Project Birth is not yet a clear usable UI path.

### S2. Source Region and Manual Trace

**Status:** PLANNED REQUIRED

Present:

- source intake, preview, identity, and exact source handoff foundations.

Missing:

- Editor source overlay;
- region selection;
- manual line/path/silhouette/mask tracing;
- source-coordinate candidate provenance.

### S3. Algorithmic Shape Extraction

**Status:** PLANNED

Missing:

- bounded contour/mask engine;
- threshold and edge settings;
- editable candidate schema integration;
- candidate comparison UI;
- extraction worker and cancellation contract.

### S4. Optional AI Shape Proposal

**Status:** PLANNED OPTIONAL

Present:

- seven prompt contracts;
- local Ollama worker foundation;
- project-owned model-call evidence;
- model-ready image boundary.

Missing:

- editable shape-candidate output;
- source-coordinate mapping;
- correction and comparison path;
- approval isolation.

### S5. Shape Editing

**Status:** PARTIAL / DETERMINISTICALLY VERIFIED FOUNDATION

PR #49 established:

- QGraphicsScene/QGraphicsView Editor canvas;
- project document selector;
- Add Rectangle command;
- visible replayed object;
- persistent undo/redo cursor;
- redo truncation;
- autosave, explicit save, reopen, and recovery;
- oversized write rejection;
- non-first document refresh loaded exactly once.

Missing:

- selection model;
- move, resize, rotate, numeric transform;
- line, polyline, pen/Bezier, freehand, ellipse, polygon, star;
- node and handle editing;
- fill/stroke;
- snapping, alignment, guides, layers, groups, mirrors, and arrays;
- compare/version/approve/export UI.

Next gate after Project Birth:

- selection and transform command foundation.

### S6. 2D Composition

**Status:** PLANNED REQUIRED

Missing:

- group/ungroup;
- join endpoints and compound paths;
- union, difference, intersection, exclusion, divide, and combine;
- parent mapping and reversible/derived operation records.

### S7. Review and Shape Library

**Status:** PLANNED REQUIRED / EVIDENCE BROWSER EXISTS

Present:

- Shape Library evidence browser distinguishes raw success, failure, and invalid records;
- approved count truthfully remains zero;
- draft lifecycle and supersession concepts exist in planning and shape schema.

Missing:

- approved-shape write authority;
- review, correction-request, approval, rejection, versioning, supersession;
- editable approved Shape Library reopen path;
- provenance comparison view.

### S8. 2D Export and Forge Pack

**Status:** PLANNED REQUIRED

Missing:

- verified SVG adapter;
- verified PNG adapter;
- named output profiles;
- export validation and limitation reports;
- deterministic Forge Pack builder;
- Inkscape, Krita, and generic continuation fixtures.

---

## 6. Stage Two workflow state

| Workflow | Status | Present | Next dependency |
|---|---|---|---|
| T1. Declared 3D Primitive Creation | PLANNED | Product contract only | Construction recipe and component schemas |
| T2. Shape-to-Component Generation | PLANNED | Extrude/revolve/sweep/loft/shell/relief/bevel are declared methods only | Approved Stage One shapes |
| T3. Component Editing | PLANNED | No production component regeneration exists | Reversible component foundation |
| T4. Assembly and Constraint | PLANNED | Future hierarchy/anchor/connector concepts documented | Construct viewport and component identity |
| T5. Geometry Relationship and Merge | PLANNED | Group/contact/stitch/join/boolean/separate/bake distinctions documented | Assembly authority and validators |
| T6. 3D Validation, Export, and Continuation | PLANNED | GLB/glTF and OBJ named as core profiles only | Construct scene, mesh validation, Blender continuation fixture |

No production-ready 3D geometry, assembly, or export is claimed.

---

## 7. Workspace ledger

| Workspace | Status | Current truth |
|---|---|---|
| Start Here | MERGED / UX CORRECTION REQUIRED | Project authority methods exist; Purpose-driven Project Birth layout is next |
| Editor | MERGED / DETERMINISTICALLY VERIFIED FOUNDATION | Minimum canvas, selector, rectangle, undo/redo, autosave, save, reopen, and recovery exist |
| My Library | VERIFIED FOUNDATION | Visible bounded source grid, exact handoff, unchanged source bytes, safe shutdown |
| Shape Library | VERIFIED EVIDENCE BASELINE | Raw evidence browser only; approved editable lifecycle absent |
| Construct | PLANNED STAGE TWO | No production workspace exposed |
| Review | PLANNED | Review actions currently absent |
| Agent Workflows | VERIFIED OPTIONAL FOUNDATION | Seven prompt contracts and guarded local worker; not product centre |
| Jobs | VERIFIED FOUNDATION | Read-only truthful evidence browser |
| Export | PLANNED | No verified Stage One or Stage Two export workspace |

---

## 8. Significant merged foundation

- PR #33 — project manifest, required directories, history, atomic creation, collision refusal.
- PR #34 — one-writer project lock and recovery classification.
- PR #35 — project session and Start Here create/open/close authority.
- PR #36 — project-contained source intake and explicit processed lifecycle.
- PRs #39–#41 — asynchronous source intake/discovery and UI lifecycle corrections.
- PR #42 — project-owned model-call evidence.
- PR #44 — guided Next workflow and exact source handoff.
- PR #45 — stable My Library verifier lifecycle.
- PR #46 — live My Library startup refresh guard.
- PR #47 — accepted source-image compatibility.
- PR #48 — editor-first roadmap reconciliation.
- PR #49 — native shape document and minimum Editor.
- PR #50 — official launcher circular-import correction and fresh-process import contract.

Detailed historical PR evidence remains in GitHub and earlier ledger revisions.

---

## 9. PR #49 and #50 verification truth

### PR #49

Deterministic T1700 contracts passed for:

- blank-document creation;
- two-document discovery;
- exact one-load Editor refresh;
- Add Rectangle rendering;
- undo/redo;
- autosave recovery;
- explicit canonical save;
- restart restore;
- oversized-write containment;
- stale temporary-file containment;
- transaction rollback;
- read-only recovery after interruption;
- project-session regressions;
- source-truth and whitespace checks.

Live Editor acceptance is not yet complete.

### PR #50

Merged correction:

- `qt_panels` package import is side-effect free;
- official launcher installs guards without a circular import;
- fresh-process import order is verified;
- `PYTHONOPTIMIZE` is removed from verifier subprocesses;
- GitHub Source Truth CI installs required `libegl1` system support.

The branch opened far enough for the founder to inspect Start Here. A merged-main live rerun should accompany the Project Birth acceptance path rather than be misreported as a complete Editor pass.

---

## 10. Current blockers and decisions

### Project Birth UX

**Status:** NEXT ACTIVE GATE

Required:

```text
[Project selector........................] [Refresh Projects] [Open Selected]
[PURPOSE: ........................................] [Create Project] [Close Project]
```

Purpose is the first project event. The broader onboarding profile remains optional and progressive.

### Formal software licence

**Status:** BLOCKED FOUNDER DECISION

A recognised `LICENSE` and contributor policy are required before the first official public release. Public source visibility and free-of-charge access do not define redistribution permission.

### Stage Two activation

**Status:** BLOCKED BY STAGE ONE

No Construct implementation begins merely because the Stage Two plan exists. Stage One shape authority, review lifecycle, and interoperability must be verified first.

---

## 11. Immediate permitted sequence

1. merge the Stage One–Two documentation reconciliation after review;
2. implement Purpose-driven Project Birth and Start Here layout;
3. verify merged-main launcher and minimum Editor live acceptance;
4. implement selection and transform commands;
5. implement manual primitives and path/node editing;
6. implement source-region selection and manual trace;
7. implement bounded algorithmic extraction;
8. add optional AI proposals only through editable candidate authority;
9. implement review and Shape Library lifecycle;
10. verify SVG, PNG, and Forge Pack continuation;
11. complete Stage One release engineering;
12. begin reversible construction recipes;
13. implement Construct assemblies and relationships;
14. verify GLB/glTF and OBJ continuation;
15. complete Stage Two release engineering.

---

## 12. Current non-claims

MXZTAR Forge does not currently claim:

- a complete Stage One release;
- a Construct workspace;
- production-ready automatic vector extraction;
- automatic finished 3D reconstruction;
- engineering-grade dimensions;
- manufacturing safety;
- watertight or repaired meshes;
- finished topology, rigging, UVs, LODs, collision, or materials;
- verified SVG, PNG, GLB, or OBJ adapters;
- universal compatibility;
- an open-source licence;
- a new VX12 backup for the documentation reconciliation.

---

## 13. Verification rule

No area becomes `VERIFIED` solely because code or documentation was committed or merged.

Required evidence may include:

- source-truth checks;
- compile and fresh-process import checks;
- pure-logic and integration contracts;
- schema and migration validation;
- filesystem interruption and recovery tests;
- Qt lifecycle tests;
- manual T1700 smoke checks;
- downstream import or continuation tests.

The environment that ran the verification must be identified truthfully.
