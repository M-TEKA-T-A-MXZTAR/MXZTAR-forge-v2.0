# MXZTAR Forge v2.0 — Master Build Plan

## 1. Authority and purpose

This document is the active product, architecture, acceptance, and engineering-sequence authority for MXZTAR Forge v2.0.

It reconciles the strongest parts of the earlier editor-first plan with the finite Stage One–Two workflow architecture confirmed on 22 July 2026.

Older documents may use **Level One** and **Level Two** for the same current product capabilities. This document standardises the active language as:

- **Stage One — Forge Editor and portable 2D assets**;
- **Stage Two — Construct and portable 3D blockouts**.

Implementation milestones use letters so they cannot be confused with product stages.

**Stage One and Stage Two together define the finished MXZTAR Forge product.**

Future Product Levels Three and Four remain deferred vision. They require a separate founder decision and source-of-truth revision before any runtime work is permitted.

---

## 2. Product definition

MXZTAR Forge v2.0 is a local-first, human-governed creative construction workbench.

It helps creators move from visually useful but structurally flat source material to editable, reusable, recoverable, and portable creative assets.

The active value path is:

```text
project purpose
→ source image or blank canvas
→ trace, extract, or draw an editable shape
→ correct paths, nodes, layers, transforms, and relationships
→ approve a reusable Shape Library asset
→ combine shapes into new 2D designs
→ generate reversible 3D components
→ assemble components into recoverable structures
→ export through a verified downstream profile
```

The Forge Editor is the product centre. Source intake, Shape Library, Review, Jobs, optional local AI, Construct, validation, and export exist to support creator-led editing rather than replace it.

Forge is not merely:

- an image description tool;
- a prompt generator;
- a black-box automatic vectoriser;
- a one-click production-ready 3D converter;
- a replacement for every feature in Krita, Inkscape, Blender, CAD, game engines, or slicers.

Forge provides the governed creative-production structure between those specialist tools.

---

## 3. The workflow gaps Forge addresses

### 3.1 Source art is visually rich but structurally incomplete

Source images may contain valuable silhouettes, panels, motifs, paths, surfaces, repeated modules, and construction relationships. Downstream programs instead require editable paths, nodes, scale, hierarchy, units, geometry decisions, and disciplined formats.

### 3.2 Creators repeatedly rebuild the same missing structure

Useful material is often reconstructed across tracing software, painting tools, AI chats, Blender, CAD systems, engines, and folders. This creates duplicated effort, inconsistent versions, lost provenance, and filesystem archaeology.

### 3.3 AI output is commonly persuasive but not editable project truth

A model may produce useful observations or proposals, but prose, generated pixels, or inferred geometry are not the same as reviewed paths, reusable components, or approved assets.

### 3.4 “One-click 2D-to-3D” hides assumptions

Automatic-looking conversions may conceal scale, depth, axis, topology, parentage, and construction decisions. Forge instead records a declared reversible method and its parameters.

### 3.5 Small teams often lack a technical-art pipeline

Solo creators and small studios need continuity between idea, editable shape, component, assembly, and export without building a custom asset-management and provenance system first.

### 3.6 Cloud dependence can weaken ownership and resilience

Core manual creation, editing, saving, reopening, and export must remain useful without a network service or AI model. Source art and project truth remain locally accessible unless the user explicitly chooses an external operation.

---

## 4. Users and value

### Primary users

1. concept and visual-development artists;
2. vector, graphic, pattern, and shape-system creators;
3. indie game, environment, prop, and world-building artists;
4. Blender generalists and 3D blockout artists;
5. makers and 3D-print designers at concept and blockout stage;
6. small film, animation, fabrication, and design teams without a dedicated technical-art department;
7. creators who need reusable assets without making cloud services or expensive hardware the authority over their work.

### Primary asset

A durable Forge project containing:

- authoritative source references;
- editable shape documents;
- extraction candidates;
- reviewed Shape Library assets;
- command and correction history;
- construction recipes;
- components and assemblies;
- job and diagnostic evidence;
- approvals and supersession records;
- validated exports.

### Portable asset

