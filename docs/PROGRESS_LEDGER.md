# MXZTAR Forge v2.0 — Progress Ledger

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

**Current planning era:** Level One operational Forge Pack foundation.

**Current primary objective:** restore Jobs and Shape Library, establish durable project
authority, formalise structured analysis and review, and export the first verified
Forge Pack before beginning 2D-to-3D construction.

**Current product promise:** turn source art into structured, inspectable, reusable
production intelligence under human review, then package approved findings and shapes
for immediate continuation in specialist tools.

**Current non-promise:** automatic production-ready 3D reconstruction, engineering
accuracy, manufacturing safety, or finished CAD geometry.

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
| Historical first rentable release definition | MERGED | `docs/product/FIRST_RENTABLE_RELEASE.md`, PR #14; its access section now records the superseding free-access decision | Retain filename only as historical continuity or rename in a dedicated link-migration PR |
| Workflow compatibility matrix | MERGED | `docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md`, PR #14 | Implement encoded assessor in Phase 4 |
| Output artifact contracts | MERGED | `docs/product/OUTPUT_ARTIFACT_CONTRACTS.md`, PR #15 | Implement schemas and validators in Phase 4 |
| Project state and data authority | MERGED | `docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md`, PR #16 | Implement only after execution baseline is stable |
| Level One master build plan | MERGED | `docs/product/MASTER_BUILD_PLAN.md`, initially PR #17 and comprehensively revised after PR #27 | Follow the revised operational MVP sequence |
| Progress ledger | MERGED | This document, PR #17 | Update after every meaningful audit or implementation milestone |
| Project manifest and self-contained project directory | PLANNED | Authority contract defines requirements | Phase 2 |
| SQLite rebuild from durable artifacts | PLANNED | SQLite is derived index, not sole truth | Phase 2 exit test |
| Project lock / one-writer rule | PLANNED | Architecture contract defined | Phase 2 |
| Read-only recovery mode | PLANNED | Architecture contract defined | Phase 2 |
| Source rights context | PLANNED | Gap and artifact contracts defined | Phase 3 |
| Multi-view grouping | PLANNED | Required for honest spatial reasoning | Phase 3 |
| Scale and unit anchors | PLANNED | Required before dimensional claims | Phase 3 |
| READY / CAUTION / BLOCKED assessor | PLANNED | Matrix exists | Phase 4 |
| Shared artifact envelope and schema validation | PLANNED | Contracts exist | Phase 4 |
| Explicit approval / rejection / supersession | PLANNED | Contracts exist | Phase 4 |
| Source-art intelligence v1 | PARTIAL | Prompt and runner exist; production-grade structured contract and review are not proven | Phase 5 |
| Schematic line-network intelligence | PLANNED | Known market/product gap | Phase 6 |
| Shape and contour graph | PLANNED | Required intermediate evidence | Phase 6 |
| Layer, depth, and occlusion graph | PLANNED | Required spatial bridge | Phase 7 |
| 2.5D stacked representation | PLANNED | Core bridge between 2D evidence and later 3D | Phase 7 |
| Modular design grammar | PARTIAL | Prompt-level modular analysis exists | Phase 7 structured representation and approval |
| Concept brief translator | PARTIAL | Prompt contract exists | Phase 8 validated translator |
| Render prompt pack translator | PARTIAL | Prompt contract exists | Phase 8 validated translator |
| Blender blockout handoff | PLANNED | Defined as initial specialist-tool bridge | Phase 8 after spatial contract |
| Layered SVG handoff | PLANNED | Useful 2D/vector output | Phase 8 after line/shape contracts |
| OBJ/GLB blockout export | DEFERRED | Must not precede proven spatial, construction-recipe, and export contracts | Phase 10 |
| CAD exchange | DEFERRED | Requires units, dimensional confidence, and geometry contracts | Phase 12 |
| Benchmark corpus | PARTIAL | Simple generated shapes test exists | Expand continuously through Phases 4–12 |
| Progressive learning ledger | PLANNED | Must record approved observations, decisions, reasons, and downstream use | Add with approval in Phase 4 and extend continuously |
| Level One cockpit | PLANNED | Start Here, My Library, Agent Workflows, Review, Shape Library, Jobs, and Export are the governed workspaces | Master plan Phases 1–9 |
| Free-of-charge software access | PLANNED REQUIRED | Founder confirmed no timed trial, subscription, or feature paywall | Public-release acceptance gate |
| Voluntary founder support | PLANNED | `https://buymeacoffee.com/mxztar`; donation must not alter core access | Add truthful non-intrusive release/UI link |
| Formal open-source licence | BLOCKED | Repository is public but the founder has not selected a recognised `LICENSE` | Founder selects licence before public release |
| User access to local files | PLANNED REQUIRED | Local-first authority requires uninterrupted access independent of support/donation | Level One acceptance gate |

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

