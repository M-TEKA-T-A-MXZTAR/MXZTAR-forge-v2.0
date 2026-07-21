# MXZTAR Forge v2.0 — Progress Ledger

## Ledger purpose

This ledger records what has actually been planned, implemented, merged, verified,
observed, deferred, blocked, or rejected.

It is not a wish list and it must not imply that planned functionality already exists.

Status values:

- `VERIFIED` — implemented and supported by recorded verification evidence;
- `MERGED` — source or documentation is present on `main` through a merged PR;
- `PARTIAL` — some path exists, but the complete contract is not yet proven;
- `OBSERVED` — behaviour was seen but is not yet fully reproduced or classified;
- `PLANNED` — defined in source-of-truth documentation but not implemented;
- `PLANNED REQUIRED` — required for the active product level but not implemented;
- `BLOCKED` — cannot proceed until a named prerequisite is satisfied;
- `DEFERRED` — intentionally outside the current active product levels;
- `REJECTED` — deliberately excluded from the current product boundary.

## Ledger consolidation note

This ledger was consolidated on 22 July 2026 as part of the editor-first roadmap
realignment. Detailed pre-realignment branch notes, verification commands, and historical
entries remain preserved in Git history through merged `main` commit `0923276`.

The consolidation removes stale “PR pending” statements and superseded next-gate text. It
does not erase repository history or convert planned functionality into verified work.

## Current product state

**Current planning era:** active Product Levels One and Two.

**Current primary objective:** establish the Forge Editor as the primary daily workspace,
beginning with a native editable shape document, scratch-built 2D shape creation, source-
derived extraction, Shape Library lifecycle, and verified SVG/PNG export.

**Current Level One promise:** a creator can import a source image or open a blank shape
document, create or extract shapes, edit them manually, save reusable assets, and export
validated 2D derivatives without requiring AI.

**Current Level Two promise:** after Level One is verified, a creator can convert shapes
into reversible 3D components, assemble or stitch them in a governed 3D environment, and
export validated blockouts.

**Current non-promise:** production-ready automatic 3D reconstruction, engineering
accuracy, manufacturing safety, finished CAD solids, finished topology, or universal
format compatibility.

**Deferred product levels:** Product Level Three and Product Level Four remain `DEFERRED`
until a separate future founder decision and source-of-truth revision. No delivery date
is assigned.

## Product-level ledger

| Product level | Status | Current boundary | Activation gate |
|---|---|---|---|
| Level One — Shape Editor and portable 2D assets | ACTIVE / PARTIAL FOUNDATION | Project authority, source intake, previews, guided navigation, and evidence paths exist; the native editor and approved shape lifecycle do not yet exist | Complete the editor-first milestones and Level One acceptance journey |
| Level Two — 3D Construct and portable blockouts | PLANNED | Product contract is defined; no Construct workspace or verified 3D export is claimed | Verified Level One editor, shape lifecycle, and 2D interoperability |
| Level Three | DEFERRED | Infrastructure relationships, regional state, distributed deltas, and advanced system-scale construction are future-only | Separate future founder decision after Levels One and Two |
| Level Four | DEFERRED | Cross-device platform, operator jobs, collaboration, immersive clients, economy, persistent regions, and world simulation are future-only | Separate future founder decision after preceding levels |

## Current implementation ledger

