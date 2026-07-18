# MXZTAR-forge v2.0 — Workflow Compatibility Matrix

## 1. Purpose

This document defines the input, dependency, readiness, caution, blocking, output, and failure contracts for each first-release MXZTAR-forge workflow.

Its purpose is to prevent the application from treating every source/workflow combination as automatically valid.

The compatibility layer should answer:

* Can this workflow run?
* Should this workflow run now?
* What is missing?
* What result should be expected?
* What workflow should happen next?
* What must the interface report if execution fails?

The compatibility layer is part of the product’s workflow intelligence, not merely defensive validation.

---

## 2. Compatibility States

Every proposed workflow run must resolve to one of three states.

### READY

The selected source and current project state satisfy the workflow’s required inputs.

The interface may enable:

```text
Run Selected Workflow
```

The interface must still show:

* selected source;
* selected workflow;
* expected output;
* saved-output destination;
* estimated resource class where available.

---

### CAUTION

The workflow can run, but one or more optional dependencies, prior findings, or user directions are missing.

The interface may permit execution, but must state:

* why the result may be weaker;
* what additional input would improve it;
* what assumptions the agent may need to make;
* whether a different workflow should run first.

The user should be able to deliberately continue.

---

### BLOCKED

The workflow lacks a required source, prior output, project state, or supported data type.

The interface must:

* disable the run action;
* identify the missing requirement;
* explain how to resolve it;
* recommend one valid next action.

Blocked workflows must not silently submit malformed or meaningless requests to the model.

---

## 3. Shared Input Classes

### IMAGE_SOURCE

A supported visual source file.

Initial supported formats:

```text
.png
.jpg
.jpeg
.webp
.bmp
.tif
.tiff
```

Minimum checks:

* file exists;
* file is readable;
* extension is supported;
* file size is greater than zero;
* image decoder can open it;
* dimensions are non-zero.

Future checks may include:

* colour mode;
* resolution;
* transparency;
* corruption;
* unusually large dimensions;
* likely source suitability.

---

### USER_INTENT

Optional or required user direction describing what the creator wants from the source.

Examples:

* identify reusable modules;
* focus on surfaces and panel systems;
* extract geometric structure;
* create a concept brief for a game environment;
* prepare prompts for wall-art variations;
* recommend the most commercially useful next step.

User intent must remain distinct from machine observations.

---

### RAW_FINDING

An unapproved workflow result.

A raw finding may contain useful material, but it has not yet been accepted by the user as project truth.

---

### APPROVED_FINDING

A result or selected portion of a result that the user has accepted for reuse in downstream workflows.

Approved findings should eventually contain:

* source workflow;
* source result ID;
* approval time;
* approved content;
* optional user correction;
* provenance reference.

---

### PROJECT_STATE

The current known state of a project, including:

* selected source files;
* completed workflow runs;
* failed runs;
* raw findings;
* approved findings;
* rejected findings;
* briefs;
* prompts;
* structures;
* exports;
* user goal;
* recommended next action.

---

## 4. Shared Execution Contract

Every workflow execution must record:

* project identifier where available;
* workflow key;
* workflow contract version;
* selected source;
* source hash where practical;
* user notes;
* model;
* start time;
* completion time;
* elapsed time;
* compatibility result;
* success or failure;
* generated output;
* error detail;
* saved result path;
* recommended next action.

A written diagnostic file does not itself prove success.

The result state must be determined from the workflow result contract.

---

# 5. Workflow Matrix

## 5.1 Source-Art Intelligence

### Workflow key

```text
source_art_intelligence
```

### Purpose

Inspect a source image as creative-production material rather than merely describing its visible subject.

### Required input

* one valid `IMAGE_SOURCE`.

### Optional input

* `USER_INTENT`;
* project name;
* intended output type;
* audience or commercial use;
* prior user notes.

### Dependencies

None.

This is the preferred first workflow for a newly imported image.