A deterministic Forge Pack assembled from approved project records. A Forge Pack is an export view and continuation package, not a second project authority.

### Creator value

Forge provides one governed place to import, trace, extract, draw, edit, organise, combine, review, approve, construct, assemble, validate, and export reusable creative assets while preserving source identity and every material user decision.

---

## 5. Product principles

1. **Editor first.** The editor is a creator tool, not a read-only display of AI output.
2. **Local first.** Source art and project truth remain local unless the user explicitly chooses otherwise.
3. **Human governed.** Extraction, approval, replacement, joining, boolean operations, baking, deletion, and export remain visible decisions.
4. **AI optional.** Manual creation, editing, saving, reopening, approval, and export cannot depend on a model or network.
5. **Observed is not inferred.** Source evidence, calculation, model inference, user intent, user-created geometry, and approved truth remain distinct.
6. **Non-destructive by default.** Originals and approved prior versions remain unchanged; edits create replayable or versioned derivatives.
7. **No dead or frozen UI.** Heavy work stays outside the Qt main thread with progress, heartbeat, elapsed time, cancellation boundaries, and truthful final state.
8. **Modest hardware remains valid.** One heavy job at a time by default, bounded previews, conservative threads, no silent downloads, and no hidden escalation.
9. **Interoperability is verified, not advertised.** A format or target program is exposed only after an import, round-trip, or continuation fixture proves the adapter.
10. **Readable durable output.** JSON, Markdown, SVG, PNG, and documented interchange files remain inspectable outside Forge.
11. **Every name is a promise.** No button, format, status, AI claim, or workflow name exists without a handler, validation, persistence rule, error path, and verifier.
12. **Corrections compound value.** User edits become durable project knowledge rather than hidden memory.
13. **Specialist tools are partners.** Forge prepares useful handoffs rather than pretending to replace every downstream tool.
14. **Free access is not reduced functionality.** Voluntary support cannot gate core editing or local file access.
15. **Finite scope protects product quality.** Stage One and Stage Two must be completed before future-world features are activated.

---

## 6. Workflow, operation, and job

Forge must not call every button a workflow.

### Workflow

A **workflow** is a user journey that creates a durable state change, reusable asset, validated handoff, or recoverable project result.

Examples:

- create a project;
- extract a shape;
- approve a Shape Library asset;
- build an assembly;
- export a GLB.

### Operation

An **operation** is a reversible or explicitly derived command inside a workflow.

Examples:

- move;
- rotate;
- add node;
- mirror;
- union;
- extrude;
- stitch.

### Job

A **job** is bounded work that may take time and must expose:

- declared inputs;
- current stage;
- progress or heartbeat;
- elapsed time;
- cancellation boundary;
- saved evidence;
- truthful success, failure, cancellation, or timeout state.

Examples:

- generate a source preview;
- calculate contours;
- request an AI proposal;
- validate a mesh;
- package an export.

---

## 7. Product workflow architecture

The finished Stage One–Two product is organised into **18 first-class workflow families**:

- 4 shared platform workflows;
- 8 Stage One workflows;
- 6 Stage Two workflows.

Tools and commands live beneath these workflow families; they do not each become separate top-level workflows.

### 7.1 Shared platform workflows

#### P1. Project lifecycle

```text
Purpose
→ Create
→ Open
→ Work
→ Close
→ Reopen
→ Recover
```

#### P2. Source lifecycle

```text
External source
→ Import unchanged project-owned copy
→ Hash and identify
→ Generate bounded preview
→ Use in Editor
→ Explicitly process only the project-owned copy
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
→ Detect stale, incompatible, or interrupted state
→ Preserve last canonical truth
→ Recover or attach read-only
→ Rebuild indexes
→ Migrate only through explicit schema rules
```

### 7.2 Stage One workflows

#### S1. Blank Shape Creation

```text
Open writable project
→ New blank document
→ Select canvas and units
→ Begin manual shape creation
```

#### S2. Source Region and Manual Trace

```text
Open source
→ Select region
→ Trace line, path, silhouette, or mask
→ Correct nodes
→ Save candidate
```

#### S3. Algorithmic Shape Extraction

