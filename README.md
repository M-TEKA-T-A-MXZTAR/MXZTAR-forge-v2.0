# MXZTAR Forge v2.0

MXZTAR Forge v2.0 is a local-first, human-governed creative
concept-engineering forge from [MXZTAR Projects](https://www.mxztar.co.nz).

It helps concept artists, indie game and environment artists, Blender and 3D
blockout creators, small film/animation teams, modular-design builders, and makers
turn visual source material into structured, inspectable, reusable production
intelligence.

Forge closes the gap between an image and productive downstream work:

```text
source image
→ safe local analysis
→ observed evidence and explicit uncertainty
→ human-reviewed shapes, layers, components, and modular grammar
→ reusable Shape Library assets
→ durable Forge Pack
→ Blender, 2D, game-engine, CAD, print, and later 3D handoffs
```

Forge is not merely an image captioner, automatic art generator, or magic one-click
2D-to-production-3D converter. It preserves source authority, distinguishes evidence
from inference, keeps the user in control, and prepares work for specialist tools.

## Level One MVP

The first operational release is complete when a user can:

1. create or open a local project;
2. describe their role, intent, target program, units, and required output;
3. add source images through the Desktop Input folder;
4. browse every supported source through bounded thumbnails;
5. run one compatible local vision workflow without freezing the UI;
6. receive schema-valid structured findings or a truthful diagnostic;
7. inspect observations, inference, confidence, and unknowns;
8. correct, reject, approve, and supersede findings;
9. save approved shapes into the Shape Library;
10. inspect durable Jobs records and outputs;
11. export a Forge Pack containing readable JSON, Markdown, PNG, and SVG assets;
12. reopen the project and recover its state.

Level One does not promise production-ready meshes, engineering-grade dimensions,
manufacturing safety, finished CAD solids, automatic rigging, or perfect AI
interpretation.

## What Forge creates

A Forge Pack is a versioned local project package containing:

- source identity, hashes, origin, and rights notes;
- user and project intent;
- structured design brief;
- observed and inferred findings;
- confidence, uncertainty, and missing evidence;
- annotated source images;
- approved masks, silhouettes, and vector shapes;
- component hierarchy, layer/depth information, and modular relationships;
- construction and blockout guidance;
- job, model, validation, approval, and provenance records;
- target-specific exports.

The canonical package remains readable outside Forge. There is no single universal 3D
format, so Forge uses target profiles. JSON, Markdown, PNG, and SVG form the initial
Level One package. GLB is planned as the first general 3D blockout adapter; DXF, 3MF,
STEP, and OpenUSD follow only when their geometry and validation contracts are honest.

## Automation with control

Forge is designed to automate repetitive workflows while keeping authority with the
user. Guided Automatic is the intended default: Forge runs visible stages, reports its
assumptions, and pauses at approval gates.

Heavy operations must provide elapsed time, heartbeat, truthful status, a defined
cancellation boundary, saved outputs, and useful failure information. No AI runs on
the Qt main thread. No model downloads silently. One heavy local job runs at a time by
default.

## Future construction direction

Approved Shape Library assets will later support reversible 2D-to-3D operations such
as extrude, bevel, revolve, sweep, loft, relief, shell, and AI-assisted morph. A later
Modular Construct workspace will allow users to position components on three axes,
snap and align them, create instances and arrays, and deliberately group, assemble,
join, boolean, separate, or export them.

These capabilities are architected in the data model now but are outside the Level One
MVP implementation boundary.

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

This installs or refreshes the MXZTAR Forge application-menu and Desktop launchers,
uses the repository star icon, and creates the Desktop Input link. Existing launcher
files are backed up before replacement.

## Access, releases, and support

MXZTAR Forge software use is free of charge. There is no confirmed timed trial,
subscription, or feature paywall. Users who find it valuable may voluntarily support
the founder at [buymeacoffee.com/mxztar](https://buymeacoffee.com/mxztar).

Developers may collaborate through the public GitHub repository. Ordinary users will
be directed to versioned official releases so application code, schemas, compatible
models, and migrations remain synchronized.

A formal recognised open-source `LICENSE` and contributor policy must be selected by
the founder before the first public release. Free-of-charge access does not by itself
define permission to modify or redistribute the source code.

## Product authority

- [Master build plan](docs/product/MASTER_BUILD_PLAN.md)
- [Future Construct and World vision](docs/product/FUTURE_CONSTRUCT_AND_WORLD_VISION.md)
- [Progress ledger](docs/PROGRESS_LEDGER.md)
- [Output artifact contracts](docs/product/OUTPUT_ARTIFACT_CONTRACTS.md)
- [Level Four platform priorities](docs/product/LEVEL_FOUR_PLATFORM_PRIORITIES.md)
- [Workflow compatibility matrix](docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md)
- [Project state and data authority](docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md)
- [Source-of-truth policy](docs/SOURCE_OF_TRUTH.md)

Git history is the leading project source of truth. Local project files are the user's
working authority. VX12 backups are dated safety copies. Terminal scrollback is not
project truth.