| Area | Status | Evidence / present state | Next gate |
|---|---|---|---|
| Repository source-of-truth policy | VERIFIED | `docs/SOURCE_OF_TRUTH.md`; Git history is authoritative | Keep required-document verifier aligned |
| Coding-practice and controlled-change rules | VERIFIED | Repository instructions and source-truth verification | Apply to every PR |
| Modest-hardware runtime policy | VERIFIED | CPU-only target, conservative threads, one heavy job by default | Preserve in editor and geometry operations |
| Relocatable repository launcher | VERIFIED historically | Checkout-relative launcher and verifier were merged and exercised during relocation | Preserve during release packaging |
| Desktop and application-menu launchers | VERIFIED historically | Repository installer and T1700 use established | Revalidate for official release packaging |
| Project manifest and self-contained directory | VERIFIED | PR #33; durable manifest, required directories, history, atomic creation, collision refusal | Extend only through versioned editor schema migration |
| Project one-writer lock and recovery classification | VERIFIED | PR #34; exclusive ownership and uncertain-state containment | Preserve for editor autosave and recovery |
| Project session and Start Here authority | VERIFIED | PR #35; create/open/close, writer release, read-only recovery attachment | Keep editor mutations session-owned |
| Project-contained source intake and processed lifecycle | VERIFIED | PR #36; copy/hash/preview, atomic authority updates, duplicate identity, explicit project-copy processing | Preserve external-byte immutability |
| Asynchronous project-source intake and discovery | VERIFIED | PRs #39–#41 and later deterministic reruns; Qt remains responsive and worker shutdown is cooperative | Reuse safe worker patterns for extraction |
| My Library visible source grid | VERIFIED | Visible cards, bounded thumbnails, exact source handoff, unchanged source bytes, safe shutdown | Add editor handoff without replacing source authority |
| Guided Next workflow | VERIFIED | PR #44 and project-source intake UI contract; safe navigation and exact-source handoff are covered | Extend guidance to Editor without silent heavy actions |
| My Library verifier lifecycle | VERIFIED | PR #45; stable idle detection and safe thread cleanup | Preserve in future asynchronous panels |
| Live My Library startup refresh guard | VERIFIED | PR #46; focused guard verifier and isolated deterministic rerun passed | Preserve worker ownership boundary |
| Accepted source-image compatibility | MERGED / DETERMINISTICALLY VERIFIED | PR #47; PNG, JPEG, WebP, BMP, TIFF, and GIF accepted for intake/preview under the documented boundary | Natural live confirmation when representative user files are available |
| Current model-ready image boundary | VERIFIED CONTRACT | PNG, JPEG, and WebP are model-ready; BMP, TIFF, and GIF are blocked before Ollama pending normalized derivatives | Implement provenance-preserving normalization before widening model support |
| Agent worker success/failure distinction | VERIFIED historically | Failed `AgentResult` records no longer become UI success merely because diagnostics were saved | Preserve in editor-assisted jobs |
| Project-owned model-call evidence | MERGED | PR #42; logs/diagnostics remain incomplete evidence, not approved artifacts | Define structured finding and review schema only when needed by editor assistance |
| Jobs evidence browser | VERIFIED historically | Read-only success/failure/invalid distinction and safe asynchronous shutdown | Add project-native editor and extraction job records |
| Shape Library evidence browser | VERIFIED historically | Raw shape-harvest evidence remains distinct from approved shapes; approved count truthfully zero | Replace evidence-only baseline with editable approved shape lifecycle |
| Native editable shape document | PLANNED REQUIRED | Editor-first contract defined in the master plan; no runtime schema exists | Next active milestone |
| Blank document creation | PLANNED REQUIRED | Required for AI-independent editing | Native shape document and project-owned save path |
| Scratch-built primitives and paths | PLANNED REQUIRED | Required Level One creator workflow | Editor command and undo/redo foundation |
| Node, handle, transform, layer, snapping, group, and boolean editing | PLANNED REQUIRED | Defined in Level One Editor contract | Incremental verified editor tools |
| Source-region selection and manual tracing | PLANNED REQUIRED | Required extraction baseline independent of AI | Editor canvas and source overlay model |
| Algorithmic contour/mask extraction | PLANNED | No approved extraction engine exists | Manual trace and editable candidate schema first |
| AI-assisted extraction proposals | PLANNED OPTIONAL | Prompt-level shape analysis exists; no approved editable-shape output | Candidate schema, source coordinates, and human correction path |
| Review, approval, rejection, versioning, and supersession | PLANNED REQUIRED | Artifact concepts exist; no approved shape runtime path | Editable shape schema and Shape Library write authority |
| SVG export profile | PLANNED REQUIRED | SVG is named as a core Level One output; no verified adapter is claimed | Native shape document and round-trip fixture |
| PNG export profile | PLANNED REQUIRED | PNG is named as a core Level One derivative; no editor export adapter is claimed | Native shape rendering and metadata contract |
| JPEG/WebP/TIFF/PDF derived profiles | PLANNED | Expose only after format-specific validation | Core SVG/PNG profiles first |
| Reversible 2D-to-3D component generation | PLANNED LEVEL TWO | No production component schema or operation history exists | Verified Level One shapes and construction-recipe schema |
| Construct 3D workspace | PLANNED LEVEL TWO | No viewport, assembly, stitch, or construction history is claimed | Reversible components first |
| GLB/glTF export | PLANNED LEVEL TWO | Named first general 3D adapter; not implemented | Construct scene contract and downstream import test |
| OBJ export | PLANNED LEVEL TWO | Named fallback profile; not implemented | Mesh and limitation contract |
| STL/3MF/DXF adapters | PLANNED LATER | Require format-specific units and validation | Core Level Two profiles first |
| STEP/OpenUSD/FBX adapters | DEFERRED ADAPTERS | Require mature solid, assembly, legal, and round-trip contracts | Separate verified adapter milestones |
| Formal software licence | BLOCKED | Public repository has no founder-selected recognised `LICENSE` | Founder decision before official public release |
| Free-of-charge core access | PLANNED REQUIRED | Confirmed product policy; no timed trial, subscription, or core feature paywall | Release acceptance and UI wording |
| Voluntary founder support | PLANNED | `https://buymeacoffee.com/mxztar`; cannot alter file access or core features | Truthful non-intrusive release/UI link |