## 2026-07-19 — PR #27 visible library grid and Desktop Input

Status: `VERIFIED` on the T1700 after merge at `9167bf5`.

Branch: `agent/library-grid-desktop-input`.

Files changed:

- `README.md`;
- `docs/PROGRESS_LEDGER.md`;
- `src/qt_panels/my_library_panel.py`;
- `tools/install_desktop_launchers.sh`;
- `tools/verify_desktop_launchers.py`;
- `tools/verify_my_library_contract.py`.

Established:

- every discovered source appears as a visible card rather than a hidden selector;
- thumbnail decoding runs incrementally outside the Qt main thread;
- card icons retain bounded pixmaps;
- folder-qualified labels distinguish duplicate basenames;
- the selected preview remains compact;
- the exact selected original reaches Agent Workflows;
- active AI work rejects unsafe source replacement;
- source bytes remain unchanged;
- the Desktop Input link exposes the canonical input folder.

Reproduction commands used by the branch and local verification contracts:

```bash
cd /home/michael/MXZTAR-forge-v2.0
QT_QPA_PLATFORM=offscreen PYTHONPATH=src \
  .venv/bin/python tools/verify_my_library_contract.py

python3 tools/verify_desktop_launchers.py
python3 -m py_compile \
  src/qt_panels/my_library_panel.py \
  tools/verify_my_library_contract.py \
  tools/verify_desktop_launchers.py
```

Recorded T1700 My Library verification result after merge:

```text
PASS: all six source images appear as visible cards
PASS: every source card has a thumbnail
PASS: card icons retain only card-sized pixmaps
PASS: source cards retain folder-qualified labels
PASS: selected preview height is compact
PASS: grid selection emits the exact SourceArtItem
PASS: handoff navigates to Agent Workflows
PASS: active AI job rejects source replacement
PASS: discovery and handoff leave all source bytes unchanged
PASS: visible My Library grid verified
```

Remaining boundary:

- the grid is source intake, not yet the durable project/processed-source lifecycle;
- Shape Library and Jobs still require restoration around current authority contracts;
- source analysis, approval, and Forge Pack export remain incomplete.

Status changes:

- My Library visible-card baseline: `MERGED` → `VERIFIED` on the T1700;
- Desktop Input link: `MERGED` with repository installer-contract verification; live
  presence remains a local installation fact rather than repository state.

Backup status: no new VX12 backup was recorded for this UI verification; no backup is
claimed by this ledger entry.

## 2026-07-19 — Level One product-definition planning

Status: `PLANNED` until the documentation PR merges.

Founder decisions recorded:

- operational Level One MVP takes priority over advanced 3D construction;
- primary value is reviewed production intelligence and a durable Forge Pack;
- Start Here will collect progressive local user and project intent;
- workflows should normally be automated but remain visible and human governed;
- approved shapes form the basis of later reversible 2D-to-3D construction;
- later Modular Construct provides three-axis placement, alignment, instances, arrays,
  grouping, assembly, join, boolean operations, and verified export;
