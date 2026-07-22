# MXZTAR Forge v2.0

**Turn source art into editable 2D shapes, reusable components, and reversible 3D blockouts—without surrendering your files or creative decisions to a cloud pipeline.**

MXZTAR Forge v2.0 is a local-first creative construction workbench from [MXZTAR Projects](https://www.mxztar.co.nz). It is being built for concept artists, vector and graphic artists, game and environment creators, Blender blockout artists, makers, and small production teams that need to convert visual ideas into structured, reusable assets.

Forge is not another image captioner and it is not a black-box “make 3D” promise. Its purpose is to close the difficult gap between **an image that contains useful design language** and **an asset that can be edited, reused, assembled, validated, and handed into another production tool**.

## The workflow gap

Creative source material often contains valuable silhouettes, panels, motifs, paths, surfaces, repeated modules, and structural relationships. The difficulty is that those ideas are trapped in pixels or sketches while downstream tools expect something more disciplined:

- editable paths, nodes, contours, layers, and transforms;
- scale, units, axes, origins, pivots, hierarchy, and connection points;
- explicit decisions about grouping, joining, boolean operations, and baking;
- version history, provenance, approval state, and recoverable project files;
- export settings that match the next program rather than a vague “universal” format.

Creators commonly rebuild this missing structure across tracing software, painting tools, AI chats, Blender, CAD programs, game engines, and loosely organised folders. That costs time, breaks continuity, and makes good source art harder to compound into a reusable asset system.

## What Forge changes

Forge provides one governed project path:

```text
source image or blank canvas
→ trace, extract, or draw an editable shape
→ correct paths, nodes, layers, transforms, and relationships
→ approve a reusable Shape Library asset
→ combine shapes into new 2D designs
→ generate reversible 3D components
→ assemble components into recoverable structures
→ export through a verified downstream profile
```

The intended value is not that Forge replaces Krita, Inkscape, Blender, game engines, CAD systems, or slicers. The value is that Forge preserves the missing **creative-production structure between them**.

### Practical value to a creator

- **Recover useful structure from source art.** Trace manually, generate bounded extraction candidates, or request optional AI proposals without confusing proposals with approved truth.
- **Create from scratch.** Build shapes with primitives and path tools even when no source image or AI model is available.
- **Compound assets instead of rebuilding them.** Save corrected shapes as versioned Shape Library assets and reuse them in later projects.
- **Keep transformations reversible.** Preserve command history, parent relationships, construction recipes, undo/redo, autosave, and recovery state.
- **Make assembly decisions explicit.** Distinguish group, contact, stitch, join, boolean, separate, and bake instead of hiding different operations behind one button.
- **Prepare reliable handoffs.** Export through named profiles with units, axes, hierarchy, provenance, validation evidence, and declared limitations.
- **Retain local ownership.** Keep source art and authoritative project records locally accessible and inspectable.
- **Remain useful on modest hardware.** Manual workflows are first-class; AI is optional; heavy work is bounded and kept away from the Qt main thread.

## Who Forge is for

Forge is designed for:

- concept and visual-development artists;
- vector, graphic, pattern, and shape-system creators;
- indie game, prop, environment, and world-building artists;
- Blender generalists and 3D blockout artists;
- makers and 3D-print designers working at concept or blockout stage;
- small film, animation, fabrication, and design teams without a dedicated technical-art pipeline;
- creators who want reusable assets without making cloud services or expensive hardware the authority over their work.

## The finished product boundary

MXZTAR Forge is planned as two complete product stages.

### Stage One — Forge Editor

Stage One delivers the local 2D shape editor and portable 2D asset system:

```text
project purpose
→ source intake or blank shape document
→ manual, algorithmic, or optional AI-assisted shape candidate
→ path and node editing
→ composition and explicit 2D geometry operations
→ review, approval, versioning, and Shape Library reuse
→ verified SVG, PNG, and Forge Pack output
```

A complete Stage One user can create or extract shapes, correct them manually, combine them into new editable designs, save reusable assets, recover work after interruption, and continue through a validated downstream 2D workflow.

### Stage Two — Construct

Stage Two extends approved shapes and declared primitives into reversible 3D blockouts:

```text
approved 2D shape or 3D primitive
→ declared extrude, revolve, sweep, loft, shell, relief, or bevel recipe
→ editable 3D component
→ positioned instances, anchors, connectors, and hierarchy
→ recoverable assembly
→ explicit geometry relationship or derived merge
→ verified GLB/glTF and OBJ continuation
```

**Stage Two is the planned finished-product boundary.** Future Product Levels Three and Four remain deferred vision and are not current implementation instructions.

## Controlled workflow architecture

Forge uses three different concepts so the product does not become an unstructured collection of buttons:

- **Workflow:** a user journey that creates durable project value.
- **Operation:** a reversible command inside a workflow.
- **Job:** bounded work that may take time and must expose progress, elapsed time, cancellation, evidence, and truthful failure state.

The Stage One–Two product is organised into **18 first-class workflow families**:

- 4 shared platform workflows;
- 8 Stage One workflows;
- 6 Stage Two workflows.

The detailed taxonomy, artifact map, code-impact model, acceptance boundaries, and build sequence are defined in the [Master Build Plan](docs/product/MASTER_BUILD_PLAN.md) and [Workflow Compatibility Matrix](docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md).

## Current development state

Forge is an active development project, not yet a finished end-user release.

### Verified or merged foundation

- local project manifests and self-contained project directories;
- one-writer project locking and explicit recovery classification;
- project-contained source intake with unchanged external source bytes;
- bounded source previews and broadened image compatibility;
- guarded asynchronous Qt worker lifecycle;
- project-owned job and model-call evidence;
- My Library, Shape Library evidence, Jobs, and guided navigation foundations;
- native versioned shape-document schema;
- minimum Editor canvas, blank-document creation, rectangle command, undo/redo, autosave, save, reopen, rollback, and recovery contracts;
- corrected official launcher import order.

### Still required for Stage One

- purpose-driven Project Birth workflow and clearer Start Here authority layout;
- full selection, transform, path, node, layer, group, snapping, array, and 2D boolean tools;
- source-region selection, manual tracing, and editable extraction candidates;
- approval, rejection, versioning, supersession, and editable Shape Library authority;
- verified SVG, PNG, and Forge Pack export profiles;
- release installation, migration, backup, recovery, licence, and documentation gates.

### Planned after verified Stage One

- reversible construction recipes;
- Construct 3D viewport and component editing;
- anchors, connectors, hierarchy, instances, and assemblies;
- explicit stitch, join, boolean, separate, and bake workflows;
- verified GLB/glTF and OBJ downstream continuation.

No capability is considered verified merely because code was committed or merged. Deterministic contracts, T1700 live checks, recovery tests, and downstream import evidence are required at the appropriate gate.

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

Accepted source originals currently include:

- PNG;
- JPEG/JPG;
- WebP;
- BMP;
- TIFF/TIF;
- GIF, using the first frame for preview generation.

Originals remain unchanged and authoritative. PNG, JPEG, and WebP are currently model-ready. BMP, TIFF, and GIF may be imported and previewed but remain blocked from local vision-model execution until a separately verified normalized derivative preserves provenance.

## Automation without hidden authority

Forge supports four automation levels:

| Mode | Behaviour |
|---|---|
| Manual | Tools execute only direct user commands |
| Assisted | Forge proposes an action and waits for approval |
| Guided Automatic | Forge runs a visible reversible sequence and pauses at gates |
| Batch Automatic | Forge applies user-approved rules and reports exceptions |

Guidance may navigate, select an exact source, or suggest the next safe action. It must not silently start a heavy model call, approve a shape, apply an irreversible merge, delete an asset, switch projects, or export.

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

The repository is currently intended for controlled development and verification.

Launch from an existing configured checkout:

```bash
./run_mxztar_forge.sh
```

Install or refresh the Desktop and application-menu launchers:

```bash
bash tools/install_desktop_launchers.sh
```

Ordinary users will be directed to versioned official releases when the Stage One release gates are complete.

## Access, licence, and support

Use of the official MXZTAR Forge software is intended to be free of charge. There is no confirmed timed trial, subscription, or core-feature paywall. Voluntary support may be offered through [Buy Me a Coffee](https://buymeacoffee.com/mxztar), but support status must not control access to local work or core editing features.

This repository is public, but a recognised software `LICENSE` and contributor policy have not yet been selected. Until that release gate is complete, public visibility must not be mistaken for permission to modify or redistribute the software.

## Product authority

- [Master Build Plan](docs/product/MASTER_BUILD_PLAN.md) — product boundary, workflows, architecture, acceptance, and build sequence
- [Workflow Compatibility Matrix](docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md) — readiness, inputs, outputs, failure, and next-action rules
- [Progress Ledger](docs/PROGRESS_LEDGER.md) — current verified, merged, partial, planned, blocked, and deferred state
- [Project State and Data Authority](docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md) — durable project truth and recovery hierarchy
- [Output Artifact Contracts](docs/product/OUTPUT_ARTIFACT_CONTRACTS.md) — durable workflow and export records
- [Source-of-Truth Policy](docs/SOURCE_OF_TRUTH.md) — repository and documentation authority
- [Future Construct and World Vision](docs/product/FUTURE_CONSTRUCT_AND_WORLD_VISION.md) — deferred vision only
- [Level Four Platform Priorities](docs/product/LEVEL_FOUR_PLATFORM_PRIORITIES.md) — deferred vision only

Git history is the leading software-project source of truth. The user’s validated project files are the authority for their creative work. Terminal scrollback is not project truth.
