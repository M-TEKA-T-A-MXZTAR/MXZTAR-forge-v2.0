# MXZTAR-forge v2c0 — Master Build Plan

## 1. What we are building

MXZTAR-forge v2c0 is a local-first, human-governed creative concept-engineering forge.

It turns source art into structured, inspectable, reusable production intelligence. It is not merely an image captioner, an automatic art generator, or a one-click 2D-to-3D converter.

Its core responsibility is to recover and organise the design grammar contained in source material so a creator can deliberately move toward:

- reusable 2D assets;
- vector and extraction candidates;
- structured concept briefs and prompt packs;
- 2.5D stacked constructions;
- modular blockout systems;
- Blender and CAD handoffs;
- later OBJ/GLB and production-oriented 3D workflows;
- saleable digital asset packs where the result is suitable.

Core value path:

```text
source art
→ source suitability and rights context
→ visual and schematic intelligence
→ line, shape, layer, depth, perspective, and module evidence
→ observed versus inferred structure
→ approved reusable design grammar
→ concept brief / extraction map / module plan / prompt pack
→ 2D derivative, 2.5D stack, blockout, Blender/CAD, or later 3D handoff
→ review, correction, benchmark, learning, and reuse
```

The product closes the missing bridge between “AI sees a picture” and “a creator receives usable spatial production data.”

## 2. Who it serves

Primary users:

- visual artists with strong source art but limited 3D or CAD experience;
- concept artists and industrial-design thinkers;
- game, film, animation, environment, and world-building planners;
- Blender blockout and kitbash creators;
- modular design-system builders;
- creators who need structured prompts, briefs, extraction maps, and component families;
- solo creators working on modest CPU-only hardware.

## 3. The market and workflow gaps

### 3.1 Generic image-description gap

General vision models describe visible subjects but usually do not identify production-useful structure: reusable silhouettes, construction lines, layers, panels, ribs, shells, joints, connectors, surfaces, repeated grammar, extraction priorities, risks, and next actions.

MXZTAR-forge must inspect source art as production material, not merely as a picture.

### 3.2 Schematic and line-network gap

Technical drawings, apex views, abstract diagrams, and layered line art need specialised interpretation of:

- connected and interrupted line networks;
- open and closed contours;
- centre lines and symmetry axes;
- nested regions;
- intersection and attachment points;
- line weight and likely semantic roles;
- stacked levels and sectional relationships.

This is a known weak point and must become a first-class engineering track.

### 3.3 Spatial bridge gap

The missing middle between 2D art and 3D construction is an explicit intermediate representation.

It must hold:

- source-plane coordinates;
- contour and region identities;
- depth-order hypotheses;
- occlusion relationships;
- perspective cues;
- symmetry and repetition rules;
- component hierarchy;
- module relationships;
- scale and unit assumptions;
- confidence and uncertainty.

This representation is more important than prematurely generating a finished mesh.

### 3.4 Observation-versus-inference gap

Every workflow must distinguish:

- observed source evidence;
- calculated or derived geometry;
- user-supplied intent;
- model inference;
- speculative design extension;
- approved project truth.

### 3.5 Workflow compatibility gap

Not every source is appropriate for every workflow. The system must classify a proposed run as READY, CAUTION, or BLOCKED and explain missing inputs, expected output, recommended prior work, and what not to do yet.

### 3.6 Persistent project-truth gap

Useful work cannot live only in terminal scrollback, chat, or volatile UI state. The forge requires durable versioned artifacts, provenance, approvals, rejections, supersession, project history, rebuildable SQLite indexing, and non-destructive recovery.

### 3.7 Benchmark and quality gap

Plausible prose is not sufficient evidence of quality. The system needs repeatable benchmarks for:

- shape and contour detection;
- line-network interpretation;
- repeated-form recognition;
- layer and depth ordering;
- perspective cues;
- observed/inferred separation;
- module-family consistency;
- output-schema validity;
- provenance protection;
- user-correction retention.

