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
| Agent worker / QThread path | PARTIAL | Worker implementation exists and now has a contract verifier on the worker-only path; panel wiring remains absent | Wire only after execution baseline and final-state UI contract are verified |
| Agent Workflows source selector | VERIFIED manually | User selected an image and workflow | Reproduce in controlled compatibility test |
| UI run control | PARTIAL | Historical run existed, but current `AgentPanel` has no live run button or worker connection | Restore only after worker and UI final-state contract are proven |
| Random workflow run | OBSERVED | A saved output was shown alongside an `AgentResult(ok=False)` / Ollama HTTP 400; later audit confirmed saved-failure records are valid and worker success semantics were defective | Keep OBS-001 open until UI final-state wiring is verified |
| Workflow success semantics | PENDING PR | Worker fix branch unpacks `(AgentResult, Path)` and emits success only when `AgentResult.ok` is true; verifier covers success, saved failure, and exception paths | Merge PR and run verifier locally |
| Cancellation | PLANNED | Required by build plan | Define contract and tests before adding visible control |
| Timeout handling | PARTIAL | Service has timeout concepts; complete UI/artifact behaviour not proven | Add deterministic timeout fixture and final-state test |
| Failure diagnostics | PARTIAL | Runner can save JSON; durable schema and UI truth not proven | Implement shared failure artifact after baseline audit |
| First rentable release definition | MERGED | `docs/product/FIRST_RENTABLE_RELEASE.md`, PR #14 | Maintain scope discipline |
| Workflow compatibility matrix | MERGED | `docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md`, PR #14 | Implement encoded assessor in Phase 4 |
| Output artifact contracts | MERGED | `docs/product/OUTPUT_ARTIFACT_CONTRACTS.md`, PR #15 | Implement schemas and validators in Phase 5 |
| Project state and data authority | MERGED | `docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md`, PR #16 | Implement only after execution baseline is stable |
| Master build plan | MERGED | `docs/product/MASTER_BUILD_PLAN.md`, PR #17 | Follow phased implementation order |
| Progress ledger | MERGED | This document, PR #17 | Update after every meaningful audit or implementation milestone |
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

### PR #17 — Master build plan and progress ledger

Status: `MERGED`.

Established:

- source-art-to-spatial-design intelligence product definition;
- gap map;
- phased build plan;
- progress-ledger governance;
- next permitted milestone: Execution Baseline Audit.

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

- the runner correctly saves both success records and failure diagnostic records;
- the former large JPEG source still reproduces an Ollama HTTP 400 with the current vision request path;
- the worker previously treated any returned `(AgentResult, output_path)` tuple as success because no Python exception was raised;
- therefore storage success and workflow success were conflated at the worker-signal boundary.

Required resolution:

1. inspect current contracts — completed;
2. reproduce with a known compatible pair — completed;
3. reproduce with the former failing source — completed;
4. assert exact worker signal values — pending PR verifier;
5. assert final UI label — pending future panel wiring;
6. assert saved artifact status — pending artifact-contract implementation;
7. add regression coverage — pending PR verifier.

Do not close OBS-001 until evidence proves final UI state, saved artifact status, and worker/panel wiring.

## Execution baseline audit notes

### 2026-07-06 — AgentWorker success semantics fix branch

Branch: `fix-agent-worker-success-semantics`.

Purpose:

- prevent failed `AgentResult` records from being reported to the UI as successful workflows;
- preserve the saved diagnostic path for failed-but-saved results;
- distinguish runner exceptions from saved failure diagnostics.

Files changed:

- `src/qt_panels/agent_worker.py`;
- `tools/verify_agent_worker_contract.py`;
- `docs/PROGRESS_LEDGER.md`.

Verification command after local sync:

```bash
cd "$HOME/MXZTAR-forge-v2c0" || exit 1
PYTHONPATH=src .venv/bin/python tools/verify_agent_worker_contract.py
PYTHONPATH=src .venv/bin/python -m py_compile src/qt_panels/agent_worker.py tools/verify_agent_worker_contract.py
```

Expected result:

- success result emits `finished(True, saved_path, "")`;
- saved failure result emits `finished(False, diagnostic_path, error)`;
- exception before saved result emits `finished(False, "", error)`.

Remaining blockers:

- `AgentPanel` still has no live run button, QThread lifecycle, elapsed timer, cancellation, or completion handler;
- the large JPEG source still triggers Ollama HTTP 400 and needs image-size/preflight handling before repeated full-resolution vision requests;
- swap configuration has been observed at 4 GiB and should be handled in a separate system-maintenance side quest after this PR.

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
