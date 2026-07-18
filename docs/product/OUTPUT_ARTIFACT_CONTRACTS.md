# MXZTAR-forge v2.0 — Output Artifact Contracts

## 1. Purpose

This document defines the durable files produced by MXZTAR-forge v2.0 workflows.

Its purpose is to ensure that workflow outputs are:

* structured;
* traceable;
* reviewable;
* recoverable;
* versioned;
* distinguishable as success or failure;
* safe to reuse in later workflows;
* understandable outside the application.

A workflow is not complete merely because text appears in the interface.

A workflow is complete only when its result is:

1. validated;
2. saved;
3. correctly classified;
4. traceable to its source;
5. visible to the user;
6. available for later project use.

---

## 2. Core Artifact Principles

### 2.1 Files are product outputs

Saved artifacts are part of the product, not implementation leftovers.

They must remain usable when:

* the application is closed;
* the project is copied;
* the machine is restored;
* the user changes versions;
* a later workflow consumes the result;
* the user inspects the project manually.

---

### 2.2 Success and storage are separate states

The system must distinguish:

```text
output saved
```

from:

```text
workflow succeeded
```

A diagnostic failure record may be saved successfully while the workflow itself failed.

The interface must never report a workflow as successful merely because a file was written.

---

### 2.3 Raw model output is not project truth

Model-generated results begin as raw findings.

They become approved project material only after explicit user approval or a future documented approval rule.

Initial approval states:

```text
raw
approved
rejected
superseded
```

---

### 2.4 Provenance is mandatory

Every durable workflow artifact must identify:

* the originating project;
* the workflow;
* the workflow contract version;
* the source asset;
* the source hash where available;
* the model used;
* the creation time;
* the application version;
* the parent artifact where applicable.

---

### 2.5 User files remain inspectable

Artifacts must use open, inspectable formats where practical.

Primary structured format:

```text
JSON
```

Human-readable companion formats may include:

```text
Markdown
TXT
PNG
SVG
```

Binary-only project state should be avoided for first-release planning outputs.

---

## 3. Project Artifact Layout

