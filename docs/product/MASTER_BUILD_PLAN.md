# MXZTAR Forge v2.0 — Master Build Plan

## 1. Product goal

MXZTAR Forge v2.0 is a local-first, human-governed creative concept-engineering forge.

It turns visual source material into reviewed design intelligence, reusable shapes,
editable construction instructions, and specialist-tool handoffs. It closes the gap
between “a model can describe this picture” and “a creator can continue productive
work from this result.”

Long-term value path:

```text
source art or generated source
→ source identity, rights context, and user intent
→ observed visual evidence and explicit uncertainty
→ reviewed shapes, layers, components, and modular grammar
→ reusable Shape Library assets and construction recipes
→ editable 2D, 2.5D, and 3D components
→ human-governed modular assembly
→ verified Blender, engine, CAD, print, or media handoff
```

The Level One MVP stops at a smaller, operational promise:

```text
source image
→ safe local analysis
→ structured findings
→ human review and approval
→ reusable shapes
→ durable Forge Pack
```

The MVP does not claim automatic production-ready geometry.

## 2. Asset, owner, user, and value

**Asset:** a durable Forge Pack containing source identity, structured analysis,
approved shapes, construction guidance, job evidence, and portable exports.

**Owner:** the creator controls their local source material, project records,
approvals, derivatives, and exports. MXZTAR controls the Forge application and its
official releases.

**Primary Level One users:**

1. indie game, environment, and prop artists;
2. concept and visual-development artists;
3. Blender generalists and 3D blockout artists;
4. small game, film, animation, and design teams without a technical-art department;
5. makers and 3D-print designers at concept and handoff stage.

**User problem:** image tools produce pictures or captions, while production tools
expect structure, scale, hierarchy, geometry decisions, and file discipline. Creators
currently reconstruct that missing information manually across folders, notes, AI
chats, tracing tools, Blender, CAD, and game engines.

**Forge value:** preserve source authority, recover design grammar, expose inference,
retain corrections, create reusable components, recommend the next valid action, and
package the result for immediate continuation in another tool.

## 3. Product principles

1. **Local first.** Source art and project truth remain local unless the user explicitly
   chooses an external operation.
2. **Human governed.** Automation may propose and execute reversible work; approval,
   destructive change, joining, replacement, and export remain visible user decisions.
3. **Observed is not inferred.** Source evidence, calculation, model inference, user
   intent, speculation, and approved truth are separate states.
4. **No dead or frozen UI.** Heavy work runs outside the Qt main thread with progress,
   heartbeat, elapsed time, cancellation boundaries, and truthful final state.
5. **Modest hardware remains valid.** One heavy local job at a time by default, bounded
   previews, conservative threads, no silent downloads, and no hidden escalation.
6. **Readable durable output.** JSON, Markdown, SVG, PNG, and documented interchange
   files remain inspectable outside Forge.
7. **Every name is a promise.** No button, format, status, or AI claim exists without a
   complete and verified workflow.
8. **Corrections compound value.** User review creates durable project knowledge rather
   than hidden, unreviewed memory.
9. **Specialist tools are partners.** Forge prepares and validates handoffs; it does not
   pretend to replace Krita, Blender, game engines, CAD systems, or slicers.
10. **Free access is not reduced functionality.** Official software use is free of
    charge. Users may voluntarily support the founder at
    `https://buymeacoffee.com/mxztar`.

## 4. Level One MVP acceptance boundary

Level One is complete only when a new user can:

1. install and launch an official release;
2. create or open a local project;
3. provide a reusable user profile and project-specific intent;
4. populate the Desktop Input folder and see every supported source;
5. inspect a bounded preview without modifying the original;
6. select an appropriate workflow through READY, CAUTION, or BLOCKED assessment;
7. run one local vision workflow without freezing the UI;
8. receive schema-valid structured findings or a truthful diagnostic artifact;
9. review observed evidence, inference, confidence, and unknowns;
10. rename, correct, reject, approve, or supersede findings;
11. save approved shapes into the Shape Library;
12. inspect job history, model identity, elapsed time, status, and saved outputs;
13. export a verified Forge Pack;
14. move successfully processed source art to an explicit processed-source location;
15. reopen the project and recover its durable state without relying on terminal history.

