# MXZTAR Forge v2.0

**Turn source art and scratch-built shapes into editable 2D documents, project-owned 3D blockouts, reusable components, and verified downstream assets—without surrendering project authority to a cloud pipeline.**

MXZTAR Forge v2.0 is a local-first, human-governed creative concept-engineering forge from [MXZTAR Projects](https://www.mxztar.co.nz).

It is being built for concept artists, vector and graphic artists, pattern and shape-system creators, indie game and environment creators, Blender blockout artists, makers, and small teams that need structured reusable assets without making expensive hardware or cloud services the authority over their work.

Forge is an active development project, not yet a finished end-user release.

## The workflow gap

Creative source material often contains useful silhouettes, motifs, paths, panels, repeated modules, and structural relationships. Those ideas may be trapped in pixels while downstream tools expect:

- editable paths, nodes, contours, layers, and transforms;
- units, axes, origins, pivots, hierarchy, and connection points;
- explicit grouping, assembly, stitch, join, boolean, and bake decisions;
- provenance, approval, version history, and recoverable project files;
- output settings proven for the next program.

Creators commonly rebuild this missing structure across tracing tools, painting software, AI chats, Blender, CAD applications, game engines, and loosely organised folders.

Forge is designed to preserve and compound that structure in one governed project path.

## Intended product path

```text
Purpose
→ project
→ source image, starter asset, or blank document
→ editable geometry
→ correction and review
→ reusable 2D asset
→ reversible 3D component
→ recoverable construction
→ verified downstream handoff
```

Forge does not pretend to replace Krita, Inkscape, Blender, CAD systems, game engines, slicers, or other specialist tools. It prepares useful governed handoffs between them.

## Current development foundation

The repository baseline assessed through merged PR #80 includes:

- Purpose-driven local project creation;
- one-writer project authority and read-only recovery classification;
- project open, close, switch, rename, and recoverable Project Trash foundations;
- project-contained source intake with unchanged external source bytes;
- bounded source previews and guarded Qt worker lifecycle;
- read-only Jobs and Shape Library evidence browsers;
- optional local Ollama assessment saved as project evidence;
- native project-owned shape documents;
- Rectangle, Square, Circle, Ellipse, and Star creation;
- durable command replay, Undo, Redo, autosave, canonical save, rollback, and reopen;
- direct 2D movement with click-offset preservation;
- direct durable 2D resize with proportional Square and Circle behaviour;
- project-owned 3D object scenes linked to native shapes;
- paired 2D/3D position and planar-size synchronization;
- direct 3D movement and resize;
- explicit Select, Move, Rotate, Resize, and Orbit View modes;
- front orthographic 3D Design View on entry, with deliberate Perspective and Orbit controls;
- stable camera and world landmarks during object manipulation;
- positioning guides, measurements, optional snapping, and separated wheel-routing modes;
- Save Project transaction, project/document controls, and CodeQL Advanced repository checks.

Individual features carry focused verification. A fresh consolidated T1700 live acceptance of the complete official runtime remains the next pre-feature gate.

The precise status is maintained in the [Current Capability Boundary](docs/product/CURRENT_CAPABILITY_BOUNDARY.md).

## Important current limitations

Forge does **not** currently provide:

- freeform paths, Bezier nodes, or handle editing;
- exact source-region manual tracing;
- deterministic contour, threshold, edge, mask, line, or silhouette candidates;
- AI-generated authoritative editable geometry;
- approved reusable Shape Library assets or reversible library insertion;
- complete layers, groups, arrays, mirrors, or 2D boolean composition;
- a general shape-to-component recipe registry;
- persistent areas, surfaces, anchors, sockets, groups, or assemblies;
- reversible effect stacks;
- stitch/weld, join mesh, 3D booleans, separate, or bake;
- advanced revolve, sweep, loft, shell, relief, bevel, or mesh editing;
- verified SVG, PNG, GLB/glTF, or OBJ continuation profiles;
- engineering-grade, watertight, printable, or manufacturing-safe output claims.

## Ollama assessment is not shape extraction

The optional local-agent path can inspect project-owned source art and record findings such as likely regions, shapes, symmetry, repetition, or production recommendations.

Current boundary:

```text
project-owned source
→ optional local-model assessment
→ raw project evidence or proposal
→ no authoritative editable geometry
```

Required future geometry boundary:

```text
exact source region
→ manual trace or deterministic candidate
→ editable coordinates and path identity
→ user correction
→ review and approval
```

A model may classify, explain, rank, or suggest. It does not silently become project truth.

## Current 2D-to-3D boundary

The five implemented native shapes become linked extruded objects inside a project-owned `mxztar_forge_object_scene`.

Current object authority includes:

- source-shape membership;
- XYZ position;
- width, height, and depth;
- X/Y/Z rotation;
- colour and opacity;
- reversible edits;
- camera and viewport state;
- atomic save, rollback, and restart restoration.

This is a real creative blockout foundation. It is not automatic production reconstruction or a complete Construct system.

## Finished product boundary

### Stage One — Forge Editor and portable 2D assets

```text
project and source authority
→ blank or source-derived editable geometry
→ path and composition editing
→ deterministic or optional AI-assisted candidates
→ review, approval, versioning, and reusable Shape Library assets
→ verified 2D continuation
```

### Stage Two — Construct and portable 3D blockouts

```text
approved shape or declared primitive
→ reversible component recipe
→ editable component
→ pivots, anchors, surfaces, groups, and recoverable assemblies
→ explicit geometry relationships and derived operations
→ verified 3D continuation
```

**Stage One and Stage Two together define MXZTAR Forge v2.0.** Product Levels Three and Four remain deferred vision.

## Current engineering order

The current programme is:

```text
Recoup accepted decisions and working behaviour
→ Regroup authority, runtime composition, and verification
→ Prove the complete PR #80 Editor baseline
→ Proceed to Freeform Path Authority
```

The ordered gates and exclusions are maintained in the [Active Engineering Plan](docs/product/ACTIVE_ENGINEERING_PLAN.md).

## Governance and engineering authority

- [Source of Truth](docs/SOURCE_OF_TRUTH.md)
- [Master Build Plan](docs/product/MASTER_BUILD_PLAN.md)
- [Current Capability Boundary](docs/product/CURRENT_CAPABILITY_BOUNDARY.md)
- [Active Engineering Plan](docs/product/ACTIVE_ENGINEERING_PLAN.md)
- [Progress Ledger](docs/PROGRESS_LEDGER.md)
- [Final Runtime Composition](docs/architecture/FINAL_RUNTIME_COMPOSITION.md)
- [Regression and Drift Prevention](docs/architecture/REGRESSION_AND_DRIFT_PREVENTION.md)
- [Agent Operating Rules](AGENTS.md)

Historical correction and future-vision documents preserve evidence and product lore. They are not current engineering instructions unless the Source of Truth explicitly promotes them.

## Local-first and modest-hardware policy

- project truth stays in durable local files;
- originals remain unchanged;
- long work stays outside the Qt main thread;
- one heavy local job at a time by default;
- previews and collections remain bounded;
- no silent model download or hidden parallel escalation;
- success, failure, invalid evidence, timeout, and failure-before-save remain distinct;
- core creation and editing must remain useful without AI or network access.

## Launch and verification

Use the repository launcher from the canonical checkout:

```bash
./run_mxztar_forge.sh
```

Run the complete repository verification suite with:

```bash
bash scripts/verify_source_truth.sh
```

Interaction-heavy changes also require focused final-runtime verification and recorded T1700 live acceptance before they become accepted product baseline.

## Access, licence, and claims

Official access remains free of charge and founder support is voluntary.

A recognised open-source licence must not be claimed until a repository `LICENSE` is deliberately selected and added.

Forge does not claim engineering certification, manufacturing safety, universal interoperability, or finished-release status before the corresponding evidence exists.