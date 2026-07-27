# MXZTAR Forge v2.0 — Current Capability Boundary

**Snapshot date:** 27 July 2026  
**Merged runtime baseline:** `main` through PR #66 at `5c2c91d`  
**Active branch evidence:** PR #67 replaces the rejected always-open Editor action tree with one compact fixed command strip; automated verification passes and T1700 live acceptance remains pending

## 1. Purpose

This document is the concise present-tense companion to the Master Build Plan and the active Asset Generation and Construct Architecture addendum.

It distinguishes:

1. capability available on merged `main`;
2. capability implemented and deterministically verified but still awaiting applicable live acceptance;
3. incomplete foundations;
4. planned capability.

The Master Build Plan remains the finished-product boundary. `ASSET_GENERATION_AND_CONSTRUCT_ARCHITECTURE.md` controls the nearer engineering sequence. The Progress Ledger records dated delivery history.

## 2. Status vocabulary

| Status | Meaning |
|---|---|
| VERIFIED | Appropriate automated and recorded T1700 evidence exists for the stated boundary |
| DETERMINISTICALLY VERIFIED | Automated contracts pass; additional visual or downstream acceptance may still be required |
| PARTIAL | Useful implementation exists, but the complete user workflow does not |
| PLANNED | Required by the product plan but not implemented |
| DEFERRED | Outside the active Stage One–Two delivery sequence |

## 3. Current capability matrix

