# MXZTAR Forge v2.0 — Current Capability Boundary

**Snapshot date:** 6 August 2026  
**Merged runtime baseline:** `main` through PR #81 at `e8659d5`  
**Current engineering gate:** R1 final-runtime mapping, followed by R2 acceptance harness correction before new broad feature work

## 1. Purpose

This document is the concise present-tense authority for what Forge can do now.

It does not define the finished product. See:

- `MASTER_BUILD_PLAN.md` for the Stage One–Two finished boundary;
- `RECOVERY_AND_COMPLETION_PLAN.md` for the active engineering order;
- `../architecture/FINAL_RUNTIME_AND_STATE_AUTHORITY_MAP.md` for the official composed runtime and state owners;
- `../PROGRESS_LEDGER.md` for chronology;
- `../REGRESSION_AND_DRIFT_REGISTER.md` for causal learning.

## 2. Status vocabulary

| Status | Meaning |
|---|---|
| VERIFIED | Applicable automated and recorded T1700 evidence exists |
| DETERMINISTICALLY VERIFIED | Automated contracts pass; additional live, downstream or release acceptance may remain |
| PARTIAL | Useful foundation exists, but the complete user workflow does not |
| PLANNED | Required by the active product plan but not implemented |
| DEFERRED | Outside the active Stage One–Two delivery sequence |

## 3. Current product truth

Forge currently provides a real local project, editable primitive and 2D/3D blockout foundation. It is not yet a complete reusable-asset or assembly product.

### Project and document foundation

| Capability | State | Current truth |
|---|---|---|
| Purpose-driven project creation | VERIFIED foundation | Start Here creates project authority and guides the user into an Editor document |
| Open, close, reopen and recovery | VERIFIED foundation | Project-owned files, writer authority, recovery classification and read-only recovery contracts exist |
| Fresh project and document creation from Editor | DETERMINISTICALLY VERIFIED | Unique writable project/document creation and authority restoration are implemented |
| Project switching | DETERMINISTICALLY VERIFIED | Start Here and Editor switching preserve project/document synchronization and restore prior authority after failed switching |
| Recoverable Project Trash | DETERMINISTICALLY VERIFIED | Selected direct-child projects move into hidden project trash with confirmation, lock checks, active-work blocking, receipt and rollback; no permanent-delete command exists |
| Save, autosave, rollback and reopen | VERIFIED foundation | Native document state is durable and replayable within implemented command families |

### Editor and direct interaction

| Capability | State | Current truth |
|---|---|---|
| Native editable shape document | VERIFIED foundation | Versioned project-owned shape document and command replay exist |
| Primitive creation | PARTIAL Stage One | Rectangle, Square, Circle, Ellipse and Star are implemented; freeform paths and node editing are not |
| Select and direct 2D movement | DETERMINISTICALLY VERIFIED through PR #78 | Implemented shapes can be selected and moved through durable command state |
| Direct 2D resize | DETERMINISTICALLY VERIFIED through PR #80 | All five primitives support direct durable resizing with minimum-geometry validation |
| Direct deletion | DETERMINISTICALLY VERIFIED | Explicit selection is required; paired 2D shape and 3D object membership persists correctly |
| Undo and redo | DETERMINISTICALLY VERIFIED | Implemented shape creation, movement, resize, deletion and object edits use reversible command state where defined |
| Safe Editor re-entry | DETERMINISTICALLY VERIFIED through PR #77 | Re-entry returns to Select rather than retaining a hazardous action mode |
| Compact command strip | DETERMINISTICALLY VERIFIED foundation | Document, Shape, Edit, Object and View remain available in a fixed compact row; historical always-open tree was rejected after live usability failure |
| Continuously visible interaction controls | DETERMINISTICALLY VERIFIED foundation | Sticky control bar, page scrolling, active-output reveal and explicit wheel-routing modes are implemented |

### 3D blockout foundation

| Capability | State | Current truth |
|---|---|---|
| Shape-to-object extrusion | DETERMINISTICALLY VERIFIED foundation | The five native primitives produce project-owned extruded 3D objects linked to source shape IDs |
| Object selection and direct movement | DETERMINISTICALLY VERIFIED through PR #78 | Selected objects move directly; nonselected objects remain unchanged under covered contracts |
| Object resize and numeric editing | DETERMINISTICALLY VERIFIED foundation | Position, width, height, depth, rotation, colour and opacity persist |
| Object versus camera interaction | DETERMINISTICALLY VERIFIED foundation | Object manipulation and empty-space camera navigation are separated |
| Stable Design View | DETERMINISTICALLY VERIFIED through PR #79 | Front orthographic view is the editing default; orbit and perspective are deliberate viewing controls |
| Pointer-following precision | DETERMINISTICALLY VERIFIED foundation | Screen/world transform correction reduces drag drift; a complete final-runtime camera-state event matrix remains part of R2 |
| Smart positioning guides | DETERMINISTICALLY VERIFIED | Transient X/Y guides, centre deltas, nearest-object measurements and bounded optional snapping exist |
| Camera, grid, line, perspective and zoom persistence | DETERMINISTICALLY VERIFIED foundation | View state persists through existing object-scene authority |

