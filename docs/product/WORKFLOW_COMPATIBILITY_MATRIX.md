# MXZTAR Forge v2.0 — Workflow Compatibility Matrix

## 1. Purpose

This document defines readiness, input, output, blocking, failure, and next-action rules for the 18 first-class Stage One–Two workflow families.

It replaces the older assumption that the seven optional AI prompt contracts were the entire product workflow system.

The optional agent workflows remain supported jobs, but Forge is now organised around creator journeys that produce durable project value.

The compatibility layer must answer:

- Can this workflow run?
- Should it run now?
- What is missing?
- What durable result will it create or change?
- What remains reversible?
- What must the interface report on failure?
- What is the next safe action?

A workflow is not complete merely because text appears or a file is written.

---

## 2. Workflow classes

### Workflow

A user journey that creates a durable state change, reusable asset, validated handoff, or recoverable project result.

### Operation

A reversible or explicitly derived command inside a workflow.

### Job

Bounded work that may take time and must expose progress, elapsed time, cancellation, evidence, and truthful final state.

---

## 3. Compatibility states

Every proposed workflow resolves to one state.

### READY

Required inputs and authority are present. The primary action may be enabled.

The UI still shows:

- selected project and source where applicable;
- expected durable output;
- authority and approval implications;
- storage destination;
- reversibility or derivation boundary;
- estimated resource class where available.

### CAUTION

The workflow can run, but optional context, validation, scale, prior review, or target-profile information is missing.

The UI states:

- why the result may be weaker;
- which assumptions will be made;
- what additional input would improve it;
- whether another workflow should happen first;
- whether the user may deliberately continue.

### BLOCKED

A required project, source, artifact, authority, schema, adapter, or runtime dependency is missing or invalid.

The UI must:

- disable the primary action;
- identify the missing requirement;
- explain how to resolve it;
- recommend one valid next action;
- avoid creating a misleading output record.

### READ_ONLY

The project is attached but writable authority is unavailable because of a lock, recovery condition, unsupported schema, or durability uncertainty.

Inspection and safe export of already-valid material may remain available. Mutations must be disabled.

---

## 4. Shared authority and input classes

### WRITABLE_PROJECT

A validated project session for which the current Forge process owns the writer lease.

### ATTACHED_PROJECT

A validated project attached in writable or read-only state.

### PROJECT_PURPOSE

The exact creator statement used to begin a project. It is not a hidden profile and is preserved as the first project event.

### SOURCE_ASSET

A supported project-owned source copy with identity, hash, origin, rights notes where supplied, and unchanged external source bytes.

### SOURCE_REGION

A bounded region of a SOURCE_ASSET with exact source coordinates.

### SHAPE_DOCUMENT

A valid native editable shape document owned by the project.

### SHAPE_CANDIDATE

Manual, algorithmic, or model-proposed geometry that is editable but not approved.

### APPROVED_SHAPE

A reviewed Shape Library asset with durable approval and provenance.

### CONSTRUCTION_RECIPE

A declared reversible operation that derives a 3D component from a shape or primitive.

### COMPONENT

An editable 3D object with recipe, transform, parent, units, and validation state.

### ASSEMBLY

A recoverable hierarchy of components, instances, anchors, connectors, and declared relationships.

### OUTPUT_PROFILE

A named adapter and validator for a downstream format or program.

---

## 5. Shared execution contract

Every asynchronous job records:

- project and workflow identifiers;
- workflow contract version;
- selected input artifact IDs;
- source hash where applicable;
- algorithm or model identity;
- start and completion time;
- elapsed time;
- compatibility result;
- terminal status;
- saved evidence path;
- output artifact IDs;
- validation result;
- error detail;
- recommended next action.

A saved diagnostic does not prove workflow success. A successful job does not imply user approval.

---

# 6. Platform workflows

## P1. Project lifecycle

**Journey**

```text
Purpose → Create → Open → Work → Close → Reopen → Recover
```

