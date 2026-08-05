# MXZTAR Forge v2.0 — Current Capability Boundary

**Snapshot date:** 6 August 2026  
**Repository baseline assessed:** merged `main` through PR #80  
**Current programme:** governance recovery, final-runtime proof, then new geometry work

## 1. Purpose

This document records present-tense product truth.

It does not define the finished product, preserve detailed PR history, or issue the engineering queue.

Use:

- `MASTER_BUILD_PLAN.md` for the finished Stage One–Two boundary;
- `ACTIVE_ENGINEERING_PLAN.md` for the ordered current gate;
- `docs/PROGRESS_LEDGER.md` for dated evidence and causal lessons;
- `docs/architecture/FINAL_RUNTIME_COMPOSITION.md` for the application that actually runs.

## 2. Status vocabulary

| Status | Meaning |
|---|---|
| LIVE VERIFIED | Applicable automated evidence and recorded T1700 live acceptance exist for the stated boundary |
| DETERMINISTICALLY VERIFIED | Focused automated evidence exists; fresh live, downstream, or release proof may remain |
| MERGED FOUNDATION | Capability is on `main`, but this snapshot does not claim a complete fresh acceptance pass |
| PARTIAL | Useful implementation exists, but the complete user workflow does not |
| PLANNED | Required by the active product plan but not implemented |
| DEFERRED | Outside the active MXZTAR Forge v2.0 delivery sequence |

Merge status alone is not acceptance evidence.

## 3. Current capability matrix

### Project and application authority

| Capability | Status | Current truth |
|---|---|---|
| Purpose-driven project creation | MERGED FOUNDATION | Stable project identity, safe directory creation, Purpose preservation, history, and writable authority exist |
| Project open, close, switch, rename, and recovery classification | MERGED FOUNDATION | One-writer authority, read-only recovery, selector synchronization, display-name rename, and rollback protections exist |
| Recoverable Project Trash | MERGED FOUNDATION | Selected canonical projects move into hidden recoverable trash; no permanent-delete command is exposed |
| Project and document lifecycle | MERGED FOUNDATION | Fresh project/document creation, close, deliberate reopen, deletion, and project-owned state are implemented |
| Save Project transaction | DETERMINISTICALLY VERIFIED | Combined shape/scene/project save, membership reconciliation, no-op handling, and rollback are implemented |
| Relocatable launcher and desktop entry support | MERGED FOUNDATION | Repository launcher follows its checkout; installation helpers exist |
| Final runtime composition | PARTIAL / DOCUMENTED | Official installer and shell composition is now documented; consolidation and one shared final-runtime verifier remain planned |

### Source, evidence, and optional local AI

| Capability | Status | Current truth |
|---|---|---|
| Project-owned source intake | MERGED FOUNDATION | External source bytes remain unchanged; validated project copies, hashes, previews, history, and rollback exist |
| Bounded source previews | MERGED FOUNDATION | Large originals use bounded derivatives; original paths remain authoritative for declared workflows |
| Source image compatibility | MERGED FOUNDATION | Accepted formats are discoverable and previewable within declared boundaries; model-ready formats remain narrower |
| My Library | MERGED FOUNDATION | Read-only visual source browser, exact handoff, background lifecycle, and clean shutdown contracts exist |
| Jobs | MERGED FOUNDATION | Read-only success, failure, and invalid evidence browser exists |
| Shape Library | PARTIAL | Raw shape-analysis evidence browser exists; approved reusable asset authority does not |
| Optional Ollama assessment | PARTIAL | Local model calls can save project evidence; they do not create authoritative editable geometry |
| Adaptive modest-hardware policy | MERGED FOUNDATION | Conservative CPU/GPU detection and one-heavy-job default exist; no silent parallel escalation is authorised |

### Native 2D editing

| Capability | Status | Current truth |
|---|---|---|
| Native shape-document authority | MERGED FOUNDATION | Versioned project-owned documents, command replay, autosave, canonical save, rollback, reopen, and recovery exist |
| Rectangle, Square, Circle, Ellipse, and Star | MERGED FOUNDATION | Five native primitives can be created and persisted |
| Direct 2D selection and movement | DETERMINISTICALLY VERIFIED through PR #78 | Shape body drag preserves click offset, writes one durable command, synchronizes paired 3D X/Y, and supports Undo/Redo |
| Direct 2D resize | DETERMINISTICALLY VERIFIED through PR #80 | One selection outline and bottom-right handle resize shapes; Square and Circle preserve equal sides; minimum size and paired 3D synchronization exist |
| Direct paired deletion | MERGED FOUNDATION | Explicit selection removes the linked 2D shape and 3D object through project authority |
| Freeform paths, nodes, and handles | PLANNED | No durable line/Bezier path editing authority exists yet |
| Source-region manual tracing | PLANNED | No exact source-region-to-editable-path workflow exists yet |
| Deterministic contour or mask candidates | PLANNED | No contour, threshold, edge, mask, line, or silhouette engine creates editable candidates |
| Layers, groups, arrays, mirrors, and 2D booleans | PLANNED | The complete composition workflow is not implemented |
| Approved Shape Library insertion | PLANNED | No approval/version/supersession lifecycle or reversible insertion command exists |
| Verified SVG/PNG continuation | PLANNED | No named downstream profile is exposed |

### 3D object and interaction foundation