### Valid source types

* PNG;
* JPEG;
* WEBP;
* BMP;
* TIFF.

### READY conditions

The workflow is ready when:

* exactly one valid image is selected;
* the file exists and is readable;
* the local model is available;
* the Ollama API is reachable;
* no conflicting agent job is active.

### CAUTION conditions

Return caution when:

* no user intent is supplied;
* the image is extremely simple;
* the image is unusually large;
* the image contains very small or unclear detail;
* the image appears to be a screenshot rather than source art;
* the source contains many unrelated subjects;
* the user expects exact factual identification that local visual inference cannot guarantee.

Suggested message:

```text
This workflow can run, but adding a production goal will help the system identify more useful structures, motifs, and asset opportunities.
```

### BLOCKED conditions

Block when:

* no source is selected;
* the selected path does not exist;
* the file cannot be decoded;
* the source type is unsupported;
* Ollama is unavailable;
* the configured model is missing;
* another AI workflow is already active.

### Output contract

The result should contain:

1. visible content;
2. structural and layer observations;
3. reusable motifs;
4. reusable surfaces;
5. candidate objects or components;
6. production possibilities;
7. uncertainties and quality risks;
8. recommended next workflow.

### Failure contract

On failure, save:

* workflow key;
* source path;
* model;
* error category;
* error detail;
* elapsed time;
* diagnostic output path;
* recovery recommendation.

The UI must say:

```text
Workflow failed
```

It must not say:

```text
Workflow completed successfully
```

merely because a diagnostic JSON file was saved.

### Recommended next workflows

Depending on findings:

* `shape_structure_harvest`;
* `modular_set_perspective`;
* `concept_brief`;
* `recommend_next_step`.

---

## 5.2 Shape / Structure Harvest

### Workflow key

```text
shape_structure_harvest
```

### Purpose

Identify reusable silhouettes, shapes, curves, layers, structural stacks, repeated forms, and potential extraction zones.

### Required input

* one valid `IMAGE_SOURCE`.

### Optional input

* source-art intelligence result;
* approved visual findings;
* user extraction goal;
* intended output format.

### Dependencies

No mandatory prior workflow for the initial release.

A source-art intelligence result is recommended.

### READY conditions

Ready when:

* a supported image is selected;
* the user has requested shape, structure, layer, or extraction analysis;
* the image contains identifiable visual forms.

### CAUTION conditions

Return caution when:

* no source-art intelligence result exists;
* the image is heavily photographic with few separable structures;
* the source is low resolution;
* the user expects automatic vector tracing;
* transparency or layer boundaries are unclear.

Suggested message:

```text
This workflow can identify candidate structures, but it does not yet perform automatic vector extraction or guarantee clean production cut-outs.
```

### BLOCKED conditions

Block when:

* no readable source exists;
* the selected item is not an image;
* the file is corrupt;
* the model or service is unavailable;
* a job is already active.

### Output contract

The result should contain:

* major silhouettes;
* geometric and organic forms;
* repeated forms;
* layer relationships;
* structural stacks;
* perspective cues;
* extraction zones;
* likely SVG/PNG candidates;
* manual reconstruction guidance;
* priority ranking.

### Failure contract

The failure result must distinguish between:

* file failure;
* image decoding failure;
* model-service failure;
* timeout;
* malformed model output;
* unsupported result shape.

### Recommended next workflows

* `modular_set_perspective`;
* `concept_brief`;
* `recommend_next_step`.

---

## 5.3 Modular-Set Perspective

### Workflow key

```text
modular_set_perspective
```

### Purpose

Interpret source art as a possible system of reusable construction modules.

### Required input

Initial release:

* one valid `IMAGE_SOURCE`.

Preferred mature contract:

* one valid `IMAGE_SOURCE`;
* one approved source-art intelligence or shape-harvest result.

### Optional input