```text
Select source region
→ Configure bounded edge or threshold settings
→ Generate candidates
→ Compare
→ Choose one for editing
```

#### S4. Optional AI Shape Proposal

```text
Select source region
→ Request local model proposal
→ Record model, assumptions, and confidence
→ Display candidate
→ Edit, reject, or retain as raw evidence
```

#### S5. Shape Editing

```text
Select shape
→ Edit paths, nodes, handles, and properties
→ Transform
→ Undo/redo
→ Autosave
→ Save version
```

#### S6. 2D Composition

```text
Select multiple shapes
→ Align, mirror, array, group, or connect
→ Apply explicit path or boolean operation
→ Produce a derived editable shape
```

#### S7. Review and Shape Library

```text
Candidate
→ Review
→ Correct
→ Approve / Reject
→ Version / Supersede
→ Save reusable Shape Library asset
```

#### S8. 2D Export and Forge Pack

```text
Approved shape or composition
→ Choose validated output profile
→ Validate
→ Export SVG and/or PNG
→ Record provenance and limitations
→ Build deterministic Forge Pack
```

### 7.3 Stage Two workflows

#### T1. Declared 3D Primitive Creation

```text
Open Construct
→ Choose primitive
→ Set units and parameters
→ Create editable component
```

#### T2. Shape-to-Component Generation

```text
Approved 2D shape
→ Choose declared construction recipe
→ Set parameters
→ Generate reversible component
→ Retain parent relationship
```

Declared recipes may include:

- extrude;
- revolve;
- sweep;
- loft;
- relief;
- shell;
- bevel.

#### T3. Component Editing

```text
Select component
→ Edit recipe parameters
→ Edit transforms, origin, and pivot
→ Regenerate
→ Preserve parent shape and history
```

#### T4. Assembly and Constraint

```text
Place components
→ Position, rotate, and scale
→ Add anchors or connectors
→ Define hierarchy or contact
→ Save recoverable assembly
```

#### T5. Geometry Relationship and Merge

```text
Select components
→ Choose relationship or derived geometry operation
→ Preview result
→ Validate tolerance and limitations
→ Apply reversible or explicitly baked result
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
→ Validate units, axes, hierarchy, names, and geometry
→ Choose GLB/glTF or OBJ profile
→ Export
→ Import into named downstream program
→ Record continuation result
```

---

## 8. Operation and job scale

The controlled Stage One–Two product is expected to contain approximately:

- 18 first-class workflow families;
- 60–80 reversible or explicitly derived operations;
- 10–14 asynchronous job types;
- 12–15 core durable artifact schemas;
- 9 principal workspaces.

These are architecture estimates, not quotas. Shared abstractions should reduce duplication. Artificial files or god modules must not be created merely to match a number.

### Estimated Stage One operations

Approximately 35–45 commands across:

- selection, pan, and zoom;
- primitives and path creation;
- node and handle editing;
- path repair and simplification;
- transforms, numeric properties, snapping, and alignment;
- layers, grouping, locking, and visibility;
- duplication, mirror, and arrays;
- fill and stroke;
- explicit 2D booleans;
- review, approval, versioning, and export actions.

### Estimated Stage Two operations

Approximately 25–35 commands across:

- primitives and construction recipes;
- recipe parameter changes;
- 3D transforms, origins, and pivots;
- camera and viewport controls;
- anchors, connectors, hierarchy, instances, mirrors, and arrays;
- assembly relationships;
- stitch, join, booleans, separate, and bake;
- validation and export.

---

## 9. Project Birth and Start Here contract

Start Here gathers only enough information to begin useful work.

The project authority block should use this primary layout:

```text
Project Authority
[Project selector........................] [Refresh Projects] [Open Selected]

[PURPOSE: ........................................] [Create Project] [Close Project]
```

### No project open

- project selector enabled;
- Refresh Projects enabled;
- Open Selected enabled only when a project is selected;
- Purpose enabled;
- Create Project enabled only when Purpose contains valid text;
- Close Project disabled.

### Project open

- selector, Refresh, Open, Purpose editing, and Create disabled;
- Purpose displays the attached project purpose;
- Close Project enabled when no guarded mutation is active;
- writable, locked, and recovery authority remain explicit.

