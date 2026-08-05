# MXZTAR Forge v2.0 — Master Build Plan

## 1. Purpose and authority

This document defines the stable finished-product boundary for MXZTAR Forge v2.0.

It contains:

- product identity and value;
- active Stage One–Two scope;
- core principles;
- finite workflow families;
- durable authority rules;
- milestone logic;
- release acceptance.

It deliberately does **not** contain current PR history, temporary branch state, the immediate engineering queue, or detailed correction narratives.

Use:

- `CURRENT_CAPABILITY_BOUNDARY.md` for present-tense implementation truth;
- `ACTIVE_ENGINEERING_PLAN.md` for the current ordered gate;
- `docs/PROGRESS_LEDGER.md` for dated evidence and causal learning;
- `docs/SOURCE_OF_TRUTH.md` for authority resolution.

## 2. Product definition

MXZTAR Forge v2.0 is a local-first, human-governed creative concept-engineering forge.

It helps creators turn source art, sketches, and scratch-built shapes into structured, editable, reusable, recoverable, and portable creative assets.

The product value path is:

```text
purpose
→ project
→ source image, starter asset, or blank document
→ editable geometry
→ correction and review
→ reusable 2D asset
→ reversible 3D component
→ recoverable construction
→ verified downstream handoff
```

Forge is not merely:

- an image captioner;
- a prompt generator;
- a black-box automatic vectoriser;
- a one-click production-ready 2D-to-3D converter;
- an engineering-certification or manufacturing-safety system;
- a replacement for Krita, Inkscape, Blender, CAD systems, game engines, or slicers.

Forge preserves the missing production structure between specialist tools.

## 3. Active product horizon

### Stage One — Forge Editor and portable 2D assets

Stage One provides:

- project and source authority;
- blank and source-derived editable geometry;
- path, node, handle, transform, composition, and explicit 2D operations;
- deterministic and optional AI-assisted candidate workflows;
- correction, review, approval, versioning, and reusable Shape Library assets;
- validated 2D continuation and Forge Pack output.

### Stage Two — Construct and portable 3D blockouts

Stage Two provides:

- declared primitives and reversible shape-to-component recipes;
- editable component parameters and transforms;
- pivots, anchors, sockets, areas, surfaces, focus targets, and named views;
- groups and recoverable assemblies;
- explicit geometry relationships and derived operations;
- validated 3D continuation profiles.

**Stage One and Stage Two together define MXZTAR Forge v2.0.**

Product Levels Three and Four remain deferred vision. They require a separate founder decision and source-of-truth revision before runtime work is authorised.

## 4. Intended users and durable value

Primary users include:

- concept and visual-development artists;
- vector, graphic, pattern, and shape-system creators;
- indie game, environment, prop, film, and animation creators;
- Blender generalists and blockout artists;
- makers and 3D-print designers at concept and blockout stage;
- small teams without a dedicated technical-art pipeline;
- creators who need local ownership and recovery on modest hardware.

The primary commercial and creative asset is a durable Forge project containing, as implemented over time:

- exact Purpose and stable project identity;
- unchanged project-owned source copies and provenance;
- editable shape documents;
- candidate and correction history;
- approved reusable assets;
- project-owned object scenes;
- construction recipes, components, and assemblies;
- job and diagnostic evidence;
- approvals and supersession records;
- validated export records.

A Forge Pack is a deterministic continuation package assembled from approved project records. It is not a competing project authority.

## 5. Product principles

1. **Editor first.** Forge is a creator workbench, not a read-only AI report viewer.
2. **Local first.** Project truth remains local unless the user deliberately chooses otherwise.
3. **Human governed.** Consequential approval, deletion, migration, merge, bake, publishing, and export decisions remain visible.
4. **AI optional.** Core creation, editing, saving, recovery, approval, and export do not depend on a model or network.
5. **Observed is not inferred.** Source evidence, calculation, model proposal, user-created geometry, and approved truth remain distinct.
6. **Non-destructive by default.** Originals and approved prior versions remain recoverable.
7. **No dead or frozen UI.** Long work runs outside the Qt main thread with truthful progress and terminal state.
8. **Modest hardware remains valid.** One heavy job at a time, bounded decoding, conservative threads, no silent downloads.
9. **Every name is a promise.** No control or format claim exists without implementation, persistence, failure handling, and proof.
10. **State authority is explicit.** Selection, preview, autosave, canonical state, and project attachment are not interchangeable.
11. **Interoperability is verified.** A target format is advertised only after named continuation or round-trip evidence.
12. **Corrections compound value.** User edits become durable project knowledge.
13. **Finite scope protects quality.** Stage One and Stage Two take priority over distant platform vision.
14. **Reliability is product value.** Regression prevention protects user trust, founder time, demonstrations, support, and sales.
15. **Specialist tools are partners.** Forge prepares governed handoffs rather than pretending to replace every downstream tool.

