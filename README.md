# MXZTAR Forge v2.0

**Turn source art and scratch-built shapes into editable 2D documents, project-owned 3D blockouts, reusable components and verified downstream assets—without surrendering project authority to a cloud pipeline.**

MXZTAR Forge v2.0 is a local-first creative-construction workbench from [MXZTAR Projects](https://www.mxztar.co.nz). It is being built for concept artists, vector and graphic artists, game and environment creators, Blender blockout artists, makers and small teams that need to convert visual ideas into structured, reusable assets.

Forge is not another image captioner and it is not a black-box “make 3D” promise. Its purpose is to close the gap between **an image or idea containing useful design language** and **an asset that can be edited, reused, assembled, validated, recovered and handed into another production tool**.

Forge is an active development project, not yet a finished end-user release.

## Product value path

```text
project purpose
→ source image or blank document
→ trace, extract or draw editable geometry
→ correct paths, nodes, transforms and relationships
→ approve a reusable Shape Library asset
→ combine shapes into new 2D designs
→ generate reversible 3D components
→ assemble components into recoverable structures
→ export through a verified downstream profile
```

Forge is not intended to replace Krita, Inkscape, Blender, game engines, CAD systems or slicers. It preserves the missing creative-production structure between them.

## Current merged foundation

The merged runtime through PR #80 currently includes:

- Purpose-driven local project creation;
- one-writer project authority and explicit recovery classification;
- fresh project and blank-document creation from Start Here or Editor;
- safe project switching and recoverable Project Trash;
- project-contained source intake with bounded previews;
- guarded asynchronous Qt worker lifecycle;
- project-owned job and model-call evidence;
- native versioned shape-document authority;
- Rectangle, Square, Circle, Ellipse and Star creation;
- direct 2D selection, movement and durable resizing;
- explicit deletion, Undo, Redo, autosave, canonical save, rollback and reopen;
- project-owned 3D object scenes linked to native shapes;
- direct 3D object selection, movement, resize and numeric editing;
- stable front orthographic Design View as the editing default;
- deliberate orbit, perspective and zoom viewing controls;
- transient positioning guides and bounded optional snapping;
- compact continuously visible Editor command controls;
- persistent camera, grid, line, perspective and zoom state;
- paired 2D/3D membership through supported commands;
- CodeQL Advanced analysis for GitHub Actions and Python.

The precise evidence boundary, limitations and next gate are maintained in the [Current Capability Boundary](docs/product/CURRENT_CAPABILITY_BOUNDARY.md).

## Important current limitations

Forge does **not** currently provide a complete source-image-to-reusable-asset or approved-shape-to-recoverable-assembly journey.

Not implemented:

- manual tracing into editable paths;
- pen, Bezier, freehand, node or handle editing;
- deterministic contour, threshold, edge, mask or silhouette candidates;
- authoritative AI-generated geometry;
- full layers, groups, mirrors, arrays, alignment and 2D booleans;
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

No absent capability should appear as a functioning control or public claim.

## Ollama assessment is not shape extraction

The optional local-agent path can inspect source art and record likely shapes, regions, symmetry, repetition or production recommendations.

Current path:

```text
2D source image
→ bounded preview
→ optional Ollama assessment
→ raw evidence or planning record
→ no editable traced geometry
```

Required future path:

```text
exact source region
→ manual trace or deterministic contour proposal
→ editable candidate geometry
→ user correction
→ review and approval
→ optional Shape Library reuse
```

Ollama may classify, rank, name or explain candidate geometry. Coordinates, editable paths, user correction and explicit approval establish project truth.

## Current 2D-to-3D authority

The five implemented native shapes become real extruded objects in a project-owned `mxztar_forge_object_scene`.

Current object authority includes:

- source-shape membership;
- XYZ position;
- width, height and depth;
- X/Y/Z rotation;
- colour and opacity;
- reversible object edits;
- camera and viewport state;
- atomic save, rollback and restart restoration.

This is a meaningful 3D blockout foundation. It is not yet a complete mesh modeller, assembly system or production-ready CAD release.

## Current engineering gate

Before broad new feature work, Forge is completing a recovery and consolidation gate:

1. reconcile governing documents and remove frozen verifier assumptions;
2. map the official launcher, final Editor composition and state owners;
3. convert PR #66–#80 lessons into final-runtime regression contracts;
4. verify real event delivery, pointer lock, persistence and recovery;
5. complete applicable T1700 live interaction acceptance;
6. begin the Stage One editable-path and manual-trace foundation only after the baseline is stable.

The [Recovery and Completion Plan](docs/product/RECOVERY_AND_COMPLETION_PLAN.md) controls this sequence. The [Regression and Drift Register](docs/REGRESSION_AND_DRIFT_REGISTER.md) preserves causal learning.

## Finished product boundary

### Stage One — Forge Editor

Stage One delivers the local 2D shape editor and portable 2D asset system:

```text
project purpose
→ source intake or blank shape document
→ manual, algorithmic or optional AI-assisted candidate
→ path and node editing
→ composition and explicit 2D geometry operations
→ review, approval, versioning and Shape Library reuse
→ verified SVG, PNG and Forge Pack output
```

### Stage Two — Construct

Stage Two extends approved shapes and declared primitives into reversible 3D blockouts:

```text
approved 2D shape or declared 3D primitive
→ reversible construction recipe
→ editable 3D component
→ positioned instances, anchors, connectors and hierarchy
→ recoverable assembly
→ explicit geometry relationship or derived merge
→ verified GLB/glTF and OBJ continuation
```

**Stage One and Stage Two together define the planned finished-product boundary.** Future Product Levels Three and Four remain deferred.

## Local-first and human-governed

Forge separates:

- unchanged source evidence;
- algorithmic calculation;
- model inference;
- user-created geometry;
- reviewed and approved project truth;
- exported derivatives.

A successful job does not imply approval. A saved diagnostic does not imply workflow success. An AI proposal does not become reusable geometry until the creator reviews and accepts it.

Durable project files are authoritative. SQLite may index them, but it must not become the only place where creative work exists.

## Source-image compatibility

Accepted source originals currently include PNG, JPEG/JPG, WebP, BMP, TIFF/TIF and GIF using the first frame for preview generation.

Originals remain unchanged and authoritative. PNG, JPEG and WebP are currently model-ready. BMP, TIFF and GIF may be imported and previewed but remain blocked from local vision-model execution until a separately verified normalized derivative preserves provenance.

## Modest-hardware policy

Safe defaults remain available for CPU-only systems:

- `OLLAMA_NUM_THREAD=2` when hardware is unknown or modest;
- `OLLAMA_NUM_PARALLEL=1` by default;
- one heavy local job at a time;
- bounded and rebuildable previews;
- no AI work on the Qt main thread;
- no silent model downloads;
- no hidden parallelism or unexplained long-running process.

## Development checkout

Launch from an existing configured checkout:

```bash
./run_mxztar_forge.sh
```

Install or refresh the Desktop and application-menu launchers:

```bash
bash tools/install_desktop_launchers.sh
```

Ordinary users will be directed to versioned official releases after the relevant release gates are complete.

## Access, licence and support

Use of official MXZTAR Forge software is intended to be free of charge. There is no confirmed timed trial, subscription or core-feature paywall. Voluntary support may be offered through [Buy Me a Coffee](https://buymeacoffee.com/mxztar), but support status must not control access to local work or core editing features.

This repository is public, but a recognised software `LICENSE` and contributor policy have not yet been selected. Public visibility must not be mistaken for permission to modify or redistribute the software.

## Product authority

- [Master Build Plan](docs/product/MASTER_BUILD_PLAN.md) — finished Stage One–Two product boundary
- [Recovery and Completion Plan](docs/product/RECOVERY_AND_COMPLETION_PLAN.md) — active consolidation and engineering sequence
- [Current Capability Boundary](docs/product/CURRENT_CAPABILITY_BOUNDARY.md) — concise present-tense capability audit
- [Progress Ledger](docs/PROGRESS_LEDGER.md) — dated implementation and verification chronology
- [Regression and Drift Register](docs/REGRESSION_AND_DRIFT_REGISTER.md) — causal learning and recurrence prevention
- [Workflow Compatibility Matrix](docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md) — readiness, inputs, outputs, blocking and next-action rules
- [Project State and Data Authority](docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md) — durable project truth and recovery hierarchy
- [Output Artifact Contracts](docs/product/OUTPUT_ARTIFACT_CONTRACTS.md) — durable workflow and export records
- [Source-of-Truth Policy](docs/SOURCE_OF_TRUTH.md) — repository and documentation authority

Git history is the leading software-project source of truth. Validated project files are the authority for a user’s creative work. Terminal scrollback is not project truth.