### Purpose is the first project event

On Create Project, Forge must:

1. preserve the exact user purpose;
2. derive a safe display name and directory slug without changing the stored purpose;
3. create and open the canonical project transactionally;
4. store purpose in `project.json`;
5. append a durable `project_created` history event;
6. offer a blank shape document or source-intake path;
7. guide the user to the next safe reversible action.

A long onboarding profile must not block project creation or blank-document work.

---

## 10. Workspaces and navigation

Planned application menus:

```text
File | Edit | View | Project | Source | Shapes | Construct | Analyse | Export | Settings | Help
```

Principal workspaces:

1. Start Here;
2. **Editor** — primary daily workspace;
3. My Library;
4. Shape Library;
5. Construct — Stage Two;
6. Review;
7. Agent Workflows;
8. Jobs;
9. Export.

After a project is open, Forge should normally return the user to the last valid Editor or Construct state rather than treating onboarding or AI workflows as the application centre.

The guided Next control may automate safe navigation and exact selection. It must not silently:

- start a heavy model call;
- approve a shape;
- apply an irreversible merge;
- delete an asset;
- switch projects;
- export.

Unavailable actions remain documented but are not exposed as dead controls.

---

## 11. Project authority and durable artifacts

The project directory is a self-contained recovery boundary.

Durable project files are authoritative. SQLite may support search, sorting, recent-project state, queues, and rebuildable indexes, but it is never the sole authority for creative work.

Target project layout:

```text
project/
├── project.json
├── README.md
├── source/
│   ├── originals/
│   └── previews/
├── findings/
├── structures/
│   ├── shape-documents/
│   ├── extraction-candidates/
│   ├── approved-shapes/
│   ├── construction-recipes/
│   ├── components/
│   └── assemblies/
├── briefs/
├── prompts/
├── diagnostics/
├── logs/
├── history/
└── exports/
```

Runtime code may create a directory only after the associated schema, authority, migration, and recovery rules are implemented.

### Core authoritative artifact types

1. project manifest;
2. project history event;
3. source asset record;
4. source preview record;
5. native shape document;
6. extraction candidate;
7. approved Shape Library asset;
8. approval or rejection record;
9. supersession or version record;
10. job or evidence record;
11. construction recipe;
12. editable 3D component;
13. assembly document;
14. export and Forge Pack record.

Every material artifact requires:

- stable ID and schema version;
- project, source, and parent relationships;
- actor classification: user, algorithm, or model;
- coordinate system, units, bounds, and transforms where applicable;
- operation history;
- validation and approval state;
- timestamps and content hash;
- correction and supersession history;
- intended output profile and known limitations.

---

## 12. Unified shape lifecycle

Source-derived and scratch-built shapes converge on one lifecycle. A manually created shape is not secondary to an algorithmic or AI-derived shape.

```text
blank document or source region
→ candidate shape
→ editable shape document
→ reviewed
  ├→ approved Shape Library asset
  ├→ correction requested → revised version → reviewed
  └→ rejected

approved shape
  ├→ superseded by later approved version
  ├→ 2D export
  └→ construction recipe
      → editable 3D component
      → positioned instance
      → group or assembly
      → explicit contact / stitch / join / boolean / bake result
      → verified export
```

No raw model record is presented as an approved Shape Library asset.

---

## 13. Forge Editor contract

Stage One requires a real canvas and document model, not a collection of single-purpose buttons.

Minimum tool families:

- select, box-select, pan, and zoom;
- line, polyline, pen/Bezier, freehand, and trace tools;
- rectangle, ellipse, polygon, star, and configurable primitives;
- node and handle editing;
- open/close path, reverse, simplify, smooth, split, join endpoints, and duplicate-point repair;
- fill and stroke properties;
- transform, numeric position/size/rotation, alignment, distribution, and snapping;
- duplicate, mirror, radial/linear array, group, ungroup, layer, lock, and visibility;
- union, difference, intersection, exclusion, divide, and combine as explicit 2D operations;
- anchors, connection points, symmetry axes, guides, and optional grid;
- undo/redo with bounded durable history;
- save, autosave/recovery, version, compare, approve, and export.