## 6. Workflow, operation, and job

### Workflow

A user journey that produces durable project value, a reusable asset, a recoverable state transition, or a validated handoff.

### Operation

A reversible command or explicitly derived action inside a workflow.

### Job

Bounded work that may take time and exposes:

- declared inputs;
- current stage;
- progress or heartbeat;
- elapsed time;
- cancellation boundary where safe;
- saved evidence;
- truthful success, failure, cancellation, invalid, or timeout state.

## 7. The 18 first-class workflow families

### Shared platform workflows

#### P1. Project lifecycle

```text
Purpose → Create → Open → Work → Save → Close → Reopen → Recover
```

#### P2. Source lifecycle

```text
External source
→ unchanged project-owned copy
→ identity and hash
→ bounded preview
→ declared use
→ explicit derivative or processed transition
```

#### P3. Job and evidence lifecycle

```text
Queued
→ Running
→ Succeeded / Failed / Cancelled / Timed out / Invalid
→ Evidence saved
→ User-visible result and next action
```

#### P4. Recovery, migration, and integrity

```text
Validate
→ detect interruption or incompatibility
→ preserve last canonical truth
→ recover or attach read-only
→ rebuild indexes
→ migrate only through explicit rules
```

### Stage One workflows

#### S1. Blank Shape Creation

Create a project-owned editable document and begin manual geometry without AI or network access.

#### S2. Source Region and Manual Trace

Select an exact source region, trace editable geometry, correct it, and preserve source mapping and provenance.

#### S3. Deterministic Shape Extraction

Generate bounded contour, edge, threshold, mask, line, or silhouette candidates and choose one for editing.

#### S4. Optional AI Shape Proposal

Record local-model assessment or proposals with model identity, assumptions, confidence, and source evidence. AI output remains proposal or raw evidence until converted into editable geometry and reviewed.

#### S5. Shape Editing

Edit paths, nodes, handles, properties, transforms, and command history with autosave, save, Undo, Redo, reopen, and recovery.

#### S6. 2D Composition

Align, distribute, mirror, array, group, connect, or apply explicit path and boolean operations to produce editable derived geometry.

#### S7. Review and Shape Library

Correct, approve, reject, version, supersede, and insert reusable assets through explicit reversible commands.

#### S8. 2D Validation and Continuation

Validate and export through named SVG, PNG, and Forge Pack profiles with provenance and limitations.

### Stage Two workflows

#### T1. Declared 3D Primitive Creation

Create an editable project-owned component from a declared primitive with units, parameters, and provenance.

#### T2. Shape-to-Component Generation

Apply a declared reversible recipe to an approved 2D shape while preserving the parent relationship.

#### T3. Component Editing

Edit recipe parameters, transforms, origin, pivot, and regeneration state without losing parentage or history.

#### T4. Assembly and Constraint

Place components, add anchors or sockets, define hierarchy or contact, and save a recoverable assembly.

#### T5. Geometry Relationship and Derived Operations

Preview and deliberately apply distinct operations such as group, contact, stitch/weld, join, boolean, separate, or bake.

#### T6. 3D Validation and Continuation

Validate units, axes, hierarchy, names, and geometry before named GLB/glTF or OBJ continuation proof.

## 8. Durable authority model

The project directory is the recovery boundary.

Validated durable files are authoritative. SQLite, caches, previews, queues, recent-state settings, and in-memory objects may accelerate or display state but remain rebuildable.

Durable artifact classes may include:

1. project manifest;
2. project history event;
3. source asset and preview record;
4. native shape document;
5. extraction candidate;
6. approval, rejection, version, and supersession record;
7. approved Shape Library asset;
8. project-owned object scene;
9. recipe and component record;
10. area, surface, pivot, anchor, socket, group, and assembly record;
11. job, diagnostic, and validation evidence;
12. export and Forge Pack record.

