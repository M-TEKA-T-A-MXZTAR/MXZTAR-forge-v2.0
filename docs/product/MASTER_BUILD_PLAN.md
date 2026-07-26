# MXZTAR Forge v2.0 — Master Build Plan

## 1. Authority and purpose

This document is the active product, architecture, acceptance, and engineering-sequence authority for MXZTAR Forge v2.0.

It defines:

- the finished Stage One–Two product boundary;
- the current verified runtime foundation;
- the 18 first-class workflow families;
- durable project and artifact authority;
- Editor and Construct responsibilities;
- acceptance criteria;
- the immediate permitted engineering sequence.

The dated implementation state is recorded in `docs/PROGRESS_LEDGER.md`. The concise present-tense audit is recorded in `docs/product/CURRENT_CAPABILITY_BOUNDARY.md`.

Older documents may use **Level One** and **Level Two** for the same active product capabilities. This document standardises the active language as:

- **Stage One — Forge Editor and portable 2D assets**;
- **Stage Two — Construct and portable 3D blockouts**.

**Stage One and Stage Two together define the planned finished MXZTAR Forge v2.0 product.**

Future Product Levels Three and Four remain deferred vision. They require a separate founder decision and source-of-truth revision before runtime work is permitted.

---

## 2. Product definition

MXZTAR Forge v2.0 is a local-first, human-governed creative construction workbench.

It helps creators move from visually useful but structurally flat source material—or from a blank document—to editable, reusable, recoverable, and portable creative assets.

The product value path is:

```text
project purpose
→ source image or blank document
→ trace, extract, or draw editable geometry
→ correct paths, nodes, transforms, and relationships
→ approve a reusable Shape Library asset
→ combine shapes into new 2D designs
→ generate reversible 3D components
→ assemble components into recoverable structures
→ export through a verified downstream profile
```

The Editor is the product centre. Source intake, Shape Library, Review, Jobs, optional local AI, Construct, validation, and export exist to support creator-led editing rather than replace it.

Forge is not merely:

- an image description tool;
- a prompt generator;
- a black-box automatic vectoriser;
- a one-click production-ready 3D converter;
- a replacement for Krita, Inkscape, Blender, CAD systems, game engines, or slicers.

Forge provides governed creative-production structure between those specialist tools.

---

## 3. Users and durable value

### Primary users

1. concept and visual-development artists;
2. vector, graphic, pattern, and shape-system creators;
3. indie game, environment, prop, and world-building artists;
4. Blender generalists and 3D blockout artists;
5. makers and 3D-print designers at concept and blockout stage;
6. small film, animation, fabrication, and design teams without a dedicated technical-art pipeline;
7. creators who need reusable assets without making cloud services or expensive hardware the authority over their work.

### Primary asset

A durable Forge project containing, as implemented over time:

- project identity and exact Purpose;
- authoritative source references and unchanged project-owned source copies;
- editable shape documents;
- extraction candidates;
- reviewed Shape Library assets;
- command and correction history;
- project-owned 3D object scenes;
- construction recipes;
- components and assemblies;
- job and diagnostic evidence;
- approvals and supersession records;
- validated exports.

### Portable asset

A deterministic Forge Pack assembled from approved project records. A Forge Pack is an export view and continuation package, not a second project authority.

---

## 4. Product principles

1. **Editor first.** Forge is a creator tool, not a read-only display of AI output.
2. **Local first.** Source art and project truth remain local unless the user explicitly chooses otherwise.
3. **Human governed.** Extraction, approval, replacement, joining, boolean operations, baking, deletion, and export remain visible decisions.
4. **AI optional.** Manual creation, editing, saving, reopening, approval, and export cannot depend on a model or network.
5. **Observed is not inferred.** Source evidence, calculation, model inference, user intent, user-created geometry, and approved truth remain distinct.
6. **Non-destructive by default.** Originals and approved prior versions remain unchanged; edits create replayable or versioned derivatives.
7. **No dead or frozen UI.** Heavy work stays outside the Qt main thread with progress, heartbeat, elapsed time, cancellation boundaries, and truthful terminal state.
8. **Modest hardware remains valid.** One heavy job at a time by default, bounded previews, conservative threads, no silent downloads, and no hidden escalation.
9. **Interoperability is verified, not advertised.** A format or target program is exposed only after an import, round-trip, or continuation fixture proves the adapter.
10. **Readable durable output.** JSON, Markdown, SVG, PNG, and documented interchange files remain inspectable outside Forge where practical.
11. **Every name is a promise.** No button, status, format, AI claim, or workflow name exists without a handler, persistence rule, error path, and verifier.
12. **Corrections compound value.** User edits become durable project knowledge rather than hidden memory.
13. **Specialist tools are partners.** Forge prepares useful handoffs rather than pretending to replace every downstream tool.
14. **Free access is not reduced functionality.** Voluntary support cannot gate core editing or local file access.
15. **Finite scope protects quality.** Stage One and Stage Two must be completed before future-world features are activated.