* intended 2D or 3D use;
* scale assumptions;
* target engine or application;
* desired module count;
* user notes;
* approved findings.

### Dependencies

Recommended:

1. `source_art_intelligence`;
2. `shape_structure_harvest`.

### READY conditions

Ready when:

* source art is valid;
* visible repeated forms or structural relationships exist;
* the user wants modular, kitbash, environment, blockout, product-system, or component analysis.

### CAUTION conditions

Return caution when:

* no prior findings have been approved;
* the source contains few repeated forms;
* the source is primarily photographic;
* the user has not stated whether the target is 2D, 3D, environment, object, or interface work;
* the workflow must infer modules not literally present in the image.

All inferred modules must be labelled as speculative.

Suggested message:

```text
This workflow may propose design extensions beyond what is directly visible. Speculative modules will be labelled separately from observed forms.
```

### BLOCKED conditions

Block when:

* no source is selected;
* source validation fails;
* the user requires production-ready geometry;
* the user requires dimensional accuracy not available from the source;
* a required approved finding is mandated by a future strict mode but is missing.

### Output contract

The result should contain separate sections for:

#### Observed modules

Forms directly supported by the source.

#### Inferred modules

Plausible extensions derived from the source design language.

#### Module families

Groups such as:

* panels;
* ribs;
* shells;
* plates;
* frames;
* connectors;
* joints;
* towers;
* surfaces;
* trims;
* interfaces.

#### Relationships

* parent/child;
* attachment;
* repetition;
* symmetry;
* stacking;
* rotation;
* scaling;
* adjacency.

#### Production direction

* suggested naming;
* extraction order;
* blockout order;
* potential 2D outputs;
* potential future 3D outputs.

### Failure contract

A result must fail rather than fabricate confidence when:

* no useful modular relationship can be identified;
* the source is too unclear;
* the model returns unusable or empty output;
* required provenance cannot be recorded.

### Recommended next workflows

* `concept_brief`;
* `render_prompt_pack`;
* `recommend_next_step`.

---

## 5.4 Prototype Imagination

### Workflow key

```text
prototype_imagination
```

### Purpose

Use source art as a design seed for possible products, machines, environments, interfaces, vehicles, tools, systems, or speculative concepts.

### Required input

* one valid `IMAGE_SOURCE`;
* one `USER_INTENT`.

### Optional input

* source-art intelligence result;
* approved motifs;
* approved structures;
* target audience;
* target industry;
* physical or digital constraint;
* production limits.

### Dependencies

Recommended:

* `source_art_intelligence`.

### READY conditions

Ready when:

* the source is valid;
* the user has stated an intended prototype category or problem space;
* speculative output is acceptable.

### CAUTION conditions

Return caution when:

* user intent is vague;
* no audience or use case is provided;
* the source has little connection to functional design;
* the user may mistake speculative concepts for engineering feasibility.

Suggested message:

```text
This workflow generates speculative concept directions. It does not verify engineering feasibility, safety, manufacturing suitability, or regulatory compliance.
```

### BLOCKED conditions

Block when:

* no user intent exists;
* the user requests certified engineering output;
* the requested result would require legal, safety, medical, structural, or technical certification;
* the source is invalid;
* the model is unavailable.

### Output contract

The result should contain:

* prototype name;
* user problem;
* proposed function;
* observed source influence;
* speculative extensions;
* primary components;
* interaction model;
* possible audience;
* production considerations;
* constraints;
* risks;
* next validation step.

### Failure contract

Failure must be reported when:

* the model returns only generic image description;
* no prototype relationship can be explained;
* the output does not distinguish observation from speculation;
* the result makes unsupported feasibility claims.

### Recommended next workflows

* `concept_brief`;
* `render_prompt_pack`;
* `recommend_next_step`.

---

## 5.5 Concept Brief

### Workflow key

```text
concept_brief
```

### Purpose