## Verified foundation summary

### Planning and authority foundations

- PR #14 established the historical first-release workflow and compatibility concepts.
- PR #15 established artifact-envelope, status, provenance, validation, and failure
  concepts.
- PR #16 established durable project files as authority and SQLite as a rebuildable
  derivative.
- PR #17 established the original master plan and progress-ledger governance.
- PRs #33–#36 established the current verified project manifest, locking, session, source
  intake, and processed-source authority.

### Operational shell and source workflow

- My Library evolved from a selector into a visible bounded-thumbnail grid with exact
  source handoff and safe shutdown.
- Jobs and Shape Library provide truthful read-only evidence baselines without inventing
  approval or extraction.
- Agent Workflows execute outside the Qt main thread and preserve success, saved failure,
  and unsaved failure distinctions.
- Project-owned sources save model-call evidence under project logs or diagnostics while
  remaining explicitly incomplete and unapproved.

### Recent merged sequence

| PR | Merged result | Recorded boundary |
|---|---|---|
| #39 | Asynchronous project-aware source intake and discovery | Intake is not analysis, extraction, approval, or processing |
| #40 | Hardware-kind project-intake UI verifier deadline | Production behaviour unchanged |
| #41 | Stable Qt idle detection for intake/discovery handoff | Verifier-only lifecycle correction |
| #42 | Project-owned workflow run evidence | Successful model call is not completed workflow or approved artifact |
| #43 | My Library minimum-layout and retained preview correction | Source authority unchanged |
| #44 | Guided Next workflow | Heavy Ollama execution remains explicit human action |
| #45 | My Library verifier lifecycle correction | Production behaviour unchanged |
| #46 | Live startup refresh guard | Worker ownership prevents QThread replacement race |
| #47 | Broadened source image compatibility and PNG thumbnail fix | BMP/TIFF/GIF accepted for preview but blocked from model execution |

## 22 July 2026 deterministic verification record

Repository state at verification:

- local branch: `main` only;
- remote branch: `origin/main` only;
- working tree: clean;
- merged head: `0923276`.

Isolated persistent-log results:

```text
source-image-compatibility  0
live-startup-refresh-guard  0
my-library-contract         0
project-source-intake       0
guided-workflow-discovery   127
source-truth                0
```

Interpretation:

- source-image compatibility contract passed;
- live startup refresh guard passed;
- My Library contract passed;
- project-source intake UI contract passed;
- guided Next behaviour passed inside the project-source intake UI contract;
- `guided-workflow-discovery 127` means no separately named guided verifier was found,
  not that guided behaviour failed;