| Capability | Status | Current truth |
|---|---|---|
| Project-owned 3D object scene | MERGED FOUNDATION | Five native shapes become linked extruded objects with persistent scene authority |
| Object position, size, depth, rotation, colour, and opacity | MERGED FOUNDATION | Numeric project-owned properties and inspector controls exist |
| Direct 3D movement | DETERMINISTICALLY VERIFIED through PR #78 | Selected-object drag maps pointer movement to the fixed-Z XY plane while preserving camera state and nonselected objects |
| Direct 3D resize | DETERMINISTICALLY VERIFIED | Select-mode resize handle and advanced Resize mode coexist within implemented bounds |
| Explicit Select, Move, Rotate, Resize, and Orbit modes | DETERMINISTICALLY VERIFIED | Object transforms and camera orbit are separated; one command is committed per completed transform |
| Front orthographic 3D Design View | DETERMINISTICALLY VERIFIED through PR #79 | 3D entry resets to a centred front orthographic design presentation; Perspective and Orbit remain deliberate controls |
| 3D re-entry interaction | DETERMINISTICALLY VERIFIED | Re-entry selects object-manipulation mode rather than leaving the first drag as camera orbit |
| Stable camera and world origin during object edits | DETERMINISTICALLY VERIFIED | Fixed landmarks and camera state remain unchanged while selected objects move |
| Positioning guides and measurements | DETERMINISTICALLY VERIFIED | Transient guides and measurements exist during movement |
| Optional snapping | DETERMINISTICALLY VERIFIED | Snapping is explicit and off by default; disabling guides disables invisible snapping |
| Mouse-wheel page scroll and 3D zoom modes | DETERMINISTICALLY VERIFIED | Scroll, direct 3D zoom, and Ctrl+wheel zoom routes are separated through real Qt event delivery |
| Compact fixed Editor command strip | MERGED FOUNDATION | Current command categories remain reachable above the scroll viewport through temporary dropdowns rather than the rejected permanent tree |
| General shape-to-component recipe registry | PLANNED | Current primitive extrusion is not yet a general reviewed recipe system |
| Persistent areas, surfaces, pivots, anchors, sockets, or focus targets | PLANNED | No durable subset or connection authority exists |
| Object groups and recoverable assemblies | PLANNED | Scene membership is not assembly hierarchy or contact authority |
| Effect stacks and visual effect families | PLANNED | No reversible targetable effect-stack core exists |
| Stitch/weld, join, boolean, separate, or bake | PLANNED | These remain distinct unimplemented operations |
| Revolve, sweep, loft, shell, relief, bevel, or mesh editing | PLANNED | Advanced creation is outside the current foundation |
| Verified GLB/glTF or OBJ continuation | PLANNED | No named downstream profile is exposed |

### Repository and verification controls

| Capability | Status | Current truth |
|---|---|---|
| Source Truth suite | MERGED FOUNDATION | Compile, documentation, Qt, project, object, movement, resize, guide, wheel, and prompt contracts are aggregated |
| CodeQL Advanced | MERGED FOUNDATION | GitHub Actions and Python analyses are configured |
| Final-runtime real-event verification | PARTIAL | Several focused verifiers use real Qt events and final classes; one shared official-runtime fixture remains the next governance/acceptance gate |
| Documentation freshness control | RECOVERING | The former verifier protected a PR #63-era snapshot; this governance pass replaces it with structural current-authority checks |
| T1700 consolidated acceptance through PR #80 | REQUIRED NEXT | Individual gates carry evidence, but one complete fresh interaction baseline remains the next pre-feature gate |

## 4. What the current 2D-to-3D path actually does

```text
native Rectangle / Square / Circle / Ellipse / Star
→ durable 2D shape command state
→ linked project-owned extruded 3D object
→ synchronized position and planar size
→ independent depth, rotation, colour, opacity, camera, and scene state
```

This is a real blockout foundation. It is not automatic production reconstruction, topology repair, manufacturing validation, or a complete Construct workflow.

## 5. Current AI boundary

```text
project-owned source
→ optional local-model assessment
→ raw project evidence or proposal
→ no authoritative editable geometry
```

Required future geometry authority is:

```text
exact source region
→ manual trace or deterministic candidate
→ editable coordinates and path identity
→ user correction
→ review and approval
```

A model may classify, explain, rank, or suggest. It does not silently become project truth.

## 6. Current non-claims

Forge does not currently claim:

- finished Stage One or Stage Two release readiness;
- approved reusable Shape Library assets;
- freeform path or source-tracing capability;
- automatic production-quality 2D-to-3D reconstruction;
- stable surface subsets, anchors, sockets, groups, or assemblies;
- reversible effect stacks;
- advanced mesh operations;
- engineering-grade, watertight, printable, or manufacturing-safe output;
- verified SVG, PNG, GLB/glTF, OBJ, CAD, game-engine, or slicer continuation;
- cloud collaboration, marketplace, immersive world, or Product Level Four capability.

## 7. Immediate acceptance boundary

Before new geometry capability begins, Gate G1 in `ACTIVE_ENGINEERING_PLAN.md` must prove the complete official runtime through:

- direct 2D movement and resize;
- paired 3D synchronization;
- Undo/Redo and persistence;
- front orthographic 3D entry and deliberate navigation modes;
- object movement and resize without camera drift;
- project/document controls, guides, wheel routing, save, reopen, and clean shutdown;
- T1700 live interaction.

This snapshot changes when present-tense capability or evidence changes—not merely because a planning idea is added.