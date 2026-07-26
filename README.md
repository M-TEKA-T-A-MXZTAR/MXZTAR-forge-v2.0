# MXZTAR Forge v2.0

**Turn source art and scratch-built shapes into editable 2D documents, project-owned 3D blockouts, reusable components, and verified downstream assets—without surrendering project authority to a cloud pipeline.**

MXZTAR Forge v2.0 is a local-first creative construction workbench from [MXZTAR Projects](https://www.mxztar.co.nz). It is being built for concept artists, vector and graphic artists, game and environment creators, Blender blockout artists, makers, and small teams that need to convert visual ideas into structured, reusable assets.

Forge is not another image captioner and it is not a black-box “make 3D” promise. Its purpose is to close the difficult gap between **an image or idea that contains useful design language** and **an asset that can be edited, reused, assembled, validated, recovered, and handed into another production tool**.

## The workflow gap

Creative source material often contains valuable silhouettes, panels, motifs, paths, surfaces, repeated modules, and structural relationships. Those ideas may be trapped in pixels or sketches while downstream tools expect:

- editable paths, nodes, contours, layers, and transforms;
- scale, units, axes, origins, pivots, hierarchy, and connection points;
- explicit grouping, assembly, stitch, join, boolean, and bake decisions;
- version history, provenance, approval state, and recoverable project files;
- output settings that match the next program rather than a vague “universal” format.

Creators commonly rebuild this missing structure across tracing software, painting tools, AI chats, Blender, CAD programs, game engines, and loosely organised folders. Forge is designed to preserve and compound that structure in one governed project path.

## Intended product path

```text
project purpose
→ source image or blank document
→ trace, extract, or draw editable geometry
→ correct paths, nodes, transforms, and relationships
→ approve a reusable Shape Library asset
→ combine shapes into new designs
→ generate reversible 3D components
→ assemble components into recoverable structures
→ export through a verified downstream profile
```

Forge is not intended to replace Krita, Inkscape, Blender, game engines, CAD systems, or slicers. It preserves the missing creative-production structure between them.

## Current verified development foundation

Forge is an active development project, not yet a finished end-user release.

The merged runtime currently includes:

- Purpose-driven local project creation;
- one-writer project authority and explicit recovery classification;
- fresh project and blank-document creation from Start Here or Editor;
- safe project switching from Start Here and Editor;
- project-contained source intake with unchanged external source bytes;
- bounded previews and accepted image compatibility;
- guarded asynchronous Qt worker lifecycle;
- project-owned job and model-call evidence;
- native versioned shape-document authority;
- Rectangle, Square, Circle, Ellipse, and Star creation;
- durable command replay, Undo, Redo, autosave, canonical save, rollback, and reopen;
- project-owned 3D object scenes linked to native shapes;
- real XYZ position, width, height, depth, three-axis rotation, colour, and opacity;
- CPU-rendered 3D viewport, object selection, drag movement, resize, orbit, and zoom;
- numeric Object Inspector;
- persistent perspective, grid, line, camera, and zoom state;
- paired 2D/3D membership during Undo, Redo, and explicit deletion;
- direct deletion that requires an explicit selection;
- exact restoration of prior project authority after failed switching or fresh-project creation;
- CodeQL Advanced analysis for GitHub Actions and Python;
- deterministic T1700 Source Truth verification.

### Important current limitations

Forge does **not** currently:

- trace editable paths from a 2D source image;
- calculate contour, threshold, mask, or silhouette candidates;
- turn Ollama findings directly into editable geometry;
- provide pen, Bezier, freehand, node, or handle editing;
- display transient smart guides, centre measurements, equal-gap guides, or distance labels;
- provide an approved reusable Shape Library lifecycle;
- insert Shape Library assets into the current document;
- create hierarchy, anchors, connectors, or recoverable assemblies;
- stitch, weld, join meshes, apply 3D booleans, separate, or bake;
- provide revolve, sweep, loft, shell, relief, bevel, vertex, face, or sculpt tools;
- export through verified SVG, PNG, GLB/glTF, or OBJ profiles.

The [Current Capability Boundary](docs/product/CURRENT_CAPABILITY_BOUNDARY.md) records the precise implemented, partial, and planned state.

## Ollama assessment is not shape extraction

The existing optional local-agent path can inspect source art and record findings such as likely shapes, regions, symmetry, repetition, or production recommendations.

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

Ollama may classify, rank, name, or explain candidate geometry. Coordinates, editable paths, user correction, and explicit approval establish project truth.

## Current 2D-to-3D boundary

The five implemented native shapes become real extruded objects in a project-owned `mxztar_forge_object_scene`.

Current object authority includes:

- source-shape membership;
- XYZ position;
- width, height, and depth;
- X/Y/Z rotation;
- colour and opacity;
- reversible object edits;
- camera and viewport state;
- atomic save, rollback, and restart restoration.

This is a real 3D blockout foundation. It is not yet a complete mesh modeller, assembly system, or production-ready CAD release.

## Next direct-manipulation milestone

The next planned runtime gate is transient smart positioning guidance:

- centre and nearest-object alignment lines;
- edge and centre comparisons;
- live X/Y/Z and nearest-distance values;
- equal-gap guidance;
- guides that appear only while moving an object;
- immediate guide removal when movement ends;
- separate `Guides` and `Snap to guides` controls;
- bounded snap tolerance;
- preserved empty-space orbit behaviour;
- CPU-safe calculations for the T1700.

## Finished product boundary

MXZTAR Forge is planned as two complete product stages.

### Stage One — Forge Editor

Stage One delivers the local 2D shape editor and portable 2D asset system:

```text
project purpose
→ source intake or blank shape document
→ manual, algorithmic, or optional AI-assisted candidate
→ path and node editing
→ composition and explicit 2D geometry operations
→ review, approval, versioning, and Shape Library reuse
→ verified SVG, PNG, and Forge Pack output
```

### Stage Two — Construct

Stage Two extends approved shapes and declared primitives into reversible 3D blockouts:

```text
approved 2D shape or declared 3D primitive
→ reversible construction recipe
→ editable 3D component
→ positioned instances, anchors, connectors, and hierarchy
→ recoverable assembly
→ explicit geometry relationship or derived merge
→ verified GLB/glTF and OBJ continuation
```

**Stage One and Stage Two together define the planned finished-product boundary.** Future Product Levels Three and Four remain deferred vision.

## Controlled workflow architecture

Forge distinguishes:

- **Workflow:** a user journey that creates durable project value;
- **Operation:** a reversible or explicitly derived command inside a workflow;
- **Job:** bounded work that may take time and must expose progress, elapsed time, evidence, cancellation boundaries, and truthful terminal state.

The Stage One–Two product contains 18 first-class workflow families: four shared platform workflows, eight Stage One workflows, and six Stage Two workflows.

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

## Access, licence, and support

Use of official MXZTAR Forge software is intended to be free of charge. There is no confirmed timed trial, subscription, or core-feature paywall. Voluntary support may be offered through [Buy Me a Coffee](https://buymeacoffee.com/mxztar), but support status must not control access to local work or core editing features.

This repository is public, but a recognised software `LICENSE` and contributor policy have not yet been selected. Public visibility must not be mistaken for permission to modify or redistribute the software.

## Product authority

- [Master Build Plan](docs/product/MASTER_BUILD_PLAN.md) — product boundary, architecture, acceptance, and engineering sequence
- [Workflow Compatibility Matrix](docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md) — readiness, inputs, outputs, blocking, and next-action rules
- [Progress Ledger](docs/PROGRESS_LEDGER.md) — dated verified, merged, partial, planned, blocked, and deferred state
- [Current Capability Boundary](docs/product/CURRENT_CAPABILITY_BOUNDARY.md) — concise present-tense capability audit
- [Project State and Data Authority](docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md) — durable project truth and recovery hierarchy
- [Output Artifact Contracts](docs/product/OUTPUT_ARTIFACT_CONTRACTS.md) — durable workflow and export records
- [Source-of-Truth Policy](docs/SOURCE_OF_TRUTH.md) — repository and documentation authority

Git history is the leading software-project source of truth. Validated project files are the authority for a user’s creative work. Terminal scrollback is not project truth.
