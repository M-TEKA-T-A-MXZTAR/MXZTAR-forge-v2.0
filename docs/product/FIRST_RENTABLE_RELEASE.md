# MXZTAR-forge v2.0 — First Rentable Release

> **Historical filename, revised authority:** this document originated before the
> founder confirmed free-of-charge access. “First rentable release” now means the first
> release that creates durable user value; it does not mean a paid entitlement. The
> current Level One scope and sequencing authority is
> `docs/product/MASTER_BUILD_PLAN.md`.

## 1. Purpose

The first rentable release of MXZTAR-forge v2.0 helps a creator turn source artwork into structured creative-production material.

It is not merely an image-description tool.

Its purpose is to help the user:

1. understand what useful visual material exists in source art;
2. identify reusable forms, structures, motifs, surfaces, and systems;
3. convert those findings into production-ready planning material;
4. receive a clear recommended next action;
5. save the resulting work into an organised local project structure.

The first release must be useful without promising unfinished automation.

---

## 2. Core Product Promise

MXZTAR-forge v2.0 turns source art into:

* visual intelligence;
* reusable structure and shape findings;
* concept briefs;
* prompt packs;
* production directions;
* organised concept-folder outputs;
* clear next-step recommendations.

The system should help users move from:

source image
→ understanding
→ structured findings
→ production intent
→ reusable output
→ next action

---

## 3. Intended Users

The first release is designed for:

* visual artists;
* concept artists;
* graphic designers;
* prompt-assisted creators;
* 3D and blockout planners;
* game, animation, and film concept planners;
* modular design-system builders;
* creators who possess source art but are unsure how to convert it into further usable assets.

The system is especially useful to solo creators who need clear workflow guidance rather than a complicated wall of controls.

---

## 4. Primary User Problem

The user has artwork, sketches, abstract imagery, generated images, patterns, or complex visual compositions.

The user may not know:

* which structures are reusable;
* which forms should be extracted;
* which visual systems are present;
* which output should be made next;
* how the source could become a concept pack;
* whether a selected workflow is appropriate;
* how to organise findings into production material.

MXZTAR-forge should answer those questions in a controlled sequence.

---

## 5. First-Release User Journey

The first rentable release should support this journey:

1. Start a local project.
2. Add or select source art.
3. Choose the intended outcome.
4. Assess whether the source is suitable for that workflow.
5. Run one compatible workflow.
6. Display elapsed time and live progress.
7. Save the result automatically.
8. Preview the structured result.
9. Allow the user to approve, reject, or revise findings.
10. Recommend one next action.
11. Produce or update a concept folder.
12. Preserve an output history and audit trail.

The system should not encourage random workflow combinations without explaining compatibility.

---

## 6. Required First-Release Workflows

### 6.1 Source-Art Intelligence

**Input**

* one supported image;
* optional user notes.

**Purpose**

Inspect the source as creative-production material.

**Required output**

* visible contents;
* structural and layer observations;
* reusable motifs;
* reusable surfaces;
* candidate components;
* possible production uses;
* quality and uncertainty notes;
* recommended next workflow.

---

### 6.2 Shape and Structure Harvest

**Input**

* one supported image;
* optional source-art intelligence result.

**Purpose**

Identify reusable shapes, silhouettes, layers, curves, structural stacks, repeated elements, and extraction zones.

**Required output**

* candidate extraction list;
* layer observations;
* reusable shape list;
* possible vector or cutout targets;
* manual reconstruction notes;
* extraction priorities.

---

### 6.3 Modular-Set Perspective

**Input**

* one supported image;
* preferably an approved source-art intelligence or structure-harvest result.

**Purpose**

Interpret the source as a possible modular construction system.

**Required output**

* candidate modules;
* module families;
* parent and child relationships;
* connectors or joints;
* repeated construction grammar;
* suggested naming;
* possible future 2D or 3D planning uses.

Speculative ideas must be clearly distinguished from visible facts.

---

### 6.4 Concept Brief

**Input**

* source art;
* user intent;
* approved findings where available.

**Purpose**

Turn findings into a clear production brief.

**Required output**

* concept title;
* production objective;
* intended audience or use case;
* visual direction;
* constraints;
* required outputs;
* risks;
* recommended production sequence.

---

### 6.5 Render Prompt Pack

**Input**

* approved concept brief;
* source-art findings;
* optional style, material, or use constraints.

**Purpose**

Create reusable prompts that preserve the user’s design intent.

**Required output**

* primary prompt;
* controlled variations;
* material and lighting variants;
* composition variants;
* negative constraints;
* intended output type;
* provenance reference to the originating project.

---

### 6.6 Recommend Next Step

**Input**

* current project state;
* completed outputs;
* failed or incomplete workflows;
* selected user goal.

**Purpose**

Prevent the user from becoming stuck or selecting unsuitable actions.

**Required output**

* one recommended next action;
* reason;
* required input;
* expected result;
* what not to do yet.

---

## 7. Workflow Compatibility Assessment

Before a workflow runs, the system should classify the selection as:

### Ready

The selected source and current project state satisfy the workflow requirements.

### Caution

The workflow can run, but a prior result or additional user direction would improve the output.

### Blocked

The workflow lacks required input or depends on an unfinished prior stage.

Each assessment must include:

* compatibility status;
* reason;
* missing requirement;
* recommended correction;
* alternative workflow where appropriate.