Turn selected source art, approved findings, and user intent into a coherent production brief.

### Required input

At least one of:

* valid source art plus `USER_INTENT`;
* approved source-art intelligence plus `USER_INTENT`;
* approved modular or prototype findings plus `USER_INTENT`.

### Optional input

* target audience;
* product category;
* intended deliverables;
* platform;
* visual constraints;
* production budget;
* hardware constraints;
* commercial purpose;
* deadline.

### Dependencies

Preferred:

* one completed source-analysis workflow;
* at least one approved finding.

### READY conditions

Ready when:

* user intent exists;
* sufficient project context exists;
* the desired output can be described.

### CAUTION conditions

Return caution when:

* only raw findings exist;
* no findings have been approved;
* audience is unknown;
* output format is unknown;
* production limitations are not stated.

Suggested message:

```text
A brief can be generated now, but approving the most useful findings first will reduce speculation and improve consistency.
```

### BLOCKED conditions

Block when:

* no source, findings, or project intent exists;
* the user requests a brief with no identifiable objective;
* prerequisite project data cannot be read.

### Output contract

The brief should contain:

* title;
* source references;
* production objective;
* user/audience problem;
* intended use;
* visual direction;
* approved motifs and structures;
* required deliverables;
* constraints;
* exclusions;
* risks;
* production order;
* acceptance criteria;
* recommended next workflow.

### Failure contract

Fail when:

* the output lacks a production objective;
* the output invents approved findings;
* source provenance is lost;
* required sections are missing;
* the result cannot be parsed or stored.

### Recommended next workflows

* `render_prompt_pack`;
* concept-folder assembly;
* `recommend_next_step`.

---

## 5.6 Render Prompt Pack

### Workflow key

```text
render_prompt_pack
```

### Purpose

Create reusable visual-generation prompts based on approved project intent and findings.

### Required input

Initial release:

* valid source art or concept brief;
* `USER_INTENT`.

Preferred contract:

* approved concept brief;
* approved visual findings.

### Optional input

* target image model;
* dimensions;
* aspect ratio;
* intended medium;
* material direction;
* lighting direction;
* composition;
* colour constraints;
* prohibited elements;
* variation count.

### Dependencies

Preferred:

1. `concept_brief`;
2. approved findings.

### READY conditions

Ready when:

* a clear intended visual result exists;
* source provenance is available;
* the prompt pack can reference approved design intent.

### CAUTION conditions

Return caution when:

* no concept brief exists;
* findings are still raw;
* no target generator is specified;
* no output dimensions or medium are known;
* the source has licensing or ownership uncertainty.

Suggested message:

```text
The prompt pack can be generated, but model-specific wording and output controls may need manual adjustment.
```

### BLOCKED conditions

Block when:

* no intended output is defined;
* no source or approved project material exists;
* the request requires prohibited, unlawful, or harmful content;
* source ownership or permission is explicitly disputed;
* project data cannot be read.

### Output contract

The pack should contain:

* prompt-pack title;
* source/project reference;
* primary prompt;
* controlled variants;
* composition variants;
* material variants;
* lighting variants;
* negative constraints;
* consistency anchors;
* target-model notes;
* intended use;
* provenance record.

### Failure contract

Fail when:

* the result is only one unstructured prompt;
* source intent is lost;
* variants contradict approved constraints;
* provenance is missing;
* output cannot be stored.

### Recommended next workflows

* manual review;
* My Prompts save;
* concept-folder assembly;
* `recommend_next_step`.

---

## 5.7 Recommend Next Step

### Workflow key

```text
recommend_next_step
```

### Purpose

Choose one sensible next action based on project state, completed work, missing inputs, and the user’s goal.

### Required input

* readable `PROJECT_STATE`.

For a new untracked source, the selected image may act as minimal project state.

### Optional input

* user goal;
* time available;
* preferred output;
* approved findings;
* previous failures;
* resource state.

### Dependencies

