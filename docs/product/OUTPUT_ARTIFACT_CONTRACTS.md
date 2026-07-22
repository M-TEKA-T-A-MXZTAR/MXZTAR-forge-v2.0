# MXZTAR Forge v2.0 — Output Artifact Contracts

## 1. Purpose

This document defines the durable files produced or changed by MXZTAR Forge Stage One and Stage Two workflows.

Its purpose is to ensure that user work remains:

- structured;
- traceable;
- reviewable;
- recoverable;
- versioned;
- distinguishable as success, failure, raw proposal, and approved truth;
- safe to reuse in later workflows;
- understandable outside the application where practical.

A workflow is not complete merely because text appears in the interface or a file is written.

A workflow is complete only when its result is:

1. validated;
2. saved or transactionally rejected;
3. correctly classified;
4. traceable to its inputs and actor;
5. visible to the user;
6. available for later project use where successful;
7. recoverable after restart or interruption.

---

## 2. Core artifact principles

### 2.1 Durable project files are product outputs

Saved project artifacts are not implementation leftovers. They must remain usable when:

- Forge is closed;
- the project is copied;
- the machine is restored;
- the application is updated;
- SQLite is rebuilt;
- a later workflow consumes the result;
- the user inspects the project manually.

### 2.2 Storage success and workflow success are different

The system distinguishes:

```text
artifact or diagnostic saved
```

from:

```text
workflow or job succeeded
```

A failure record may be stored successfully while the workflow itself failed. The UI must never report success merely because bytes were written.

### 2.3 Proposal, editable state, and approved truth are different

Forge distinguishes:

- source evidence;
- algorithmic or model proposal;
- user-created or corrected editable geometry;
- reviewed and approved project truth;
- exported derivative.

Raw model output does not become an approved shape, component, assembly, or export authority automatically.

### 2.4 Provenance is mandatory

Every material artifact identifies:

- originating project;
- workflow family or operation;
- schema and contract versions;
- input artifact IDs;
- source asset and hash where applicable;
- actor: user, algorithm, or model;
- creation and update time;
- application version;
- parent and superseded artifact IDs;
- validation and approval state;
- intended output profile and known limitations where applicable.

### 2.5 Historical files are preserved

Approved prior versions, raw proposals, rejected candidates, and superseded artifacts remain historically inspectable unless an explicit retention policy later authorises removal.

State changes require durable records. Moving files between directories is not sufficient authority by itself.

### 2.6 Open and inspectable formats are preferred

Primary structured formats:

- JSON;
- JSON Lines for append-only history;
- Markdown for human-readable reports;
- SVG and PNG for Stage One interchange;
- documented GLB/glTF and OBJ profiles for Stage Two interchange.

Binary-only project authority should be avoided where a durable inspectable representation is practical.

---

## 3. Project artifact layout

The target project structure is:

```text
project-name/
├── project.json
├── README.md
├── source/
│   ├── originals/
│   └── previews/
├── findings/
│   ├── raw/
│   ├── approved/
│   ├── rejected/
│   └── superseded/
├── structures/
│   ├── shape-documents/
│   │   └── .autosave/
│   ├── extraction-candidates/
│   ├── approved-shapes/
│   ├── construction-recipes/
│   ├── components/
│   └── assemblies/
├── briefs/
├── prompts/
├── diagnostics/
├── logs/
├── history/
└── exports/
```

Rules:

- a directory is created only after its schema and authority contract are implemented;
- accepted source originals remain unchanged;
- autosave remains separate from canonical truth;
- exports are derivatives, not project authority replacements;
- SQLite indexes files by project-relative path and remains rebuildable.

---

## 4. Core artifact classes

The Stage One–Two product uses approximately 14 core durable artifact classes.

| Class | Purpose | Typical authority |
|---|---|---|
| Project manifest | Project identity and declared current state | Canonical |
| Project history event | Append-only material state change | Canonical history |
| Source asset record | Source identity, hash, origin, rights notes, project path | Canonical |
| Source preview record | Rebuildable bounded preview metadata | Derived |
| Native shape document | Editable 2D geometry and replayable command state | Canonical current revision |
| Extraction candidate | Manual, algorithmic, or AI-proposed editable geometry | Raw/editable |
| Approved Shape Library asset | Reviewed reusable shape and compatibility declarations | Approved truth |
| Review/approval record | Approval, rejection, correction request, or review decision | Canonical decision |
| Supersession/version record | Relationship between historical and current versions | Canonical decision |
| Job/evidence record | Execution, progress, terminal state, output and diagnostics | Evidence |
| Construction recipe | Reversible shape/primitive-to-component derivation | Canonical editable recipe |
| Component document | Editable 3D component, transform, parent and validation | Canonical current revision |
| Assembly document | Hierarchy, instances, anchors, connectors and relationships | Canonical current revision |
| Export/Forge Pack record | Named profile, validation, derivatives, provenance, limitations | Derived handoff |

