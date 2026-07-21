# MXZTAR Forge v2.0 — Master Build Plan

## 1. Product definition

MXZTAR Forge v2.0 is a local-first, human-governed creative asset editor and
concept-engineering forge.

The **Forge Editor** is the product centre and is expected to become the most-used
workspace. Source analysis, local AI, Shape Library, jobs, construction, and export exist
to support creator-led editing rather than replace it.

The active value path is:

```text
source image or blank canvas
→ extract a candidate shape or create one from scratch
→ edit nodes, contours, layers, transforms, and construction properties
→ save a reusable, versioned Shape Library asset
→ assemble or derive components in a reversible 3D environment
→ export through a validated profile for another user workflow or program
```

A creator must be able to produce useful assets without installing or running an AI
model. AI is optional assistance for observation, extraction proposals, construction
suggestions, and next-step guidance.

Forge does not claim automatic production-ready geometry merely because an image was
analysed or a 3D preview was generated.

## 2. Active product levels and deferred levels

Product **Levels** describe user capability. They are not the same as implementation
milestones or pull-request numbers.

### Level One — Shape Editor and portable 2D assets

Level One establishes the primary daily tool:

```text
project
→ source intake or blank shape document
→ source-derived or scratch-built shape
→ manual editing and review
→ reusable Shape Library entry
→ verified 2D export and Forge Pack
```

Level One must work locally and remain useful without AI.

### Level Two — 3D Construct and portable blockouts

Level Two extends approved or scratch-built shapes into a reversible 3D construction
workflow:

```text
approved 2D shape or primitive
→ declared 3D construction operation
→ editable component
→ positioned instances and assemblies
→ explicit stitch / join / boolean / group operations
→ verified 3D export
```

Level Two is an active planned product level. It follows the verified Level One editor
foundation; it is not part of the deferred future-world programme.

### Level Three — deferred

Level Three infrastructure relationships, regional state, distributed deltas, and
advanced system-scale construction remain **DEFERRED** until a future founder-approved
planning date. No Level Three runtime work is permitted merely because Level One or
Level Two documentation exists.

### Level Four — deferred

Level Four cross-device platform, operator jobs, browser/tablet/mobile/AR/VR clients,
collaboration, authorship economy, persistent regions, and world simulation remain
**DEFERRED** until a future founder-approved planning date.

`FUTURE_CONSTRUCT_AND_WORLD_VISION.md` and `LEVEL_FOUR_PLATFORM_PRIORITIES.md` preserve
vision only. They are not current implementation instructions, delivery dates, or
feature claims.

## 3. Asset, owner, users, and value

**Primary asset:** a durable Forge project containing authoritative source references,
editable shape documents, approved Shape Library assets, construction history,
assemblies, job evidence, and validated exports.

**Portable asset:** a deterministic Forge Pack assembled from approved project records.
It is an export view, not a second project authority.

**Owner:** the creator controls their local source material, project records, editable
derivatives, approvals, assemblies, and exports. MXZTAR controls the Forge application
and its official releases.

**Primary users:**

1. concept, visual-development, graphic, and vector artists;
2. indie game, environment, prop, and world-building artists;
3. Blender generalists and 3D blockout artists;
4. makers and 3D-print designers at concept and blockout stage;
5. small film, animation, game, fabrication, and design teams without a dedicated
   technical-art department;
6. creators who need reusable shapes but do not want their workflow to depend on cloud
   services or expensive hardware.

**User problem:** source images contain useful structure, but production programs expect
editable paths, layers, scale, hierarchy, geometry decisions, and disciplined file
formats. Creators repeatedly rebuild that missing structure across tracing tools,
painting programs, AI chats, Blender, CAD, engines, and folders.

**Forge value:** provide one governed place to import, extract, draw, edit, organise,
assemble, validate, and export reusable creative assets while preserving source identity
and every material user decision.

## 4. Product principles

1. **Editor first.** The editor is a complete creator tool, not a read-only preview of AI
   output.
2. **Local first.** Source art and project truth remain local unless the user explicitly
   chooses an external operation.
3. **Human governed.** Extraction, joining, replacement, boolean operations, baking, and
   export remain visible user decisions.
4. **AI optional.** Manual creation, editing, saving, and export cannot depend on an AI
   model or network connection.
5. **Observed is not inferred.** Source evidence, calculation, model inference, user
   intent, speculation, and approved truth remain separate states.