None, but its value increases as project history grows.

### READY conditions

Ready when:

* the system can inspect at least one selected source or existing project record.

### CAUTION conditions

Return caution when:

* no user goal is known;
* project records are incomplete;
* previous runs exist but have not been reviewed;
* the recommendation depends on assumptions.

### BLOCKED conditions

Block when:

* no source or project state exists;
* project state is unreadable;
* another process is currently modifying the same project state;
* the system cannot identify any valid next action.

### Output contract

The result must contain exactly one primary recommendation:

* next action;
* reason;
* required input;
* expected result;
* compatibility state;
* what not to do yet.

Optional alternatives may be listed after the primary recommendation, but must not replace it with a confusing menu.

### Failure contract

Fail when:

* multiple equal actions are returned without prioritisation;
* the recommendation refers to unavailable UI controls;
* the recommendation ignores blocked dependencies;
* project state was not actually inspected.

### Recommended next workflows

The recommendation itself selects the next workflow.

---

# 6. Initial Compatibility Summary

| Workflow                  |          Image required | User intent required | Prior approved finding required | Can run as first workflow |
| ------------------------- | ----------------------: | -------------------: | ------------------------------: | ------------------------: |
| Source-art intelligence   |                     Yes |                   No |                              No |                       Yes |
| Shape / structure harvest |                     Yes |                   No |                              No |         Yes, with caution |
| Modular-set perspective   |                     Yes |                   No |                    No initially |         Yes, with caution |
| Prototype imagination     |                     Yes |                  Yes |                              No |          Only with intent |
| Concept brief             |             Conditional |                  Yes |                       Preferred |         Usually not first |
| Render prompt pack        |             Conditional |                  Yes |                       Preferred |         Usually not first |
| Recommend next step       | Source or project state |                   No |                              No |                       Yes |

---

# 7. Compatibility Assessment Output Shape

The future compatibility assessor should return a stable structure comparable to:

```json
{
  "workflow_key": "modular_set_perspective",
  "status": "caution",
  "reason": "The source is valid, but no approved structural findings exist.",
  "missing_requirements": [],
  "recommended_improvements": [
    "Run source_art_intelligence first",
    "Approve useful structural findings"
  ],
  "can_run": true,
  "recommended_alternative": "source_art_intelligence",
  "expected_output": "A provisional modular-set proposal with speculative ideas labelled separately."
}
```

Allowed status values:

```text
ready
caution
blocked
```

---

# 8. Interface Behaviour Contract

When workflow selection changes, the application should display:

* compatibility state;
* reason;
* required inputs;
* missing inputs;
* expected output;
* recommended prior workflow;
* whether execution is enabled.

### READY

```text
Status: Ready
Action: Run Selected Workflow
```

### CAUTION

```text
Status: Caution
Action: Continue deliberately
Recommended first: [workflow]
```

### BLOCKED

```text
Status: Blocked
Run control: disabled
Next action: [specific correction]
```

The compatibility message must be visible before execution begins.

---

# 9. Planning Decisions Still Required

The following require later system-design decisions:

1. Whether concept briefs require approved findings in strict mode.
2. Whether prompt packs may run directly from source art.
3. How approval and rejection are represented.
4. How project state is versioned.
5. How source hashes are stored.
6. How large-image limits are calculated.
7. How timeouts differ by hardware class.
8. Whether a failed workflow can be retried with modified settings.
9. How compatibility rules are versioned.
10. How local-only trial licensing interacts with offline access.

---

# 10. Next Planning Event

Create:

```text
docs/product/OUTPUT_ARTIFACT_CONTRACTS.md
```

That document must define the durable files produced by each workflow, including:

* filename pattern;
* directory;
* schema version;
* required fields;
* provenance;
* success/failure state;
* validation;
* approval state;
* migration expectations.

No new workflow should be considered complete until its output artifact contract is defined and verifiable.

