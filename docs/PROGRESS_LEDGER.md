# MXZTAR-forge v2.0 — Progress Ledger

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
| Relocatable repository launcher | PARTIAL | Branch launcher derives its checkout path from `BASH_SOURCE`, uses checkout-local `.venv` when present, and has a relocation verifier | Run verifier locally and update external desktop launchers after merge |
| Coding-practice principles | VERIFIED | Existing source-truth document and controlled-change rules | Apply to every runtime milestone |
| CPU-safe local policy | VERIFIED | Two-thread, one-parallel-job policy documented; CPU-only target established | Confirm runtime uses policy in every execution path |
| Ollama HTTP service path | VERIFIED | Prior text and vision probes passed through `http://127.0.0.1:11434/api/generate` | Re-run against current installation and record exact versions |
| Default local vision model | VERIFIED historically | `qwen2.5vl:3b` passed simple-image vision probe | Reconfirm model availability and current digest/version |
| Seven prompt contracts | VERIFIED historically | `source_art_intelligence`, `modular_set_perspective`, `prototype_imagination`, `shape_structure_harvest`, `concept_brief`, `render_prompt_pack`, `recommend_next_step` | Re-run verifier on current `main` |
| Agent runner JSON save path | VERIFIED historically | Simple-image source-art intelligence probe saved JSON output | Validate against new artifact-contract expectations |
| Agent worker / QThread path | PARTIAL | Worker is wired to `AgentPanel` through a dedicated `QThread`; deterministic panel verifier covers lifecycle and final-state behaviour | Run verifier and manual Ollama smoke test locally before merge |
| Agent Workflows source selector | VERIFIED manually | User selected an image and workflow | Reproduce in controlled compatibility test |
| My Library source-art baseline | MERGED | Read-only source discovery, preview, facts, open-folder action, and exact `SourceArtItem` handoff merged in PR #23 | Verify bounded thumbnails and manual library-to-workflow path on large real source art |
| UI run control | PARTIAL | Selected source/workflow can launch one background job with locked controls, elapsed time, heartbeat, progress, and saved path feedback | Verify against a known-compatible local source/model pair |
| Random workflow run | OBSERVED | A saved output was shown alongside an `AgentResult(ok=False)` / Ollama HTTP 400; later audit confirmed saved-failure records are valid and worker success semantics were defective | Keep OBS-001 open until UI final-state wiring is verified |
| Workflow success semantics | MERGED | `AgentWorker` unpacks `(AgentResult, Path)` and emits success only when `AgentResult.ok` is true; worker verifier covers success, saved failure, and exception paths | Preserve distinction in panel and artifact contracts |
| Cancellation | PLANNED | No misleading cancel control is exposed; active jobs prevent unsafe window close and retain the service timeout boundary | Define cooperative request/model cancellation contract before adding a button |
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
cd "$HOME/MXZTAR-forge-v2.0" || exit 1
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

## 2026-07-19 — Safe AgentPanel execution branch

Branch: `agent/restore-safe-ai-runner`.

Purpose:

- restore one honest, user-visible source-art workflow without placing AI work on the Qt main thread;
- enforce one active heavy job through the only execution panel;
- show elapsed time, heartbeat, progress, final result, and saved output/diagnostic path;
- prevent unsafe application close while the worker is active.

Files changed:

- `src/qt_panels/agent_panel.py`;
- `src/qt_app.py`;
- `tools/verify_agent_panel_execution_contract.py`;
- `docs/PROGRESS_LEDGER.md`.

Verification commands:

```bash
PYTHONPATH=src .venv/bin/python tools/verify_agent_worker_contract.py
QT_QPA_PLATFORM=offscreen PYTHONPATH=src .venv/bin/python tools/verify_agent_panel_execution_contract.py
PYTHONPATH=src .venv/bin/python -m py_compile \
  src/qt_panels/agent_panel.py \
  src/qt_app.py \
  tools/verify_agent_panel_execution_contract.py
```

Expected evidence:

- worker runs outside the Qt main thread;
- a second launch is rejected while active;
- success, saved failure, and unsaved failure remain distinct;
- timer and controls return to idle after every final state;
- application close is rejected while a job is active.

Remaining boundary:

- this PR does not claim cooperative cancellation;
- the existing 600-second service timeout remains the hard request boundary;
- the former large-JPEG HTTP 400 still requires a separate source-image preflight milestone;
- a known-compatible manual Ollama run remains required before marking the end-to-end path VERIFIED.

## 2026-07-19 — My Library source-art baseline branch

Branch: `agent/build-my-library-source-baseline`.

Purpose:

- replace the My Library placeholder with a useful read-only source-art browser;
- preview supported images and display their path, type, size, and library section;
- hand the exact selected `SourceArtItem` to Agent Workflows;
- navigate to the workflow panel without copying, moving, renaming, or modifying the source;
- keep workflow outputs and approved artifacts explicitly deferred until durable project contracts exist.

Files changed:

- `src/qt_panels/my_library_panel.py`;
- `src/qt_panels/agent_panel.py`;
- `src/qt_app.py`;
- `tools/verify_my_library_contract.py`;
- `docs/PROGRESS_LEDGER.md`.