**Required input**

- Create: valid PROJECT_PURPOSE and no attached project.
- Open: selected canonical project and no attached project.
- Close: attached project and no guarded mutation.

**READY**

- project root is accessible;
- project name/slug can be derived safely;
- no collision exists for creation;
- session authority can be acquired or truthfully classified.

**CAUTION**

- project is opened read-only;
- optional project metadata is absent;
- migration is available but not yet applied.

**BLOCKED**

- Purpose is empty for creation;
- path escapes the project root;
- project already exists under the derived identity;
- another guarded mutation is active;
- schema is unsupported and no safe read-only path exists.

**Durable output**

- project manifest;
- writer lock where writable;
- `project_created`, `project_opened`, `project_closed`, or recovery history event.

**Next**

- blank shape creation or source intake.

---

## P2. Source lifecycle

**Journey**

```text
External source → Import copy → Hash → Preview → Use → Explicitly process project copy
```

**Required input**

- WRITABLE_PROJECT;
- readable supported source file;
- ownership or rights note when the user supplies one.

**READY**

- file can be decoded;
- size and dimensions are within bounded intake rules;
- no duplicate source identity conflict exists.

**CAUTION**

- format is importable but not model-ready;
- source is unusually large or low resolution;
- rights information is incomplete.

**BLOCKED**

- no writable project;
- source does not exist or cannot be decoded;
- source path is unsafe;
- duplicate handling cannot be resolved truthfully.

**Durable output**

- unchanged project-owned source copy;
- source asset record and hash;
- rebuildable preview;
- manifest and history updates.

**Next**

- source-region/manual-trace, algorithmic extraction, optional AI proposal, or source review.

---

## P3. Job lifecycle

**Journey**

```text
Queued → Running → Succeeded / Failed / Cancelled / Timed out → Evidence → Next action
```

**Required input**

- declared workflow/job contract;
- valid inputs;
- available worker capacity;
- known cancellation boundary.

**BLOCKED**

- conflicting heavy job already active;
- required worker dependency missing;
- output destination unavailable;
- job contract lacks a truthful terminal-state path.

**Durable output**

- terminal evidence or diagnostic record;
- elapsed time and execution metadata;
- output artifact references where successful.

**Next**

- review output, correct input, retry through an explicit action, or choose another workflow.

---

## P4. Recovery, migration, and integrity

**Required input**

- ATTACHED_PROJECT or project directory selected for assessment.

**READY**

- canonical files validate;
- any migration has an explicit versioned rule;
- recovery can preserve last valid truth.

**CAUTION**

- stale temporary files exist but canonical truth is valid;
- rebuildable index is missing;
- project opens read-only pending user action.

**BLOCKED**

- competing authorities cannot be reconciled safely;
- required migration is unavailable;
- durability state is uncertain and mutation would risk canonical truth.

**Durable output**

- validation, recovery, migration, or index-rebuild record;
- no silent modification during assessment.

**Next**

- reopen writable, remain read-only, restore backup, or apply explicit migration.

---

# 7. Stage One workflows

## S1. Blank Shape Creation

**Required input:** WRITABLE_PROJECT.

**READY:** native shape schema supported; no conflicting document transaction active.

**BLOCKED:** project read-only; storage or manifest transaction unavailable.

**Durable output:** canonical SHAPE_DOCUMENT, manifest registration, history event.

**Next:** shape editing.

---

## S2. Source Region and Manual Trace

**Required input:** WRITABLE_PROJECT, SOURCE_ASSET, selected SOURCE_REGION.

**READY:** source preview and coordinate mapping are available.

**CAUTION:** scale or perspective is unknown; fine detail may require manual interpretation.

**BLOCKED:** no source region; source identity or coordinate mapping unavailable.

**Durable output:** editable SHAPE_CANDIDATE with source coordinates and provenance.

**Next:** shape editing, review, or rejection.

---

## S3. Algorithmic Shape Extraction