6. **Non-destructive by default.** Originals remain unchanged; editor and construction
   operations create versioned derivatives with undo/redo and history.
7. **No dead or frozen UI.** Heavy work runs outside the Qt main thread with progress,
   heartbeat, elapsed time, cancellation boundaries, and truthful final state.
8. **Modest hardware remains valid.** One heavy local job at a time by default, bounded
   previews, conservative threads, no silent downloads, and no hidden escalation.
9. **Interoperability is verified, not advertised.** A format or target program is exposed
   only after a fixture and round-trip or import test proves the adapter.
10. **Readable durable output.** JSON, Markdown, SVG, PNG, and documented interchange
    files remain inspectable outside Forge.
11. **Every name is a promise.** No button, format, status, or AI claim exists without a
    complete handler, result, error path, persistence rule, and verifier.
12. **Corrections compound value.** User edits become durable project knowledge rather
    than hidden, unreviewed memory.
13. **Specialist tools are partners.** Forge creates useful handoffs and does not pretend
    to replace every feature of Krita, Inkscape, Blender, game engines, CAD systems, or
    slicers.
14. **Free access is not reduced functionality.** Official software use is free of
    charge. Voluntary support may be offered at `https://buymeacoffee.com/mxztar` but
    cannot gate core editing or file access.

## 5. Level One acceptance boundary

Level One is complete only when a new user can:

1. install and launch an official release;
2. create, open, close, and safely recover a local project;
3. import a supported source image without changing external bytes, or create a blank
   shape document;
4. inspect a bounded source preview and preserve source identity and rights notes;
5. request shape candidates through a manual, algorithmic, or optional AI-assisted path;
6. create shapes from scratch using primitives and path tools;
7. select, move, add, remove, and edit nodes and handles;
8. edit open and closed contours, holes, fill, stroke, bounds, anchors, and symmetry;
9. use transforms, snapping, alignment, duplication, mirroring, arrays, grouping, layers,
   visibility, locking, undo, and redo;
10. perform explicit non-destructive 2D boolean operations with inspectable results;
11. compare a source-derived candidate with the source and correct it manually;
12. rename, reject, approve, supersede, and version a shape;
13. save and reopen a reusable Shape Library entry;
14. inspect jobs, diagnostics, model identity where applicable, elapsed time, and saved
   evidence;
15. export a validated SVG and PNG derivative through a named profile;
16. export a deterministic Forge Pack with provenance and limitations;
17. move only the project-owned source copy through an explicit processed-source action;
18. restart Forge and recover editable state without relying on terminal history.

Level One does not promise:

- production-ready topology or finished 3D meshes;
- engineering-grade dimensions from an unscaled image;
- watertight or manufacture-safe geometry;
- hidden-surface reconstruction;
- automatic CAD solids, rigging, UVs, LODs, collision, or final materials;
- unattended publishing or sales;
- unlimited parallel jobs;
- perfect extraction or AI interpretation;
- Level Three or Level Four platform functionality.

## 6. Level Two acceptance boundary

Level Two is complete only when a user can:

1. open an approved Level One shape or create a declared 3D primitive;
2. generate a reversible 3D component using an explicit operation such as extrude,
   revolve, sweep, loft, shell, relief, or bevel;
3. inspect and edit operation parameters without destroying the source shape;
4. work in orthographic and perspective views with units, axes, origin, pivots, and
   transform gizmos;
5. position, rotate, scale, duplicate, mirror, array, hide, lock, and instance components;
6. create and edit anchors, connectors, hierarchy, and assembly relationships;
7. distinguish group, assembly, contact, stitch/weld, join mesh, boolean union, boolean
   difference, separate, and bake;
8. preview intersections, open boundaries, normals, and declared export limitations;
9. retain non-destructive construction history and parent-child provenance;
10. save, reopen, and continue a 3D construction;
11. export through a verified GLB profile and at least one validated fallback profile;
12. import the exported result into the named downstream tool and complete the recorded
    round-trip or continuation test.

Level Two does not claim engineering certification, manufacturing safety, automatic
repair, finished topology, or universal compatibility.

## 7. Workspaces and navigation

Forge adopts a mature creative-application layout without copying another product:

```text
File | Edit | View | Project | Source | Shapes | Construct | Analyse | Export | Settings | Help
```

Primary workspaces:

1. Start Here;
2. **Editor** — the primary daily workspace;
3. My Library;
4. Shape Library;
5. Construct — active in Level Two;
6. Review;
7. Agent Workflows;
8. Jobs;
9. Export.

After a project is open, Forge should normally return the user to the last valid editor
state rather than treating onboarding or AI workflows as the application centre.

The always-visible guided Next control may automate safe navigation and exact selection.
It must never silently start a heavy model call, approve a shape, apply an irreversible
join, delete an asset, switch projects, or export.

Deferred workspaces and unavailable actions are documented but not exposed as dead
controls.

## 8. Project authority and editable documents

The canonical project authority remains the self-contained project defined by
`docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md` and
`docs/product/OUTPUT_ARTIFACT_CONTRACTS.md`.

Current contracted directories remain authoritative. New editor records must use a
versioned schema and a documented migration before runtime writes begin. Proposed editor
records belong beneath the existing `structures/` authority rather than in an unrelated
parallel workspace:

```text
project/
├── project.json
├── source/
│   ├── originals/
│   └── previews/
├── findings/
├── structures/
│   ├── shape-documents/
│   ├── approved-shapes/
│   ├── construction-recipes/
│   └── assemblies/
├── briefs/
├── prompts/
├── diagnostics/
├── logs/
├── history/
└── exports/
```

This layout is a planning target until its schema and migration are implemented. Runtime
code must not create these proposed subdirectories merely because they appear here.

Every material editor or construction artifact carries:

- stable ID and schema version;
- project and source relationship;
- creator identity: user, algorithm, or model;
- coordinate space, units, bounds, and transforms;
- operation history and parent IDs;
- validation and approval state;
- timestamps and content hash;
- correction and supersession history;
- intended output profile and known limitations.

SQLite may index these files but is never the sole authority.

## 9. Source-image intake and compatibility

Accepted source originals currently include:

- PNG;
- JPEG/JPG;
- WebP;
- BMP;
- TIFF/TIF;
- GIF, with the first frame used for preview generation.

Accepted originals remain unchanged and authoritative. Bounded previews are rebuildable
derivatives.

Current model-ready source formats are PNG, JPEG, and WebP. BMP, TIFF, and GIF may be
imported and previewed but must remain blocked from model execution until a separately
verified normalized model-input derivative preserves provenance.

Future source adapters may include layered documents, vector files, camera captures, or
generated sources only through explicit contracts. Text-to-image is an optional later
input adapter and is not required for editing.

## 10. Unified shape lifecycle

Source-derived and scratch-built shapes converge on one lifecycle. A manually created
shape is not secondary to an AI-derived shape.

```text
blank document or source region
→ candidate shape
→ editable shape document
→ reviewed
  ├→ approved Shape Library asset
  ├→ correction requested → revised version → reviewed
  └→ rejected

approved shape
  ├→ superseded by a later approved version
  ├→ 2D export
  └→ construction recipe
      → editable 3D component
      → positioned instance
      → group or assembly
      → explicit stitch / join / boolean / bake result
      → verified export
```

A Shape Library entry may contain:

- original source reference where applicable;
- manual/source-derived origin classification;
- editable path and node representation;
- mask, silhouette, vector outline, and holes;
- fill, stroke, layers, groups, anchors, bounds, centre, and symmetry axes;
- dimensional assumptions and confidence;
- intended role: profile, panel, trim, cutout, path, decoration, volume source, or
  connector;
- approval state, correction history, and parent-child provenance;
- compatible construction and export profiles.

## 11. Forge Editor contract

The Level One Editor requires a real canvas and document model, not a collection of
single-purpose buttons.

Minimum tool families:

- select, box-select, pan, and zoom;
- line, polyline, pen/Bezier, freehand, and trace tools;
- rectangle, ellipse, polygon, star, and configurable primitive tools;
- node and handle editing;
- open/close path, reverse path, simplify, smooth, split, join endpoints, and remove
  duplicate points;
- fill and stroke properties;
- transform, numeric position/size/rotation, alignment, distribution, and snapping;
- duplicate, mirror, radial/linear array, group, ungroup, layer, lock, and visibility;
- union, difference, intersection, exclusion, divide, and combine as explicit 2D boolean
  operations;
- anchors, connection points, symmetry axes, construction guides, and optional grid;
- undo/redo with bounded durable history;
- save, autosave/recovery, version, compare, approve, and export.