- three-second hover Insights teach users what controls do;
- official software use is free of charge;
- voluntary founder support is available at `https://buymeacoffee.com/mxztar`;
- a formal recognised open-source licence remains a founder release decision;
- versioned official releases are the primary ordinary-user distribution channel.

Planning artifacts:

- `README.md` — public goal and Level One boundary;
- `docs/product/MASTER_BUILD_PLAN.md` — product, data, workflow, roadmap, release, and
  future construction authority;
- `docs/product/FIRST_RENTABLE_RELEASE.md` — historical scope reconciled with the
  confirmed free-access model;
- `docs/PROGRESS_LEDGER.md` — decisions, current state, next gate, and evidence.

This milestone changes documentation only. It does not claim that Start Here, Review,
Shape Library, Jobs, Forge Pack export, 2D-to-3D, or Modular Construct are implemented.

## 2026-07-19 — Read-only Jobs panel baseline branch

Status: `PLANNED` until the implementation PR merges and the T1700 verifier passes.

Branch: `agent/restore-truthful-jobs-panel`.

Purpose:

- make previously saved workflow work findable without filesystem archaeology;
- recover legacy success, saved-failure, and malformed JSON records truthfully;
- scan record files outside the Qt main thread;
- refresh after Agent Workflows saves an output or diagnostic;
- remain a read-only evidence browser rather than a second execution authority;
- expose no fake retry, cancel, delete, approval, or export actions.

Files in scope:

- `src/core/job_records.py`;
- `src/qt_panels/jobs_panel.py`;
- `src/qt_panels/agent_panel.py`;
- `src/qt_app.py`;
- `tools/verify_jobs_panel_contract.py`;
- `docs/PROGRESS_LEDGER.md`.

Verification commands:

```bash
QT_QPA_PLATFORM=offscreen PYTHONPATH=src \
  .venv/bin/python tools/verify_jobs_panel_contract.py

QT_QPA_PLATFORM=offscreen PYTHONPATH=src \
  .venv/bin/python tools/verify_agent_panel_execution_contract.py

PYTHONPATH=src .venv/bin/python -m py_compile \
  src/core/job_records.py \
  src/qt_panels/jobs_panel.py \
  src/qt_panels/agent_panel.py \
  src/qt_app.py \
  tools/verify_jobs_panel_contract.py
```

Boundary:

- legacy records remain in their current runner-owned directories;
- this branch does not implement the future project manifest, job IDs, migration,
  duration schema, retry, cancellation, deletion, approval, or Forge Pack export;
- malformed records are displayed as `INVALID`, not silently discarded;
- individual record reads are capped at 2 MiB, retained recent candidates are capped
  at 500, and decoded record bodies are capped at 16 MiB per refresh;
- inaccessible directories and record-stat failures surface as scan warnings;
- application close requests asynchronous scan interruption and defers destruction
  until every panel-owned `QThread` reports idle.

Backup status: no backup is claimed before merge and T1700 verification.

## 2026-07-19 — Read-only Shape Library evidence baseline branch

Status: `PLANNED` until the implementation PR merges and passes on the T1700.

Branch: `agent/restore-shape-library-evidence`.

Audit finding:

- no approved shape artifacts currently exist;
- legacy `shape_structure_harvest` records are raw AI reports, not extracted masks,
  SVGs, geometry, or approved reusable components;
- the project/approval authority required to create approved shapes is a later phase;
- inventing `workspace/data/shapes/approved` now would conflict with the canonical
  project layout.

Purpose:

- replace the Shape Library placeholder with a useful read-only evidence browser;
- load only when the user opens Shape Library, avoiding duplicate startup scans;
- filter existing Jobs evidence to shape-harvest records;
- preserve raw `SUCCESS`, `FAILED`, and `INVALID` distinctions;
- state visibly that approved shapes remain zero;
- expose no fake approval, extraction, correction, Morph, Make 3D, delete, or export
  action;
- participate in asynchronous application shutdown.