**Required input:** WRITABLE_PROJECT and SOURCE_REGION.

**READY:** bounded extraction engine available; settings validate.

**CAUTION:** photographic or noisy source; uncertain holes or boundaries; low resolution.

**BLOCKED:** engine unavailable; unsafe workload; unsupported source derivative; conflicting job active.

**Durable output:** one or more raw editable SHAPE_CANDIDATE records plus job evidence.

**Next:** compare candidates and open one in shape editing.

---

## S4. Optional AI Shape Proposal

**Required input:** WRITABLE_PROJECT, model-ready SOURCE_REGION, available configured model.

**READY:** local model reachable; no conflicting heavy job; provenance can be recorded.

**CAUTION:** model may infer geometry not visibly supported; scale, depth, or hidden surfaces unknown.

**BLOCKED:** model missing; service unreachable; source format not model-ready; no source coordinates; user disabled AI.

**Durable output:** raw proposal/evidence and optional editable SHAPE_CANDIDATE; never automatic approval.

**Next:** manual correction, rejection, or comparison with source.

---

## S5. Shape Editing

**Required input:** WRITABLE_PROJECT and valid SHAPE_DOCUMENT or SHAPE_CANDIDATE.

**READY:** command schema supported; document within bounds; writable authority retained.

**CAUTION:** candidate contains unresolved self-intersections, open contours, or uncertain scale.

**BLOCKED:** document invalid or oversized; project read-only; command unsupported; transaction marker requires recovery.

**Durable output:** autosave or canonical shape revision with replayable command history.

**Next:** continue editing, 2D composition, review, or export after approval.

---

## S6. 2D Composition

**Required input:** two or more compatible editable shapes or paths.

**READY:** selected geometry shares a supported coordinate and unit context.

**CAUTION:** mixed open/closed paths, self-intersections, uncertain winding, or destructive-looking result.

**BLOCKED:** no valid selection; incompatible units or coordinate spaces; operation lacks a reversible/derived result contract.

**Durable output:** grouped relationship, connected path, compound shape, or named boolean derivative with parent IDs.

**Next:** shape editing or review.

---

## S7. Review and Shape Library

**Required input:** valid reviewed shape revision and WRITABLE_PROJECT.

**READY:** provenance, integrity, bounds, and validation state are present.

**CAUTION:** dimensional assumptions or source uncertainty remain and must be declared.

**BLOCKED:** raw model text without editable geometry; invalid document; missing provenance; unresolved corruption.

**Durable output:** approval, rejection, correction-request, version, or supersession record; approved Shape Library asset where accepted.

**Next:** reuse, 2D export, or Stage Two construction recipe.

---

## S8. 2D Export and Forge Pack

**Required input:** APPROVED_SHAPE or approved composition and available OUTPUT_PROFILE.

**READY:** adapter and profile validator pass; destination is writable.

**CAUTION:** target profile requires flattening or loses unsupported features.

**BLOCKED:** no approved input; adapter unverified; validation fails; destination collision unresolved.

**Durable output:** SVG and/or PNG derivative, export report, provenance record, and deterministic Forge Pack where requested.

**Next:** downstream continuation or Stage Two construction.

---

# 8. Stage Two workflows

## T1. Declared 3D Primitive Creation

**Required input:** WRITABLE_PROJECT and supported primitive definition.

**READY:** units, dimensions, origin, and component schema validate.

**BLOCKED:** no writable project; invalid dimensions; unsupported primitive.

**Durable output:** editable COMPONENT and creation recipe.

**Next:** component editing or assembly.

---

## T2. Shape-to-Component Generation

**Required input:** APPROVED_SHAPE and supported CONSTRUCTION_RECIPE.

**READY:** shape topology is compatible with the chosen recipe; units and axis assumptions are declared.

**CAUTION:** open paths, holes, relief depth, or scale require assumptions.

**BLOCKED:** unapproved or invalid shape; unsupported recipe; regeneration cannot preserve parent provenance.