The editor must distinguish:

- source pixels;
- extracted candidates;
- user-created geometry;
- temporary selections and guides;
- approved project truth;
- exported derivatives.

No editor operation silently overwrites an imported original or approved prior version.

---

## 14. Shape extraction contract

Extraction is one way to begin editing, not the final product.

The first extraction system provides:

- source-region selection;
- manual trace baseline;
- line, contour, region, mask, and silhouette candidates;
- open/closed contours, holes, intersections, endpoints, symmetry, and nesting;
- threshold and edge settings for algorithmic extraction;
- visible confidence and limitations for AI proposals;
- editable candidate paths on the same canvas used for scratch-built shapes;
- exact source coordinates and source hash;
- no automatic approval.

Manual tracing and correction remain available when no extraction engine or model is installed.

---

## 15. Construct contract

Stage Two provides:

- three-axis scene and camera views;
- orthographic and perspective modes;
- transform gizmos and numeric transforms;
- units, grid, origin, pivots, snapping, anchors, connectors, and hierarchy;
- locking, visibility, duplication, mirroring, arrays, instances, and undo/redo;
- non-destructive construction history;
- component and assembly inspection;
- export-profile validation.

“One-click Make 3D” means “create a reversible preview using a declared method.” It does not mean “produce a finished object.”

Group, assembly, contact, stitch, join mesh, boolean, separate, and bake remain distinct operations and artifact states.

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

### Core Stage One outputs

- native versioned Forge shape document;
- Forge Pack JSON and human-readable Markdown;
- SVG for editable vectors, silhouettes, masks, and supported layered 2D construction;
- PNG for transparent derivatives, masks, previews, and annotated evidence.

### Later validated 2D profiles

- JPEG;
- WebP;
- TIFF;
- PDF;
- DXF.

These remain hidden or unavailable until format-specific validation passes.

### Core Stage Two outputs

- GLB/glTF as the first general 3D blockout and engine-friendly adapter;
- OBJ as a simple fallback with explicit material and hierarchy limitations.

### Later validated 3D adapters

- STL;
- 3MF;
- STEP;
- FBX;
- OpenUSD.

Each requires separate units, geometry, legal, packaging, or downstream continuation evidence.

### Planned target profiles

- Krita raster continuation;
- Inkscape SVG continuation;
- Blender blockout and modular assembly;
- Godot game asset;
- Unity game asset;
- Unreal Engine prop or environment;
- generic GLB/glTF;
- generic OBJ;
- generic 2D CAD profile;
- 3D-print concept;
- generic Forge Pack.

---

## 17. Optional production intelligence and agent workflows

Structured intelligence supports the editor; it does not block manual work.

Useful fields may include:

- source identity and hash;
- visible objects, motifs, surfaces, and regions;
- line, contour, layer, depth, and occlusion evidence;
- component IDs, hierarchy, anchors, connectors, and transforms;
- masks, silhouettes, vector candidates, holes, and interior contours;
- symmetry, repetition, module families, and variation rules;
- scale, units, perspective, and camera assumptions;
- colour and material observations;
- construction recommendations;
- observed, inferred, user-created, and approved classification;
- confidence, uncertainty, contradiction, and missing evidence;
- intended downstream profile;
- review, correction, rejection, approval, and supersession records.

Current prompt contracts remain optional support jobs:

- source_art_intelligence;
- modular_set_perspective;
- prototype_imagination;
- shape_structure_harvest;
- concept_brief;
- render_prompt_pack;
- recommend_next_step.

They are not the 18 first-class product workflows and cannot become project truth without the appropriate review and artifact path.

---

## 18. Automation and user control

| Mode | Behaviour |
|---|---|
| Manual | Tools execute only direct user commands |
| Assisted | Forge proposes an action and waits for approval |
| Guided Automatic | Forge runs a visible reversible sequence and pauses at gates |
| Batch Automatic | Forge applies user-approved rules and reports exceptions |

Manual and Assisted modes are first-class. Guided Automatic may support onboarding but must never force automation.