Optional concept briefs, prompt packs, source-art findings, modular proposals, and recommendations remain additional planning artifacts. They do not replace geometry authority.

---

## 5. Identity and naming

Every durable artifact has a stable unique ID.

Recommended patterns:

```text
project_<safe-slug>_<short-id>
source_<utc-stamp>_<short-id>
shape_doc_<utc-stamp>_<short-id>
shape_<utc-stamp>_<short-id>
recipe_<utc-stamp>_<short-id>
component_<utc-stamp>_<short-id>
assembly_<utc-stamp>_<short-id>
job_<utc-stamp>_<short-id>
export_<utc-stamp>_<short-id>
```

Rules:

- IDs remain stable after file rename;
- filenames are safe, deterministic where required, and collision-resistant;
- the original source filename is preserved in provenance;
- UTC timestamps are used for generated names and events;
- no canonical artifact is silently overwritten;
- later versions use explicit version and supersession relationships.

---

## 6. Shared metadata contract

Every material artifact schema includes or references these fields where applicable:

```json
{
  "schema_name": "mxztar_forge_example",
  "schema_version": "1.0.0",
  "artifact_id": "shape_20260722T000000Z_a8f2c1",
  "artifact_type": "approved_shape",
  "project_id": "project_example",
  "status": "valid",
  "approval_state": "approved",
  "created_at_utc": "2026-07-22T00:00:00Z",
  "updated_at_utc": "2026-07-22T00:00:00Z",
  "application": {
    "name": "MXZTAR Forge v2.0",
    "version": "0.0.0-development"
  },
  "actor": {
    "type": "user",
    "identifier": null
  },
  "provenance": {},
  "validation": {},
  "integrity": {},
  "limitations": [],
  "parent_artifact_ids": [],
  "supersedes_artifact_ids": []
}
```

A specialised schema may use different internal structure, but it must preserve equivalent identity, provenance, validation, integrity, and lifecycle information.

---

## 7. Shared status values

### Execution status

Allowed terminal and transient job states:

```text
queued
running
succeeded
failed
cancelled
timed_out
partially_succeeded
```

Rules:

- `queued` and `running` are transient;
- durable job records normally use a terminal state;
- `partially_succeeded` explains exactly what succeeded and failed;
- `failed` contains an error object;
- `succeeded` contains no fatal validation error;
- `cancelled` records who or what cancelled the job;
- `timed_out` records the configured timeout and cancellation/cleanup result.

### Artifact validity status

```text
valid
invalid
recovery_required
read_only
migrated
superseded
```

### Approval state

```text
not_applicable
raw
editable_candidate
review_requested
correction_requested
approved
rejected
superseded
```

Approval is never inferred from successful generation or file storage.

---

## 8. Actor and provenance contract

Actor type:

```text
user
algorithm
model
migration
system_recovery
```

The provenance object should include:

```json
{
  "source_asset_ids": [],
  "source_hashes": [],
  "source_regions": [],
  "parent_artifact_ids": [],
  "workflow_family": "S5_shape_editing",
  "operation_type": "add_rectangle",
  "job_id": null,
  "model": null,
  "user_purpose": "",
  "user_notes": "",
  "coordinate_space": "cartesian_2d_top_left_y_down",
  "units": "px"
}
```

Rules:

- project-relative paths are preferred;
- absolute paths appear only where required for diagnostics and are not portable authority;
- SHA-256 is used for content identity where implemented;
- missing values are `null` or absent, never fabricated;
- user purpose and intent remain distinct from machine observation;
- model-proposed geometry identifies model, prompt/contract, and source region.

---

## 9. Validation and integrity contract

A validation record includes:

```json
{
  "is_valid": true,
  "validator_name": "shape_document_validator",
  "validator_version": "1.0.0",
  "validated_at_utc": "2026-07-22T00:00:00Z",
  "checks": [
    {
      "name": "required_fields_present",
      "passed": true,
      "message": "All required fields are present."
    }
  ],
  "warnings": []
}
```

Integrity may include:

- content SHA-256;
- manifest relationship validation;
- file-size boundary;
- command-history boundary;
- parent existence;
- version/supersession consistency;
- output-profile checksum.

A file may be written but fail validation. In that case it does not become canonical approved truth.