### 3.8 Toolchain-fragmentation gap

Creators currently move manually between image folders, tracing tools, notes, AI chats, Blender, CAD, prompt files, and exports. MXZTAR-forge should become the governed bridge without pretending to replace every specialist tool.

### 3.9 Hardware-access gap

Many local AI tools assume powerful GPUs. The forge must remain useful on CPU-only hardware through conservative resource governance, one heavy job at a time, two-thread defaults, visible elapsed time and heartbeat, cancellation and timeout handling, no main-thread AI work, and no silent model downloads.

### 3.10 Creator-skill and next-action gap

A 2D creator may not know which spatial decision should happen next. The interface must apply the LEVER principle: current state, end goal, workflow chain, one primary next action, next few events, and what not to do yet.

## 4. Additional gaps to bake in

### 4.1 Multi-view evidence

Support front, side, top, section, detail, and alternate-angle sources. Never pretend one image provides complete geometry.

### 4.2 Scale and measurement anchors

Allow units, known dimensions, grids, or reference objects. Dimensional claims remain unknown until anchored.

### 4.3 Camera and perspective estimation

Record vanishing points, horizon hypotheses, projection type, camera uncertainty, and correction decisions.

### 4.4 Depth and occlusion graph

Represent which region is in front of, behind, attached to, embedded in, or intersecting another region.

### 4.5 Parametric and modular grammar

Record repetition, symmetry, rotation, scaling, attachment, stacking, substitution, and family rules.

### 4.6 Human correction as first-class data

Users must be able to correct contours, labels, hierarchy, depth, module membership, and confidence. Corrections persist and influence later workflows through an audit-trailed learning ledger.

### 4.7 Round-trip validation

Future Blender/CAD exports must be re-importable or verifiable against the approved intermediate representation. File creation alone does not prove export success.

### 4.8 Rights and provenance context

Record ownership assertions, licence notes, source origin, and commercial-use status without claiming legal verification the application did not perform.

### 4.9 Product and audience opportunity mapping

Approved structures may be classified into opportunities such as vector packs, modular concept packs, kitbash planning packs, reference boards, texture/motif libraries, prompt packs, game/film planning kits, and later 3D blockout projects. This is recommendation, not automatic publication.

### 4.10 Explicit interoperability profiles

Define versioned handoffs rather than a vague export button:

- PNG/JPEG/TIFF reference boards;
- SVG vector layers;
- JSON spatial/intermediate representation;
- Blender Python or scene-manifest handoff;
- future OBJ/GLB blockout export;
- future CAD exchange only after units and geometry contracts are proven.

## 5. Non-goals for the first rentable release

The first release must not promise:

- automatic production-ready 3D meshes;
- engineering certification;
- manufacturing safety;
- dimensionally accurate reconstruction from an unscaled single image;
- perfect hidden-surface recovery;
- automatic CAD solids;
- autonomous publishing or sales;
- unlimited parallel jobs;
- cloud dependence;
- learning from unreviewed hidden memory.

## 6. Architectural product layers

1. **Source library and project boundary** — source identity, hashes, rights, previews, projects, and multi-view grouping.
2. **Suitability and compatibility** — READY/CAUTION/BLOCKED workflow decisions.
3. **Visual and schematic intelligence** — contours, lines, regions, motifs, layers, perspective, repeats, components, and uncertainty.
4. **Spatial intermediate representation** — hierarchy, depth, occlusion, transforms, module rules, scale assumptions, and confidence.
5. **Human review and approval** — correction, approval, rejection, and supersession.
6. **Production translators** — briefs, extraction maps, prompt packs, module manifests, 2.5D plans, and specialist-tool handoffs.
7. **Benchmark and learning system** — measurable quality, corrections, decisions, and approved lessons.
8. **Commercial and entitlement boundary** — 60-day free access and later NZD 10/month without endangering user-owned local project files.

