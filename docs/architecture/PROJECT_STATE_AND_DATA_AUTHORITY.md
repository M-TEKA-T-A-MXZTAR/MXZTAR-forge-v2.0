# MXZTAR-forge v2.0 — Project State and Data Authority

## 1. Purpose

This document defines how MXZTAR-forge v2.0 stores, reconstructs, validates, and protects project state.

Its purpose is to prevent competing sources of truth between:

* JSON artifacts;
* SQLite indexes;
* project metadata;
* approval records;
* history logs;
* cached UI state;
* manually edited files.

The system must always be able to answer:

* What is authoritative?
* What is derived?
* What can be rebuilt?
* What happens if data sources disagree?
* How is corruption detected?
* How is state restored after interruption or machine failure?

---

## 2. Core Decision

### Durable project artifacts are authoritative

The authoritative record of project work is the set of durable project files stored inside the project directory.

These include:

* `project.json`;
* source asset metadata;
* workflow artifacts;
* approval records;
* supersession records;
* project history;
* structured diagnostics;
* approved briefs;
* approved prompt packs.

### SQLite is an index and acceleration layer

SQLite may be used for:

* fast lookup;
* filtering;
* sorting;
* UI state;
* recent-project lists;
* search indexes;
* artifact summaries;
* cached compatibility assessments;
* execution queues;
* resumable job metadata.

SQLite is not the sole source of truth for durable creative work.

If the database is lost or corrupted, the project must remain recoverable from project files.

---

## 3. Authority Hierarchy

When data sources disagree, use this order:

1. validated durable artifact files;
2. signed or hashed approval and supersession records;
3. append-only project history;
4. `project.json`;
5. rebuilt SQLite index;
6. cached UI state;
7. transient in-memory state.

Lower-priority data must never silently override higher-priority data.

---

## 4. Project Directory as Recovery Boundary

Each project directory is a self-contained recovery boundary.

A copied project should preserve:

* project identity;
* source references;
* source metadata;
* workflow results;
* approvals;
* rejections;
* supersession history;
* briefs;
* prompts;
* diagnostics;
* logs;
* project history.

The user should not require the original machine-wide SQLite database to reopen a project.

---

## 5. `project.json` Contract

`project.json` is the project manifest.

It should contain:

```json
{
  "schema_name": "mxztar_forge_project",
  "schema_version": "1.0.0",
  "project_id": "project_example",
  "project_name": "Example Project",
  "created_at_utc": "2026-06-25T00:00:00Z",
  "updated_at_utc": "2026-06-25T00:00:00Z",
  "application_version_created": "0.0.0-development",
  "application_version_last_opened": "0.0.0-development",
  "project_status": "active",
  "primary_goal": "",
  "source_asset_ids": [],
  "current_artifact_ids": [],
  "approved_artifact_ids": [],
  "superseded_artifact_ids": [],
  "last_recommendation_artifact_id": null,
  "history_path": "history/project_history.jsonl",
  "integrity": {
    "manifest_sha256": null,
    "last_validated_at_utc": null
  }
}
```

The manifest is authoritative for project identity and declared current state, but it must be validated against the actual artifact files.

---

## 6. Derived SQLite Data

SQLite records may include:

* project ID;
* project path;
* project name;
* last opened time;
* artifact ID;
* artifact type;
* workflow key;
* status;
* approval state;
* source asset ID;
* created time;
* validation status;
* user-facing summary;
* search text;
* file path.

Every SQLite artifact row must reference a durable project-relative file path.

A database row without a corresponding durable artifact must be treated as stale or invalid.

---

## 7. Rebuild Contract

The SQLite index must be rebuildable from project files.

A rebuild should:

1. locate the project directory;
2. validate `project.json`;
3. enumerate durable artifacts;
4. validate schema names and versions;
5. identify approvals and supersession links;
6. reconstruct current project state;
7. rebuild database rows;
8. record warnings for missing or conflicting files;
9. preserve original files;
10. report the rebuild result.

Rebuild must not modify project artifacts unless a separate migration is explicitly performed.

---

## 8. Current-State Reconstruction

Current project state is reconstructed from:

* project manifest;
* durable artifacts;
* approval records;
* supersession records;
* history events.

For each artifact:

1. validate file structure;
2. read artifact ID;
3. read status;
4. read approval state;
5. identify parent artifacts;
6. identify superseded artifacts;
7. identify approval derivatives;
8. determine whether the artifact is current;
9. index the result.

An artifact is current when it is:

* valid;
* not rejected;
* not superseded;
* not replaced by a later approved derivative;
* relevant to the current project manifest.

---

## 9. Raw, Approved, Rejected, and Superseded State

### Raw

Generated but not accepted as project truth.

### Approved

Explicitly accepted by the user.

### Rejected

Explicitly excluded from downstream project truth.

### Superseded

Historically preserved but replaced conceptually by a newer artifact.