Level One does not promise:

- production-ready topology or finished 3D meshes;
- engineering-grade dimensions from an unscaled image;
- watertight or manufacture-safe geometry;
- hidden-surface reconstruction;
- automatic CAD solids, rigging, UVs, LODs, or final materials;
- unattended publishing or sales;
- unlimited parallel jobs;
- perfect AI interpretation;
- a complete CAD or modular 3D editor.

## 5. Start Here and intent model

Onboarding must gather useful intent without confronting every user with one giant
form. Fields are progressive, editable, and separated by authority.

### 5.1 Persistent local user profile

- discipline and role;
- experience level;
- programs used;
- preferred units;
- usual target platforms and asset types;
- preferred output profiles;
- default project and export locations;
- local privacy and network preferences;
- accessibility and learning-mode preferences;
- permission for AI-generated source material;
- automatically detected hardware profile, with visible policy.

### 5.2 Per-project intent

- project name and purpose;
- source origin, ownership assertion, and licence notes;
- target application or workflow;
- intended asset or scene type;
- 2D, 2.5D, blockout, CAD-concept, print-concept, or modular intent;
- required accuracy, scale, and units;
- structural versus decorative priority;
- symmetry, repetition, modularity, material, and style expectations;
- desired outputs and quality/time preference;
- free-form direction.

### 5.3 Conditional intent

- game/VR/AR: engine, platform, scale, polygon target, collision, LOD, interaction;
- film/animation: shot context, camera distance, detail tier, scene role;
- CAD: dimensional authority, tolerance, solid/surface intent, manufacturing context;
- 3D print: process, units, wall constraints, watertightness, slicer target;
- 2D: canvas, colour, layer, vector/raster, and print requirements.

Hidden profiling is prohibited. The user can inspect, correct, export, or remove their
profile and project intent.

## 6. Project authority and Forge Pack export

No single industry file is universal. The canonical internal project layout remains
the authority defined by `docs/product/OUTPUT_ARTIFACT_CONTRACTS.md`, including
`source/originals`, `source/previews`, status-separated `findings`, `structures`,
`briefs`, `prompts`, `diagnostics`, `logs`, `history`, and `exports`. Workflows must not
invent competing internal locations.

A Forge Pack is a deterministic, versioned **export view** assembled from approved
project artifacts. It is portable output, not a second project-state authority. Its
manifest retains the originating project/artifact IDs and hashes so it can be traced
back to project truth.

```text
forge-pack/
├── forge-pack.json
├── source/
│   └── source-reference.json
├── analysis/
│   ├── design-brief.json
│   ├── design-brief.md
│   ├── observations.json
│   ├── uncertainties.json
│   └── annotated-source.png
├── shapes/
│   ├── shape-catalog.json
│   ├── masks/
│   ├── silhouettes/
│   └── vectors/
├── construction/
│   ├── component-hierarchy.json
│   ├── spatial-layers.json
│   └── blockout-plan.md
├── exports/
├── job-evidence/
├── provenance/
└── export-report.json
```

Every material artifact carries an ID, schema version, source relationship, creator
or model, timestamps, status, validation result, approval state, and supersession
history. SQLite may index these files but is never the sole authority.

The initial portable outputs are:

- JSON for machine-readable project intelligence;
- Markdown for human-readable briefs and instructions;
- PNG for masks, previews, and annotated evidence;
- SVG for reviewed silhouettes and vector construction;
- GLB later as the first general 3D blockout adapter;
- OBJ as a simple legacy mesh fallback;
- DXF for later 2D CAD profiles;
- 3MF for later additive-manufacturing handoff;
- STEP only after dimensional and solid-geometry contracts are proven;
- OpenUSD later for complex composed production scenes.

## 7. Structured production intelligence contract

Forge must create more than prose. The structured representation includes:

- source identity and hash;
- visible objects, motifs, surfaces, and regions;
- line and contour evidence;
- component IDs and hierarchy;
- masks, silhouettes, vector candidates, holes, and interior contours;
- layers, depth order, occlusion, and attachment hypotheses;
- symmetry, repetition, module families, and variation rules;
- source-plane coordinates, anchors, centres, and bounds;
- scale, units, perspective, and camera assumptions;
- colour and material observations;
- construction recommendations;
- observed/inferred/user-supplied/approved classification;
- confidence, uncertainty, contradiction, and missing evidence;
- intended downstream profile;
- review, correction, rejection, approval, and supersession records.

## 8. Shape and component lifecycle

A Shape Library entry is not merely a crop. It may contain:

- original source reference;
- mask and vector outline;
- holes, centre, bounds, symmetry axes, and anchors;
- dimensional assumptions and confidence;
- intended role: profile, panel, trim, cutout, volume, path, or decoration;
- approval state and correction history;
- proposed construction methods;
- later derived 3D components and instances.

Lifecycle transitions:

```text
candidate
→ reviewed
  ├→ approved shape
  ├→ correction requested → corrected candidate → reviewed
  └→ rejected

approved shape
  ├→ superseded by a later approved shape
  └→ construction recipe
      → editable 3D component
      → positioned instance
      → group / assembly / joined mesh / boolean result
      → verified export
```

Parent-child provenance must survive every derivative.

## 9. Automation with user control

Forge exposes explicit automation levels:

| Level | Behaviour |
|---|---|
| Manual | Tools execute only direct user commands |
| Assisted | Forge proposes an action and waits for approval |
| Guided Automatic | Forge runs a visible workflow and pauses at approval gates |
| Batch Automatic | Forge applies user-approved rules and reports exceptions |

Guided Automatic is the default.

Every automated run declares inputs, stages, model or algorithm, storage destination,
assumptions, workload state, elapsed time, heartbeat, cancellation boundary, outputs,
failures, and next action. No unapproved rule becomes hidden project truth.

## 10. UI and learning architecture

Forge adopts a mature creative-application layout without copying another product:

```text
File | Edit | View | Project | Source | Analyse | Shapes | Construct | Export | Settings | Help
```

Primary workspaces:

1. Start Here;
2. My Library;
3. Agent Workflows;
4. Review;
5. Shape Library;
6. Jobs;
7. Export;
8. later Modular Construct.

The centre is the active canvas or workspace. Toolbars and resizable panels surround
it. Layout and geometry persist safely.

Every important control has:

- a concise normal tooltip;
- after a three-second hover, an optional Insight explaining what it does, when to use
  it, what changes, whether it is reversible, what it creates, and one example;
- Learning Mode, Tooltips Only, New Features, and Insights Off preferences.

## 11. Future modular 3D construction

This is architected now but excluded from Level One implementation.

The Modular Construct workspace will provide three-axis positioning, orthographic and
perspective views, transform gizmos, units, snapping, numeric transforms, anchors,
hierarchy, locking, visibility, duplication, mirroring, arrays, undo/redo, and
non-destructive construction history.

Approved 2D shapes may later use explicit operations:

- extrude;
- bevel;
- revolve;
- sweep;
- loft;
- relief;
- shell;
- AI-assisted morph with stated assumptions.

One-click Make 3D means “generate a reversible preview using a declared method,” not
“claim a finished object.” Group, assembly, join mesh, boolean union, boolean
difference, separate, and bake remain distinct operations.

Assistance may suggest alignment, mating edges, symmetry, arrays, intersections, and
attachment points. The user approves movement and irreversible changes.

## 12. Text-to-image source generation

Text-to-image is a later input adapter, not an MVP dependency. It requires a separate
generation model; the local vision model does not provide this capability.

Requirements:

- explicit model installation and storage consent;
- no silent model downloads;
- visible prompt, negative prompt, seed where available, settings, model, and date;
- generated/imported provenance distinction;
- source approval before analysis;
- externally generated images remain valid inputs.