Verification commands:

```bash
QT_QPA_PLATFORM=offscreen PYTHONPATH=src \
  .venv/bin/python tools/verify_my_library_contract.py

PYTHONPATH=src .venv/bin/python -m py_compile \
  src/qt_panels/my_library_panel.py \
  src/qt_panels/agent_panel.py \
  src/qt_app.py \
  tools/verify_my_library_contract.py
```

Expected evidence:

- supported source art is discovered and previewed;
- the exact selected source reaches Agent Workflows;
- source replacement is rejected while an AI job is active;
- source bytes remain unchanged through discovery and handoff;
- an empty library disables actions and explains where source art belongs.

Remaining boundary:

- My Library currently represents the Source Art stage only;
- durable workflow-output browsing, approvals, prompts, and concept folders depend on later project and artifact contracts;
- no ownership or licence verification is inferred from file discovery.

## 2026-07-19 — Relocatable launcher branch

Branch: `agent/make-launcher-relocatable`.

Purpose:

- remove the hard-coded checkout directory from `run_mxztar_forge.sh`;
- make the launcher derive the repository directory from its own file location;
- prefer the checkout-local virtual-environment interpreter;
- keep execution correct after an intentional directory rename;
- verify relocation without starting the Qt application.

Files changed:

- `run_mxztar_forge.sh`;
- `tools/verify_relocatable_launcher.py`;
- `docs/PROGRESS_LEDGER.md`.

Verification commands:

```bash
python3 tools/verify_relocatable_launcher.py
bash -n run_mxztar_forge.sh
```

Remaining local installation step after merge:

- rename `$HOME/MXZTAR-forge-v2c0` to `$HOME/MXZTAR-forge-v2.0` only after checking the destination does not already exist;
- back up and update the external application-menu and Desktop `.desktop` files;
- confirm both launchers resolve to the canonical checkout and repository launcher.

## 2026-07-19 — Bounded large-source thumbnail branch

Branch: `agent/bound-large-source-previews`.

Observed defect:

- My Library attempted to construct a full-resolution `QPixmap` for very large source art;
- Qt rejected the decode when it exceeded the 256 MB allocation limit;
- raising the global allocation ceiling would risk UI freeze and excessive memory use on modest hardware.

Purpose:

- retain the original source file and exact workflow handoff path;
- decode at most a 1600×1200 UI derivative when the Qt handler reports scaled-decode support;
- reject unsafe large preview decoding before image read while keeping the source selectable;
- cache the bounded thumbnail under `workspace/cache/source_previews`;
- invalidate cache identity when source path, byte size, or modification time changes;
- rerender window resizes from the bounded in-memory image rather than decoding the source again;
- keep preview failure non-blocking so the original remains selectable.

Files changed:

- `src/core/paths.py`;
- `src/core/source_preview_cache.py`;
- `src/qt_panels/my_library_panel.py`;
- `tools/verify_large_source_preview_contract.py`;
- `tools/verify_source_preview_cache_contract.py`;
- `.gitignore`;
- `docs/PROGRESS_LEDGER.md`.

Verification commands:

```bash
QT_QPA_PLATFORM=offscreen PYTHONPATH=src \
  .venv/bin/python tools/verify_large_source_preview_contract.py

PYTHONPATH=src .venv/bin/python tools/verify_source_preview_cache_contract.py

git check-ignore workspace/cache/source_previews/private-source.png

PYTHONPATH=src .venv/bin/python -m py_compile \
  src/core/paths.py \
  src/core/source_preview_cache.py \
  src/qt_panels/my_library_panel.py \
  tools/verify_large_source_preview_contract.py \
  tools/verify_source_preview_cache_contract.py
```

Boundary:

- thumbnail files are rebuildable, Git-ignored, count/byte-bounded cache, not project truth;
- this PR does not resize or overwrite original source art;
- AI-request image preflight remains a separate execution-path gate before large-source model testing;
- the application does not raise Qt's global allocation limit.

## 2026-07-19 — My Apps and Desktop launcher restoration branch

Branch: `agent/restore-desktop-launchers`.

Purpose:

- provide one application-menu launcher and one Desktop launcher;
- use the canonical MXZTAR Forge v2.0 name;
- use a repository-owned gold star SVG icon;
- target the checkout's relocatable `run_mxztar_forge.sh`;
- back up existing launcher files before replacement;
- validate the complete installation in an isolated temporary home.

Files changed:

- `assets/icons/mxztar-forge-star.svg`;
- `tools/install_desktop_launchers.sh`;
- `tools/verify_desktop_launchers.py`;
- `README.md`;
- `docs/PROGRESS_LEDGER.md`.

Verification commands:

```bash
python3 tools/verify_desktop_launchers.py
bash -n tools/install_desktop_launchers.sh
python3 -m py_compile tools/verify_desktop_launchers.py
```

Local installation command after merge:

```bash
bash tools/install_desktop_launchers.sh
```

Boundary:

- the installer writes only the two named launcher files under the user's
  application-menu and Desktop directories;
- an existing target launcher is backed up before replacement;
- the star icon remains repository-owned and versioned.

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