The editor must distinguish:

- source pixels;
- extracted candidates;
- user-created geometry;
- temporary selections and guides;
- approved project truth;
- exported derivatives.

No editor operation may silently overwrite an imported original or an approved prior
version.

## 12. Shape extraction contract

Extraction is one way to begin editing, not the final product.

The first extraction system should provide:

- source region selection;
- line, contour, region, mask, and silhouette candidates;
- open/closed contours, holes, intersections, endpoints, symmetry, and nesting;
- threshold and edge settings where algorithmic extraction is used;
- visible confidence and limitations where AI assistance is used;
- editable candidate paths on the same canvas used for scratch-built shapes;
- exact source coordinates and source hash;
- no automatic approval.

Manual tracing and correction remain available even when no extraction engine or model is
installed.

## 13. Construct workspace and 3D assembly

The Level Two Construct workspace provides:

- three-axis scene and camera views;
- orthographic and perspective modes;
- transform gizmos and numeric transforms;
- units, grid, origin, pivots, snapping, anchors, connectors, and hierarchy;
- locking, visibility, duplication, mirroring, arrays, instances, and undo/redo;
- non-destructive construction history;
- component and assembly inspection;
- export-profile validation.

Approved 2D shapes may use declared operations:

- extrude;
- bevel;
- revolve;
- sweep;
- loft;
- relief;
- shell;
- optional AI-assisted morph with stated assumptions.

“One-click Make 3D” means “create a reversible preview using a declared method.” It does
not mean “produce a finished object.”

The UI and artifact schema must keep these operations distinct:

- **group:** selection and transform relationship only;
- **assembly:** components retain identity and relationship metadata;
- **contact/mate:** declared positional relationship without geometry merge;
- **stitch/weld:** merge compatible boundaries or vertices under explicit tolerance;
- **join mesh:** combine mesh objects while retaining declared source mapping where
  possible;
- **boolean union/difference/intersection:** create a derived result from named inputs;
- **bake:** intentionally collapse reversible history into a new derivative.

## 14. Interoperability and output profiles

No single industry file is universal. Forge uses named output profiles with declared
units, scale, coordinate system, up-axis, origin, pivots, hierarchy, names, materials,
textures, limitations, and validation evidence.

### 14.1 Core Level One outputs

- native versioned Forge shape document;
- Forge Pack JSON and human-readable Markdown;
- SVG for editable vectors, silhouettes, masks, and layered 2D construction where
  supported;
- PNG for transparent raster derivatives, masks, previews, and annotated evidence.

### 14.2 Validated 2D derivatives

These may be exposed after format-specific verification:

- JPEG for flattened delivery where transparency is not required;
- WebP for compact web-oriented delivery;
- TIFF for high-quality raster exchange and print-oriented profiles;
- PDF for documented review or vector/raster handoff where a complete PDF contract is
  implemented;
- DXF for 2D CAD profiles after units and path restrictions are proven.

### 14.3 Core Level Two outputs

- GLB/glTF as the first general 3D blockout and engine-friendly adapter;
- OBJ as a simple legacy mesh fallback with explicit material and hierarchy limitations.

### 14.4 Later validated adapters

- STL for simple additive-manufacturing geometry after mesh validation;
- 3MF after units, materials, packaging, and print validation;
- STEP only after dimensional authority and solid-geometry contracts are proven;
- FBX only if a lawful, maintainable adapter and target-program round trip are proven;
- OpenUSD for complex composed scenes after assembly semantics are mature.

### 14.5 Target workflow profiles

Planned profiles include:

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

A profile remains hidden or marked unavailable until its export, validation, downstream
import, and documented limitation checks pass.

## 15. Structured production intelligence

Forge must create more than prose, but structured intelligence now supports the editor
rather than blocking manual work.

Useful structured fields include:

- source identity and hash;
- visible objects, motifs, surfaces, and regions;
- line, contour, layer, depth, and occlusion evidence;
- component IDs, hierarchy, anchors, connectors, and transforms;
- masks, silhouettes, vector candidates, holes, and interior contours;
- symmetry, repetition, module families, and variation rules;
- scale, units, perspective, and camera assumptions;
- colour and material observations;
- construction recommendations;
- observed/inferred/user-created/approved classification;
- confidence, uncertainty, contradiction, and missing evidence;
- intended downstream profile;
- review, correction, rejection, approval, and supersession records.

