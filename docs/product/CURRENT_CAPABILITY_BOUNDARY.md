# MXZTAR Forge v2.0 — Current Capability Boundary

**Snapshot date:** 26 July 2026  
**Runtime baseline:** merged `main` through PR #58  
**Evidence baseline:** T1700 focused Project Birth verification and complete Source Truth verification, exit code `0`

## 1. Purpose

This document is the concise current-state companion to the Master Build Plan.

It answers three separate questions without mixing them:

1. What Forge can do now.
2. What foundation exists but remains incomplete.
3. What is planned but not implemented.

The Master Build Plan remains the finished-product and engineering-sequence authority. The Progress Ledger records dated delivery history. This document prevents planned capability from being mistaken for current runtime capability.

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
| Native editable shape document | VERIFIED foundation | Versioned project-owned shape document, command replay, autosave, canonical save, rollback and reopen are implemented |
| Build 2D shapes from scratch | PARTIAL | Rectangle, Square, Circle, Ellipse and Star are implemented; freeform path, pen, node and handle tools are not |
| Undo and redo | DETERMINISTICALLY VERIFIED | Shape creation and 3D object edits use durable reversible command state within the implemented command families |
| Direct delete | DETERMINISTICALLY VERIFIED | Explicit selection is required; paired 2D shape and 3D object deletion persists without misusing Undo |
| Turn native shapes into 3D objects | DETERMINISTICALLY VERIFIED foundation | The five implemented primitives become real extruded project-owned 3D objects |
| Edit one 3D object | DETERMINISTICALLY VERIFIED | Position, width, height, depth, three-axis rotation, colour and opacity are persisted; nonselected objects remain unchanged |
| 3D viewport navigation | DETERMINISTICALLY VERIFIED | Empty-space drag orbits the view, wheel input zooms, perspective/grid/line state persists |
| Smart positioning guides | PLANNED | No transient alignment lines, distance labels, centre measurements or optional snapping contract exists yet |
| Extract shapes from a 2D image by tracing | PLANNED | Source intake and previews exist, but no manual tracing path creates editable geometry |
| Extract shapes algorithmically | PLANNED | No contour, threshold, edge, mask or silhouette engine currently creates editable candidates |
| Extract shapes through Ollama | PARTIAL evidence only | Ollama may assess source art and describe likely shapes or extraction zones; it does not currently create authoritative editable geometry |
| Approve a reusable Shape Library asset | PLANNED | Shape Library is an evidence browser; approval, rejection, versioning and supersession authority are absent |
| Insert Shape Library assets into a document | PLANNED | No approved reusable asset schema and no Insert into Current Document operation are exposed |
| Group or assemble 3D objects | PLANNED | Scene membership exists, but hierarchy, anchors, connectors and recoverable assembly authority do not |
| Stitch, weld, join mesh or boolean merge | PLANNED | These operations are deliberately distinct and not implemented |
| Advanced 3D creation from scratch | PARTIAL | Primitive extrusion and numeric editing exist; revolve, sweep, loft, shell, relief, bevel, vertex/face editing and sculpting do not |
| SVG, PNG, GLB/glTF or OBJ export | PLANNED | No named validated downstream output profile is exposed |
| CodeQL Advanced security analysis | VERIFIED repository control | GitHub Actions and Python analyses run through the merged advanced workflow |

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
2D image
→ exact source region
→ manual trace or deterministic contour proposal
→ editable candidate geometry
→ user correction
→ review and approval
→ optional Shape Library reuse
```

Ollama may classify, name, rank or explain candidate geometry. It may not become the sole geometry authority. Coordinates, paths, user correction and explicit approval establish project truth.

## 5. Current 2D-to-3D authority

The implemented foundation converts each supported native shape into one extruded object linked by source shape ID.

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

This is a real 3D blockout foundation. It is not yet the complete Construct workflow or a production mesh modeller.

## 6. Smart-guide requirement

The next direct-manipulation milestone must add transient, CPU-safe positioning guidance.

While moving one selected object, Forge should compare it with:

- scene centre;
- nearest object centre;
- nearest object edges;
- matching X, Y and Z positions;
- equal gaps between neighbouring objects.

The viewport should display small live values such as:

```text
Centre X: +24
Nearest object: 86
Left gap: 42
Z difference: 15
```

Required interaction rules:

1. Guides appear only while moving an object.
2. Values update continuously during movement.
3. Guides disappear immediately when movement ends.
4. Visual guides and snapping remain separate controls.
5. `Guides: On/Off`, `Snap to guides: On/Off`, and a bounded snap tolerance are explicit.
6. Moving one object must not change any nonselected object.
7. Calculations remain bounded for the T1700 and do not require AI.

## 7. Viewport interaction contract

```text
Drag selected object     → move that object
Drag resize handle       → resize that object
Click empty viewport     → clear selection
Drag empty viewport      → orbit or reorient perspective
Mouse wheel              → zoom
```

Smart guides must extend this contract without making empty-space orbit ambiguous.

## 8. Shape Library completion boundary

A real reusable library requires more than reading Ollama reports.

Before `Insert into Current Document` may appear, Forge needs:

- an editable approved-shape schema;
- provenance and integrity validation;
- approval, rejection, correction, version and supersession records;
- bounded library discovery;
- compatibility checks for the current document coordinate and unit context;
- insertion as a reversible command;
- duplicate-instance and source-identity rules;
- restart and copied-project recovery tests.

Raw findings remain evidence and cannot be inserted as approved geometry.

## 9. Merge and assembly completion boundary

The UI must not use one vague `Merge` command for different meanings.

Forge must distinguish:

- group;
- assembly;
- contact or mate;
- stitch or weld;
- join mesh;
- boolean union;
- boolean difference;
- boolean intersection;
- separate;
- bake.

Each operation requires named inputs, preview, persistence, undo or declared derivative behaviour, validation, failure handling and parent mapping.

## 10. Immediate engineering order

1. smart guides, measurements, optional snapping and empty-space orbit regressions;
2. freeform editable paths, nodes and handles;
3. source-region selection and manual tracing;
4. deterministic contour and mask candidates;
5. Ollama-assisted candidate assessment through the same editable path;
6. review, approval and real Shape Library insertion;
7. 2D composition, alignment, grouping and explicit booleans;
8. advanced reversible 3D construction recipes;
9. assemblies, anchors, connectors and distinct merge operations;
10. verified 2D and 3D output profiles.

Every item remains subject to focused PR scope, deterministic verification, T1700 evidence and truthful documentation updates.