---

## 5. Current verified runtime baseline — 26 July 2026

The merged runtime foundation includes:

- Purpose-driven Project Birth;
- safe create, open, close, reopen, and read-only recovery authority;
- fresh project and document creation from Editor;
- project switching from Start Here and Editor;
- restoration of prior project authority after failed switch or fresh-project creation;
- project-contained source intake and bounded previews;
- optional local-agent evidence and seven prompt contracts;
- native versioned shape documents;
- Rectangle, Square, Circle, Ellipse, and Star commands;
- command replay, Undo, Redo, autosave, canonical save, rollback, and reopen;
- project-owned `mxztar_forge_object_scene` state;
- real extruded 3D objects linked to native shapes;
- XYZ position, width, height, depth, three-axis rotation, colour, and opacity;
- CPU-rendered 3D viewport;
- click selection, drag movement, resize, empty-space orbit, and zoom;
- numeric Object Inspector;
- persistent camera, perspective, grid, line, and zoom state;
- paired 2D/3D membership during Undo, Redo, and direct deletion;
- explicit-selection deletion;
- guarded active-work authority;
- CodeQL Advanced analysis for GitHub Actions and Python;
- complete deterministic Source Truth verification on the T1700.

This baseline is a real integrated shape/object CAD foundation. It is not a complete Stage One or Stage Two release.

---

## 6. Current non-implemented boundaries

Forge does not currently implement:

- manual tracing into editable paths;
- deterministic contour, threshold, mask, or silhouette candidates;
- Ollama-generated authoritative geometry;
- pen, Bezier, freehand, node, or handle editing;
- full layers, groups, mirrors, arrays, snapping, alignment, or 2D booleans;
- transient smart guides, distance labels, equal-gap guidance, or snap tolerance;
- reviewed and approved Shape Library assets;
- insertion of reusable library assets into the current document;
- hierarchy, anchors, connectors, or recoverable assemblies;
- stitch, weld, join mesh, 3D boolean, separate, or bake operations;
- revolve, sweep, loft, shell, relief, bevel, vertex/face editing, or sculpting;
- verified SVG, PNG, GLB/glTF, or OBJ continuation profiles;
- engineering-grade or manufacturing-safe geometry claims.

Planned capability must not appear in the interface as if it were implemented.

---

## 7. Workflow, operation, and job

Forge must not call every button a workflow.

### Workflow

A user journey that creates a durable state change, reusable asset, validated handoff, or recoverable project result.

Examples: create a project, trace a shape, approve a library asset, build an assembly, export a GLB.

### Operation

A reversible or explicitly derived command inside a workflow.

Examples: move, rotate, add node, mirror, union, extrude, stitch.

### Job

Bounded work that may take time and must expose:

- declared inputs;
- current stage;
- progress or heartbeat;
- elapsed time;
- cancellation boundary;
- saved evidence;
- truthful success, failure, cancellation, or timeout state.

Examples: generate a preview, calculate contours, request an AI proposal, validate a mesh, package an export.

---

## 8. Product workflow architecture

The finished Stage One–Two product contains **18 first-class workflow families**.

### 8.1 Shared platform workflows

#### P1. Project lifecycle

```text
Purpose → Create → Open → Work → Close → Reopen → Recover
```

#### P2. Source lifecycle

```text
External source
→ import unchanged project-owned copy
→ hash and identify
→ generate bounded preview
→ use in Editor
→ explicitly process only the project-owned copy
```

#### P3. Job lifecycle