| Capability | Current state | Current truth |
|---|---|---|
| Purpose-driven project creation | VERIFIED | Start Here preserves Purpose, derives safe identity, writes project authority, and guides the user to one blank Editor document |
| Open, close, reopen and recover projects | VERIFIED foundation | One-writer authority, recovery classification, canonical files and read-only recovery contracts exist |
| Create a fresh project from Editor | DETERMINISTICALLY VERIFIED | Entering Editor while detached creates a unique writable project and one blank document |
| Switch projects from Start Here or Editor | DETERMINISTICALLY VERIFIED | Project authority, document chooser and dependent panels remain synchronized; failed switching restores prior authority |
| Recoverable Project Trash | DETERMINISTICALLY VERIFIED on merged main | Start Here and Editor place Delete Project beside switching; the exactly selected direct-child project is moved into hidden `.project-trash` with typed-name confirmation, lock checks, active-work blocking, receipt-failure rollback and a recovery receipt; no permanent-delete command exists |
| Native editable shape document | VERIFIED foundation | Versioned project-owned shape document, command replay, autosave, canonical save, rollback and reopen are implemented |
| Build 2D shapes from scratch | PARTIAL | Rectangle, Square, Circle, Ellipse and Star are implemented; freeform path, pen, node and handle tools are not |
| Undo and redo | DETERMINISTICALLY VERIFIED | Shape creation and 3D object edits use durable reversible command state within implemented command families |
| Direct delete | DETERMINISTICALLY VERIFIED | Explicit selection is required; paired 2D shape and 3D object deletion persists without misusing Undo |
| Turn native shapes into 3D objects | DETERMINISTICALLY VERIFIED foundation | The five implemented primitives become real extruded project-owned 3D objects |
| Edit one 3D object | DETERMINISTICALLY VERIFIED | Position, width, height, depth, three-axis rotation, colour and opacity persist; nonselected objects remain unchanged |
| 3D viewport navigation | DETERMINISTICALLY VERIFIED on merged main | Empty-space drag orbits; real wheel zoom is consumed by the 3D viewport without also scrolling the page; final manual interaction acceptance remains pending |
| Active output reveal | DETERMINISTICALLY VERIFIED on merged main | Switching or explicitly reselecting 2D/3D repositions the existing outer scrollbar so the selected output begins inside visible page range |
| Smart positioning guides | DETERMINISTICALLY VERIFIED on merged main | PR #60 provides transient X/Y lines, X/Y/Z centre deltas, nearest-object measurements and rotation-aware bounds |
| Optional snapping | DETERMINISTICALLY VERIFIED on merged main | Separate control, off by default, bounded 1–50 scene-unit tolerance, X/Y only; guides off also disables snapping |
| Mouse-wheel page scrolling | DETERMINISTICALLY VERIFIED on merged main | Wheel over 2D or 3D output scrolls the existing outer page by default without changing 3D zoom |
| Explicit 3D wheel zoom | DETERMINISTICALLY VERIFIED on merged main | Real Qt wheel delivery changes zoom and leaves the page scrollbar unchanged when direct zoom or Ctrl+wheel zoom is authorised |
| Sticky Editor control bar | DETERMINISTICALLY VERIFIED on merged main | PR #65 fixes the Editor interaction row directly above the scroll viewport; page movement cannot move the row away |
| Compact Editor command strip | DETERMINISTICALLY VERIFIED on PR #67 branch | Document, Shape, Edit, Object and View share one fixed row with a shortened wheel selector; each real menu opens temporarily and closes after selection, the duplicate in-page category buttons are hidden while the document selector remains, the row is capped at 48 pixels and fits the supported 760-pixel minimum window width |
| Extract shapes from a 2D image by tracing | PLANNED — brought forward | Source intake and previews exist, but no manual tracing path creates editable geometry |
| Extract shapes algorithmically | PLANNED — brought forward | No contour, threshold, edge, mask or silhouette engine creates editable candidates |
| Extract shapes through Ollama | PARTIAL evidence only | Ollama may assess source art and describe likely shapes or extraction zones; it does not create authoritative editable geometry |
| Shipped starter source-asset pack | PLANNED — brought forward | The application has an `assets` root, but no versioned starter-pack manifest, bundled editable-copy workflow, or installed asset set exists |
| Approve a reusable Shape Library asset | PLANNED — brought forward | Shape Library is an evidence browser; approval, rejection, versioning and supersession authority are absent |
| Insert Shape Library assets into a document | PLANNED — brought forward | No approved reusable asset schema and no `Insert into Current Document` operation are exposed |
| Shape-to-component recipe registry | PLANNED — brought forward | Current primitive extrusion is integrated, but there is no general reviewed-shape recipe registry or parameterized parent-history contract |
| Persistent object areas or surface subsets | PLANNED — brought forward | No stable area IDs, face/panel/edge subsets, local frames, normals, or stale-parent repair authority exist |
| Primary focus object or surface | PLANNED — brought forward | The viewport can select one object, but no persisted focus target, focus pivot, named surface focus, or context-command framework exists |
| Anchors, sockets and central construct placement | PLANNED — brought forward | Current scene-centre guidance exists, but no persistent anchors, sockets, surface-normal alignment, compatibility rules, or construct-origin placement workflow exists |
| Object groups | PLANNED — brought forward | No persistent named selection sets, shared movement/visibility authority, or group-targeted effects exist |
| Recoverable assemblies | PLANNED — brought forward | Scene membership exists, but hierarchy, anchors, contacts, constraints, replacement, and assembly recovery authority do not |
| Reversible surface-effect stacks | PLANNED — brought forward | Greebling, roughness, distortion, bend, logic wiring, and metallic hue profiles are architecture only |
| Visual seams | PLANNED — brought forward | No area-to-area seam, gasket, rim, trim, conduit, or bridging-detail command exists |
| Stitch, weld, join mesh or boolean merge | PLANNED | These operations are deliberately distinct and not implemented |
| Advanced 3D creation from scratch | PARTIAL | Primitive extrusion and numeric editing exist; revolve, sweep, loft, shell, relief, bevel, vertex/face editing and sculpting do not |
| SVG, PNG, GLB/glTF or OBJ export | PLANNED | No named validated downstream output profile is exposed |
| CodeQL Advanced security analysis | VERIFIED repository control | GitHub Actions and Python analyses run through the merged advanced workflow |

Historical merged-main label: `Pinned Editor options | DETERMINISTICALLY VERIFIED on merged main` proved only that controls were outside the scroll content. PR #65 added viewport-top geometry. PR #66 then introduced an always-open action tree that passed deterministic checks but failed T1700 live acceptance because it consumed too much workspace. PR #67 supersedes that rejected current-state interaction with one compact command strip.

Historical PR #63 branch labels retained for evidence traceability: `Explicit 3D wheel zoom | DETERMINISTICALLY VERIFIED on PR #63 branch` and `Active output reveal | DETERMINISTICALLY VERIFIED on PR #63 branch`.

The earlier interaction requirement remains true: Document, Shape, Edit, Object and View actions remain available after scrolling to the bottom, but only one fixed category row is displayed.

Deterministic verification uses real `QWheelEvent` delivery through Qt rather than direct fake-handler calls.