State changes must be represented by durable records.

The system must not rely only on moving files between directories.

---

## 10. Approval Authority

User approval is authoritative.

A successful workflow run does not imply approval.

Approval should create a durable approval record containing:

* approval ID;
* source artifact ID;
* approved content;
* user corrections;
* approval time;
* approving actor;
* notes.

Downstream workflows should prefer approved material where available.

---

## 11. Supersession Authority

Supersession must be explicit.

A newer artifact may supersede one or more older artifacts.

The newer artifact or a dedicated supersession record must identify:

```json
{
  "supersedes_artifact_ids": [
    "art_older"
  ]
}
```

The older artifact remains preserved.

Its historical existence must remain visible in project history.

---

## 12. History Authority

`project_history.jsonl` is append-oriented.

It records major project events, including:

* project creation;
* source addition;
* workflow execution;
* workflow failure;
* approval;
* rejection;
* supersession;
* migration;
* export;
* restoration;
* database rebuild;
* manual-edit detection.

History is not the only source of truth, but it is the authoritative event trail.

A missing history line must not erase an otherwise valid artifact.

---

## 13. Write Ordering

Durable writes should follow this order:

1. validate input;
2. create run ID;
3. record run start;
4. generate result;
5. validate result;
6. write artifact to temporary file;
7. flush and close;
8. re-read and validate temporary file;
9. atomically rename to final path;
10. append project history event;
11. update `project.json`;
12. update SQLite index;
13. notify the UI.

SQLite must be updated after the durable artifact exists.

---

## 14. Atomicity Rules

The system should use atomic replacement where practical.

For new artifacts:

* write temporary file;
* validate;
* rename to final file.

For `project.json`:

* write `project.json.tmp`;
* validate;
* preserve prior manifest as backup where practical;
* atomically replace.

The system must not leave partially written JSON as valid state.

---

## 15. Concurrent-Write Prevention

Only one writer may modify a project at a time.

Initial desktop strategy:

* process-level project lock;
* lock file inside the project directory;
* unique writer ID;
* process ID;
* creation time;
* host identifier where practical.

Example:

```json
{
  "lock_schema": "mxztar_forge_project_lock",
  "writer_id": "writer_001",
  "process_id": 12345,
  "created_at_utc": "2026-06-25T00:00:00Z",
  "host": "mk-T1700"
}
```

A stale lock must not be removed silently.

The system should verify whether the owning process still exists before offering recovery.

---

## 16. Read-Only Recovery Mode

If project integrity is uncertain, the application should open the project in read-only recovery mode.

Read-only recovery mode should permit:

* inspection;
* validation;
* export;
* backup;
* diagnostic generation;
* database rebuild preview.

It should block:

* new workflow writes;
* approvals;
* supersession;
* migration;
* manifest replacement.

---

## 17. Corruption Detection

The system should detect:

* malformed JSON;
* missing required fields;
* duplicate artifact IDs;
* missing referenced artifacts;
* broken parent links;
* broken supersession links;
* invalid schema versions;
* hash mismatches;
* truncated history lines;
* database rows with missing files;
* manifest references to nonexistent files.

Corruption must be reported precisely.

The application must not silently “fix” uncertain project truth.

---

## 18. Hashing Policy

SHA-256 should be used for:

* source assets;
* durable artifacts where practical;
* project manifest integrity;
* export packages.

Hashes support:

* corruption detection;
* duplicate detection;
* manual-edit detection;
* provenance.

A missing hash must be represented as `null`.

A hash mismatch must not be ignored.

---

## 19. Manual File Edits

Users may inspect and edit their project files manually.

The application must distinguish:

* valid manual edit;
* invalid manual edit;
* schema-breaking edit;
* hash-changing edit;
* externally replaced file.

When a manual edit is detected:

1. do not overwrite it automatically;
2. validate the edited file;
3. compare hashes;
4. report the difference;
5. offer re-indexing if valid;
6. offer read-only recovery if invalid;
7. append a history event if accepted.

Manual edits should not automatically become approved project truth.

---

## 20. Database Corruption

If SQLite is corrupted:

* preserve the corrupt database;
* rename it with a timestamp;
* create a fresh database;
* rebuild from durable artifacts;
* report warnings;
* do not alter project artifacts.

Example preserved filename:

```text
mxztar_forge.sqlite.corrupt.20260625T000000Z
```

---

## 21. Missing Database

A missing SQLite database is recoverable.

The application should:

1. create a new database;
2. scan known project directories;
3. validate manifests;
4. rebuild indexes;
5. restore recent-project metadata where available.

The absence of SQLite must not destroy project access.

---

## 22. Missing Artifact

If `project.json` references a missing artifact:

* mark the project degraded;
* record the missing artifact ID;
* do not silently remove the reference;
* search expected directories;
* offer restore-from-backup guidance;
* permit read-only access where possible.

---

## 23. Orphan Artifact