Manual editor documents may exist before this full intelligence schema is complete.
Invalid model output cannot become approved editor truth.

## 16. Automation and user control

Forge exposes explicit automation levels:

| Level | Behaviour |
|---|---|
| Manual | Tools execute only direct user commands |
| Assisted | Forge proposes an action and waits for approval |
| Guided Automatic | Forge runs a visible reversible workflow and pauses at gates |
| Batch Automatic | Forge applies user-approved rules and reports exceptions |

Manual and Assisted modes are first-class. Guided Automatic may be the onboarding
default, but the editor must never force automation.

Every automated run declares inputs, stages, model or algorithm, storage destination,
assumptions, workload state, elapsed time, heartbeat, cancellation boundary, outputs,
failures, and next action.

## 17. Start Here and intent model

Start Here gathers only the information needed to open a useful editor session.
Progressive optional fields may include:

- project name and purpose;
- source origin, ownership assertion, and licence notes;
- target application or workflow;
- intended asset type;
- preferred units and output profile;
- 2D, 2.5D, blockout, CAD-concept, print-concept, or modular intent;
- accuracy, scale, symmetry, repetition, material, and style expectations;
- local privacy, network, accessibility, and learning preferences.

Hidden profiling is prohibited. The user can inspect, correct, export, or remove stored
profile and project intent.

A long onboarding questionnaire must not block a creator from opening a project and
starting a blank shape document.

## 18. UI and learning architecture

The centre of Editor and Construct is the active canvas or viewport. Toolbars and
resizable panels surround it. Layout, geometry, zoom, selection, active document, and
safe tool state persist.

Every important control has:

- a concise normal tooltip;
- after a three-second hover, an optional Insight explaining what it does, when to use
  it, what changes, whether it is reversible, what it creates, and one example;
- Learning Mode, Tooltips Only, New Features, and Insights Off preferences.

The interface should use visual hierarchy and slow guidance rather than requiring users
to infer click order. Flashing must remain slow, non-aggressive, and disableable.

## 19. Build milestones

Lettered milestones replace the former numbered phase sequence to avoid confusion with
Product Levels Three and Four.

### Milestone A — Verified local foundation

Status: substantially complete.

- canonical identity and source truth;
- relocatable launcher and desktop launchers;
- modest-hardware policy;
- project manifest, locking, session, and source authority;
- asynchronous source intake and discovery;
- bounded previews and broadened image compatibility;
- guarded Qt worker lifecycle;
- guided Next flow;
- project-owned model-call evidence.

Exit: merged deterministic contracts pass on the T1700, the working tree is clean, and
no live startup thread abort remains.

### Milestone B — Editor architecture and native shape document

**Next active milestone.**

- define the native shape-document schema and coordinate model;
- define editor commands, durable history, autosave, recovery, and versioning;
- build the primary canvas, tool state, selection model, layer model, and property panels;
- add blank-document creation and safe reopen;
- expose no unsupported tools.

Exit: a blank shape document can be created, edited through one verified command, saved,
closed, reopened, and recovered after an interrupted save.

### Milestone C — Manual 2D creation and editing

- primitives, pen/path, node editing, transforms, snapping, guides, layers, groups,
  duplication, mirroring, arrays, and undo/redo;
- fill/stroke and explicit 2D boolean operations;
- deterministic editor-command fixtures.

Exit: a user can build a non-trivial reusable shape from scratch without AI.

### Milestone D — Source-derived shape extraction

- source-region selection;
- manual trace baseline;
- algorithmic contour/mask candidates;
- optional AI proposal adapter;
- source-coordinate provenance and correction tools.

Exit: a source-derived shape can be corrected on the same editor canvas and remains
traceable to unchanged source bytes.

### Milestone E — Review and Shape Library lifecycle

- candidate/review/approve/reject/supersede/version workflow;
- editable Shape Library entries;
- comparison and provenance views;
- no raw AI record presented as an approved shape.

Exit: approved manual and source-derived shapes reopen as editable reusable assets.

### Milestone F — Level One interoperability and Forge Pack

- SVG and PNG adapters;
- deterministic package builder;
- adapter validation, export report, provenance, and limitations;
- Inkscape/Krita/generic continuation tests.

Exit: a fresh downstream session can import and continue from exported Level One assets
without filesystem archaeology.

### Milestone G — Level One release engineering

