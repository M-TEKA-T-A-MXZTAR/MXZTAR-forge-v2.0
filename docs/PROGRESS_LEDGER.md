# MXZTAR-forge v2c0 — Progress Ledger

## Ledger purpose

This ledger records what has actually been planned, implemented, verified, observed, deferred, or left unresolved.

It is not a wish list and it must not be used to imply that planned functionality already exists.

Status values:

- `VERIFIED` — implemented and supported by recorded verification evidence;
- `MERGED` — source or documentation is present on `main` through a merged PR;
- `PARTIAL` — some path exists, but the complete contract is not yet proven;
- `OBSERVED` — behaviour was seen but not yet reproduced or classified;
- `PLANNED` — defined in source-of-truth documentation but not implemented;
- `BLOCKED` — cannot proceed until a named prerequisite is satisfied;
- `DEFERRED` — intentionally outside the current milestone;
- `REJECTED` — deliberately excluded from the current product boundary.

## Current product state

**Current planning era:** source-art-to-spatial-design intelligence foundation.

**Current primary objective:** establish an honest, repeatable execution baseline before implementing project-state storage, schematic intelligence, spatial representation, or 3D translators.

**Current product promise:** turn source art into structured visual, schematic, modular, and spatial production intelligence under human review.

**Current non-promise:** automatic production-ready 3D reconstruction.

## Milestone ledger

| Area | Status | Evidence / present state | Next gate |
|---|---|---|---|
| Repository source-of-truth policy | VERIFIED | `docs/SOURCE_OF_TRUTH.md`; Git history leads, terminal scrollback does not | Keep verifier aligned with new required documents |
| Coding-practice principles | VERIFIED | Existing source-truth document and controlled-change rules | Apply to every runtime milestone |
| CPU-safe local policy | VERIFIED | Two-thread, one-parallel-job policy documented; CPU-only target established | Confirm runtime uses policy in every execution path |
| Ollama HTTP service path | VERIFIED | Prior text and vision probes passed through `http://127.0.0.1:11434/api/generate` | Re-run against current installation and record exact versions |
| Default local vision model | VERIFIED historically | `qwen2.5vl:3b` passed simple-image vision probe | Reconfirm model availability and current digest/version |
| Seven prompt contracts | VERIFIED historically | `source_art_intelligence`, `modular_set_perspective`, `prototype_imagination`, `shape_structure_harvest`, `concept_brief`, `render_prompt_pack`, `recommend_next_step` | Re-run verifier on current `main` |
| Agent runner JSON save path | VERIFIED historically | Simple-image source-art intelligence probe saved JSON output | Validate against new artifact-contract expectations |
| Agent worker / QThread path | MERGED historically | Worker implementation and UI wiring milestone were merged before later planning work | Audit current code and thread lifecycle |
| Agent Workflows source selector | VERIFIED manually | User selected an image and workflow | Reproduce in controlled compatibility test |
| UI run control | VERIFIED manually | User launched a selected workflow without reported UI freeze | Re-run with success and failure fixtures |
| Random workflow run | OBSERVED | A saved output was shown alongside an `AgentResult(ok=False)` / Ollama HTTP 400; selection was random, so defect was not declared | Reproduce under known source/workflow combinations; classify payload, compatibility, and return contract |
| Workflow success semantics | PARTIAL | Historical output suggests saved diagnostic and workflow success may have been conflated | Ensure failed result cannot be displayed as success |
| Cancellation | PLANNED | Required by build plan | Define contract and tests before adding visible control |
| Timeout handling | PARTIAL | Service has timeout concepts; complete UI/artifact behaviour not proven | Add deterministic timeout fixture and final-state test |
| Failure diagnostics | PARTIAL | Runner can save JSON; durable schema and UI truth not proven | Implement shared failure artifact after baseline audit |
| First rentable release definition | MERGED | `docs/product/FIRST_RENTABLE_RELEASE.md`, PR #14 | Maintain scope discipline |
| Workflow compatibility matrix | MERGED | `docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md`, PR #14 | Implement encoded assessor in Phase 4 |
| Output artifact contracts | MERGED | `docs/product/OUTPUT_ARTIFACT_CONTRACTS.md`, PR #15 | Implement schemas and validators in Phase 5 |
| Project state and data authority | MERGED | `docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md`, PR #16 | Implement only after execution baseline is stable |
| Master build plan | PENDING PR | `docs/product/MASTER_BUILD_PLAN.md` on current planning branch | Merge current planning PR |
| Progress ledger | PENDING PR | This document on current planning branch | Merge current planning PR and update thereafter |
| Project manifest and self-contained project directory | PLANNED | Authority contract defines requirements | Phase 2 |
| SQLite rebuild from durable artifacts | PLANNED | SQLite is derived index, not sole truth | Phase 2 exit test |
| Project lock / one-writer rule | PLANNED | Architecture contract defined | Phase 2 |
| Read-only recovery mode | PLANNED | Architecture contract defined | Phase 2 |
| Source rights context | PLANNED | Gap and artifact contracts defined | Phase 3 |
| Multi-view grouping | PLANNED | Required for honest spatial reasoning | Phase 3 |
| Scale and unit anchors | PLANNED | Required before dimensional claims | Phase 3 |
| READY / CAUTION / BLOCKED assessor | PLANNED | Matrix exists | Phase 4 |
| Shared artifact envelope and schema validation | PLANNED | Contracts exist | Phase 5 |
| Explicit approval / rejection / supersession | PLANNED | Contracts exist | Phase 5 |
| Source-art intelligence v1 | PARTIAL | Prompt and runner exist; production-grade structured contract and review are not proven | Phase 6 |
| Schematic line-network intelligence | PLANNED | Known market/product gap | Phase 7 |
| Shape and contour graph | PLANNED | Required intermediate evidence | Phase 7 |
| Layer, depth, and occlusion graph | PLANNED | Required spatial bridge | Phase 8 |
| 2.5D stacked representation | PLANNED | Core bridge between 2D evidence and later 3D | Phase 8 |
| Modular design grammar | PARTIAL | Prompt-level modular analysis exists | Phase 9 structured representation and approval |
| Concept brief translator | PARTIAL | Prompt contract exists | Phase 10 validated translator |
| Render prompt pack translator | PARTIAL | Prompt contract exists | Phase 10 validated translator |
| Blender blockout handoff | PLANNED | Defined as initial specialist-tool bridge | Phase 10 after spatial contract |
| Layered SVG handoff | PLANNED | Useful 2D/vector output | Phase 10 after line/shape contracts |
| OBJ/GLB blockout export | DEFERRED | Must not precede proven spatial and export contracts | Later Phase 10 |
| CAD exchange | DEFERRED | Requires units, dimensional confidence, and geometry contracts | Later Phase 10 |
| Benchmark corpus | PARTIAL | Simple generated shapes test exists | Phase 11 expanded corpus |
| Progressive learning ledger | PLANNED | Must record approved observations, decisions, reasons, and downstream use | Phase 11 |
| Rentable-release cockpit | PLANNED | LEVER contract defined | Phase 12 |
| 60-day trial | PLANNED | Commercial model defined | Phase 13 |
| NZD 10/month subscription | PLANNED | Commercial model defined; GST only when correctly configured | Phase 13 |
| User access to local files after entitlement lapse | PLANNED REQUIRED | Product boundary requires protection of user-owned files | Phase 13 acceptance gate |