Deterministic verification also uses real dropdown-menu mouse clicks, fixed window-relative geometry, a 760-pixel minimum-width layout check, isolated settings, canonical project discovery, real filesystem moves, receipt-failure rollback and background-thread drainage inside a temporary projects root.

## 4. Image-to-shape authority

Forge must not confuse visual assessment with geometry extraction.

### Current path

```text
2D image
→ project-owned source copy and bounded preview
→ optional Ollama assessment or raw findings
→ no editable traced shape is created
```

### Required implemented path

```text
2D image or bundled source asset
→ exact source region
→ manual trace or deterministic contour proposal
→ editable candidate geometry
→ user correction
→ review and approval
→ optional Shape Library reuse
→ declared shape-to-component recipe
```

Ollama may classify, name, rank or explain candidate geometry. It may not become the sole geometry authority. Coordinates, editable paths, user correction and explicit approval establish project truth.

## 5. Starter source-asset boundary

The application path registry already defines an `assets` root, but Forge does not yet ship a governed starter pack.

Before bundled assets may be advertised, Forge needs:

- a versioned starter-pack manifest;
- stable IDs, hashes, provenance, licence, compatibility and dependency metadata;
- read-only installed assets;
- an explicit copy-into-project command before editing;
- integrity checks and failure handling;
- offline availability;
- migration and update rules;
- separation between bundled, project-owned and private user assets.

## 6. Current 2D-to-3D authority

Each supported native primitive becomes one extruded object linked by source shape ID.

Current object authority includes:

- project-owned `mxztar_forge_object_scene` state;
- stable object and source-shape membership;
- XYZ position;
- width, height and depth;
- X, Y and Z rotation;
- colour and opacity;
- camera, perspective, grid, line and zoom state;
- reversible object edits;
- atomic save, rollback and restart restoration.

This is a real 3D blockout foundation. It is not the complete Construct workflow or a production mesh modeller.

## 7. Smart-guide authority

PR #60 is merged. Its focused verifier and complete T1700 Source Truth suite exit `0`.

Interaction rules include:

1. Guides appear only while moving one selected object.
2. Measurements update continuously during movement.
3. Guides disappear immediately on release.
4. `Position Guides` and `Snap to Guides` remain separate controls.
5. Snapping is off by default.
6. Turning guides off also disables snapping, preventing invisible forced movement.
7. Tolerance is explicitly bounded from 1 to 50 scene units.
8. Snapping changes only the selected object's X/Y position.
9. Nonselected objects remain unchanged.
10. Empty-space drag remains orbit.

Not included yet:

- equal-gap or distribution guides;
- persistent user guide objects;
- transform gizmos;
- anchor, socket, pivot, or surface-normal snapping;
- dimensional engineering tolerance claims.

## 8. PR #61–PR #67 scrolling, zoom and continuously visible controls

```text
Scroll page                  → wheel over 2D or 3D output moves the outer page
Zoom 3D view                 → wheel over 3D output zooms; wheel over 2D scrolls
Scroll page; Ctrl+wheel zoom → normal wheel scrolls; Ctrl+wheel over 3D zooms
```

The compact selector displays shortened labels—`Scroll`, `3D zoom`, and `Ctrl+wheel zoom`—while tooltips and status messages retain the full behaviour descriptions.

Required interaction rules:

1. `Scroll page` is the first-run default.
2. Page scrolling uses the existing outer `QScrollArea`; no competing scroll authority is created.
3. Selecting 2D or 3D brings the active output into visible page range after layout settles.
4. Explicitly reselecting the already-active output reveals it again.
5. Scroll mode never changes 3D zoom.
6. Zoom occurs only when the selected mode authorises it.
7. An authorised 3D zoom event is delivered once, accepted, and consumed before page propagation.
8. Direct zoom and Ctrl+wheel zoom leave the page scrollbar unchanged.
9. Wheel over 2D output continues to scroll the page in every mode.
10. Sidebar navigation is not intercepted.
11. The selected mode persists through existing application settings.
12. The Editor controls occupy a dedicated row directly above `page_scroll`, outside the scrolling content.
13. The control bar retains the same window-relative top coordinate while the Editor page scrolls from top to maximum.
14. The row hides on unrelated pages and returns to the same viewport-top position in Editor.
15. Document, Shape, Edit, Object and View remain visible as one compact fixed category row.
16. Each category opens its existing real menu temporarily and the dropdown closes after an action is selected.
17. The original in-page category buttons are hidden so only the current-document selector remains in that scrolling row.
18. The fixed row is no more than 48 pixels high and fits the supported 760-pixel minimum window width without clipping the wheel selector.
19. Project files, geometry and object-scene schema are unchanged.