**Durable output:** CONSTRUCTION_RECIPE and editable COMPONENT linked to the parent shape.

**Next:** component editing or assembly.

---

## T3. Component Editing

**Required input:** editable COMPONENT with valid recipe/history.

**READY:** component regenerates within workload and schema bounds.

**CAUTION:** parameter change may create intersections, open boundaries, or export limitations.

**BLOCKED:** baked-only geometry with no editable recipe; invalid parent; project read-only.

**Durable output:** updated recipe/component revision and construction history.

**Next:** assembly, validation, or export.

---

## T4. Assembly and Constraint

**Required input:** two or more COMPONENT records or instances.

**READY:** units and coordinate system compatible; anchors/connectors validate.

**CAUTION:** contact is visually plausible but not dimensionally authoritative; hierarchy may be deep or cyclic.

**BLOCKED:** incompatible units; cyclic hierarchy; missing component identity; unsupported constraint.

**Durable output:** ASSEMBLY with hierarchy, instances, transforms, anchors, connectors, and relationship records.

**Next:** geometry relationship/merge or validation/export.

---

## T5. Geometry Relationship and Merge

**Required input:** compatible selected components and explicit operation choice.

**READY:** operation validator can preview and preserve named inputs or create a declared derivative.

**CAUTION:** tolerance, open boundaries, normals, self-intersections, or topology loss require disclosure.

**BLOCKED:** ambiguous “join” request; unsupported geometry; irreversible bake not explicitly confirmed; result cannot be validated.

**Durable output:** relationship record, reversible history step, or explicit baked derivative with parent mapping.

**Next:** component correction, assembly continuation, or 3D validation/export.

---

## T6. 3D Validation, Export, and Continuation

**Required input:** valid COMPONENT or ASSEMBLY and verified GLB/glTF or OBJ OUTPUT_PROFILE.

**READY:** units, axes, names, hierarchy, geometry, and destination validate.

**CAUTION:** target profile loses materials, instances, hierarchy, or construction history.

**BLOCKED:** adapter unverified; fatal mesh validation; unsupported hierarchy; no named downstream continuation test.

**Durable output:** GLB/glTF or OBJ derivative, validation report, provenance, limitations, and downstream continuation evidence.

**Next:** continue in the named downstream tool or return to Forge for correction.

---

# 9. Optional agent jobs

The seven prompt contracts remain optional assistance:

- `source_art_intelligence`;
- `modular_set_perspective`;
- `prototype_imagination`;
- `shape_structure_harvest`;
- `concept_brief`;
- `render_prompt_pack`;
- `recommend_next_step`.

They use the shared Job lifecycle and must still distinguish READY, CAUTION, and BLOCKED.

Common blocks include:

- no valid source;
- unsupported or non-model-ready format;
- model unavailable;
- Ollama unreachable;
- conflicting heavy job;
- missing provenance destination;
- user-disabled AI.

Their outputs begin as raw findings or planning artifacts. They do not become approved shapes, components, assemblies, or export authority without the corresponding Stage One or Stage Two review path.

---

## 10. Guided next-action rules

The guided Next system may:

- identify the current workflow family;
- select an exact source or document;
- navigate to the required workspace;
- focus the next safe control;
- explain why an action is READY, CAUTION, BLOCKED, or READ_ONLY.

It must not silently:

- create or switch projects;
- start a heavy model or extraction job;
- approve or reject an artifact;
- apply a boolean, stitch, join, or bake;
- delete or process a source;
- export.

---

## 11. Verification requirement

Every workflow family requires proportionate evidence:

- schema and pure-logic validation;
- authority and persistence tests;
- failure and recovery tests;
- UI enable/disable and truthful status tests;
- thread/cancellation tests for jobs;
- command undo/redo and replay tests for operations;
- manual T1700 smoke checks;
- downstream import or continuation evidence for output profiles.

No workflow is `VERIFIED` solely because its code was merged.
