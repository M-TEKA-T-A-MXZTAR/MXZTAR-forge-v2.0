# MXZTAR Forge v2.0 — Active Engineering Plan

**Plan date:** 6 August 2026  
**Repository baseline assessed:** merged `main` through PR #80  
**Current programme:** recoup, regroup, proceed

## 1. Role of this document

This is the near-term ordered execution authority.

It answers:

- what gate is active now;
- what must already be true before work begins;
- what the gate may change;
- what it must preserve;
- what evidence closes the gate;
- what work remains out of scope.

The Master Build Plan defines the stable finished-product boundary. The Current Capability Boundary records what exists now. The Progress Ledger records dated evidence and causal learning.

## 2. Baseline recovered through PR #80

The current merged foundation includes, at its implemented contract boundary:

- project creation, switching, rename, close, recoverable deletion, locking, and recovery classification;
- native project-owned shape documents;
- Rectangle, Square, Circle, Ellipse, and Star creation;
- autosave, canonical save, rollback, Undo, Redo, reopen, and direct paired deletion;
- project-owned 3D object scenes linked to 2D source shapes;
- direct 2D movement with click-offset preservation;
- direct durable 2D resize, including proportional Square and Circle behaviour;
- paired 2D/3D position and size synchronization;
- direct 3D object movement and resize;
- explicit Select, Move, Rotate, Resize, and Orbit View modes;
- front orthographic 3D Design View on 3D entry, with deliberate Perspective and Orbit controls retained;
- stable world/camera presentation during object manipulation;
- positioning guides, measurements, optional snapping, and wheel-routing controls;
- Save Project transaction and project/document controls;
- local-first source intake, evidence browsers, optional Ollama assessment, and modest-hardware guards.

Merged implementation is not automatically equivalent to fresh live acceptance. Evidence status is recorded separately.

## 3. Gate G0 — Governance recovery and final-runtime proof

**Status:** ACTIVE

### Purpose

Stop current-state documentation from lagging behind the code and ensure every future verifier targets the official composed runtime.

### Required work

- simplify document authority;
- record the final runtime composition;
- establish regression-causality and invariant rules;
- update the current capability snapshot through PR #80;
- replace fossilised documentation checks with structural checks;
- ensure historical correction documents cannot silently outrank current authority.

### Preserved invariants

No runtime feature, schema, project file, UI control, AI behaviour, export claim, or existing user data changes in this gate.

### Exit evidence

- documentation files and links pass;
- updated documentation verifier passes;
- Source Truth shell syntax passes;
- no runtime Python behaviour is modified;
- founder review of the recovered product sequence.

## 4. Gate G1 — Final-runtime acceptance and interaction baseline

**Status:** NEXT

### Purpose

Create one dependable acceptance baseline for the Editor before adding new geometry capability.

### Entry conditions

- G0 merged;
- official launcher and installer order documented;
- all relevant final-runtime classes resolvable from one verifier fixture.

### Required proof

Using the official final runtime:

1. create or open a writable project and document;
2. add every implemented primitive;
3. select and move a 2D shape while preserving click offset;
4. resize each supported shape, including proportional Square and Circle constraints;
5. verify one durable command per completed action;
6. verify paired 3D position and size synchronization;
7. Undo and Redo both operations;
8. enter 3D and confirm front orthographic Design View;
9. move and resize the selected 3D object without moving camera/grid landmarks;
10. enter Orbit View and Perspective deliberately, then return to 2D and 3D;
11. confirm 3D re-entry restores the intended Design View and Select interaction;
12. Save Project, close, reopen, and compare canonical state;
13. verify project switching, document lifecycle, wheel routing, guides, snapping, and clean shutdown remain usable.

### Exit evidence

- focused final-runtime contract;
- complete Source Truth pass;
- T1700 live interaction acceptance;
- no restoration side quest opened by the gate.

### Out of scope

No freeform path, tracing, extraction, starter pack, library approval, new 3D recipe, effect, assembly, or export capability.

## 5. Gate S1 — Freeform Path Authority

**Status:** PLANNED AFTER G1

### User outcome

Create and edit a durable open or closed path from a blank document without AI or network access.

### Minimum complete slice