- source-truth, Python compilation, required documents, and all seven prompt contracts
  passed.

Live acceptance boundary:

- no representative user PNG, BMP, or TIFF was available for a separate manual visual
  acceptance run;
- PR #47 is therefore deterministically verified and provisionally accepted;
- live confirmation may occur naturally when those formats enter a real workflow;
- no live-format failure is currently recorded.

## Unresolved observation register

### OBS-001 — Historical Ollama HTTP 400 and confusing completion text

Status: `PARTIAL RESOLUTION`.

Resolved portions:

- worker success semantics distinguish successful result, saved failure diagnostic, and
  exception;
- project-owned model evidence distinguishes `model_call_succeeded` from completed,
  validated, or approved workflow output;
- non-model-ready formats are blocked before Ollama under PR #47.

Still open:

- the historically failing large JPEG/model combination requires current controlled
  reproduction before being classified closed;
- full structured findings and editor-assisted extraction output remain unimplemented;
- cancellation and timeout artifact behaviour remain incomplete.

Do not close OBS-001 solely because the editor-first roadmap reduces AI centrality.

### OBS-002 — Live representative PNG/BMP/TIFF acceptance not performed

Status: `OBSERVED ABSENCE`, not a defect.

- deterministic fixtures exercised portrait PNG, BMP, TIFF, and GIF paths;
- no suitable user file was available for a manual visual acceptance run;
- the system is provisionally accepted until natural live use supplies evidence.

## 22 July 2026 — Editor-first roadmap realignment

Status: `PLANNED`; documentation branch `agent/editor-first-roadmap`; draft PR #48.

Founder decisions recorded:

- the Forge Editor becomes the primary daily workspace and expected most-used feature;
- users must be able to import source images, extract shapes, create shapes from scratch,
  edit them, save reusable assets, and export relevant interoperable formats;
- Level One is the AI-independent 2D Shape Editor and portable-asset foundation;
- Level Two adds reversible 2D-to-3D components, a governed 3D Construct environment,
  assembly/stitch distinctions, and validated 3D export;
- Product Levels Three and Four remain deferred until a future explicit decision;
- no single format is universal, so adapters must declare target workflow, units, axes,
  limitations, and verification evidence;
- existing verified project authority, source immutability, modest-hardware policy, and
  Qt worker safety remain mandatory.

Documentation changed:

- `README.md`;
- `docs/product/MASTER_BUILD_PLAN.md`;
- `docs/PROGRESS_LEDGER.md`.

This branch changes planning documentation only. It does not claim that the editor,
manual drawing tools, extraction, approved Shape Library writes, 3D construction, or new
export adapters are implemented.

Verification required before merge:

```bash
bash scripts/verify_source_truth.sh
git diff --check main...HEAD
```

Backup status: no new VX12 backup is claimed by this documentation branch.

## Next permitted milestone

Milestone name: **Editor architecture and native shape document**.

Required scope:

1. define one versioned native shape-document schema;
2. define coordinate space, units, bounds, path/node representation, layers, groups,
   anchors, fill/stroke, and source relationships;
3. define editor command, undo/redo, durable history, autosave, recovery, and
   supersession rules;
4. build the minimum project-owned blank-document Editor shell;
5. prove create, one reversible edit, save, close, reopen, and interrupted-write recovery;
6. expose no unsupported drawing, boolean, extraction, 3D, or export controls.

Exit gate:

- a blank shape document is durable project truth;
- the user can make one verified reversible edit;
- restart restores the editable document;
- a failed or interrupted save cannot replace the last valid version;
- the milestone works without AI or network access;
- all existing project, source, My Library, Jobs, Agent Workflows, and Qt lifecycle
  contracts remain green.

## Ledger update contract

Every meaningful merged milestone must add or update:

- date;
- PR number;
- branch;
- purpose and exact scope;
- files changed;
- verification commands;
- verification result;
- status changes;
- new and closed observations;
- remaining blockers;
- next permitted milestone;
- backup status where relevant.

No milestone may be marked `VERIFIED` solely because code was committed or a PR was
merged.