Every automated run declares inputs, stages, model or algorithm, storage destination, assumptions, workload state, elapsed time, heartbeat, cancellation boundary, outputs, failures, and next action.

---

## 19. Shared implementation architecture

### 19.1 Command framework

All material Editor and Construct changes use a common command contract:

```text
validate
→ apply
→ persist or autosave
→ undo
→ redo
→ serialize
→ replay
```

A command records:

- command ID;
- operation type;
- parameters;
- affected artifact IDs;
- before/after references where required;
- timestamp;
- actor;
- validation result.

### 19.2 Product registry

Forge requires a registry that distinguishes:

- interactive workflow;
- editor operation;
- construct operation;
- asynchronous job;
- export adapter;
- validation profile.

The seven AI prompt contracts remain a separate optional agent registry.

### 19.3 Selection model

One shared selection contract must serve:

- source regions;
- 2D paths;
- nodes and handles;
- groups and layers;
- 3D components;
- assembly members.

### 19.4 Provenance graph

Every derivative remains traceable:

```text
export
← assembly
← components
← construction recipes
← approved shapes
← shape documents
← source regions
← unchanged source assets
```

### 19.5 Validation framework

Validation is profile-driven rather than scattered across controls.

Initial profiles include:

- project integrity;
- shape document;
- approved Shape Library asset;
- SVG export;
- PNG export;
- construction recipe;
- component;
- assembly;
- GLB/glTF export;
- OBJ export.

---

## 20. Expected codebase scale

Each workflow may require:

1. schema or domain contract;
2. core service or engine;
3. persistence and transaction handling;
4. UI controller or workspace integration;
5. command or job adapter;
6. validator;
7. deterministic verifier;
8. fixture data;
9. documentation and migration notes.

A realistic finished Stage One–Two repository may contain approximately:

| Code family | Estimated scale |
|---|---:|
| Core schemas and domain models | 12–18 modules |
| Project, persistence, and authority services | 10–15 modules |
| 2D geometry and editor engines | 15–25 modules |
| 3D construction and assembly engines | 15–25 modules |
| Qt workspaces, controllers, and reusable widgets | 15–22 modules |
| Export adapters and validators | 8–14 modules |
| Background workers and job infrastructure | 6–10 modules |
| Migrations and compatibility handlers | 5–10 modules |
| Deterministic tests, verifiers, and fixtures | 40–70 files |
| Release, installation, and recovery tooling | 8–15 files |

This is an order-of-magnitude architecture estimate, not a requirement to manufacture files.

---

## 21. Stage One acceptance boundary

Stage One is complete only when a new user can:

1. install and launch an official release;
2. enter a Purpose and create, open, close, and safely recover a local project;
3. import a supported source image without changing external bytes, or create a blank shape document;
4. inspect a bounded source preview and preserve source identity and rights notes;
5. create candidates through manual, algorithmic, or optional AI-assisted paths;
6. create shapes from scratch using primitives and path tools;
7. select, move, add, remove, and edit nodes and handles;
8. edit open and closed contours, holes, fill, stroke, bounds, anchors, and symmetry;
9. use transforms, snapping, alignment, duplication, mirroring, arrays, grouping, layers, visibility, locking, undo, and redo;
10. perform explicit non-destructive 2D path and boolean operations with inspectable results;
11. compare a source-derived candidate with the source and correct it manually;
12. rename, reject, approve, supersede, and version a shape;
13. save and reopen a reusable Shape Library entry;
14. inspect jobs, diagnostics, model identity where applicable, elapsed time, and saved evidence;
15. export validated SVG and PNG derivatives through named profiles;
16. export a deterministic Forge Pack with provenance and limitations;
17. process only the project-owned source copy through an explicit action;
18. restart Forge and recover editable state without relying on terminal history;
19. import the exported result into a fresh named downstream session and continue work.

Stage One does not promise:

- production-ready topology or finished 3D meshes;
- engineering-grade dimensions from an unscaled image;
- watertight or manufacture-safe geometry;
- hidden-surface reconstruction;
- automatic CAD solids, rigging, UVs, LODs, collision, or final materials;
- unattended publishing or sales;
- unlimited parallel jobs;
- perfect extraction or AI interpretation;
- future Product Level Three or Four functionality.