The first-release project structure should follow this contract:

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
│   ├── raw/
│   ├── approved/
│   └── superseded/
├── briefs/
│   ├── draft/
│   ├── approved/
│   └── superseded/
├── prompts/
│   ├── draft/
│   ├── approved/
│   └── superseded/
├── recommendations/
├── exports/
├── diagnostics/
├── logs/
└── history/
```

Not every directory must be populated immediately.

The directory contract exists so later workflows do not invent competing storage locations.

---

## 4. Artifact Identity

Every durable artifact must have a unique identifier.

Recommended format:

```text
art_<utc-timestamp>_<short-random-id>
```

Example:

```text
art_20260625T041530Z_a8f2c1
```

The identifier must remain stable after creation.

Renaming the file must not change the artifact ID stored inside the artifact.

---

## 5. Filename Contract

Recommended filename pattern:

```text
<workflow-key>__<source-stem>__<utc-timestamp>__<artifact-id>.<extension>
```

Example:

```text
source_art_intelligence__mxztar_test_shapes__20260625T041530Z__art_20260625T041530Z_a8f2c1.json
```

Rules:

* use lowercase;
* replace spaces with underscores;
* remove unsafe filesystem characters;
* preserve the original source filename inside provenance;
* use UTC timestamps in filenames;
* do not silently overwrite an existing artifact;
* create a new artifact for each run;
* use explicit supersession links rather than replacing historical files.

---

## 6. Shared Artifact Envelope

Every JSON artifact must contain a common top-level envelope.

```json
{
  "schema_name": "mxztar_forge_output_artifact",
  "schema_version": "1.0.0",
  "artifact_id": "art_20260625T041530Z_a8f2c1",
  "artifact_type": "workflow_result",
  "workflow_key": "source_art_intelligence",
  "workflow_contract_version": "1.0.0",
  "project_id": "project_example",
  "status": "succeeded",
  "approval_state": "raw",
  "created_at_utc": "2026-06-25T04:15:30Z",
  "completed_at_utc": "2026-06-25T04:16:12Z",
  "elapsed_seconds": 42.0,
  "application": {
    "name": "MXZTAR-forge v2.0",
    "version": "0.0.0-development"
  },
  "execution": {},
  "provenance": {},
  "result": {},
  "validation": {},
  "recommendation": {},
  "error": null
}
```

---

## 7. Shared Status Values

Allowed workflow result status values:

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

* `queued` and `running` are transient execution states;
* durable final artifacts should normally use a terminal state;
* `partially_succeeded` must include an explanation;
* `failed` must include an error object;
* `succeeded` must not contain a fatal error;
* `cancelled` must state who or what cancelled the run;
* `timed_out` must record the configured timeout.

---

## 8. Shared Approval States

Allowed approval states:

```text
not_applicable
raw
approved
rejected
superseded
```

Use:

* `not_applicable` for diagnostics and execution logs;
* `raw` for newly generated findings;
* `approved` after explicit user approval;
* `rejected` after explicit user rejection;
* `superseded` when a newer artifact replaces it conceptually.

Approval must not be inferred from successful generation.

---

## 9. Execution Metadata Contract

The `execution` object should contain:

```json
{
  "run_id": "run_20260625T041530Z_39fd10",
  "model_provider": "ollama",
  "model_name": "qwen2.5vl:3b",
  "model_digest": null,
  "host_mode": "local",
  "thread_limit": 2,
  "parallel_limit": 1,
  "timeout_seconds": 300,
  "attempt_number": 1,
  "triggered_by": "user",
  "worker_type": "qt_thread_worker"
}
```

Required fields:

* run ID;
* model provider;
* model name;
* local or remote mode;
* timeout;
* attempt number;
* trigger source.

Optional fields:

* model digest;
* hardware profile;
* temperature;
* seed;
* prompt token count;
* output token count;
* retry reason.

---

## 10. Provenance Contract

The `provenance` object should contain:

```json
{
  "source_assets": [
    {
      "asset_id": "asset_001",
      "project_relative_path": "source/originals/mxztar_test_shapes.png",
      "original_filename": "mxztar_test_shapes.png",
      "mime_type": "image/png",
      "size_bytes": 123456,
      "width_px": 1000,
      "height_px": 1000,
      "sha256": "example-hash"
    }
  ],
  "parent_artifact_ids": [],
  "user_notes": "",
  "user_intent": "",
  "prompt_contract_key": "source_art_intelligence",
  "prompt_contract_version": "1.0.0"
}
```

Rules:

* project-relative paths are preferred;
* absolute paths may be recorded only in diagnostics where necessary;
* hashes should use SHA-256;
* missing hashes must be represented as `null`, not fabricated;
* parent artifacts must be identified explicitly;
* user intent must remain distinct from machine-generated findings.

---

## 11. Validation Contract

The `validation` object should contain:

```json
{
  "is_valid": true,
  "validator_version": "1.0.0",
  "validated_at_utc": "2026-06-25T04:16:12Z",
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

A result may be:

* successfully generated;
* successfully saved;
* but invalid against its artifact schema.

In that case, the final workflow status must not be `succeeded`.

Recommended classification:

```text
failed
```

or:

```text
partially_succeeded
```

depending on whether useful recoverable content exists.

---

## 12. Error Contract

When a workflow does not succeed, the `error` object must contain:

```json
{
  "category": "model_http_error",
  "code": "OLLAMA_HTTP_400",
  "message": "The local model service rejected the request.",
  "technical_detail": "400 Client Error: Bad Request",
  "recoverable": true,
  "suggested_action": "Verify the selected model and request payload, then retry.",
  "exception_type": "HTTPError",
  "stage": "model_request"
}
```

Allowed initial error categories:

```text
source_missing
source_unreadable
source_unsupported
source_decode_error
compatibility_blocked
model_unavailable
model_missing
model_http_error
model_timeout
model_output_empty
model_output_malformed
validation_failed
storage_failed
permission_denied
cancelled_by_user
unexpected_internal_error
```

The user-facing message should be understandable.

Technical details should be preserved in the artifact without becoming the only visible explanation.

---

## 13. Source-Art Intelligence Artifact

### Workflow key

```text
source_art_intelligence
```

### Directory

```text
findings/raw/
```

### Artifact type

```text
visual_intelligence_finding
```

### Required result fields

```json
{
  "summary": "",
  "visible_content": [],
  "structural_observations": [],
  "layer_observations": [],
  "reusable_motifs": [],
  "reusable_surfaces": [],
  "candidate_components": [],
  "production_possibilities": [],
  "uncertainties": [],
  "quality_notes": [],
  "recommended_next_workflow": ""
}
```

### Validation rules

A successful result must contain:

* a non-empty summary;
* at least one visible-content observation;
* at least one production-relevant observation;
* an uncertainty section;
* a recommended next workflow.

A generic image caption alone is invalid.

### Approval behaviour

New result:

```text
raw
```

User may approve:

* the full artifact;
* selected findings;
* a corrected derivative artifact.

Approved material moves conceptually to:

```text
findings/approved/
```

The original raw artifact remains preserved.

---

## 14. Shape and Structure Harvest Artifact

### Workflow key

```text
shape_structure_harvest
```

### Directory

```text
structures/raw/
```

### Artifact type

```text
shape_structure_map
```

### Required result fields

```json
{
  "major_silhouettes": [],
  "geometric_forms": [],
  "organic_forms": [],
  "repeated_forms": [],
  "layer_relationships": [],
  "structural_stacks": [],
  "perspective_cues": [],
  "extraction_zones": [],
  "vector_candidates": [],
  "raster_cutout_candidates": [],
  "manual_reconstruction_guidance": [],
  "priority_order": []
}
```

### Validation rules

A successful result must identify at least one of:

* silhouette;
* structure;
* repeated form;
* extraction zone.

The artifact must not claim that extraction has occurred unless an actual extracted file exists.

### Future child artifacts

Possible later outputs:

```text
SVG
PNG
mask files
coordinate maps
layer manifests
```

These are not automatically implied by this planning artifact.

---

## 15. Modular-Set Perspective Artifact

### Workflow key

```text
modular_set_perspective
```

### Directory

```text
structures/raw/
```

### Artifact type

```text
modular_system_proposal
```

### Required result fields

```json
{
  "observed_modules": [],
  "inferred_modules": [],
  "module_families": [],
  "relationships": [],
  "connection_rules": [],
  "repetition_rules": [],
  "naming_proposals": [],
  "two_dimensional_uses": [],
  "future_three_dimensional_uses": [],
  "production_order": [],
  "uncertainties": []
}
```

### Validation rules

The artifact must separate:

```text
observed_modules
```

from:

```text
inferred_modules
```

Speculative modules must never be presented as directly observed facts.

A successful result must contain at least one module or an explicit valid finding that the source is unsuitable for modular interpretation.

---

## 16. Prototype Imagination Artifact

### Workflow key

```text
prototype_imagination
```

### Directory

```text
findings/raw/
```

### Artifact type

```text
prototype_concept
```

### Required result fields

```json
{
  "prototype_name": "",
  "problem_statement": "",
  "proposed_function": "",
  "source_influences": [],
  "speculative_extensions": [],
  "primary_components": [],
  "interaction_model": [],
  "intended_users": [],
  "production_considerations": [],
  "constraints": [],
  "risks": [],
  "next_validation_step": ""
}
```

### Validation rules

A successful artifact must:

* identify a problem or intended function;
* distinguish source influence from speculation;
* contain at least one constraint;
* avoid unsupported engineering, safety, or certification claims.

---

## 17. Concept Brief Artifact

### Workflow key

```text
concept_brief
```

### Directory

Initial state:

```text
briefs/draft/
```

Approved state:

```text
briefs/approved/
```

### Artifact type

```text
concept_brief
```

### Required result fields

```json
{
  "title": "",
  "production_objective": "",
  "audience_or_user": "",
  "problem_or_opportunity": "",
  "intended_use": "",
  "visual_direction": [],
  "approved_motifs": [],
  "approved_structures": [],
  "required_deliverables": [],
  "constraints": [],
  "exclusions": [],
  "risks": [],
  "production_sequence": [],
  "acceptance_criteria": [],
  "recommended_next_workflow": ""
}
```

### Validation rules

A successful concept brief must contain:

* a title;
* a production objective;
* intended use;
* at least one deliverable;
* at least one constraint;
* acceptance criteria.

A brief must not silently treat raw findings as approved findings.

---

## 18. Render Prompt Pack Artifact

### Workflow key

```text
render_prompt_pack
```

### Directory

Initial state:

```text
prompts/draft/
```

Approved state:

```text
prompts/approved/
```

### Artifact type

```text
render_prompt_pack
```

### Required result fields

```json
{
  "title": "",
  "intended_output": "",
  "target_model": null,
  "primary_prompt": "",
  "controlled_variants": [],
  "composition_variants": [],
  "material_variants": [],
  "lighting_variants": [],
  "negative_constraints": [],
  "consistency_anchors": [],
  "model_specific_notes": [],
  "provenance_summary": ""
}
```

### Validation rules

A successful prompt pack must contain:

* one primary prompt;
* at least one controlled variation;
* negative or exclusion constraints;
* intended output;
* provenance summary.

A single unstructured paragraph is not a valid prompt pack.

---

## 19. Recommend Next Step Artifact

### Workflow key

```text
recommend_next_step
```

### Directory

```text
recommendations/
```

### Artifact type

```text
next_step_recommendation
```

### Required result fields

```json
{
  "primary_action": "",
  "reason": "",
  "required_input": [],
  "expected_result": "",
  "compatibility_status": "",
  "what_not_to_do_yet": [],
  "alternative_actions": []
}
```

### Validation rules

A successful result must contain exactly one primary action.

Alternative actions may exist, but must not replace prioritisation.

The recommendation must not reference:

* unavailable controls;
* nonexistent workflows;
* missing project artifacts as if they exist.

---

## 20. Compatibility Assessment Artifact

Compatibility assessment may be transient in the interface, but when saved it should use:

### Directory

```text
history/
```

### Artifact type

```text
workflow_compatibility_assessment
```

### Required fields

```json
{
  "workflow_key": "",
  "status": "ready",
  "reason": "",
  "missing_requirements": [],
  "recommended_improvements": [],
  "can_run": true,
  "recommended_alternative": null,
  "expected_output": ""
}
```

Allowed status values:

```text
ready
caution
blocked
```

---

## 21. Diagnostic Artifact

### Directory

```text
diagnostics/
```

### Artifact type

```text
workflow_diagnostic
```

### Approval state

```text
not_applicable
```

### Required fields

```json
{
  "run_id": "",
  "workflow_key": "",
  "failure_stage": "",
  "source_summary": {},
  "execution_summary": {},
  "error": {},
  "recovery_actions": [],
  "related_artifact_ids": []
}
```

A diagnostic artifact must never be placed in an approved findings directory.

---

## 22. Execution Log Artifact

### Directory

```text
logs/
```

### Recommended filename

```text
run_<run-id>.jsonl
```

### Format

JSON Lines.

Each line represents one event.

Example:

```json
{"timestamp_utc":"2026-06-25T04:15:30Z","event":"run_started","run_id":"run_001"}
{"timestamp_utc":"2026-06-25T04:15:31Z","event":"source_validated","run_id":"run_001"}
{"timestamp_utc":"2026-06-25T04:16:12Z","event":"run_failed","run_id":"run_001"}
```

Initial event types:

```text
run_queued
run_started
source_validated
compatibility_assessed
model_request_started
heartbeat
model_response_received
validation_started
validation_failed
artifact_saved
run_succeeded
run_failed
run_cancelled
run_timed_out
```

Logs should support troubleshooting without becoming the only record of the result.

---

## 23. Project History Artifact

### Directory

```text
history/
```

### Recommended format

```text
project_history.jsonl
```

Project history events may include:

```text
project_created
source_added
source_removed
workflow_run
finding_approved
finding_rejected
artifact_superseded
brief_approved
prompt_pack_approved
export_created
project_restored
schema_migrated
```

History should be append-oriented.

Earlier records should not be rewritten without a documented migration.

---

## 24. Approval Derivative Contract

When selected raw findings are approved, the system should create an approval derivative rather than altering the original artifact invisibly.

Example:

```json
{
  "schema_name": "mxztar_forge_approval_record",
  "schema_version": "1.0.0",
  "approval_id": "approval_001",
  "source_artifact_id": "art_001",
  "approved_at_utc": "2026-06-25T05:00:00Z",
  "approved_by": "user",
  "approved_content": [
    {
      "field": "reusable_motifs",
      "item_indexes": [0, 2]
    }
  ],
  "user_corrections": [],
  "notes": ""
}
```

This preserves:

* the original raw output;
* the user’s approval decision;
* later corrections;
* downstream provenance.

---

## 25. Supersession Contract

When an artifact is replaced conceptually, the newer artifact should record:

```json
{
  "supersedes_artifact_ids": [
    "art_older"
  ]
}
```

The older artifact should not be deleted automatically.

Its approval state may become:

```text
superseded
```

Supersession must not erase project history.

---

## 26. Storage Failure Behaviour

If artifact storage fails after model execution:

* do not report full success;
* preserve the result in memory long enough to offer retry where practical;
* record the storage error;
* identify the intended path;
* avoid overwriting unrelated files;
* do not silently discard the model result.

Recommended final status:

```text
partially_succeeded
```

if the generated content is still recoverable.

Otherwise:

```text
failed
```

---

## 27. Atomic Save Requirement

Structured artifacts should be saved atomically where practical.

Recommended sequence:

1. write to a temporary file in the target directory;
2. flush and close;
3. validate the temporary file;
4. rename into the final path;
5. record the final path;
6. update project history.

This reduces the risk of partially written JSON after interruption.

---

## 28. Overwrite Policy

The system must not silently overwrite durable artifacts.

Allowed behaviours:

* create a new artifact;
* create a versioned derivative;
* explicitly replace through a confirmed migration;
* mark an earlier artifact as superseded.

Disallowed behaviour:

```text
write new result over an existing approved artifact without warning
```

---

## 29. Schema Versioning

Initial shared schema version:

```text
1.0.0
```

Version format:

```text
major.minor.patch
```

Use:

* major for incompatible structural changes;
* minor for backward-compatible field additions;
* patch for clarifications and validation fixes.

Every artifact must include:

```text
schema_name
schema_version
```

---

## 30. Migration Expectations

When schema changes occur, the system should:

* detect the artifact schema version;
* preserve the original artifact;
* create a migrated derivative or backup;
* record the migration;
* validate the migrated artifact;
* report failures clearly;
* never pretend migration succeeded when validation failed.

Future migration record example:

```json
{
  "migration_id": "migration_001",
  "source_schema_version": "1.0.0",
  "target_schema_version": "1.1.0",
  "source_artifact_id": "art_001",
  "migrated_artifact_id": "art_002",
  "status": "succeeded",
  "created_at_utc": "2026-06-25T06:00:00Z"
}
```

---

## 31. Manual Inspection Requirement

A user opening a saved JSON artifact should be able to determine:

* what workflow created it;
* what source it came from;
* whether it succeeded;
* whether it was approved;
* when it was created;
* what model was used;
* what result was produced;
* what should happen next;
* whether an error occurred.

The application must not require hidden database knowledge to interpret core workflow files.

---

## 32. Privacy Requirements

Artifacts must not unnecessarily record:

* home-directory details;
* unrelated absolute paths;
* environment secrets;
* API keys;
* access tokens;
* passwords;
* hidden system prompts containing secrets;
* unrelated personal metadata.

Local diagnostic detail should be sufficient for repair without exposing credentials.

---

## 33. Source Ownership and Licensing Notes

The artifact system may record user-supplied ownership or licensing notes.

Example:

```json
{
  "rights_context": {
    "user_asserted_owner": true,
    "licence_notes": "",
    "commercial_use_status": "user_noted",
    "verification_status": "not_verified_by_application"
  }
}
```

The system must not claim legal verification it has not performed.

---

## 34. Minimum First-Release Artifact Set

The first rentable release should support durable artifacts for:

1. project metadata;
2. source asset metadata;
3. compatibility assessments;
4. source-art intelligence;
5. shape and structure harvest;
6. modular-set perspective;
7. concept brief;
8. render prompt pack;
9. next-step recommendation;
10. diagnostics;
11. execution logs;
12. project history;
13. approval records.

Prototype imagination may remain included if retained in the first-release workflow set.

---

## 35. Acceptance Criteria

The output artifact system is ready for implementation when:

1. every first-release workflow has an artifact type;
2. every artifact has a stable identity;
3. every artifact records provenance;
4. success and failure are distinguishable;
5. approval state is explicit;
6. raw findings remain preserved;
7. approved derivatives can be traced;
8. filenames cannot silently collide;
9. validation results are recorded;
10. storage failures are represented honestly;
11. project history can record major events;
12. schema versions are present;
13. future migrations can be supported;
14. users can inspect their files outside the application;
15. secrets and irrelevant private paths are excluded.

---

## 36. Decisions Still Required

The following remain planning decisions:

1. exact project ID format;
2. exact artifact ID generator;
3. whether SQLite indexes the artifact files;
4. whether JSON files or SQLite are authoritative;
5. whether approval records are separate files or embedded derivatives;
6. whether source images are copied or referenced;
7. maximum supported source size;
8. preview generation rules;
9. retention policy for diagnostics;
10. whether cancelled runs save partial model output;
11. how project exports package history and diagnostics;
12. how offline licensing interacts with project access;
13. whether users can edit structured artifacts manually;
14. how manual edits are detected and validated;
15. how future cloud-assisted workflows preserve provenance.

---

## 37. Next Planning Event

Create:

```text
docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md
```

That document must decide:

* which data source is authoritative;
* the relationship between JSON artifacts and SQLite;
* how project state is reconstructed;
* how concurrent writes are prevented;
* how corruption is detected;
* how backups and restoration work;
* how manually edited files are handled;
* how history, approvals, and supersession affect current state.

No project-state implementation should begin until data authority is explicitly defined.