```text
Queued
→ Running
→ Succeeded / Failed / Cancelled / Timed out
→ Evidence saved
→ User-visible result and next action
```

#### P4. Recovery, migration, and integrity

```text
Validate project
→ detect stale, incompatible, or interrupted state
→ preserve last canonical truth
→ recover or attach read-only
→ rebuild indexes
→ migrate only through explicit schema rules
```

### 8.2 Stage One workflows

#### S1. Blank Shape Creation

```text
Open writable project
→ New blank document
→ select canvas and units
→ begin manual shape creation
```

#### S2. Source Region and Manual Trace

```text
Open source
→ select exact region
→ trace line, path, silhouette, or mask
→ correct nodes
→ save candidate
```

#### S3. Algorithmic Shape Extraction

```text
Select source region
→ configure bounded edge or threshold settings
→ generate candidates
→ compare
→ choose one for editing
```

#### S4. Optional AI Shape Proposal

```text
Select source region
→ request local model assessment or proposal
→ record model, assumptions, and confidence
→ display evidence or candidate
→ edit, reject, or retain as raw evidence
```

Ollama assessment alone is not extraction. Editable coordinates and user correction are required before geometry becomes project truth.

#### S5. Shape Editing

```text
Select shape
→ edit paths, nodes, handles, and properties
→ transform
→ Undo/Redo
→ autosave
→ save version
```

#### S6. 2D Composition

```text
Select multiple shapes
→ align, mirror, array, group, or connect
→ apply explicit path or boolean operation
→ produce a derived editable shape
```

#### S7. Review and Shape Library

```text
Candidate
→ Review
→ Correct
→ Approve / Reject
→ Version / Supersede
→ Save reusable Shape Library asset
→ Insert through a reversible document command
```

#### S8. 2D Export and Forge Pack

```text
Approved shape or composition
→ choose validated output profile
→ validate
→ export SVG and/or PNG
→ record provenance and limitations
→ build deterministic Forge Pack
```

### 8.3 Stage Two workflows

#### T1. Declared 3D Primitive Creation

```text
Open Construct
→ choose primitive
→ set units and parameters
→ create editable component
```

#### T2. Shape-to-Component Generation

```text
Approved 2D shape
→ choose declared construction recipe
→ set parameters
→ generate reversible component
→ retain parent relationship
```

Declared recipes may include extrude, revolve, sweep, loft, relief, shell, and bevel.

#### T3. Component Editing

```text
Select component
→ edit recipe parameters
→ edit transforms, origin, and pivot
→ regenerate
→ preserve parent shape and history
```

#### T4. Assembly and Constraint

```text
Place components
→ position, rotate, and scale
→ add anchors or connectors
→ define hierarchy or contact
→ save recoverable assembly
```

#### T5. Geometry Relationship and Merge

```text
Select components
→ choose explicit relationship or geometry operation
→ preview result
→ validate tolerance and limitations
→ apply reversible or explicitly baked result
```

The UI and artifact schemas must distinguish:

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

#### T6. 3D Validation, Export, and Continuation

```text
Component or assembly
→ validate units, axes, hierarchy, names, and geometry
→ choose GLB/glTF or OBJ profile
→ export
→ import into named downstream program
→ record continuation result
```

---

## 9. Project authority and durable artifacts

The project directory is a self-contained recovery boundary.

Durable project files are authoritative. SQLite may support search, sorting, recent-project state, queues, and rebuildable indexes, but it is never the sole authority for creative work.

Implemented or planned artifact classes include:

1. project manifest;
2. project history event;
3. source asset record;
4. source preview record;
5. native shape document;
6. project-owned object-scene document;
7. extraction candidate;
8. approved Shape Library asset;
9. approval or rejection record;
10. supersession or version record;
11. job or evidence record;
12. construction recipe;
13. editable 3D component;
14. assembly document;
15. export and Forge Pack record.

A proposed directory or artifact does not become runtime authority merely because it appears in documentation. Runtime code creates it only after schema, transaction, migration, recovery, and verification rules exist.

---

## 10. Unified shape and object lifecycle

```text
blank document or source region
→ candidate shape
→ editable shape document
→ reviewed
  ├→ approved Shape Library asset
  ├→ correction requested → revised version → reviewed
  └→ rejected

approved shape or declared primitive
→ construction recipe or primitive extrusion
→ editable 3D component/object
→ positioned instance
→ group or assembly
→ explicit contact / stitch / join / boolean / bake result
→ verified export
```