Verification commands:

```bash
cd /home/michael/MXZTAR-forge-v2.0
QT_QPA_PLATFORM=offscreen PYTHONPATH=src \
  .venv/bin/python tools/verify_shape_library_contract.py

QT_QPA_PLATFORM=offscreen PYTHONPATH=src \
  .venv/bin/python tools/verify_agent_panel_execution_contract.py
```

Boundary: this baseline creates no approved shape schema, files, or directory. Approval
requires the future project-authority and review workflows.

Backup status: no backup is claimed before merge and T1700 verification.

## Immediate next milestone after this ledger merges

Milestone name: **Project authority and lifecycle foundation**.

Required scope:

- create/open project manifest and canonical directory structure;
- source originals/previews and explicit processed-source lifecycle;
- stable artifact/run/project IDs and atomic writes;
- one-writer lock, read-only recovery, and SQLite rebuild boundary;
- no approval UI until durable approval derivatives can be written and validated.

Exit gate: durable project truth survives restart and derived-index deletion without
inventing competing storage locations.

## 2026-07-19 — Panel-owned QThread shutdown regression

Status: `VERIFIED` on the T1700 after PR #30 merged at `140c99c`.

Observed after PR #29 merge:

- every AgentPanel execution assertion printed `PASS`;
- process teardown then reported `QThread: Destroyed while thread '' is still running`;
- the verifier aborted and produced a core dump;
- therefore the verifier run is not a valid overall pass.

Root cause:

- the full-window verifier constructs My Library, which starts background thumbnail
  loading;
- window close stopped the Jobs scan introduced by PR #29 but did not stop My Library's
  pre-existing `ThumbnailLoader`;
- destroying a panel-owned running `QThread` is a fatal Qt lifecycle violation.

Required fix:

- My Library and Jobs expose non-blocking interruption requests and idle signals;
- main-window close requests both background scans to stop, rejects the current close
  event immediately, and keeps the Qt event loop responsive;
- the window closes automatically only after both panels report idle;
- AgentPanel and My Library verifiers assert no panel-owned thread remains running.

Verification commands:

```bash
cd /home/michael/MXZTAR-forge-v2.0
QT_QPA_PLATFORM=offscreen PYTHONPATH=src \
  .venv/bin/python tools/verify_agent_panel_execution_contract.py

QT_QPA_PLATFORM=offscreen PYTHONPATH=src \
  .venv/bin/python tools/verify_my_library_contract.py
```

Recorded result:

- AgentPanel execution contract passed and exited normally;
- My Library contract passed and exited normally;
- Jobs contract passed and exited normally after its shutdown API changed;
- no `QThread: Destroyed`, abort, or core dump followed any rerun.

Backup status: no new VX12 backup was recorded for the verification; no backup is
claimed by this entry.

## 2026-07-20 — Future Construct and World vision capture

Status: `PLANNED` until the documentation PR merges.

Purpose:

- preserve the founder's long-term direction without expanding or reordering Level One;
- define the product-family horizon: Forge, Construct, Infrastructure Builder, World;
- record lateral shape reasoning, modular compatibility, alignment/weld distinctions,
  materials, lighting, mechatronics, and hyper-grid command architecture;
- establish rig-friendly cyber-art as maximum visual identity per unit of computation;
- preserve the moon-scale infrastructure, ecology, authorship, fair-rights, portability,
  and generational-persistence vision;
- identify present-day ID, provenance, coordinate, compatibility, history, and
  performance-metadata consequences.

Authority:

- `docs/product/FUTURE_CONSTRUCT_AND_WORLD_VISION.md` is future vision, not a Level One
  implementation or marketing contract;
- `docs/product/MASTER_BUILD_PLAN.md` links to it without changing current phase order;
- the next permitted milestone remains Project Authority and Lifecycle Foundation.

Boundary: no 3D editor, renderer, world simulation, virtual ownership, cloud service,
engineering validation, or future-product feature is claimed as implemented.

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
