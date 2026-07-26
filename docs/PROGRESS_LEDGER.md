# MXZTAR Forge v2.0 — Progress Ledger

**Ledger date:** 27 July 2026  
**Repository:** `M-TEKA-T-A-MXZTAR/MXZTAR-forge-v2.0`  
**Active product horizon:** integrated shape/object CAD, Stage One and Stage Two  
**Merged runtime baseline:** `b84f188` through PR #63  
**Current delivery gate:** PR #64 asset-generation and Construct architecture reconciliation  
**Current branch:** `agent/bring-forward-asset-generation-construct-architecture`

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

Forge is developing as a sophisticated but approachable local CAD workbench based on editable shapes, reusable assets, real 3D components, and recoverable construction relationships.

The product value path is now explicitly:

```text
Purpose
→ project
→ source image, bundled starter asset, or blank document
→ editable path and shape
→ manual, deterministic, or optional AI-assisted candidate
→ reviewed reusable asset
→ reversible 3D component
→ selectable object, surface, or area
→ pivot, anchor, and surface-assisted placement
→ group or recoverable assembly
→ reversible effect stack
→ explicit connection or geometry operation
→ portable output
```

Asset extraction and generation are brought forward because they create the reusable asset pool from which later components, groups, assemblies, and constructions compound.

The software will ship with a founder-controlled starter source-asset pack. Bundled assets remain read-only application assets and must be copied into a user project before editing.

Interaction controls must remain reachable while the user is working. Selecting a 2D or 3D output must bring that output into visible range, and an explicitly selected zoom mode must not also scroll the page.

Moving objects together around a central construct point must never silently group, assemble, stitch, weld, join, boolean, separate, or bake them.

This direction does not authorise fake perspective effects, unsupported automatic reconstruction, manufacturing claims, engineering-material claims, or dead context-menu options.

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
- PR #60 — transient positioning guides, measurements, optional snapping, rotation-aware bounds, and preserved empty-space orbit.
- PR #61 — default mouse-wheel page scrolling, selectable 3D zoom modes, and pinned Editor options.
- PR #62 — isolated wheel-verifier settings and guaranteed Qt background-thread cleanup.
- PR #63 — real wheel-event consumption, active-output reveal, and reselecting an already-active output to reveal it again.

---

## 4. Recorded T1700 evidence

### Established merged-main repository boundary

Status: **VERIFIED for the deterministic repository boundary**.

Recorded evidence includes:

- Project Birth focused verifier exit code `0`;
- complete Source Truth verification exit code `0`;
- required documentation files present;
- documentation runtime-state contract passes;
- listed Python files compile;
- CodeQL Advanced contract passes;
- launcher import contract passes;
- native shape, 3D object, single-object usability, project authoring, paired deletion, positioning-guide, wheel-routing, and prompt contracts pass.

### Smart-guide evidence

Status: **DETERMINISTICALLY VERIFIED on merged `main`**.

Recorded evidence:

- focused positioning-guide contract exit code `0`;
- complete Source Truth exit code `0`;
- rotation-aware 90-degree and 45-degree bounds pass;
- guidance-only movement does not force position;
- snapping remains separate and off by default;
- nonselected objects remain unchanged;
- empty-space drag remains orbit.

### PR #61 and PR #62 interaction evidence

Status: **MERGED and deterministically verified; live acceptance found two remaining defects**.

Recorded evidence:

- focused isolated wheel verifier exit code `0`;
- complete T1700 Source Truth exit code `0`;
- page scrolling is the first-run default;
- pinned Editor options remain outside the scroll area;
- settings persistence and Qt thread cleanup pass.

Live T1700 inspection then found:

1. switching to `3D Object View` left the object viewport below the current visible page range;
2. selecting `Zoom 3D view` still allowed the real wheel event to scroll the outer page.

The earlier verifier called handlers directly and therefore did not prove real Qt event delivery or parent propagation.

### PR #63 live 3D output reveal and wheel-event routing

Status: **DETERMINISTICALLY VERIFIED on the PR #63 branch; T1700 live acceptance pending**.

Recorded post-merge T1700 automated evidence:

- T1700 synchronized to merge commit `b84f188`;
- focused real-event verifier exit code `0`;
- complete Source Truth exit code `0`;
- switching from 2D to 3D reveals the selected output;
- reselecting the already-active 3D action reveals its output;
- real wheel zoom changes zoom without page-scroll leakage;
- Ctrl+wheel zoom changes zoom without page-scroll leakage;
- wheel over 2D continues to scroll the page;
- real `QWheelEvent` objects are sent through Qt;
- no Qt thread shutdown warning appears.

Final manual live acceptance of those corrected interactions remains required before the interaction gate becomes fully VERIFIED.

No downstream export, production mesh, manufacturing, tracing, approved library, persistent surface-area, effect-stack, or advanced assembly acceptance is implied.

---

## 5. Current workspace truth