No raw model record is presented as an approved Shape Library asset.

---

## 11. Forge Editor contract

The Editor is a real canvas and document model, not a collection of single-purpose buttons.

Completed foundation:

- project and document choosers;
- five native primitives;
- durable shape commands;
- 2D and 3D synchronized membership;
- object selection and direct manipulation;
- numeric object properties;
- empty-space orbit and zoom;
- save, autosave, rollback, reopen, and recovery;
- explicit delete;
- active-work authority guards.

Required tool families still include:

- select and box-select;
- line, polyline, pen/Bezier, freehand, and trace tools;
- node and handle editing;
- path repair and simplification;
- fill and stroke properties;
- transform gizmos and numeric transforms;
- smart guides, alignment, distribution, snapping, and equal-gap assistance;
- duplicate, mirror, radial/linear array, group, ungroup, layer, lock, and visibility;
- union, difference, intersection, exclusion, divide, and combine as explicit 2D operations;
- anchors, connection points, symmetry axes, and guides;
- compare, review, approve, version, and export.

The Editor must distinguish source pixels, extraction candidates, user-created geometry, temporary selections and guides, approved project truth, and exported derivatives.

---

## 12. Smart positioning guides contract

The next direct-manipulation gate adds transient visual guidance while moving one selected object.

Guide candidates include:

- scene centre;
- nearest object centre;
- nearest object edges;
- matching X, Y, and Z positions;
- equal gaps between neighbours.

Small live values may include:

```text
Centre X: +24
Nearest object: 86
Left gap: 42
Z difference: 15
```

Required rules:

1. Guides appear only while movement is active.
2. Values update continuously.
3. Guides disappear immediately when movement ends.
4. Visual guides and snapping are separate controls.
5. `Guides`, `Snap to guides`, and bounded tolerance are explicit.
6. Nonselected objects remain unchanged.
7. Empty-space drag continues to orbit the view.
8. Calculations remain bounded and CPU-safe for the T1700.

---

## 13. Shape extraction contract

Extraction is one way to begin editing, not the final product.

The required first extraction system provides:

- exact source-region selection;
- manual trace baseline;
- line, contour, region, mask, and silhouette candidates;
- open/closed contours, holes, intersections, endpoints, symmetry, and nesting;
- threshold and edge settings for deterministic extraction;
- visible confidence and limitations for AI assessment;
- editable candidate paths on the same canvas used for scratch-built shapes;
- exact source coordinates and source hash;
- no automatic approval.

Manual tracing and correction remain available when no extraction engine or model is installed.

---

## 14. Shape Library contract

A real reusable library requires:

- editable approved-shape schema;
- provenance and integrity validation;
- approval, rejection, correction, version, and supersession records;
- bounded discovery;
- document compatibility checks;
- reversible `Insert into Current Document` command;
- duplicate-instance and source-identity rules;
- restart and copied-project recovery tests.

The current evidence browser does not satisfy this contract.

---

## 15. Construct and merge contract

The current object-scene foundation provides primitive extrusion, direct manipulation, camera state, reversible edits, and persistence.

The complete Stage Two Construct workflow still requires:

- construction-recipe schema;
- advanced recipes including revolve, sweep, loft, shell, relief, and bevel;
- origins, pivots, transform gizmos, units, and axes;
- anchors, connectors, hierarchy, instances, arrays, and assemblies;
- distinct group, contact, stitch/weld, join mesh, boolean, separate, and bake operations;
- geometry validation and named export profiles.

“One-click Make 3D” means “create a reversible preview using a declared method.” It does not mean “produce a finished object.”

---

## 16. Interoperability and output profiles

No single industry file is universal. Forge uses named output profiles with declared:

- units and scale;
- coordinate system and up-axis;
- origin and pivots;
- hierarchy and names;
- material or texture assumptions where applicable;
- known limitations;
- validation evidence.

Core planned Stage One outputs:

- native versioned Forge shape document;
- Forge Pack JSON and Markdown;
- validated SVG;
- validated PNG.

Core planned Stage Two outputs:

- GLB/glTF;
- OBJ fallback with explicit limitations.