---

## 22. Stage Two acceptance boundary

Stage Two—and therefore the planned finished product—is complete only when a new user can:

1. open an approved Stage One shape or create a declared 3D primitive;
2. generate a reversible 3D component using an explicit recipe;
3. inspect and edit operation parameters without destroying the source shape;
4. work in orthographic and perspective views with units, axes, origin, pivots, and transform gizmos;
5. position, rotate, scale, duplicate, mirror, array, hide, lock, and instance components;
6. create and edit anchors, connectors, hierarchy, and assembly relationships;
7. distinguish group, assembly, contact, stitch/weld, join mesh, boolean, separate, and bake;
8. preview intersections, open boundaries, normals, and declared export limitations;
9. retain non-destructive construction history and parent-child provenance;
10. save, close, reopen, recover, and continue a 3D construction;
11. export through a verified GLB/glTF profile and a validated OBJ fallback;
12. import the exported result into Blender or another named supported tool;
13. continue editing without losing declared units, axes, names, hierarchy, or provenance.

Stage Two does not claim engineering certification, manufacturing safety, automatic repair, finished topology, automatic rigging, or universal compatibility.

---

## 23. Delivery programme

### Stage One programme — Forge Editor

#### Milestone A — Verified local foundation

Status: substantially complete.

- canonical identity and source truth;
- relocatable launcher and desktop launchers;
- modest-hardware policy;
- project manifest, locking, session, and source authority;
- asynchronous source intake and discovery;
- bounded previews and image compatibility;
- guarded Qt worker lifecycle;
- guided navigation;
- project-owned model-call evidence;
- native shape-document and minimum Editor foundation;
- corrected official launcher import order.

Exit: merged deterministic contracts pass on the T1700, the working tree is clean, and the live application opens and closes without startup abort.

#### Milestone B — Project Birth and Editor authority

- Purpose-driven Start Here layout;
- project-created history event;
- safe name/slug derivation;
- create/open/close/recovery UI contract;
- return to last valid editor state;
- live minimum Editor acceptance.

Exit: a user creates a project from Purpose, enters the Editor, creates and saves a blank document, closes, reopens, and recovers it.

#### Milestone C — Manual 2D creation and editing

- selection and transform command foundation;
- primitives, pen/path, and node editing;
- snapping, guides, layers, groups, duplication, mirrors, and arrays;
- fill/stroke and explicit 2D booleans;
- deterministic editor-command fixtures.

Exit: a user builds a non-trivial reusable shape from scratch without AI.

#### Milestone D — Source-derived shape extraction

- source overlay and region selection;
- manual trace baseline;
- bounded algorithmic contour and mask candidates;
- optional AI proposal adapter;
- source-coordinate provenance and correction tools.

Exit: a source-derived shape is corrected on the same canvas and remains traceable to unchanged source bytes.

#### Milestone E — Review and Shape Library lifecycle

- candidate/review/approve/reject/supersede/version workflow;
- editable Shape Library entries;
- comparison and provenance views;
- no raw AI record presented as an approved shape.

Exit: approved manual and source-derived shapes reopen as editable reusable assets.

#### Milestone F — Stage One interoperability and Forge Pack

- SVG and PNG adapters;
- deterministic package builder;
- adapter validation, export report, provenance, and limitations;
- Inkscape, Krita, and generic continuation tests.

Exit: a fresh downstream session imports and continues from exported Stage One assets without filesystem archaeology.

#### Milestone G — Stage One release engineering

- clean install, update, rollback, removal, migration, backup, and recovery;
- versioned GitHub release and checksums;
- recognised licence and contributor-policy decision;
- release notes and website download path;
- free-access and voluntary-support wording.

Exit: a new user completes the Stage One journey and retains local editable work.

### Stage Two programme — Construct

#### Milestone H — Reversible 2D-to-3D components

- construction-recipe schema;
- extrude, revolve, sweep, loft, shell, relief, and bevel;
- editable parameters and parent provenance;
- component validation.

Exit: an approved 2D shape produces a reversible editable 3D component.

#### Milestone I — Construct workspace and assembly