- one native path schema integrated into the existing shape document;
- line and cubic Bezier segments;
- stable node and handle IDs;
- select, add, move, and delete node;
- open/close path command;
- fill/stroke boundary stated truthfully;
- command replay, Undo, Redo, autosave, save, reopen, rollback, and validation;
- no automatic 3D conversion until a separate recipe exists.

### Preserved invariants

All five primitives, direct movement/resize, paired object scenes, project controls, camera, guides, settings, and evidence panels remain unchanged.

### Exit evidence

Pure path-state tests, final-runtime Qt editing tests, interruption/reopen proof, complete Source Truth, and T1700 live acceptance.

## 6. Gate S2 — Source Region and Manual Trace

**Status:** PLANNED

### User outcome

Select an exact source region and manually trace it into editable path geometry.

### Requirements

- source image remains unchanged;
- project-owned source and bounded preview remain distinct;
- region coordinates are durable and map correctly to source pixels;
- trace geometry is editable, not merely a raster mask;
- source, region, transform, and author provenance persist;
- no model call is required.

### Out of scope

Automatic contouring, AI geometry authority, approval, and export.

## 7. Gate S3 — Deterministic Extraction Candidates

**Status:** PLANNED

### User outcome

Generate bounded contour, threshold, edge, mask, or silhouette candidates from a selected source region and choose one for editing.

### Requirements

- candidates remain proposals until selected and edited;
- parameters, source region, seed where applicable, and algorithm version persist;
- generation is a bounded job outside the Qt main thread;
- candidate comparison and rejection remain visible;
- no candidate silently becomes approved truth.

## 8. Gate S4 — Starter Source-Asset Pack

**Status:** PLANNED

### User outcome

Browse versioned bundled starter assets offline and copy one into the current project before editing.

### Requirements

- read-only installed pack;
- manifest, IDs, hashes, provenance, licence, version, and compatibility metadata;
- integrity validation;
- explicit copy-into-project command;
- no mutation of installed originals;
- clear separation from private user assets and approved Shape Library assets.

## 9. Gate S5 — Review and Shape Library Authority

**Status:** PLANNED

### User outcome

Review an editable candidate, approve or reject it, version or supersede it, and insert an approved reusable shape through a reversible document command.

### Requirements

- human approval;
- approval, rejection, correction, version, and supersession records;
- stable library asset identity;
- explicit `Insert into Current Document` command;
- provenance and licence preserved;
- raw AI evidence never presented as an approved shape.

## 10. Gate T1 — Shape-to-Component Recipe Registry

**Status:** PLANNED AFTER STAGE ONE FOUNDATION

Generalise the existing primitive extrusion foundation into declared, reversible shape-to-component recipes.

Initial work should preserve parent shape identity, recipe parameters, units, axes, origin, regeneration, failure state, and Undo/Redo.

No recipe name may appear before its full persistence and verification path exists.

## 11. Later ordered gates

After the preceding gates pass:

1. persistent areas and surface subsets;
2. pivots, anchors, sockets, focus targets, and named views;
3. modular placement around a central construct point;
4. object groups and recoverable assemblies;
5. reversible effect-stack core;
6. bounded visual effect families;
7. explicit visual seams;
8. separately verified stitch/weld, join, boolean, separate, and bake operations;
9. verified SVG/PNG continuation;
10. verified GLB/glTF and OBJ continuation.

Placement never silently becomes grouping, assembly, stitch, weld, join, boolean, separate, or bake.

## 12. Deferred work

The following remain outside the active v2.0 execution sequence unless current authority is deliberately revised:

- Product Levels Three and Four;
- persistent shared worlds;
- immersive or civilisation-platform runtime;
- cloud-dependent project authority;
- unsupported engineering or manufacturing certification;
- marketplace, economy, or monetisation controls inside Forge before the core asset workflow is reliable.

## 13. Priority rule

When a side quest appears, choose in this order:

1. prevent data loss, authority corruption, unsafe behaviour, or a launch blocker;
2. restore an already accepted user workflow;
3. remove a blocker to the active gate;
4. improve verification fidelity or final-runtime clarity;
5. continue the active gate;
6. defer convenience, decoration, speculative architecture, and distant vision.

The objective is not maximum PR count. It is dependable compounding user value.