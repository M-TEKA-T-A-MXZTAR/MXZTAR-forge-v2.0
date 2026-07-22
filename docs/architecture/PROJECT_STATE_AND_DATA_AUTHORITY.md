# MXZTAR Forge v2.0 — Project State and Data Authority

## 1. Purpose

This document defines how MXZTAR Forge stores, reconstructs, validates, migrates, and protects project state across Stage One and Stage Two.

Its purpose is to prevent competing sources of truth between:

- durable project artifacts;
- `project.json`;
- project history;
- approval and supersession records;
- autosaves and transaction markers;
- SQLite indexes;
- cached UI state;
- in-memory objects;
- manually edited files.

The system must always be able to answer:

- What is authoritative?
- What is derived or rebuildable?
- What may be edited?
- What happens when sources disagree?
- How is corruption detected?
- How is interrupted work recovered?
- How is a copied project reopened without the original machine database?

---

## 2. Core decision

### Durable project artifacts are authoritative

The authoritative record of creative work is the set of validated durable files stored inside the project directory.

These include, where implemented:

- `project.json`;
- source asset records and unchanged project-owned source copies;
- native shape documents;
- extraction candidates;
- approved Shape Library assets;
- review, approval, rejection, and supersession records;
- construction recipes;
- components and assemblies;
- project history;
- job and diagnostic evidence;
- validated export records.

### SQLite is an index and acceleration layer

SQLite may support:

- fast lookup, filtering, and sorting;
- recent-project lists;
- search indexes;
- artifact summaries;
- cached compatibility assessments;
- UI layout and selection state;
- execution queues and resumable job metadata.

SQLite is never the sole authority for durable creative work.

If the database is lost or corrupted, a valid project must remain recoverable from project files.

---

## 3. Authority hierarchy

When data sources disagree, use this order:

1. validated canonical durable artifact files;
2. durable approval, rejection, correction, and supersession records;
3. append-only project history;
4. validated `project.json` declarations;
5. a validated newer autosave offered through explicit recovery;
6. rebuilt SQLite index;
7. cached UI state;
8. transient in-memory state;
9. terminal scrollback or unsaved notes.

Lower-priority data must never silently override higher-priority data.

A transaction marker or uncertain durability state may reduce authority to read-only even when a canonical file still exists.

---

## 4. Project directory as recovery boundary

Each project directory is self-contained and portable.

A copied project should preserve:

- project identity and exact Purpose;
- source copies, identity, hashes, and rights notes;
- editable shape documents and autosave/recovery state;
- extraction candidates;
- approved Shape Library assets;
- review, correction, rejection, and supersession history;
- construction recipes, components, and assemblies;
- jobs, diagnostics, and logs;
- exports and validation evidence;
- project history.

The user must not require the original machine-wide SQLite database to reopen a project.

---

## 5. Target project layout