## 13. Interoperability profiles

Each adapter declares units, scale, coordinate system, up-axis, origins, pivots,
hierarchy, names, materials, textures, output files, limitations, and validation.

Planned profiles:

- Krita/Inkscape 2D Construction;
- Blender Blockout;
- Unreal Engine Prop or Environment;
- Godot Game Asset;
- Unity Game Asset;
- Generic GLB;
- Generic CAD Profile;
- 3D Printing Concept;
- Generic Forge Pack.

## 14. Implementation roadmap

### Phase 0 — Governance and safe runtime foundation

Status: substantially complete.

- canonical identity and source truth;
- relocatable application and Desktop launchers;
- adaptive modest-hardware policy;
- bounded source previews;
- one guarded QThread AI runner;
- My Library visible-card baseline;
- prompt and worker contracts.

Exit: current merged verifiers pass on the T1700 and documentation no longer claims a
commercial subscription or implemented functionality that does not exist.

### Phase 1 — Restore the operational shell

- restore Jobs with durable truthful records;
- restore Shape Library around the new lifecycle contract;
- establish top menu and workspace navigation without dead controls;
- add Help/Insights foundation;
- retain responsive layout and safe window behaviour.

Exit: users can navigate sources, workflows, jobs, and shapes; every visible control
has its complete handler, engine/helper, input, output, error, feedback, persistence
where required, and verification path. Deferred workspaces and unavailable actions are
documented but are not exposed as placeholder controls.

### Phase 2 — Project authority and lifecycle

- project creation/opening;
- manifest and self-contained directory;
- input, processed-source, shape, job, export, and history authorities;
- atomic writes and IDs;
- one-writer lock;
- SQLite rebuild;
- read-only recovery and reconciliation.

Exit: deleting the derived index loses no project truth; restart restores state.

### Phase 3 — Start Here intent onboarding

- persistent local user profile;
- project intent and conditional target fields;
- profile inspection, correction, export, and deletion;
- target workflow profiles;
- privacy and network disclosure.

Exit: relevant intent enters workflow artifacts without hidden profiling.

### Phase 4 — Compatibility and workflow schemas

- READY/CAUTION/BLOCKED rules;
- shared artifact envelope;
- success and failure schemas;
- model/source preflight;
- validation, migration, approval, rejection, and supersession.

Exit: invalid output cannot be success; blocked jobs cannot launch.

### Phase 5 — Source-art intelligence and review

- structured visible evidence;
- components, motifs, materials, layers, and uncertainty;
- observed/inferred separation;
- annotated-source overlays;
- correction and approval workspace.

Exit: benchmark sources produce useful reviewable findings beyond captions.

### Phase 6 — Shape extraction and Shape Library

- line, contour, region, mask, and silhouette candidates;
- open/closed contours, holes, intersections, endpoints, symmetry, and nesting;
- vector candidates and manual correction;
- approved shape records and reusable naming;
- non-destructive source relationship.

Exit: an approved source-derived shape can be reopened, corrected, traced, and exported
as PNG/SVG with schema-valid metadata.

### Phase 7 — Layers, depth, and modular grammar

- layer and occlusion graph;
- anchors, transforms, perspective, and scale assumptions;
- repetition, module families, connectors, attachment, variation, and hierarchy;
- 2.5D preview and construction plan.

Exit: one project produces a reviewed modular family and inspectable 2.5D plan.

### Phase 8 — Forge Pack and first production adapters

- deterministic package builder;
- JSON, Markdown, annotated PNG, masks, and SVG;
- Blender blockout brief and scene manifest;
- adapter validation and provenance;
- export summary and limitations.

Exit: a fresh downstream session can identify, import, and continue from the package
without filesystem archaeology.

### Phase 9 — Level One release engineering

- clean install, update, rollback, and removal;
- versioned GitHub releases and checksums;
- model compatibility declaration;
- release notes, limitations, migration, backup, and recovery;
- website download path;
- voluntary support link;
- formal software licence and contributor policy.