## Merged planning milestones

### PR #14 — First rentable release and workflow compatibility

Status: `MERGED`.

Established:

- first rentable-release boundary;
- core user journey;
- first-release workflow set;
- READY / CAUTION / BLOCKED compatibility states;
- workflow inputs, dependencies, outputs, and failure expectations.

### PR #15 — Output artifact contracts

Status: `MERGED`.

Established:

- durable artifact envelope;
- statuses and approval states;
- provenance and validation;
- success/failure separation;
- atomic-save expectations;
- diagnostics, logs, history, supersession, and migration concepts.

### PR #16 — Project state and data authority

Status: `MERGED`.

Established:

- durable project files as authority;
- SQLite as rebuildable index and acceleration layer;
- project manifest responsibilities;
- write ordering and atomicity;
- one-writer project lock;
- read-only recovery;
- corruption detection;
- manual-edit handling;
- backup, restore, and reconciliation boundaries.

## Historical verified value path

The earlier implementation proved this basic backend chain at least once:

```text
selected image
→ prompt contract
→ Ollama HTTP API
→ qwen2.5vl:3b
→ constrained local execution
→ agent result
→ saved JSON output
```

This proof is important, but it does not yet prove:

- every workflow/source combination is valid;
- failures are classified correctly;
- saved JSON conforms to the new artifact contracts;
- the UI always reports final state honestly;
- cancellation, timeout, and storage failures are safe;
- source art becomes a validated spatial representation;
- any production-ready 3D export exists.

## Unresolved observation register

### OBS-001 — Random workflow produced HTTP 400 and confusing success text

Observed behaviour:

- a source and workflow were selected at random;
- output text indicated a saved path and completion;
- the displayed result also contained `AgentResult(ok=False)` and an Ollama HTTP 400 error.

Current interpretation:

- not yet a confirmed bug because source/workflow compatibility was uncontrolled;
- possible return-contract confusion between `(AgentResult, output_path)` and a success path;
- possible malformed or unsupported vision request;
- possible UI conflation of “diagnostic saved” with “workflow succeeded.”

Required resolution:

1. inspect current contracts;
2. reproduce with a known compatible pair;
3. reproduce with a known blocked pair;
4. assert exact worker signal values;
5. assert final UI label;
6. assert saved artifact status;
7. add regression coverage.

Do not close OBS-001 until evidence identifies the cause and proves the correction.

## Immediate next milestone after this ledger merges

Milestone name: **Execution Baseline Audit**.

Required branch scope:

- inspect current runtime files only;
- no feature expansion;
- no project-state implementation;
- no new export controls;
- no new models.

Required checks:

1. current branch and clean worktree;
2. current Python, PySide6, Ollama, and model state;
3. prompt-contract verifier;
4. source-library discovery;
5. simple text service probe;
6. simple vision service probe;
7. agent-runner probe;
8. worker compile and lifecycle inspection;
9. AgentPanel compile and handler inspection;
10. manual known-compatible run;
11. controlled failure run;
12. exact output and diagnostic files;
13. UI responsiveness and final-state truth;
14. update this ledger with evidence.

## Ledger update contract

Every merged milestone must add or update:

- date;
- PR number;
- branch;
- purpose;
- files changed;
- verification commands;
- verification result;
- status changes;
- new observations;
- closed observations;
- remaining blockers;
- next permitted milestone;
- backup status where relevant.

No milestone may be marked `VERIFIED` solely because code was committed or a PR was merged.