- 3D viewport, cameras, transforms, snaps, anchors, connectors, hierarchy, instances, arrays, and undo/redo;
- group, assembly, contact, stitch/weld, join, boolean, separate, and bake distinctions;
- construction history.

Exit: users assemble components into a recoverable modular construction.

#### Milestone J — Stage Two interoperability

- GLB/glTF and OBJ adapters;
- Blender and named engine continuation tests;
- mesh, hierarchy, axis, units, naming, and limitation reports;
- optional STL, 3MF, or DXF only after their gates pass.

Exit: a named downstream program imports and continues the verified blockout.

#### Milestone K — Stage Two release engineering

- installation and migration from Stage One;
- Editor/Construct compatibility declarations;
- recovery and round-trip regression suite;
- official Stage Two release.

Exit: a new user completes the shape-to-component-to-assembly-to-export journey on supported hardware.

#### Milestone L — Optional advanced adapters

- STEP after dimensional and solid contracts;
- OpenUSD after assembly semantics;
- community adapter and profile framework;
- optional text-to-image source adapter only after explicit privacy and provenance rules.

Milestone L does not activate future Product Level Three or Four.

---

## 24. Verification system

Every milestone requires proportionate evidence:

1. Markdown and source-truth checks;
2. Python compile and fresh-process import checks;
3. pure-logic unit contracts;
4. fixture-based integration contracts;
5. thread and cancellation lifecycle contracts;
6. schema and migration validation;
7. filesystem interruption and recovery tests;
8. editor command, undo/redo, and autosave recovery tests;
9. benchmark-source and scratch-built asset comparisons;
10. manual Qt smoke checks on the T1700;
11. downstream import, round-trip, or continuation checks for every export profile.

No milestone becomes `VERIFIED` solely because code was committed or merged.

---

## 25. Immediate permitted engineering sequence

The next engineering order is:

1. merge this documentation reconciliation after review and source-truth checks;
2. implement Project Birth and the corrected Start Here authority layout;
3. complete live launcher and minimum Editor acceptance on merged `main`;
4. establish selection and transform commands;
5. add manual primitives and path/node editing;
6. add source-region selection and manual trace;
7. add bounded algorithmic extraction candidates;
8. add optional AI proposals only through the editable candidate path;
9. implement Shape Library review, approval, rejection, versioning, and supersession;
10. implement and verify SVG and PNG export profiles;
11. complete Stage One release acceptance;
12. begin reversible 2D-to-3D component recipes;
13. build Construct assembly and Stage Two export profiles;
14. complete Stage Two release acceptance.

Every PR advances one coherent gate, preserves verified behaviour, updates the progress ledger, and avoids unrelated UI promises.

---

## 26. PR implementation contract

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

## 27. Explicit exclusions from the finished Stage One–Two product

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

These may exist in ZCVIOS lore or later specialist systems, but they are not required to complete MXZTAR Forge v2.0.

---

## 28. Distribution, access, and support

MXZTAR Forge is an MXZTAR Projects build from `https://www.mxztar.co.nz`.

Official software use is intended to be free of charge. There is no confirmed timed trial, subscription, or core-feature paywall. Voluntary support may be offered through `https://buymeacoffee.com/mxztar`, but it cannot gate core editing or local file access.

Ordinary users will be directed to versioned official releases so application code, schemas, model compatibility, and migrations remain synchronised.

Before the first public release, the repository must contain a recognised `LICENSE` selected by the founder and consistent contributor terms. Public source visibility and free-of-charge access do not themselves define modification or redistribution permission.

---

## 29. Future horizon authority

The separately governed future documents preserve long-term ideas without changing the active build:

- `FUTURE_CONSTRUCT_AND_WORLD_VISION.md`;
- `LEVEL_FOUR_PLATFORM_PRIORITIES.md`.

The active maturity horizon is:

- Stage One: editor-first reusable 2D shape creation and portable assets;
- Stage Two: reversible 3D component construction, assembly, and portable blockouts;
- Product Level Three: **DEFERRED**;
- Product Level Four: **DEFERRED**.

No date is assigned to Product Level Three or Four by this plan.
