# MXZTAR Forge v2.0

MXZTAR Forge v2.0 is a local-first, human-governed creative asset editor and
concept-engineering forge from [MXZTAR Projects](https://www.mxztar.co.nz).

The **Forge Editor** is the product centre. It helps concept, vector, game, environment,
Blender, 3D blockout, maker, and small production teams turn source images or blank
canvases into editable reusable shapes, governed constructions, and portable assets.

The active creator path is:

```text
source image or blank canvas
→ extract a shape candidate or create one from scratch
→ edit paths, nodes, layers, transforms, and construction properties
→ save a reusable Shape Library asset
→ assemble or derive components in a reversible 3D environment
→ export through a validated profile for another workflow or program
```

Forge is not merely an image captioner, automatic art generator, or magic one-click
2D-to-production-3D converter. It preserves source authority, distinguishes evidence
from inference, keeps the user in control, and prepares assets for specialist tools.

AI is optional assistance. Core editing, saving, reopening, and export must remain useful
without an AI model or network connection.

## Active product levels

### Level One — Shape Editor and portable 2D assets

The first operational editor release is complete when a user can:

1. create, open, close, and safely recover a local project;
2. import a supported source image without modifying external bytes, or create a blank
   shape document;
3. browse source art through bounded previews;
4. extract a candidate shape through a manual, algorithmic, or optional AI-assisted path;
5. create shapes from scratch using primitives and path tools;
6. edit nodes, handles, contours, holes, fill, stroke, transforms, layers, groups,
   snapping, symmetry, and explicit 2D boolean results;
7. use undo/redo and durable editor history;
8. correct, reject, approve, version, and supersede shapes;
9. save and reopen editable Shape Library assets;
10. inspect truthful Jobs and diagnostic records;
11. export validated SVG and PNG derivatives plus a durable Forge Pack;
12. reopen the project and continue editing without relying on terminal history.

Level One does not promise production-ready meshes, engineering-grade dimensions,
manufacturing safety, finished CAD solids, automatic rigging, or perfect extraction or
AI interpretation.

### Level Two — 3D Construct and portable blockouts

After Level One is verified, Level Two adds:

- reversible extrude, bevel, revolve, sweep, loft, relief, and shell operations;
- editable 3D components with parent-shape provenance;
- a governed 3D Construct workspace with axes, cameras, units, transforms, snapping,
  anchors, hierarchy, instances, arrays, and undo/redo;
- explicit distinctions between group, assembly, contact, stitch/weld, join mesh,
  boolean, separate, and bake;
- validated GLB/glTF and fallback 3D export profiles.

Level Two remains a planned active product level. It does not claim engineering
certification, finished topology, automatic repair, or universal compatibility.

### Levels Three and Four — deferred

Product Levels Three and Four remain deferred until a separate future founder decision
and source-of-truth revision. No date is assigned.

Future infrastructure, distributed regions, cross-device clients, operator jobs,
collaboration, immersive systems, economy, persistent regions, and world simulation are
vision only and are not current implementation instructions.

## What Forge creates

A Forge project and portable Forge Pack may contain:

- source identity, hashes, origin, and rights notes;
- native editable shape documents;
- source-derived and scratch-built shapes;
- masks, silhouettes, vectors, layers, groups, anchors, and construction guides;
- approved reusable Shape Library records;
- component hierarchy and reversible construction history;
- job, model, validation, approval, and provenance records;
- target-specific exports and limitation reports.

No single industry file is universal. Forge uses named target profiles.

Core Level One outputs are native Forge records, JSON, Markdown, SVG, and PNG. Validated
JPEG, WebP, TIFF, PDF, and DXF profiles may follow after their specific gates pass.

Core Level Two outputs are planned around GLB/glTF and OBJ. STL, 3MF, STEP, FBX, and
OpenUSD remain later format-specific milestones and are not exposed merely because they
are named.

## Source-image compatibility

Accepted source originals currently include PNG, JPEG/JPG, WebP, BMP, TIFF/TIF, and GIF
with first-frame previewing. Originals remain unchanged and authoritative.

PNG, JPEG, and WebP are currently model-ready. BMP, TIFF, and GIF may be imported and
previewed but remain blocked from Ollama until a separately verified normalized model
input preserves provenance.

## Automation with control

Forge supports manual, assisted, guided automatic, and later batch-automatic workflows.
Manual and assisted modes are first-class because the editor must work without AI.

Heavy operations must provide elapsed time, heartbeat, truthful status, a defined
cancellation boundary, saved outputs, and useful failure information. No AI runs on the
Qt main thread. No model downloads silently. One heavy local job runs at a time by
default.

The guided Next control may automate safe navigation and exact-source selection. It must
not silently start a heavy model call, approve a shape, apply an irreversible join,
delete an asset, switch projects, or export.

## Adaptive machine policy

Forge must remain safe on modest CPU-only hardware while adapting conservatively to
better machines.

Default policy:

- `OLLAMA_NUM_THREAD=2` when hardware is unknown or modest;
- `OLLAMA_NUM_PARALLEL=1` by default;
- one heavy local job at a time;
- bounded, rebuildable UI previews;
- no silent long jobs;
- no AI work on the Qt main thread;
- no dead or frozen UI;
- no silent model downloads.

GPU detection may be displayed and used by an explicit future policy, but it must not
silently enable unsafe parallelism or download models.

## Desktop installation

From the repository checkout:

```bash
bash tools/install_desktop_launchers.sh
```

This installs or refreshes the MXZTAR Forge application-menu and Desktop launchers, uses
the repository star icon, and creates the Desktop Input link. Existing launcher files
are backed up before replacement.

## Access, releases, and support

MXZTAR Forge software use is free of charge. There is no confirmed timed trial,
subscription, or feature paywall. Users who find it valuable may voluntarily support
the founder at [buymeacoffee.com/mxztar](https://buymeacoffee.com/mxztar).

Developers may collaborate through the public GitHub repository. Ordinary users will be
directed to versioned official releases so application code, schemas, compatible models,
and migrations remain synchronized.

A formal recognised open-source `LICENSE` and contributor policy must be selected by the
founder before the first public release. Free-of-charge access does not by itself define
permission to modify or redistribute the source code.

## Product authority

- [Master build plan](docs/product/MASTER_BUILD_PLAN.md)
- [Progress ledger](docs/PROGRESS_LEDGER.md)
- [Output artifact contracts](docs/product/OUTPUT_ARTIFACT_CONTRACTS.md)
- [Project state and data authority](docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md)
- [Workflow compatibility matrix](docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md)
- [Future Construct and World vision](docs/product/FUTURE_CONSTRUCT_AND_WORLD_VISION.md)
- [Level Four platform priorities](docs/product/LEVEL_FOUR_PLATFORM_PRIORITIES.md)
- [Source-of-truth policy](docs/SOURCE_OF_TRUTH.md)

Git history is the leading project source of truth. Local project files are the user's
working authority. VX12 backups are dated safety copies. Terminal scrollback is not
project truth.