An artifact is orphaned when it exists but is not referenced by the manifest or history.

The system should:

* validate it;
* identify its project ID;
* identify its provenance;
* present it for recovery review;
* avoid automatic deletion;
* allow deliberate reattachment.

---

## 24. Duplicate Artifact IDs

Duplicate artifact IDs are invalid.

The system must:

* stop automatic indexing of the conflicting records;
* report both file paths;
* preserve both files;
* require deliberate resolution;
* avoid generating a replacement ID silently.

---

## 25. Backup Contract

A valid project backup must include the complete project directory.

Recommended backup properties:

* timestamped;
* externally stored;
* integrity checked;
* restorable without SQLite;
* not dependent on application cache.

Project backups should preserve:

* source assets;
* manifests;
* artifacts;
* approvals;
* history;
* diagnostics;
* logs;
* exports.

---

## 26. Restoration Contract

Restoration should:

1. copy the project directory to a safe location;
2. validate all files;
3. verify hashes where present;
4. rebuild SQLite indexes;
5. identify missing or conflicting records;
6. open in read-only mode if integrity is uncertain;
7. append a restoration event only after successful validation.

Restoration must not overwrite an existing project without explicit confirmation.

---

## 27. Export Contract

A project export should be a self-contained package.

It should include:

* project manifest;
* selected source assets;
* selected artifacts;
* approval records;
* provenance;
* relevant history;
* export manifest;
* integrity hashes.

Diagnostics and logs may be optional depending on export purpose.

---

## 28. UI State Authority

UI state is not project truth.

Examples of non-authoritative UI state:

* selected tab;
* panel expansion;
* current preview;
* scroll position;
* temporary filters;
* unsaved text;
* cached recommendation display.

If UI state conflicts with durable artifacts, durable artifacts win.

---

## 29. In-Memory State

In-memory state is transient.

It may contain:

* active run status;
* current progress;
* pending model response;
* unsaved preview;
* temporary validation result.

Important in-memory results must be persisted before being treated as durable project state.

---

## 30. Failure During Write

If failure occurs before final artifact rename:

* preserve the temporary file where useful;
* mark it invalid or incomplete;
* write a diagnostic record if possible;
* do not index it as a valid artifact;
* do not update `project.json` as if success occurred.

If failure occurs after artifact save but before SQLite update:

* the artifact remains authoritative;
* database rebuild must recover it.

---

## 31. Failure During Manifest Update

If the artifact is saved but `project.json` update fails:

* keep the artifact;
* report partial success;
* record a diagnostic;
* do not delete the artifact;
* allow later reconciliation;
* avoid falsely reporting full success.

---

## 32. Failure During History Append

If the artifact and manifest are valid but history append fails:

* report degraded success;
* preserve the artifact;
* record the missing history event during later reconciliation;
* do not discard valid work.

---

## 33. Reconciliation Process

A reconciliation scan should:

1. validate the manifest;
2. enumerate artifacts;
3. compare manifest references;
4. compare history;
5. compare SQLite;
6. identify missing, orphaned, duplicate, or conflicting records;
7. produce a reconciliation report;
8. apply no destructive changes automatically.

---

## 34. Data Authority Summary

### Authoritative

* durable artifact files;
* approval records;
* supersession records;
* project manifest;
* project history.

### Derived

* SQLite indexes;
* search caches;
* compatibility caches;
* UI summaries;
* recent-project lists.

### Transient

* active worker state;
* progress indicators;
* unsaved previews;
* temporary model responses.

---

## 35. First-Release Implementation Rules

The first rentable release must satisfy:

1. projects remain readable without SQLite;
2. SQLite can be rebuilt;
3. durable artifacts are validated before indexing;
4. only one project writer is active;
5. writes are atomic where practical;
6. approvals are explicit;
7. supersession preserves history;
8. manual edits are detected;
9. corruption is reported;
10. recovery does not destroy original files;
11. backups contain the whole project directory;
12. the UI does not become the source of truth.

---

## 36. Acceptance Criteria

This architecture is ready for implementation when:

1. authority hierarchy is documented;
2. project manifest shape is defined;
3. database role is limited to index and acceleration;
4. rebuild behaviour is defined;
5. write ordering is defined;
6. project locking is defined;
7. corruption states are defined;
8. read-only recovery mode is defined;
9. manual-edit handling is defined;
10. backup and restoration are defined;
11. reconciliation is non-destructive;
12. no durable project state depends solely on SQLite.

---

## 37. Next Planning Event

Create:

```text
docs/architecture/FAILURE_AND_RECOVERY_MODEL.md
```

That document must define:

* workflow failure classes;
* retry rules;
* cancellation;
* timeouts;
* partial success;
* interrupted writes;
* worker crashes;
* model-service outages;
* application restarts;
* project recovery;
* user-facing failure messages;
* diagnostic requirements.

No recovery implementation should begin until failure states and recovery actions are explicitly mapped.