A documented artifact does not become runtime authority until schema, transaction, migration, recovery, and verification rules exist.

## 9. Unified asset lifecycle

```text
blank document or source region
→ proposal or candidate
→ editable geometry
→ correction
→ review
  ├→ approve and version
  ├→ request correction
  └→ reject
→ reusable asset
→ declared component recipe
→ editable component
→ positioned instance
→ group or assembly
→ explicit relationship or derived geometry operation
→ validated continuation
```

Raw model evidence never becomes an approved reusable asset automatically.

## 10. Editor contract

The Editor is one coherent document workspace.

It must eventually provide:

- blank and source-backed documents;
- primitives and freeform paths;
- selection, box selection, nodes, handles, and transforms;
- fill and stroke properties;
- layers, visibility, locking, grouping, and ordering;
- guides, alignment, distribution, snapping, and measurement;
- duplicate, mirror, symmetry, and arrays;
- explicit 2D path and boolean operations;
- review, version, approval, insertion, and continuation;
- save, autosave, rollback, reopen, and recovery.

The Editor must distinguish source pixels, candidate geometry, user-created geometry, temporary selection and guides, approved truth, and exported derivatives.

## 11. Construct contract

Construct builds reversible 3D blockouts from approved shapes and declared primitives.

It must distinguish:

1. placement;
2. snapping or alignment;
3. group;
4. recoverable assembly contact;
5. visual seam;
6. mesh stitch or weld;
7. join mesh;
8. boolean union, difference, or intersection;
9. separate;
10. bake.

Merely placing objects together performs none of operations 3–10 automatically.

Every consequential operation requires named inputs, preview, persistence, Undo/Redo or declared derivative behaviour, validation, failure handling, parent mapping, and recovery.

Visual-design effects such as greebling, roughness, distortion, bounded bend, routing, and metallic profiles require a reversible targetable effect-stack core before individual effects appear.

## 12. Interoperability contract

No format is universal.

Every exposed profile declares:

- target workflow and named downstream program where applicable;
- units, axes, origin, scale, and coordinate mapping;
- hierarchy and naming behaviour;
- supported geometry and appearance;
- known losses and exclusions;
- validation fixture;
- continuation, import, or round-trip evidence.

Naming a format in planning is not an implementation claim.

## 13. Milestone logic

The active execution sequence is maintained separately, but milestone dependencies remain stable:

1. reliable project, document, command, and final-runtime foundation;
2. freeform path authority;
3. manual source-region tracing;
4. deterministic extraction candidates;
5. starter source-asset pack;
6. review and reusable Shape Library authority;
7. verified 2D continuation;
8. general shape-to-component recipe registry;
9. areas, surfaces, pivots, anchors, sockets, focus, and named views;
10. groups and recoverable assemblies;
11. reversible effects and explicit geometry relationships;
12. verified 3D continuation;
13. release installation, recovery, documentation, and support readiness.

A later milestone may not bypass an unproven authority dependency merely because a visual prototype is possible.

## 14. Release acceptance

MXZTAR Forge v2.0 is ready for a supported release only when:

- core Stage One and Stage Two workflows are coherent and discoverable;
- no visible control is dead or misleading;
- project data survives save, close, restart, interruption, and supported migration;
- the official final runtime—not an intermediate class—passes focused and complete verification;
- interaction-heavy work has T1700 live acceptance;
- worker shutdown is clean;
- current capability and limitations are truthful;
- named output profiles have downstream evidence;
- privacy, licence, New Zealand compliance, support, and installation boundaries are documented;
- the release does not depend upon unapproved future-world infrastructure.

## 15. Omission and archival rule

To keep this plan durable:

- omit current branch names, current PR numbers, temporary defects, and dated runtime snapshots;
- omit exhaustive implementation history retained in Git and the Progress Ledger;
- omit detailed class and patch composition maintained in `FINAL_RUNTIME_COMPOSITION.md`;
- omit the immediate task queue maintained in `ACTIVE_ENGINEERING_PLAN.md`;
- preserve historical correction documents as evidence, not active scope authority;
- archive or de-authorise superseded planning rather than allowing several documents to issue competing instructions.

The Master Build Plan changes only when the intended finished product, stage boundary, core workflow taxonomy, or release definition changes.