## 7. Master implementation sequence

### Phase 0 — Governance and source-of-truth foundation

Status: substantially complete.

Required outcomes:

- first rentable release definition;
- workflow compatibility matrix;
- output artifact contracts;
- project state and data authority;
- master build plan;
- progress ledger.

Exit gate: planning documents agree on terminology, authority, and scope; the source-truth verifier checks them.

### Phase 1 — Stabilise the existing execution path

Purpose: establish an honest, repeatable runtime baseline before expansion.

Work:

1. inspect `AgentPanel`, `AgentWorker`, `agent_runner`, prompts, and service contracts;
2. reproduce the successful simple-image probe;
3. reproduce and classify the earlier random-workflow HTTP 400 observation;
4. ensure a failed `AgentResult` cannot become UI success through tuple or return-contract confusion;
5. separate saved diagnostic output from workflow success;
6. verify responsiveness, elapsed time, heartbeat, single-job protection, cancellation boundary, and final state;
7. add regression tests for success, model failure, malformed output, missing source, timeout, and storage failure.

Exit gate: one compatible workflow runs end to end; success is reported only after schema validation; failures save diagnostics and useful next actions; no Qt-main-thread AI work.

### Phase 2 — Implement project skeleton and authority model

Work:

- project creation/opening;
- `project.json` manifest;
- project directory contract;
- project lock and one-writer rule;
- atomic writes;
- artifact and run IDs;
- project history;
- SQLite as derived index;
- index rebuild;
- read-only recovery;
- reconciliation report.

Exit gate: deleting SQLite and rebuilding from project files loses no durable project truth.

### Phase 3 — Build source intake and source profiles

Work:

- recursive discovery;
- supported-image validation;
- duplicate detection by hash;
- previews;
- rights notes;
- source classification: artwork, schematic, photograph, screenshot, orthographic view, section, detail, mask, reference;
- multi-view grouping;
- scale/unit anchors;
- quality and suitability report.

Exit gate: every source has durable identity, validation, rights context, and suitability profile.

### Phase 4 — Implement compatibility assessment

Work:

- encode READY/CAUTION/BLOCKED rules;
- show reasons and missing requirements;
- recommend one prior or alternative workflow;
- version rule sets;
- save material assessments.

Exit gate: blocked workflows cannot launch; caution requires deliberate continuation; recommendations reference only real controls and workflows.

### Phase 5 — Formalise schemas and validators

Work:

- shared artifact envelope;
- workflow-specific schemas;
- status, approval, provenance, validation, and error objects;
- atomic writer;
- schema validation;
- approval derivative;
- supersession records;
- migration scaffold;
- JSONL execution and project-history logs.

Exit gate: every workflow produces a schema-valid success or failure artifact; invalid output cannot be recorded as success.

### Phase 6 — Source-art intelligence v1

Work:

- visible evidence;
- motif, surface, object, and component candidates;
- layers and structures;
- uncertainty and quality notes;
- user intent;
- observed/inferred separation;
- recommended next workflow;
- correction and approval UI.

Exit gate: benchmark sources produce useful structured findings beyond a generic caption.

### Phase 7 — Schematic and line-network intelligence

Work:

- line and contour extraction;
- connected-component graph;
- open/closed path classification;
- intersection and endpoint detection;
- centre-line and symmetry candidates;
- nested-region analysis;
- semantic line-role hypotheses;
- correction overlays;
- vector candidate records.

Exit gate: benchmark schematics yield a stable line/region graph with measurable quality and retained corrections.

### Phase 8 — Shape, layer, depth, and 2.5D representation

Work:

- shape and silhouette entities;
- layer ordering;
- occlusion graph;
- extrusion-depth hypotheses;
- stacked levels;
- transforms and anchors;
- perspective/camera hypotheses;
- confidence per relationship;
- 2.5D preview;
- non-destructive masks and extraction zones.

Exit gate: users can inspect and correct a source-derived 2.5D construction plan without generating a final mesh.