Exit: a new user can install, complete the acceptance journey, retain local work, and
recover from a failed update on supported hardware.

### Phase 10 — 2D-to-3D component generation

- construction recipe schema;
- extrude, revolve, sweep, loft, shell, relief, bevel, and morph proposals;
- editable preview and parameter controls;
- derived-component provenance;
- GLB blockout validation.

Exit: an approved 2D shape generates a reversible, editable, explicitly limited 3D
component that round-trips through the target profile.

### Phase 11 — Modular Construct workspace

- three-axis scene and camera views;
- transforms, snaps, anchors, arrays, hierarchy, instances, and undo/redo;
- assisted alignment and modular placement;
- group, assembly, join, boolean, separate, and bake distinctions;
- construction history and export.

Exit: users assemble approved components into a recoverable modular construction and
export a verified blockout.

### Phase 12 — Advanced adapters and generation

- 3MF after print validation;
- DXF and STEP after dimensional contracts;
- OpenUSD for composed scenes;
- optional text-to-image source generation;
- community adapter/profile framework.

## 15. Verification system

Every milestone requires proportionate evidence:

1. Markdown/source-truth checks;
2. Python compile/import checks;
3. pure-logic unit contracts;
4. fixture-based integration contracts;
5. thread and cancellation lifecycle contracts;
6. schema and migration validation;
7. filesystem interruption and recovery tests;
8. benchmark-source comparisons;
9. manual Qt smoke checks on the T1700;
10. downstream import and round-trip checks for every export adapter.

No milestone becomes VERIFIED solely because code was committed or merged.

## 16. Distribution, access, and support

MXZTAR Forge is a MXZTAR Projects build from `https://www.mxztar.co.nz`.

Official software use is free of charge. There is no timed trial, subscription, or
feature paywall in the confirmed product model. Users may voluntarily support the
founder at `https://buymeacoffee.com/mxztar`.

The public repository supports developer collaboration and forks. Ordinary users are
directed to versioned official releases so installation, schemas, model compatibility,
and migrations remain synchronized.

Free access and open-source permissions are related but different decisions. Before
the first public release, the repository must contain a recognised `LICENSE` selected
by the founder and consistent contributor terms. Until then, documentation must not
invent legal permissions beyond the confirmed free-of-charge access policy.

## 17. Immediate build sequence

The next permitted engineering order is:

1. reconcile the existing planning documents with this Level One contract;
2. restore Jobs;
3. define and restore Shape Library;
4. implement project authority and processed-source lifecycle;
5. implement Start Here onboarding;
6. formalise the structured analysis schema;
7. make Agent Workflows produce and validate it;
8. build Review and approval;
9. build the first Forge Pack exporter;
10. complete Level One release acceptance before 2D-to-3D implementation.

Every PR should advance one coherent gate, preserve current verified behaviour, update
the progress ledger, and avoid unrelated UI promises.

## 18. Future product horizon

The separately governed
[`FUTURE_CONSTRUCT_AND_WORLD_VISION.md`](FUTURE_CONSTRUCT_AND_WORLD_VISION.md)
preserves the long-term direction for MXZTAR Construct, rig-efficient cyber-art,
infrastructure building, and a persistent human-designed moon-scale virtual world.
It is a future vision, not a Level One feature promise, and does not change the current
phase order.

The maturity horizon is now explicit:

- Level One: operational local Forge and portable production intelligence;
- Level Two: reversible component generation and modular Construct;
- Level Three: infrastructure relationships, regional state, and offline delta
  foundations;
- Level Four: cross-device human-governed platform, operator jobs, portable personal
  archives, immersive review, optional collaboration, and the first persistent region.

Level Four priorities are governed by
[`LEVEL_FOUR_PLATFORM_PRIORITIES.md`](LEVEL_FOUR_PLATFORM_PRIORITIES.md). The planning
horizon is no earlier than approximately one year from 20 July 2026, subject to verified
completion of the preceding levels. It does not change the immediate Level One sequence.