Every profile requires a fresh named downstream import or continuation test.

---

## 17. Stage One acceptance boundary

Stage One is complete only when a new user can:

1. install and launch an official release;
2. create, open, switch, close, and safely recover a local project;
3. import a supported source image or create a blank shape document;
4. preserve source identity and unchanged external bytes;
5. create candidates manually, algorithmically, or through optional AI assistance;
6. create non-trivial shapes from scratch with primitives and path tools;
7. select, move, edit, add, and remove nodes and handles;
8. use transforms, smart guides, snapping, alignment, duplication, mirroring, arrays, grouping, layers, visibility, locking, Undo, and Redo;
9. perform explicit non-destructive 2D path and boolean operations;
10. compare source-derived candidates with source evidence and correct them;
11. rename, reject, approve, supersede, version, save, and reinsert Shape Library assets;
12. inspect jobs, diagnostics, model identity, elapsed time, and evidence;
13. export validated SVG, PNG, and Forge Pack derivatives;
14. restart Forge and recover editable state without terminal history;
15. continue work in a fresh named downstream session.

Stage One does not promise production-ready topology, engineering dimensions from an unscaled image, manufacturing safety, hidden-surface reconstruction, rigging, UVs, LODs, collision, final materials, or perfect extraction.

---

## 18. Stage Two acceptance boundary

Stage Two—and therefore the planned finished product—is complete only when a new user can:

1. open an approved Stage One shape or create a declared 3D primitive;
2. generate a reversible component using an explicit recipe;
3. inspect and edit operation parameters without destroying the source shape;
4. work in orthographic and perspective views with units, axes, origins, pivots, and transform gizmos;
5. position, rotate, scale, duplicate, mirror, array, hide, lock, and instance components;
6. create anchors, connectors, hierarchy, and assembly relationships;
7. distinguish group, assembly, contact, stitch/weld, join mesh, boolean, separate, and bake;
8. preview intersections, open boundaries, normals, and export limitations;
9. retain non-destructive construction history and parent provenance;
10. save, close, reopen, recover, and continue a 3D construction;
11. export through verified GLB/glTF and OBJ profiles;
12. import the result into Blender or another named supported tool and continue editing.

Stage Two does not claim engineering certification, manufacturing safety, automatic repair, finished topology, automatic rigging, or universal compatibility.

---

## 19. Delivery programme

### Milestone A — Local project and source foundation

Status: **VERIFIED foundation**.

Includes project manifest, locking, session authority, source intake, bounded previews, guarded workers, model evidence, launcher stability, and recovery contracts.

### Milestone B — Project Birth and project/document authority

Status: **VERIFIED / DETERMINISTICALLY VERIFIED**.

Includes Purpose-driven creation, blank document guidance, project and document switching, fresh Editor projects, failure restoration, and guarded mutations.

### Milestone C — Integrated primitive shape/object CAD foundation

Status: **DETERMINISTICALLY VERIFIED**.

Includes five native primitives, 2D/3D membership, project-owned object scenes, direct manipulation, Object Inspector, orbit, zoom, persistence, Undo/Redo, and direct deletion.

### Milestone D — Smart guides and manipulation clarity

Status: **NEXT PLANNED GATE**.

Includes transient alignment guides, measurements, optional snapping, bounded tolerance, equal-gap guidance, and orbit regressions.

### Milestone E — Freeform paths and manual tracing

Status: **PLANNED**.

Includes path, pen, node, handle, source-region, and trace tools.

### Milestone F — Deterministic and optional AI-assisted extraction

Status: **PLANNED**.

Includes contour, threshold, mask, silhouette, candidate comparison, source provenance, and Ollama-assisted assessment through editable candidate authority.

### Milestone G — Review and reusable Shape Library

Status: **PLANNED**.

Includes review, correction, approval, rejection, versioning, supersession, bounded library discovery, and reversible insertion.

### Milestone H — 2D composition and Stage One interoperability

Status: **PLANNED**.

Includes layers, groups, arrays, mirrors, alignment, 2D booleans, SVG, PNG, Forge Pack, and named downstream continuation.

### Milestone I — Advanced reversible 3D construction

Status: **PLANNED**.

Includes construction recipes, advanced generation methods, pivots, origins, and component validation.

### Milestone J — Assembly and explicit merge operations