---

## 10. Error contract

A failed workflow or transaction records:

```json
{
  "category": "validation_failed",
  "code": "SHAPE_DOCUMENT_INVALID",
  "message": "The shape document did not pass validation.",
  "technical_detail": "",
  "recoverable": true,
  "suggested_action": "Restore the last canonical revision or correct the invalid field.",
  "exception_type": null,
  "stage": "pre_commit_validation"
}
```

Initial error categories include:

```text
project_missing
project_locked
project_read_only
project_recovery_required
schema_unsupported
migration_unavailable
source_missing
source_unreadable
source_unsupported
source_decode_error
compatibility_blocked
operation_invalid
geometry_invalid
model_unavailable
model_missing
model_http_error
model_timeout
model_output_empty
model_output_malformed
validation_failed
storage_failed
transaction_failed
rollback_failed
permission_denied
cancelled_by_user
unexpected_internal_error
```

User-facing explanations remain understandable. Technical detail is preserved without becoming the only explanation.

---

## 11. Project manifest contract

`project.json` is authoritative for project identity and declared current state, validated against durable artifact files.

It includes:

- schema and project identity;
- exact creator Purpose;
- safe project display name and directory identity;
- creation/update/application versions;
- project status;
- source asset IDs;
- current artifact IDs;
- approved artifact IDs;
- superseded artifact IDs;
- history path;
- integrity fields.

Creating a project appends a durable `project_created` event containing the exact Purpose and derived name/slug result.

---

## 12. Project history event contract

Material state changes append JSON Lines events such as:

```text
project_created
project_opened
project_closed
project_recovered
source_imported
source_processed
shape_document_created
editor_command_applied
shape_saved
shape_review_requested
shape_approved
shape_rejected
shape_superseded
construction_recipe_created
component_regenerated
assembly_saved
export_created
migration_applied
```

A history event contains:

- event ID;
- event type and version;
- project ID;
- actor;
- timestamp;
- affected artifact IDs;
- concise parameters or references;
- result status;
- integrity reference where required.

History supplements canonical artifacts; it does not override a valid newer canonical file without an explicit reconstruction rule.

---

## 13. Source asset and preview contracts

### Source asset

Contains:

- source asset ID;
- project-relative original path;
- original filename;
- MIME type and accepted format;
- size, dimensions, and frame rule where applicable;
- SHA-256;
- origin and rights notes where supplied;
- model-ready classification;
- import and processing history.

External source bytes are never modified.

### Preview

Contains:

- parent source asset ID and hash;
- project-relative preview path;
- bounded dimensions and colour mode;
- decoder and preview version;
- rebuildable classification;
- creation and validation time.

A preview is never source authority.

---

## 14. Native shape document contract

The current native schema is `mxztar_forge_shape_document` version `1.0.0`.

A shape document includes:

- document and project identity;
- title and lifecycle state;
- canvas, coordinate space, units, and bounds;
- source relationships;
- layers and objects;
- replayable command history and cursor;
- revision and integrity;
- autosave/canonical relationship;
- approval and supersession fields where applicable.

Rules:

- document and history sizes remain bounded;
- commands are validated before application;
- autosave is separate from canonical truth;
- explicit save uses a multi-file transaction and rollback;
- stale `.tmp` files cannot replace canonical truth;
- an interrupted transaction marker forces explicit read-only recovery;
- unsupported commands or schema versions fail closed.

---

## 15. Extraction candidate contract

A candidate records:

- candidate ID and origin type: manual, algorithmic, or model;
- parent source asset and exact source region;
- editable path/node representation;
- open/closed contours, holes, bounds, and winding where applicable;
- extraction settings or model identity;
- confidence and limitations where generated;
- correction history;
- approval state beginning as `editable_candidate` or `raw`;
- parent/child relationships when converted into a shape document.

A candidate is not an approved Shape Library asset.

---

## 16. Approved Shape Library asset contract

An approved shape contains:

- stable shape ID and approved version;
- editable native geometry;
- source-derived or scratch-built origin classification;
- fill, stroke, layers, groups, anchors, bounds, centre, and symmetry axes where used;
- source and parent provenance;
- dimensional assumptions and confidence;
- intended role: profile, panel, trim, cutout, path, decoration, volume source, or connector;
- compatible construction recipes and output profiles;
- durable approval record;
- correction and supersession history.

Approved assets remain reopenable and editable. Exported SVG or PNG files do not replace the native approved asset.

---

## 17. Review, approval, rejection, and supersession contracts

A review decision records:

- review ID;
- target artifact and revision;
- decision type;
- approving/reviewing actor;
- timestamp;
- user corrections or notes;
- validation snapshot;
- resulting artifact IDs;
- superseded IDs where applicable.

Approval does not mutate or delete the original raw candidate. A corrected derivative may be approved while the original remains historical.

---

## 18. Job and evidence contract

A job record includes:

- job and workflow IDs;
- inputs and expected output classes;
- algorithm or model identity;
- hardware/resource policy;
- timeout and attempt;
- start, heartbeat, cancellation, and completion data;
- terminal status;
- saved output artifact IDs;
- diagnostic path;
- error object;
- recommended next action.

Jobs remain inspectable through the Jobs workspace. Evidence is not automatically approval authority.

---

## 19. Construction recipe contract

A recipe includes:

- recipe ID and version;
- parent approved shape or declared primitive;
- method: extrude, revolve, sweep, loft, relief, shell, or bevel;
- units, axes, origin, pivot, and parameters;
- assumptions and limitations;
- generated component ID;
- regeneration history;
- validation result;
- actor and provenance.

Changing a recipe regenerates a component derivative without destroying the parent shape.

---

## 20. Component contract

A component includes:

- component ID and revision;
- construction recipe or primitive parent;
- geometry representation;
- units, bounds, axes, origin, pivot, and transform;
- anchors and connectors;
- visibility, lock, instance, and hierarchy state;
- normals, open-boundary, intersection, and limitation checks;
- parent and supersession history.

A baked component is a new explicit derivative. It does not silently replace reversible history.

---

## 21. Assembly contract

An assembly includes:

- assembly ID and revision;
- component and instance IDs;
- hierarchy;
- transforms;
- anchors and connectors;
- declared relationships: group, assembly, contact/mate, stitch/weld, join mesh, boolean, separate, or bake;
- construction history;
- validation and limitations;
- export-profile compatibility.

The operation name determines the artifact meaning. A vague `join` state is prohibited.

---

## 22. Export and Forge Pack contract

An export record contains:

- export ID;
- approved input artifact IDs;
- named output profile and version;
- target program or generic profile;
- units, scale, axis, origin, pivot, hierarchy, naming, and material rules;
- validation checks;
- generated project-relative files and checksums;
- provenance graph;
- known losses and limitations;
- downstream import, round-trip, or continuation evidence where required.

Core Stage One profiles:

- SVG;
- PNG;
- Forge Pack.

Core Stage Two profiles:

- GLB/glTF;
- OBJ.

A Forge Pack contains deterministic JSON and human-readable documentation plus named approved derivatives. It is not a second editable project authority.

---

## 23. Optional agent and planning artifacts

Optional Agent Workflow outputs may include:

- source-art intelligence finding;
- shape/structure planning map;
- modular-system proposal;
- prototype concept;
- concept brief;
- render prompt pack;
- next-step recommendation.

They use the shared identity, execution, provenance, validation, error, and approval rules.

They remain planning or evidence artifacts unless a Stage One or Stage Two workflow converts reviewed material into an editable native artifact.

---

## 24. Transactions, autosave, and recovery

Material multi-file writes use:

1. pre-commit validation;
2. transaction marker where interruption could create competing truth;
3. atomic temporary writes;
4. canonical replacement;
5. manifest/history update;
6. post-write validation;
7. rollback on failure;
8. marker removal only after confirmed success or confirmed rollback.

Autosave:

- is project-owned;
- is bounded;
- never silently becomes canonical;
- may be offered as a newer recovery candidate;
- is cleared after a successful explicit canonical save where appropriate.

Uncertain rollback or interrupted transaction reopens read-only until resolved.

---

## 25. Schema migration

Every runtime-written schema has:

- schema name and semantic version;
- current validator;
- supported read versions;
- explicit migration path where offered;
- pre-migration backup or rollback rule;
- migration history event;
- post-migration validation.

Assessment alone must not mutate a project. Unsupported future schemas fail closed or attach read-only.

---

## 26. Size and workload boundaries

Every artifact class defines appropriate limits for:

- file size;
- collection count;
- command/history length;
- geometry complexity;
- preview dimensions;
- job duration;
- memory/resource class.

Limits are checked before unreadable or unmanageable bytes become canonical truth.

---

## 27. Artifact verification

Each artifact class requires proportionate evidence:

- schema fixture validation;
- round-trip serialization;
- invalid and oversized input rejection;
- transaction interruption and rollback;
- approval/supersession reconstruction;
- project copy and index rebuild;
- UI truthful status;
- downstream import or continuation for output profiles.

No artifact contract is considered verified solely because an example appears in this document.