| Workspace | Current truth |
|---|---|
| Start Here | Purpose-driven Project Birth, discovery, open/switch, close, and guided blank-document path are implemented |
| Editor | Primary integrated 2D shape and 3D object workspace; five primitives, direct manipulation, guides, wheel routing, and active-output reveal exist |
| My Library | Verified bounded source intake, previews, exact handoff, and guarded lifecycle |
| Shape Library | Evidence browser only; approved editable lifecycle and insertion are not implemented |
| Agent Workflows | Optional local-AI assessment and planning foundation; not geometry authority |
| Jobs | Verified read-only evidence browser |
| Construct | Current 3D object-scene foundation only; areas, anchors, groups, assemblies, effect stacks, and explicit connection operations remain planned |
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
- source-region tracing;
- deterministic extraction;
- layers, groups, locking, visibility, arrays, mirrors, 2D booleans, or reviewed reusable shape insertion.

### Project-owned 3D object scene

Status: **DETERMINISTICALLY VERIFIED foundation**.

Implemented on merged `main`:

- five native shapes become real extruded 3D objects;
- source shape and object membership remain linked;
- XYZ position, width, height, depth, and three-axis rotation;
- colour and opacity;
- object selection, drag movement, resize, and numeric inspector;
- empty-space orbit;
- perspective, grid, line, camera, and zoom persistence;
- reversible object edits;
- paired membership during Undo, Redo, and deletion;
- atomic save, rollback, and restart restoration;
- moving one selected object leaves nonselected objects unchanged.

Not implemented:

- persistent area or surface subsets;
- primary focus objects or surfaces as project authority;
- anchors, sockets, pivots beyond current object transform state;
- object groups or recoverable assemblies;
- surface-effect stacks;
- visual seams;
- stitch, weld, join mesh, booleans, separate, or bake;
- revolve, sweep, loft, shell, relief, bevel, vertex/face editing, or sculpting;
- verified 3D export.

---

## 7. Active asset-generation and Construct architecture

Status: **FOUNDER-AUTHORISED ACTIVE PLAN; NO NEW RUNTIME CAPABILITY CLAIMED**.

The governing addendum is:

- `docs/product/ASSET_GENERATION_AND_CONSTRUCT_ARCHITECTURE.md`.

It brings forward:

- freeform path authority;
- source-region and manual tracing;
- deterministic contour, threshold, edge, mask, and silhouette candidates;
- a versioned installed starter source-asset pack;
- review and reusable Shape Library insertion;
- reversible shape-to-component generation;
- stable object, area, surface, focus, pivot, anchor, group, and assembly records;
- central construct point and modular placement;
- reversible targetable effect stacks;
- greebling, roughness, distortion, bend, logic wiring, and metallic hue profiles;
- explicit separation of placement, snapping, grouping, assembly contact, visual seams, mesh stitch or weld, join mesh, booleans, separate, and bake.

Initial metallic visual profiles are:

- Brushed Titanium;
- Polished Chrome;
- Anodized Aluminium;
- Oxidized Copper;
- Iridescent Nickel.

Initial logic-wiring routing modes include Randomized, Symbiotic, Aligned, Radial, and Parallel.

These are planned visual-design systems, not engineering material or electronics claims.

---

## 8. Brought-forward engineering sequence

PR #63 manual live acceptance remains the final gate before new runtime work begins.

The active sequence is:

1. freeform path authority;
2. source-region selection and manual tracing;
3. deterministic extraction candidates;
4. shipped starter source-asset pack and copy-into-project command;
5. optional AI proposals through editable candidate authority;
6. review, approval, versioning, and real Shape Library insertion;
7. shape-to-component recipe registry;
8. area, surface, pivot, anchor, focus, and named perspective authority;
9. modular placement around the central construct point;
10. object groups and recoverable assemblies;
11. effect-stack core;
12. greebling, roughness, distortion, bend, logic wiring, and metallic hue profiles;
13. visual seams and separately verified stitch/weld/join/boolean/separate/bake operations;
14. verified SVG, PNG, GLB/glTF, and OBJ continuation;
15. release asset-pack installation, update, migration, backup, licence, and recovery gates.

```text
focused branch
→ deterministic verifier
→ Source Truth
→ review comments
→ merge confirmation
→ T1700 sync
→ focused output and inspection
→ complete Source Truth output and inspection
→ applicable live acceptance
→ ledger and capability-boundary update
```

---

## 9. Current non-claims

Forge does not currently claim:

- a completed CAD release;
- freeform editable paths;
- editable tracing from arbitrary source images;
- automatic editable extraction;
- a shipped starter asset pack;
- approved Shape Library insertion;
- stable selectable surface subsets;
- primary focus surfaces;
- anchors, sockets, object groups, or recoverable assemblies;
- surface-effect stacks;
- greebling, roughness, distortion, bend, logic wiring, or metallic profiles;
- visual seams;
- stitch, weld, join mesh, booleans, separate, bake, topology repair, rigging, UVs, LODs, collision, or production materials;
- engineering-grade dimensions or tolerances;
- engineering material properties;
- manufacturing safety;
- watertight or repaired meshes;
- verified SVG, PNG, GLB/glTF, or OBJ continuation;
- universal downstream compatibility;
- an open-source licence.

---

## 10. Verification rule

No capability becomes VERIFIED solely because code was committed or merged.

Evidence may include compile and import checks, schema and command replay, project integrity, interruption and rollback, Qt lifecycle and offscreen rendering, real event delivery, manual T1700 interaction, seed stability, stale-target recovery, failure rollback, and downstream continuation tests.