Deterministic verification uses real `QWheelEvent` delivery, geometric viewport assertions and a real `QTest.mouseClick` on the temporary 3D View menu action. PR #67 branch checks pass; final manual T1700 acceptance remains required.

## 9. Recoverable Project Trash authority

`Delete Project…` is a recoverable removal workflow, not permanent erasure.

Required rules:

1. Start Here and Editor expose deletion beside project switching.
2. The selected path must be one real, non-symlink, non-hidden direct child of the canonical projects root.
3. User-facing deletion requires typing the exact selected directory name.
4. Active local-AI or source-intake work blocks deletion.
5. A project held by another writer lock cannot be moved.
6. A non-active selected project may be moved without changing current project authority.
7. Moving the active project closes its writer lease and leaves Forge detached.
8. The project moves atomically into hidden `.project-trash`, so canonical project discovery excludes it.
9. A durable receipt records original path, trash path, time and whether the project was active.
10. Receipt failure attempts automatic rollback; failed moves restore the active project where possible.
11. The interface exposes no permanent-delete command.

## 10. Brought-forward Construct authority

The active architecture defines future stable records for:

```text
source asset
→ editable shape
→ component
→ module
→ area or surface subset
→ anchor or socket
→ object group
→ assembly
→ effect stack
→ connection or stitch record
```

### Focus and perspective

Planned context-command families include:

- focus construct origin;
- frame entire construct;
- set primary focus object;
- set primary focus surface;
- view along surface normal;
- perspective, orthographic front/right/top and isometric views;
- saved named views.

No context-menu item may appear before its complete command, persistence, Undo/Redo, error and verifier path exists.

### Initial effect families

Planned reversible effect families are:

- Greebling;
- Roughness;
- Distortion;
- Bend with bounded intensity;
- Logic wiring with Randomized, Symbiotic, Aligned, Radial and Parallel routing;
- metallic visual profiles: Brushed Titanium, Polished Chrome, Anodized Aluminium, Oxidized Copper and Iridescent Nickel.

These are visual-design systems, not engineering material or electronics claims.

## 11. Group, assembly and connection boundary

Forge must distinguish:

1. placement only;
2. snap or align;
3. object group;
4. recoverable assembly connection;
5. visual seam;
6. mesh stitch or weld;
7. join mesh;
8. boolean union, difference or intersection;
9. separate;
10. bake.

Merely placing objects together around the central construct point creates none of operations 3–10 automatically.

Each consequential operation requires named inputs, preview, persistence, Undo/Redo or declared derivative behaviour, validation, failure handling, parent mapping and recovery.

## 12. Immediate engineering order

PR #67 manual live acceptance remains the gate before new asset-generation runtime work.

The active order is:

1. freeform editable paths, nodes, handles and segments;
2. source-region selection and manual tracing;
3. deterministic contour, threshold, edge, mask and silhouette candidates;
4. starter source-asset pack and copy-into-project command;
5. optional AI assessment or proposals through editable candidate authority;
6. review, approval and real Shape Library insertion;
7. shape-to-component recipe registry;
8. area, surface, pivot, anchor, focus and named-view authority;
9. modular placement around the central construct point;
10. object groups and recoverable assemblies;
11. effect-stack core;
12. initial surface effects and metallic profiles;
13. visual seams and separately verified stitch/weld/join/boolean/separate/bake operations;
14. verified 2D and 3D output profiles;
15. release asset-pack installation, update, migration, backup, licence and recovery gates.

Every item remains subject to focused PR scope, deterministic verification, T1700 evidence and truthful documentation updates.

## 13. Current non-claims

Forge does not currently claim:

- permanent project erasure from the interface;
- freeform paths or tracing;
- automatic editable extraction;
- a shipped starter source-asset pack;
- approved Shape Library insertion;
- a general shape-to-component recipe registry;
- persistent area or surface subsets;
- primary focus surfaces;
- anchors, sockets, groups or recoverable assemblies;
- surface-effect stacks;
- greebling, roughness, distortion, bend, logic wiring or metallic profiles;
- visual seams;
- stitch, weld, join mesh, booleans, separate or bake;
- engineering material properties;
- manufacturing-safe geometry;
- verified SVG, PNG, GLB/glTF or OBJ continuation.