### Repository and safety controls

| Capability | State | Current truth |
|---|---|---|
| Optional local AI evidence | PARTIAL | Seven prompt contracts and agent workflows can produce evidence; AI does not create authoritative editable geometry |
| CPU-safe job policy | VERIFIED policy / PARTIAL runtime | One job at a time, asynchronous work and visible status are governing requirements; lifecycle regressions remain protected by targeted checks |
| Source Truth verification | DETERMINISTICALLY VERIFIED governance baseline through PR #81 | The hierarchy, capability baseline, causal register and semantic documentation checks pass; R1 adds the official composition target before R2 event-harness work |
| Final runtime and state-authority map | DETERMINISTICALLY VERIFIED R1 boundary | The shell launcher, six installer order, final window hierarchy, final Editor binding, major mutable-state owners and retirement status are recorded and checked without changing runtime behaviour |
| CodeQL Advanced | VERIFIED repository control | GitHub Actions and Python security analysis are configured |

## 4. Important limitations

Forge does not currently provide a complete path from source image to approved reusable editable asset.

Not implemented:

- manual tracing into editable paths;
- pen, Bezier, freehand, node or handle editing;
- deterministic contour, threshold, edge, mask or silhouette candidates;
- authoritative AI-generated geometry;
- full layers, groups, mirrors, arrays, alignment, snapping and 2D booleans;
- approval, rejection, supersession and reusable Shape Library authority;
- insertion of approved library assets into the current document;
- validated SVG or PNG continuation profiles;
- general shape-to-component recipe registry;
- persistent surfaces, areas, pivots, anchors or sockets;
- named groups and recoverable assemblies;
- reversible effect stacks;
- visual seams, stitch/weld, join mesh, 3D booleans, separate or bake;
- revolve, sweep, loft, shell, relief, bevel or mesh-level editing;
- validated GLB/glTF or OBJ continuation profiles;
- engineering-grade or manufacturing-safe geometry claims.

No absent capability may appear as a functioning control or public claim.

## 5. Runtime-composition limitation

The official launcher currently composes behaviour through multiple subclasses, panel replacements, signal rewiring, compatibility guards and startup installers.

The mapped final path is:

```text
run_mxztar_forge.sh
→ src/mxztar_forge.py
→ six startup installers
→ AuthoringEditorForgeWindow
→ DirectResizeProjectAwareEditorPanel
```

This means:

- isolated component tests may not represent the launched application;
- import and installer order can affect behaviour;
- another narrow patch can accidentally become a competing authority;
- deterministic verification must target the final composed runtime;
- compatibility layers must be retired incrementally only after equivalent final-runtime evidence exists.

The R1 map does not authorise a sweeping rewrite.

## 6. Present 2D-to-3D authority

The current durable path is:

```text
writable project
→ native primitive command
→ editable 2D shape state
→ linked extruded 3D object
→ select / move / resize / edit
→ save / close / reopen
```

This is a meaningful integrated blockout foundation. It is not yet the complete Stage One reusable-asset workflow or Stage Two recoverable-assembly workflow.

## 7. Current acceptance boundary

Automated evidence through PR #81 covers governance and substantial direct interaction and persistence behaviour, but deterministic success alone can miss live usability faults.

R1 records the official launcher, installer sequence, final class bindings and state owners. It does not prove every interaction through the final event path.

Before new broad feature work, R2 must:

1. convert PR #66–#80 lessons into official-launcher regression contracts;
2. deliver real mouse and wheel events through the final composition;
3. assert geometry, visibility and pointer/object lock;
4. confirm create, select, move, resize, delete, undo/redo, save, close and reopen stability;
5. protect interruption and rollback behaviour where applicable;
6. prevent silent verifier omission through discovery or a complete manifest;
7. complete applicable T1700 live-interaction acceptance.

## 8. Next recovery and product gates

The immediate recovery sequence is:

```text
R1 final-runtime mapping
→ R2 acceptance harness correction
→ R3 canonical interaction foundation
```

After that recovery gate closes, the next Stage One foundation is:

```text
freeform editable path
→ source-region selection
→ manual trace
→ node correction
→ review and approval
→ reusable Shape Library asset
→ reversible insertion
→ validated 2D export
```

This path has priority because it creates the first complete portable creator asset rather than adding another isolated control.

## 9. Public claim boundary

Forge may be described as:

- local-first;
- human-governed;
- designed for modest CPU-only hardware;
- capable of durable project creation and recovery;
- providing editable primitive-based 2D and 3D blockout foundations;
- under active development toward reusable 2D assets and reversible 3D assemblies.

Forge must not yet be described as:

- a complete image-to-vector system;
- a complete CAD or production mesh modeller;
- a production-ready 2D-to-3D converter;
- a complete Shape Library or assembly system;
- validated for manufacturing or engineering safety;
- open source until a recognised licence is selected.
