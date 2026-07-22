# MXZTAR Forge v2.0 — Progress Ledger

**Ledger date:** 22 July 2026  
**Repository:** `M-TEKA-T-A-MXZTAR/MXZTAR-forge-v2.0`  
**Active product horizon:** Stage One and Stage Two  
**Current delivery gate:** PR #53 — project routing and Editor menu primitives  
**Next core Stage One gate after PR #53:** selection and transform commands

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

The controlled product map contains:

- 4 shared platform workflow families;
- 8 Stage One workflow families;
- 6 Stage Two workflow families.

Stage One and Stage Two together define the planned finished product. Future Product Levels Three and Four remain deferred.

---

## 3. Product-stage ledger

| Product stage | Status | Current boundary | Exit gate |
|---|---|---|---|
| Stage One — Forge Editor and portable 2D assets | ACTIVE / PARTIAL | Project authority, Purpose-driven Project Birth, source intake, guided navigation, Jobs, native shape documents, minimum Editor commands, recovery, and PR #53 menu/primitive work | Complete selection/transforms, path editing, source tracing, extraction, Shape Library lifecycle, SVG/PNG/Forge Pack, and release engineering |
| Stage Two — Construct and portable 3D blockouts | PLANNED | Product contract and workflow families only | Verified Stage One release and approved reusable shape authority |
| Future Product Level Three | DEFERRED | Infrastructure relationships, regional state, distributed deltas, and advanced system-scale construction | Separate founder decision after Stage Two |
| Future Product Level Four | DEFERRED | Cross-device platform, operator jobs, collaboration, immersive clients, economy, persistent regions, and world simulation | Separate founder decision after preceding levels |

---

## 4. Shared platform workflow state

### P1. Project lifecycle

**Status:** VERIFIED CORE

Present and accepted on merged `main` through PR #52:

- canonical project manifest and self-contained directory;
- atomic creation and collision refusal;
- one-writer lock;
- writable, locked, and recovery classification;
- create, open, and close session methods;
- Purpose as the first project event;
- exact Purpose storage with derived bounded display name and safe slug;
- durable `project_created` history event;
- clear Start Here control states;
- creator/workflow profile remains optional;
- writer-lease release and guarded close;
- merged-main live Project Birth, blank-document, rectangle, save, close, relaunch, reopen, Purpose restore, and document restore acceptance on the T1700.

PR #53 side quest:

- make Start Here the official default launch surface;
- change Open Selected into a menu with Open Project and Go to Project;
- make Go to Project open Editor and display the current project build.

PR #53 must complete normal review, automated checks, merge, T1700 sync, and live acceptance before these new routing behaviours become VERIFIED.

### P2. Source lifecycle

**Status:** VERIFIED FOUNDATION

Present:

- project-owned source copy;
- source identity and hash;
- bounded preview generation;
- unchanged external source bytes;
- duplicate identity handling;
- explicit project-copy processing action;
- PNG, JPEG, WebP, BMP, TIFF, and GIF first-frame preview support.

Current model-ready boundary:

- PNG, JPEG, and WebP are model-ready;
- BMP, TIFF, and GIF remain blocked from model execution pending a provenance-preserving normalized derivative.

Next product gate:

- source overlay and exact region selection in the Editor.

### P3. Job lifecycle

**Status:** VERIFIED FOUNDATION

Present:

- asynchronous Qt worker patterns;
- one-active-heavy-job guard;
- elapsed time and heartbeat patterns;
- truthful success and failure distinction;
- saved diagnostics do not imply successful workflow completion;
- safe cooperative worker shutdown;
- read-only Jobs evidence browser.

Next product use:

- algorithmic extraction, optional AI proposals, validation, and export packaging.

### P4. Recovery, migration, and integrity

**Status:** VERIFIED FOUNDATION / EXPANSION REQUIRED

Present:

- atomic project creation;
- lock and recovery classification;
- shape-document transaction marker;
- canonical rollback;
- autosave recovery;
- stale temporary-file containment;
- read-only recovery on interrupted Editor transaction;
- source-truth and fresh-process launcher checks.

Required expansion:

- versioned migrations for every new Stage One and Stage Two artifact schema.

---

## 5. Stage One workflow state

### S1. Blank Shape Creation

**Status:** VERIFIED

Present:

- native `mxztar_forge_shape_document` schema version `1.0.0`;
- project-owned `structures/shape-documents/` storage;
- blank-document creation and manifest registration;
- bounded document size and command history;
- content integrity;
- autosave separate from canonical truth;
- save, reopen, rollback, and interrupted-transaction recovery;
- merged-main T1700 live create, edit, save, relaunch, reopen, and restore acceptance after PR #52.

### S2. Source Region and Manual Trace

**Status:** PLANNED REQUIRED

Present foundation:

- source intake, preview, identity, and exact source handoff.

Missing:

- Editor source overlay;
- region selection;
- manual line, path, silhouette, and mask tracing;
- source-coordinate candidate provenance.

### S3. Algorithmic Shape Extraction

**Status:** PLANNED

Missing:

- bounded contour or mask engine;
- threshold and edge settings;
- editable candidate schema integration;
- candidate comparison UI;
- extraction worker and cancellation contract.

### S4. Optional AI Shape Proposal

**Status:** PLANNED OPTIONAL

Present foundation:

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

**Status:** PARTIAL

Merged and live-accepted foundation:

- QGraphicsScene/QGraphicsView canvas;
- project document selector;
- reversible rectangle command;
- persistent undo/redo cursor;
- autosave, explicit save, reopen, and recovery;
- oversized-write containment;
- non-first document refresh loaded exactly once.

PR #53 side quest adds, subject to normal processing and live acceptance:

- compact `EDITOR; native shape-document workspace` heading;
- one upper menu row;
- Document menu: Load Project, New Blank Document, Save Document;
- Shape menu: Rectangle, Square, Circle, Ellipse, Star;
- Edit menu: Undo, Redo;
- explicit reversible command types and rendering for all five primitive shapes;
- durable restore of all primitive types after save and reopen.

Next core gate after PR #53:

- unified selection model;
- move;
- resize;
- rotate;
- numeric transform authority.

Still missing after that gate:

- line, polyline, pen/Bezier, and freehand tools;
- node and handle editing;
- fill and stroke editing;
- snapping, alignment, guides, layers, groups, mirrors, and arrays;
- compare, version, approve, and export UI.

### S6. 2D Composition

**Status:** PLANNED REQUIRED

Missing:

- group and ungroup;
- join endpoints and compound paths;
- union, difference, intersection, exclusion, divide, and combine;
- parent mapping and reversible or explicitly derived operation records.

### S7. Review and Shape Library

**Status:** PLANNED REQUIRED / EVIDENCE BROWSER EXISTS

Present:

- Shape Library evidence browser distinguishes raw success, failure, and invalid records;
- approved count truthfully remains zero;
- draft lifecycle and supersession concepts exist in planning and shape schema.

Missing:

- approved-shape write authority;
- review, correction request, approval, rejection, versioning, and supersession;
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
| T2. Shape-to-Component Generation | PLANNED | Declared methods only | Approved Stage One shapes |
| T3. Component Editing | PLANNED | No production regeneration | Reversible component foundation |
| T4. Assembly and Constraint | PLANNED | Documented concepts only | Construct viewport and component identity |
| T5. Geometry Relationship and Merge | PLANNED | Documented distinctions only | Assembly authority and validators |
| T6. 3D Validation, Export, and Continuation | PLANNED | Core profiles named only | Construct scene, mesh validation, Blender fixture |

No production-ready 3D geometry, assembly, or export is claimed.

---

## 7. Workspace ledger

| Workspace | Status | Current truth |
|---|---|---|
| Start Here | VERIFIED PROJECT BIRTH / PR #53 ROUTING IN PROCESS | Purpose-driven creation is live accepted; default-launch and Go to Project routing are in PR #53 |
| Editor | PARTIAL | Minimum live editor exists; menu tree and five primitives are in PR #53; selection/transforms remain next |
| My Library | VERIFIED FOUNDATION | Bounded source grid, exact handoff, unchanged bytes, safe shutdown |
| Shape Library | VERIFIED EVIDENCE BASELINE | Raw evidence browser only; approved editable lifecycle absent |
| Construct | PLANNED STAGE TWO | No production workspace exposed |
| Review | PLANNED | Review actions absent |
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
- PR #50 — official launcher circular-import correction.
- PR #51 — reconciled Stage One–Two product authority and public README.
- PR #52 — Purpose-driven Project Birth and Start Here authority layout.

PR #53 is the current side-quest delivery and is not recorded as merged until GitHub confirms the merge.

---

## 9. PR #52 verification truth

Automated contracts passed for:

- Purpose validation;
- exact Purpose preservation;
- display-name and slug derivation;
- first project history event;
- Start Here control states;
- optional-profile stability;
- blank-document handoff;
- project-session regressions;
- source-truth, compile, and security checks.

Founder-reported merged-main T1700 live acceptance confirmed:

- app launch;
- Start Here Project Authority layout;
- blank Purpose disables creation;
- valid Purpose enables creation;
- project creation;
- attached Purpose becomes non-editable;
- guided New Blank Document route;
- Editor open;
- rectangle add, undo, redo, and save;
- normal close and relaunch;
- project reopen;
- Purpose, saved document, and rectangle restore.

This evidence closes the Project Birth gate and the minimum blank-shape live-acceptance gate.

---

## 10. Current blockers and decisions

### PR #53 processing

**Status:** ACTIVE DELIVERY GATE

Required sequence:

1. process PR #53 and any code review findings;
2. merge only after the reviewed head is stable and checks pass;
3. sync T1700 `main` after merge confirmation;
4. perform the applicable live Start Here, Go to Project, menu, primitive, save, and reopen acceptance;
5. update this ledger only from recorded evidence;
6. begin the selection and transform PR.

### Formal software licence

**Status:** BLOCKED FOUNDER DECISION

A recognised `LICENSE` and contributor policy are required before the first official public release. Public source visibility and free-of-charge access do not define redistribution permission.

### Stage Two activation

**Status:** BLOCKED BY STAGE ONE

No Construct implementation begins merely because the Stage Two plan exists. Stage One shape authority, review lifecycle, and interoperability must be verified first.

---

## 11. Immediate permitted sequence

1. process PR #53;
2. sync T1700 after confirmed merge;
3. complete the PR #53 live app test;
4. implement the selection model;
5. implement move, resize, rotate, and numeric transforms;
6. implement manual path and node tools;
7. implement source-region selection and manual trace;
8. implement bounded algorithmic extraction;
9. add optional AI proposals only through editable candidate authority;
10. implement review and Shape Library lifecycle;
11. verify SVG, PNG, and Forge Pack continuation;
12. complete Stage One release engineering;
13. begin reversible construction recipes;
14. implement Construct assemblies and relationships;
15. verify GLB/glTF and OBJ continuation;
16. complete Stage Two release engineering.

---

## 12. Current non-claims

MXZTAR Forge does not currently claim:

- a complete Stage One release;
- selection, move, resize, rotate, or numeric transform capability;
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
- live T1700 acceptance of PR #53 before that evidence is supplied.

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

The environment that ran each verification must be identified truthfully.