Status: **PLANNED**.

Includes hierarchy, anchors, connectors, instances, recoverable assemblies, stitch/weld, join mesh, booleans, separate, and bake.

### Milestone K — Stage Two interoperability

Status: **PLANNED**.

Includes GLB/glTF, OBJ, Blender continuation, geometry reports, and named profile validation.

### Milestone L — Release engineering

Status: **PLANNED**.

Includes installation, update, rollback, migration, backup, recovery, checksums, licence, contributor policy, release notes, and official downloads.

---

## 20. Immediate permitted engineering sequence

The next engineering order is:

1. merge this documentation reconciliation after review and Source Truth checks;
2. implement smart guides, live measurements, optional snapping, and empty-space orbit regressions;
3. implement freeform editable paths, nodes, and handles;
4. implement source-region selection and manual tracing;
5. add bounded deterministic contour and mask candidates;
6. add Ollama-assisted candidate assessment only through the editable candidate path;
7. implement review, approval, versioning, and real Shape Library insertion;
8. implement 2D composition, alignment, groups, arrays, and explicit booleans;
9. implement and verify SVG, PNG, and Forge Pack profiles;
10. implement advanced reversible 3D construction recipes;
11. implement assemblies, anchors, connectors, hierarchy, and distinct merge operations;
12. implement and verify GLB/glTF and OBJ profiles;
13. complete Stage One and Stage Two release acceptance.

Every PR advances one coherent gate, preserves verified behaviour, updates the Progress Ledger and Current Capability Boundary, and avoids unrelated UI promises.

---

## 21. Verification system

Every milestone requires proportionate evidence:

1. Markdown and documentation-drift checks;
2. Python compile and fresh-process import checks;
3. pure-logic contracts;
4. fixture-based integration contracts;
5. thread and cancellation lifecycle contracts;
6. schema and migration validation;
7. filesystem interruption and recovery tests;
8. editor command, Undo/Redo, and autosave recovery tests;
9. benchmark-source and scratch-built asset comparisons;
10. manual Qt smoke checks on the T1700;
11. downstream import, round-trip, or continuation checks for every output profile.

No milestone becomes `VERIFIED` solely because code was committed or merged.

---

## 22. PR implementation contract

Every implementation PR identifies:

- product stage;
- workflow family;
- operation or job introduced;
- authoritative artifact affected;
- reversible and irreversible boundaries;
- UI exposure;
- failure and recovery behaviour;
- deterministic verifier;
- live acceptance requirement;
- documentation and ledger update.

No control appears until its complete handler, persistence, error path, and verifier exist.

---

## 23. Explicit exclusions

Stage One and Stage Two do not quietly expand into:

- automatic production-ready 3D reconstruction;
- engineering certification;
- finite-element, fluid, or structural simulation;
- electronics or PCB design;
- wiring-harness design;
- sensor or actuator control;
- robotics runtime control;
- CAM toolpaths;
- automatic manufacturing or print safety;
- finished retopology, rigging, or animation;
- universal format compatibility;
- multi-user collaboration economy;
- persistent worlds;
- distributed operator infrastructure.

These may exist in wider MXZTAR or ZCVIOS vision, but they are not required to complete MXZTAR Forge v2.0.

---

## 24. Distribution, access, and support

Official MXZTAR Forge use is intended to be free of charge. There is no confirmed timed trial, subscription, or core-feature paywall. Voluntary support may be offered through `https://buymeacoffee.com/mxztar`, but it cannot gate core editing or local file access.

Before the first public release, the repository must contain a recognised `LICENSE` selected by the founder and consistent contributor terms. Public source visibility and free-of-charge access do not themselves define modification or redistribution permission.

---

## 25. Future horizon authority

The separately governed future documents preserve long-term ideas without changing the active build:

- `FUTURE_CONSTRUCT_AND_WORLD_VISION.md`;
- `LEVEL_FOUR_PLATFORM_PRIORITIES.md`.

The active maturity horizon is:

- Stage One: editor-first reusable 2D shape creation and portable assets;
- Stage Two: reversible 3D component construction, assembly, and portable blockouts;
- Product Level Three: **DEFERRED**;
- Product Level Four: **DEFERRED**.

No date is assigned to Product Level Three or Four by this plan.