### Phase 9 — Modular design grammar

Work:

- module candidates and families;
- hierarchy;
- connectors and attachment rules;
- repetition, symmetry, scale, rotation, and stacking;
- observed versus invented modules;
- naming;
- variation constraints;
- kitbash/blockout manifest.

Exit gate: one project produces a reusable, versioned module family and controlled variation plan.

### Phase 10 — Production translators

Initial translators:

- concept brief;
- extraction map;
- render prompt pack;
- module manifest;
- source/reference board;
- 2.5D stack plan;
- Blender blockout brief;
- next-step recommendation.

Later translators after contracts are proven:

- layered SVG;
- Blender Python/scene-manifest adapter;
- OBJ/GLB blockout;
- CAD-oriented exchange.

Exit gate: every translator declares inputs, outputs, limitations, verification, and provenance; no generic “Export 3D” control exists without a validated path.

### Phase 11 — Benchmark, correction, and progressive learning

Work:

- benchmark corpus for simple shapes, schematics, layered art, perspective scenes, repeated modules, and multi-view sets;
- expected findings and tolerances;
- workflow metrics;
- correction records;
- approved lesson ledger;
- regression comparison across prompt, model, and schema versions;
- failure-trend reports.

Exit gate: improvements require benchmark evidence; approved corrections are traceable to later behaviour changes.

### Phase 12 — First rentable-release cockpit

Cockpit must show:

- current project and source;
- integrity state;
- selected goal;
- workflow chain;
- compatibility;
- one primary next action;
- active job and resource state;
- review-required items;
- latest valid artifacts;
- what not to do yet.

Exit gate: a new user can import source art, run a suitable workflow, review and approve findings, produce a useful translated output, and reopen the project without filesystem archaeology.

### Phase 13 — Packaging, trial, subscription, and release safety

Work:

- installer and launcher verification;
- clean-machine recovery test;
- continued local-project access after subscription lapse;
- 60-day trial;
- NZD 10/month entitlement boundary;
- cancellation and renewal clarity;
- privacy and licence terms;
- diagnostics export;
- update and rollback;
- known limitations.

Exit gate: commercial controls cannot endanger user-owned project files; restore, update, cancellation, and failure behaviour are tested.

## 8. Cross-cutting build rules

Every milestone must define:

- purpose and user problem;
- inputs and outputs;
- data shapes;
- handler and engine path;
- success, caution, failure, cancellation, and timeout states;
- persistence and provenance;
- UI feedback;
- targeted verification;
- regression risk;
- downstream consequences;
- progress-ledger update.

No visible control may be added without its complete functioning workflow path.

## 9. Verification strategy

Required layers:

1. static compile/import checks;
2. schema and contract validators;
3. unit tests for pure logic;
4. fixture-based integration tests;
5. worker/thread lifecycle tests;
6. file-system interruption tests;
7. project rebuild and recovery tests;
8. benchmark-source tests;
9. manual Qt smoke tests;
10. export round-trip tests when adapters exist.

## 10. Branch and milestone discipline

- one coherent milestone per branch;
- inspect before patching;
- small verified changes;
- update documentation and verifiers with behaviour;
- no unrelated cleanup;
- no claim of completion without evidence;
- merge only when clean and required checks pass;
- prune merged branches;
- update the progress ledger after each merged milestone;
- make one normal VX12 backup at the end of a meaningful work period unless a risky migration requires an immediate backup.

## 11. Immediate next milestone

After this planning PR merges:

1. synchronise local `main`;
2. inspect the live runtime and unresolved Stage 4C-4 state;
3. create a focused baseline-audit branch;
4. verify prompts, service, runner, worker, panel, and simple-image probe;
5. record the exact runtime-state matrix in the progress ledger;
6. fix only confirmed execution-contract defects;
7. add targeted regression tests;
8. do not begin project-state implementation until the execution baseline is honest and repeatable.