This is a product feature, not merely error handling.

---

## 8. Required Output System

Every successful or failed workflow run must produce a durable record.

Each result should include:

* workflow key;
* workflow version;
* model used;
* source file path or project-relative identifier;
* source file hash where practical;
* start time;
* completion time;
* elapsed time;
* user notes;
* success or failure state;
* structured output;
* error details where relevant;
* saved output path;
* recommended next action.

A failed workflow may still save a diagnostic result, but the interface must not label that result as successful.

---

## 9. Required Project Folder Structure

A project should eventually contain:

```text
project-name/
├── project.json
├── README.md
├── source/
├── findings/
│   ├── raw/
│   ├── approved/
│   └── rejected/
├── briefs/
├── prompts/
├── structures/
├── exports/
├── logs/
└── history/
```

The user must remain able to inspect, copy, export, and back up their own work.

---

## 10. User Interface Requirements

The first rentable release must provide:

* source selection;
* workflow selection;
* compatibility status;
* one primary recommended action;
* one real run control;
* elapsed time;
* live progress;
* heartbeat messages during long jobs;
* success and failure feedback;
* saved output path;
* result preview;
* prevention of accidental parallel jobs;
* clear next-step guidance.

No visible control should exist without:

* a handler;
* a workflow contract;
* input validation;
* output behaviour;
* feedback;
* error handling;
* verification;
* durable result storage.

---

## 11. Hardware and Performance Requirements

The first release must remain usable on older CPU-only computers.

Default local policy:

```text
OLLAMA_NUM_THREAD=2
OLLAMA_NUM_PARALLEL=1
```

Required behaviour:

* no local AI work on the Qt main thread;
* one AI job at a time by default;
* visible elapsed time;
* visible progress or heartbeat;
* controlled timeouts;
* recoverable failures;
* no unexplained long-running process;
* no assumption that a discrete GPU is available;
* no unnecessary model downloads;
* no screaming-fan operating model.

Hardware capability may later be assessed dynamically, but safe conservative defaults must remain available.

---

## 12. Privacy and Local Ownership

The first release is local-first.

The product should clearly state:

* where source files are read from;
* where outputs are saved;
* whether any network request occurs;
* which local model is used;
* that user work remains locally accessible;
* that the user can export and back up their project data.

No source art should be uploaded to an external service without explicit user action and clear disclosure.

---

## 13. Access and Voluntary Support Model

Confirmed access model:

* use of the official software is free of charge;
* there is no timed trial, recurring subscription, or feature paywall;
* users may voluntarily support the founder at
  `https://buymeacoffee.com/mxztar`;
* donation status must not control core functionality or access to local files.

Before public release, the project must clearly communicate:

* privacy and data-use behaviour;
* local model and network behaviour;
* licence scope;
* software limitations;
* update and support expectations;
* that voluntary support is optional and does not purchase hidden entitlement.

A recognised open-source `LICENSE` remains a separate founder decision and release
gate. Free-of-charge access alone does not define modification or redistribution terms.

---

## 14. First-Release Exclusions

The following are not required for the first rentable release:

* automatic generation of finished 3D models;
* automatic conversion into production-ready OBJ or GLB files;
* cloud rendering;
* multi-user collaboration;
* online marketplace integration;
* unattended overnight production;
* automatic merchandising;
* automatic publishing;
* autonomous purchasing;
* unlimited parallel workflows;
* perfect visual interpretation;
* claims that AI findings are always correct.

These may be planned later, but they must not delay the coherent first release.

---

## 15. First-Release Acceptance Criteria

The first rentable release is ready for controlled user testing when:

1. A user can create or open a project.
2. A user can import or select source art.
3. The system can assess workflow compatibility.
4. At least four core workflows operate end to end.
5. Long jobs do not freeze the interface.
6. All runs save structured records.
7. Failures are reported accurately.
8. Results can be reviewed and preserved.
9. The system recommends a sensible next action.
10. A concept folder can be produced or updated.
11. Local files remain accessible outside the application.
12. Free access, optional support, privacy, and licence terms are clearly presented.
13. The application can run on the target CPU-only reference machine.
14. Installation, restoration, and backup processes are documented.
15. The verified source state is preserved in GitHub and recoverable through VX12 backup.

---

## 16. Development Priority Order

### Priority A — Workflow contracts

Define exact inputs, outputs, dependencies, and failure states for every first-release workflow.

### Priority B — Compatibility assessment

Prevent unsuitable or meaningless workflow execution.

### Priority C — Reliable threaded execution

Complete and verify the worker, progress, timeout, and result contracts.

### Priority D — Structured project storage

Create stable project and output schemas.

### Priority E — Review and approval

Allow findings to move from raw to approved or rejected.

### Priority F — Concept-folder assembly

Turn approved material into a useful production package.

### Priority G — Free-access release and licence clarity

Publish clear free-access, optional-support, privacy, licence, and limitation terms
without adding entitlement enforcement.

### Priority H — Packaging and controlled user testing

Prepare installation, updates, backups, recovery, and initial user feedback.

---

## 17. Immediate Next Planning Event

Create:

```text
docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md
```

That document must define, for each workflow:

* required input;
* optional input;
* dependencies;
* valid source types;
* readiness rules;
* caution conditions;
* blocking conditions;
* output contract;
* failure contract;
* recommended next workflow.

No further workflow UI expansion should occur until that matrix exists.