- clean install, update, rollback, removal, migration, backup, and recovery;
- versioned GitHub release and checksums;
- official licence and contributor-policy decision;
- release notes and website download path;
- free-access and voluntary-support wording.

Exit: a new user completes the Level One editor journey and retains local editable work.

### Milestone H — Reversible 2D-to-3D components

- construction-recipe schema;
- extrude, revolve, sweep, loft, shell, relief, and bevel;
- editable parameters and parent provenance;
- component validation.

Exit: an approved 2D shape produces a reversible editable 3D component.

### Milestone I — Construct workspace and assembly

- 3D viewport, cameras, transforms, snaps, anchors, connectors, hierarchy, instances,
  arrays, and undo/redo;
- group, assembly, contact, stitch/weld, join, boolean, separate, and bake distinctions;
- construction history.

Exit: users assemble components into a recoverable modular construction.

### Milestone J — Level Two interoperability

- GLB/glTF and OBJ adapters;
- downstream Blender and engine continuation tests;
- mesh, hierarchy, axis, units, naming, and limitation reports;
- optional STL/3MF/DXF only after their gates pass.

Exit: a named downstream program imports and continues the verified blockout.

### Milestone K — Level Two release engineering

- installation and migration from Level One;
- editor/Construct compatibility declarations;
- recovery and round-trip regression suite;
- official Level Two release.

Exit: a new user completes the shape-to-assembly-to-export journey on supported hardware.

### Milestone L — Optional advanced adapters and generation

- STEP after dimensional and solid contracts;
- OpenUSD after assembly semantics;
- optional text-to-image source generation;
- community adapter/profile framework.

This milestone does not activate Product Level Three or Level Four.

## 20. Verification system

Every milestone requires proportionate evidence:

1. Markdown/source-truth checks;
2. Python compile/import checks;
3. pure-logic unit contracts;
4. fixture-based integration contracts;
5. thread and cancellation lifecycle contracts;
6. schema and migration validation;
7. filesystem interruption and recovery tests;
8. editor command, undo/redo, and autosave recovery tests;
9. benchmark-source and scratch-built asset comparisons;
10. manual Qt smoke checks on the T1700;
11. downstream import and round-trip checks for every export adapter.

No milestone becomes `VERIFIED` solely because code was committed or merged.

## 21. Immediate build sequence

The next permitted engineering order is:

1. merge this editor-first roadmap reconciliation;
2. define the native shape-document and editor-command contracts;
3. build the minimum blank-document Editor shell;
4. prove save, reopen, undo/redo, autosave, and interrupted-write recovery;
5. add manual primitives and path/node editing;
6. add source-region selection and manual trace;
7. add bounded algorithmic extraction candidates;
8. implement Shape Library approval/versioning for manual and source-derived shapes;
9. implement and verify SVG and PNG export profiles;
10. complete Level One release acceptance;
11. begin reversible 2D-to-3D component generation;
12. build Construct assembly and Level Two export profiles.

Product Levels Three and Four remain deferred throughout this sequence. They require a
separate future founder decision and a new source-of-truth revision.

Every PR should advance one coherent gate, preserve verified behaviour, update the
progress ledger, and avoid unrelated UI promises.

## 22. Distribution, access, and support

MXZTAR Forge is a MXZTAR Projects build from `https://www.mxztar.co.nz`.

Official software use is free of charge. There is no timed trial, subscription, or
feature paywall in the confirmed product model. Users may voluntarily support the
founder at `https://buymeacoffee.com/mxztar`.

The public repository supports developer collaboration and forks. Ordinary users are
directed to versioned official releases so installation, schemas, model compatibility,
and migrations remain synchronized.

Before the first public release, the repository must contain a recognised `LICENSE`
selected by the founder and consistent contributor terms. Until then, documentation must
not invent legal permissions beyond the confirmed free-of-charge access policy.

## 23. Future horizon authority

The separately governed future documents preserve long-term ideas without changing the
active build:

- `FUTURE_CONSTRUCT_AND_WORLD_VISION.md`;
- `LEVEL_FOUR_PLATFORM_PRIORITIES.md`.

The active maturity horizon is:

- Level One: editor-first reusable 2D shape creation and portable assets;
- Level Two: reversible 3D component construction, assembly, and portable blockouts;
- Level Three: **DEFERRED**;
- Level Four: **DEFERRED**.

No date is assigned to Level Three or Level Four by this plan.
