# MXZTAR Forge v2.0 — Current Capability Boundary

**Snapshot date:** 27 July 2026  
**Merged runtime baseline:** `main` through PR #59 at `61ab6c4`  
**Active branch evidence:** PR #60 smart positioning guide contract passes Source Truth; merged-main T1700 acceptance remains pending

## 1. Purpose

This document is the concise present-tense companion to the Master Build Plan.

It distinguishes:

1. capability available on merged `main`;
2. capability implemented and deterministically verified on the active PR branch;
3. incomplete foundations;
4. planned capability.

The Master Build Plan remains the finished-product and sequence authority. The Progress Ledger records dated delivery history.

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
| Undo and redo | DETERMINISTICALLY VERIFIED | Shape creation and 3D object edits use durable reversible command state within implemented command families |
| Direct delete | DETERMINISTICALLY VERIFIED | Explicit selection is required; paired 2D shape and 3D object deletion persists without misusing Undo |
| Turn native shapes into 3D objects | DETERMINISTICALLY VERIFIED foundation | The five implemented primitives become real extruded project-owned 3D objects |
| Edit one 3D object | DETERMINISTICALLY VERIFIED | Position, width, height, depth, three-axis rotation, colour and opacity persist; nonselected objects remain unchanged |
| 3D viewport navigation | DETERMINISTICALLY VERIFIED | Empty-space drag orbits, wheel input zooms, and perspective/grid/line state persists |
| Smart positioning guides | DETERMINISTICALLY VERIFIED on PR #60 branch | Movement shows transient X/Y lines, X/Y/Z centre deltas and nearest-object measurements; merged-main T1700 acceptance remains pending |
| Optional snapping | DETERMINISTICALLY VERIFIED on PR #60 branch | Separate control, off by default, bounded 1–50 scene-unit tolerance, X/Y only; guides off also disables snapping |
| Extract shapes from a 2D image by tracing | PLANNED | Source intake and previews exist, but no manual tracing path creates editable geometry |
| Extract shapes algorithmically | PLANNED | No contour, threshold, edge, mask or silhouette engine creates editable candidates |
| Extract shapes through Ollama | PARTIAL evidence only | Ollama may assess source art and describe likely shapes or extraction zones; it does not create authoritative editable geometry |
| Approve a reusable Shape Library asset | PLANNED | Shape Library is an evidence browser; approval, rejection, versioning and supersession authority are absent |
| Insert Shape Library assets into a document | PLANNED | No approved reusable asset schema and no `Insert into Current Document` operation are exposed |
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

Ollama may classify, name, rank or explain candidate geometry. It may not become the sole geometry authority. Coordinates, editable paths, user correction and explicit approval establish project truth.

## 5. Current 2D-to-3D authority

Each supported native shape becomes one extruded object linked by source shape ID.

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

## 6. PR #60 smart-guide authority

PR #60 adds transient, CPU-safe positioning guidance to the official authoring Editor.

While moving one selected object, Forge calculates:

- difference from the stable scene centre on X, Y and Z;
- nearest neighbouring object by centre distance;
- nearest-object surface distance using axis-aligned bounds;
- nearest-object Z difference;
- centre and min/max edge alignments against scene centre and neighbouring objects;
- X/Y snapping candidates within a bounded tolerance.

The viewport displays:

- dashed X/Y guide lines for applicable alignments;
- a compact live measurement block;
- explicit snapped-state wording where snapping applies.

Interaction rules:

1. Guides appear only while moving one selected object.
2. Measurements update continuously during movement.
3. Guides disappear immediately on release.
4. `Position Guides` and `Snap to Guides` remain separate controls.
5. Snapping is off by default.
6. Turning guides off also disables snapping, preventing invisible forced movement.
7. Tolerance is explicitly bounded from 1 to 50 scene units.
8. Snapping changes only the selected object's X/Y position.
9. Nonselected objects remain unchanged.
10. Guide evidence is transient and is not persisted as project authority.
11. The final freely moved or explicitly snapped position is saved through the existing reversible object command.
12. Empty-space drag remains orbit and never displays object-movement guides.

Not included yet:

- equal-gap or distribution guides;
- persistent user guide objects;
- transform gizmos;
- anchor or connector snapping;
- dimensional engineering tolerance claims.

## 7. Viewport interaction contract

```text
Drag selected object     → move that object; show transient guidance
Drag resize handle       → resize that object; no movement guides
Click empty viewport     → clear selection
Drag empty viewport      → orbit or reorient perspective
Mouse wheel              → zoom
Guides off               → visual guidance off and snapping forced off
Snap off                 → measurements only; no forced position
Snap on                  → selected-object X/Y may snap inside bounded tolerance
```

## 8. Shape Library completion boundary

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

After PR #60 review, merge, synchronization and live acceptance:

1. freeform editable paths, nodes and handles;
2. source-region selection and manual tracing;
3. deterministic contour and mask candidates;
4. Ollama-assisted candidate assessment through the same editable path;
5. review, approval and real Shape Library insertion;
6. 2D composition, alignment, grouping and explicit booleans;
7. advanced reversible 3D construction recipes;
8. assemblies, anchors, connectors and distinct merge operations;
9. verified 2D and 3D output profiles.

Every item remains subject to focused PR scope, deterministic verification, T1700 evidence and truthful documentation updates.