```text
project/
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

A proposed directory does not become runtime authority merely because it appears here. Runtime code creates it only after the associated schema, migration, transaction, and verifier exist.

---

## 6. `project.json` contract

`project.json` is the project manifest.

It contains or references:

```json
{
  "schema_name": "mxztar_forge_project",
  "schema_version": "1.0.0",
  "project_id": "project_example",
  "project_name": "Example Project",
  "project_slug": "example-project",
  "purpose": "Build reusable engine-panel shapes from this source art",
  "created_at_utc": "2026-07-22T00:00:00Z",
  "updated_at_utc": "2026-07-22T00:00:00Z",
  "application_version_created": "0.0.0-development",
  "application_version_last_opened": "0.0.0-development",
  "project_status": "active",
  "source_asset_ids": [],
  "current_artifact_ids": [],
  "approved_artifact_ids": [],
  "superseded_artifact_ids": [],
  "history_path": "history/project_history.jsonl",
  "integrity": {
    "manifest_sha256": null,
    "last_validated_at_utc": null
  }
}
```

Rules:

- the exact creator Purpose is preserved;
- a safe name and slug may be derived, but do not replace the stored Purpose;
- identity fields remain stable;
- current, approved, and superseded declarations validate against actual files;
- manifest changes occur through atomic project transactions;
- unsupported future versions fail closed or attach read-only.

---

## 7. Project Birth authority

Project creation is the first project workflow.

Inputs:

- creator-supplied Purpose;
- workspace project root;
- current application and schema versions.

The creation transaction must:

1. validate non-empty Purpose;
2. derive a safe display name and slug;
3. refuse unsafe paths and collisions;
4. create the canonical directory structure required by the current schema only;
5. write and validate `project.json` atomically;
6. create project history;
7. append `project_created` with exact Purpose and derived identity;
8. acquire the writer lease;
9. return one truthful writable, locked, or failure state.

A broader onboarding profile is optional and must not be required to create a project.

---

## 8. Writer authority and locks

Only one Forge process may hold writable authority for a project at a time.

The writer lease:

- is acquired through an exclusive operation;
- records enough identity to diagnose ownership;
- belongs to the active ProjectSession;
- is released on explicit close and normal application shutdown;
- is not silently stolen;
- does not become writable merely because a stale-looking file exists;
- survives UI navigation until the project is closed.

A project may attach read-only when:

- another writer owns the lock;
- a transaction marker indicates interrupted work;
- rollback durability is uncertain;
- schema migration is unavailable;
- project validation cannot safely authorise mutation.

Read-only state remains visible and disables mutations.

---

## 9. Canonical, autosave, temporary, and transaction state

### Canonical

The last fully validated explicit save registered by project authority.

### Autosave

A bounded project-owned recovery candidate separate from canonical truth.

A newer valid autosave may be offered for explicit recovery but does not silently replace canonical bytes.

### Temporary file

An implementation detail of an atomic write. A stray `.tmp` file never becomes truth merely because it is newer.

### Transaction marker

A durable indicator that a multi-file editor or project transaction may have been interrupted.

Rules:

- an active writer lock remains authoritative over an unrelated stale marker during the live owning session;
- on reopen, an unresolved marker forces explicit read-only recovery classification;
- the marker clears only after confirmed success or confirmed rollback;
- uncertain rollback remains read-only.

---

## 10. Shape-document authority

The current native shape schema is `mxztar_forge_shape_document` version `1.0.0`.

Canonical shape documents live beneath:

```text
structures/shape-documents/
```

Autosaves live beneath:

```text
structures/shape-documents/.autosave/
```

A shape save may affect:

- canonical shape document;
- project manifest;
- project history;
- autosave cleanup;
- transaction marker.

These writes form one logical transaction. Partial success is not reported as a successful save.

Document and history bounds are enforced before unreadable bytes become canonical or autosave state.

---

## 11. Candidate and approval authority

### Raw or editable candidate

A manual trace, algorithmic extraction, or model proposal not yet approved.

### Approved shape

A reviewed native shape artifact accepted for reuse.

### Rejected

Explicitly excluded from downstream approved truth while remaining historically inspectable.

### Superseded

Preserved historical artifact conceptually replaced by a later approved version.

Rules:

- successful generation does not imply approval;
- approval creates a durable decision record;
- corrected derivatives may be approved without mutating the raw candidate;
- downstream construction and export prefer current approved material;
- directory location alone does not define approval state.

---

## 12. Construction and assembly authority

### Construction recipe

The reversible derivation authority for a component generated from an approved shape or declared primitive.

### Component

The current editable 3D object and transform state produced by a recipe or primitive.

### Assembly

The authoritative hierarchy of component IDs, instances, transforms, anchors, connectors, and declared relationships.

Group, assembly, contact, stitch, join mesh, boolean, separate, and bake remain distinct durable meanings.

A baked result is a new derivative and cannot silently erase reversible parent history.

---

## 13. Export authority

Exports are validated derivatives.

An export record identifies:

- approved input artifacts;
- named output profile;
- generated project-relative files and checksums;
- units, axes, hierarchy, names, and limitation rules;
- validation result;
- downstream import or continuation evidence where required.

An SVG, PNG, GLB, OBJ, or Forge Pack never replaces the native project authority.

---

## 14. Project history

Project history is append-only JSON Lines.

Material events include:

- project creation/open/close/recovery;
- source import/processing;
- document creation and save;
- editor command application where required by the history design;
- review and approval decisions;
- version and supersession changes;
- recipe/component/assembly changes;
- exports;
- migration and recovery actions.

History supports reconstruction and audit but does not override a valid newer canonical artifact without an explicit reconstruction rule.

---

## 15. Derived SQLite data

SQLite rows may include:

- project ID, path, name, Purpose summary, and last-opened time;
- artifact ID, type, schema, status, approval state, and project-relative path;
- source and parent IDs;
- validation summary;
- user-facing search text;
- UI state and recent selection;
- queued/resumable job metadata.

Every durable-artifact row references a project-relative file.

A database row without a corresponding valid artifact is stale or invalid.

---

## 16. Rebuild contract

A project/index rebuild should:

1. locate the project directory;
2. validate `project.json`;
3. enumerate durable artifacts through bounded discovery;
4. validate schema names and versions;
5. identify approvals, rejections, corrections, and supersession links;
6. reconstruct current shapes, components, assemblies, and exports;
7. rebuild SQLite rows;
8. record warnings for missing, invalid, or conflicting files;
9. preserve original files;
10. report the rebuild result.

Rebuild does not modify project artifacts unless a separate explicit migration or repair operation is selected.

---

## 17. Current-state reconstruction

For each artifact:

1. validate file structure and integrity;
2. read artifact ID and schema version;
3. read status and approval state;
4. identify project, source, and parent relationships;
5. identify superseded artifacts;
6. determine whether it is current;
7. index or quarantine the result truthfully.

An artifact is current when it is:

- valid;
- relevant to the current project manifest;
- not rejected;
- not superseded;
- not replaced by a later approved derivative;
- consistent with required parent and approval records.

---

## 18. Conflict rules

Examples:

### Manifest references missing artifact

- preserve manifest and remaining files;
- mark reference invalid;
- warn user;
- do not fabricate replacement.

### Artifact exists but is absent from manifest

- treat as orphan or candidate recovery material;
- do not silently register it as current;
- offer explicit reconciliation where safe.

### SQLite disagrees with files

- validated files win;
- rebuild affected index rows.

### Autosave newer than canonical

- validate both;
- present recovery choice;
- do not silently replace canonical.

### Approval and artifact disagree

- fail closed for downstream approved use;
- inspect decision and content hashes;
- require explicit repair or supersession.

### Transaction marker exists

- attach read-only on reopen;
- diagnose canonical, manifest, history, and temporary state;
- clear only after confirmed resolution.

---

## 19. Corruption detection

Detection may use:

- JSON/schema validation;
- content hashes;
- manifest relationship checks;
- missing parent or source IDs;
- impossible approval/supersession links;
- duplicate IDs;
- malformed history lines;
- file-size and history bounds;
- invalid path traversal or symlink escape;
- incomplete transaction markers;
- unsupported schema versions.

Corruption warnings remain explicit. The system does not quietly discard user work.

---

## 20. Migration contract

A migration must:

1. identify source and target schema versions;
2. validate pre-migration state;
3. preserve or back up current canonical files;
4. write through atomic transaction rules;
5. append a migration history event;
6. validate the migrated project;
7. roll back or attach read-only on failure;
8. preserve unknown future fields where the schema contract requires it.

Opening a project for assessment must not mutate it automatically.

---

## 21. UI state authority

UI layout, active workspace, selected artifact, zoom, and safe tool state may be cached in SQLite or settings.

UI state:

- is lower authority than project artifacts;
- cannot make a rejected or invalid artifact current;
- cannot grant writable authority;
- cannot silently switch projects;
- may be discarded and rebuilt without losing creative work.

---

## 22. Backup and restoration

A useful backup preserves the full project directory.

Restoration should:

1. copy or locate the project;
2. validate manifest and artifacts;
3. assess lock and transaction state;
4. rebuild derived indexes;
5. report missing or conflicting data;
6. attach writable only when authority is safe.

A new VX12 backup is claimed only when it is actually created and recorded.

---

## 23. Verification requirements

Project authority changes require proportionate tests for:

- creation collisions and unsafe paths;
- one-writer acquisition and release;
- read-only lock and recovery states;
- atomic writes and rollback;
- autosave/canonical separation;
- stale temporary-file containment;
- transaction-marker recovery;
- project copying without SQLite;
- index rebuild;
- schema migration;
- approval/supersession reconstruction;
- application shutdown and guarded worker lifecycle.

No authority path is verified solely because it is documented or merged.
