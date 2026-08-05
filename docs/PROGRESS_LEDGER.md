# MXZTAR Forge v2.0 — Progress Ledger

**Ledger date:** 6 August 2026  
**Repository:** `M-TEKA-T-A-MXZTAR/MXZTAR-forge-v2.0`  
**Merged baseline assessed:** `main` through PR #80  
**Active gate:** governance recovery and final-runtime acceptance  
**Next feature gate:** Freeform Path Authority only after the complete Editor baseline passes

This ledger records concise dated product evidence, sequencing decisions, and causal learning. Git history and PR discussions retain exhaustive implementation detail.

## 1. Status vocabulary

| Status | Meaning |
|---|---|
| LIVE VERIFIED | Applicable automated evidence and recorded T1700 live acceptance exist |
| DETERMINISTICALLY VERIFIED | Focused automated evidence exists; live, downstream, or release proof may remain |
| MERGED | Change is on `main`; merge alone is not product acceptance |
| PARTIAL | Useful foundation exists, but the complete user workflow does not |
| PLANNED | Required by active Stage One–Two scope but not implemented |
| BLOCKED | A named dependency or decision prevents safe progress |
| DEFERRED | Outside the active MXZTAR Forge v2.0 sequence |

## 2. Product direction retained

MXZTAR Forge v2.0 remains a local-first, human-governed creative concept-engineering forge.

The intended value path is:

```text
Purpose
→ project
→ source image, starter asset, or blank document
→ editable geometry
→ correction and review
→ reusable 2D asset
→ reversible 3D component
→ recoverable construction
→ verified downstream handoff
```

Stage One and Stage Two define v2.0. Product Levels Three and Four remain deferred.

## 3. Recovered implementation phases

### Phase A — Repository, worker, and truthful evidence foundation

PRs #1–#31 established repository controls, agent-worker semantics, modest-hardware policy, source browsing, bounded thumbnails, guided workflow, Jobs evidence, Shape Library evidence, and clean Qt worker shutdown.

Key retained lesson: a printed PASS followed by a live `QThread` abort is a failure, not a pass.

### Phase B — Project authority and source lifecycle

PRs #33–#47 established canonical project identity, one-writer locking, read-only recovery, project sessions, copy-only source intake, asynchronous discovery, project-owned model evidence, guided source handoff, image compatibility, and startup thread guards.

Key retained lesson: selection, project attachment, project-owned copies, previews, model-ready inputs, and canonical evidence are separate states.

### Phase C — Editor-first product realignment

PRs #48–#53 established the Stage One–Two product direction, native shape-document authority, minimum reversible Editor, Purpose-driven Project Birth, project routing, menu primitives, and the five implemented native shapes.

Key retained lesson: a stable product boundary should have existed before rapid runtime expansion. It now lives in the simplified Master Build Plan.

### Phase D — Integrated shape/object CAD foundation

PRs #54–#60 established linked project-owned 3D objects, isolated single-object editing, project/document switching and deletion, CodeQL reconciliation, current-capability documentation, and transient positioning guides with optional snapping.

Key retained lesson: object state, camera state, project authority, and paired 2D/3D membership require explicit separate owners and invariants.

### Phase E — Interaction accessibility and live-acceptance corrections

PRs #61–#73 addressed page scrolling, 3D wheel routing, active-output reveal, sticky controls, rejected permanent action-tree presentation, compact command-strip recovery, document lifecycle, visible deletion, project-menu unification, selector availability, and shared project-switch targets.

Key retained lessons:

- handler calls do not prove real Qt event propagation;
- `isVisible()` does not prove useful viewport placement;
- a persistent control can still consume too much workspace;
- a deterministic test may pass while the live user journey remains poor;
- changing project controls must preserve a deliberate switch path.

### Phase F — Transform separation and direct-manipulation restoration

PRs #74–#80 separated object transforms from camera orbit, restored direct resize and Save Project, restored Select-mode movement, corrected 3D re-entry, implemented precise pointer-mapped 2D/3D movement, restored front orthographic 3D Design View, and added durable direct 2D resize.

Key retained lessons:

- adding explicit advanced modes must not erase the direct manipulation path users already rely upon;
- object movement must preserve the grabbed pointer offset and camera/grid landmarks;
- 3D entry state is part of the user contract;
- direct 2D edits must synchronize the paired 3D object through persistence and Undo/Redo;
- a feature split across several restoration PRs indicates the original user-story boundary was too narrow.

## 4. Governance-recovery finding — 6 August 2026

The repository’s present-tense capability document and Progress Ledger remained anchored around PRs #63–#67 while `main` had advanced through PR #80.

The documentation drift verifier required exact historical phrases and an old PR range. It therefore protected a stale snapshot rather than proving current truth.

The official runtime was also composed through:

- ordered startup installers;
- successive shell inheritance;
- repeated Editor panel replacement;
- method patching and retained class aliases.

This architecture made narrow repairs inexpensive, but made patch order and final-class selection part of correctness.

## 5. Recovery action

The governance-recovery branch introduces:

- a rewritten `AGENTS.md` with final-runtime, invariant, state-authority, and proof rules;
- a simplified stable `MASTER_BUILD_PLAN.md`;
- a current `CURRENT_CAPABILITY_BOUNDARY.md` through PR #80;
- `ACTIVE_ENGINEERING_PLAN.md` as the only near-term sequencing authority;
- `REGRESSION_AND_DRIFT_PREVENTION.md` as the causal engineering doctrine;
- `FINAL_RUNTIME_COMPOSITION.md` as the official launcher and patch map;
- a rewritten Source of Truth hierarchy;
- structural documentation verification instead of PR #63-era phrase preservation.

This gate changes governance and verification only. It does not claim a runtime feature change.

## 6. Current workspace truth

| Workspace | Current truth |
|---|---|
| Start Here | Project discovery, Purpose-driven creation, open/switch, close, and recoverable project management foundation exists |
| Editor | Primary integrated native 2D shape and linked 3D object workspace |
| My Library | Project/legacy source browser with bounded previews and guarded lifecycle |
| Shape Library | Raw evidence browser only; approval and reusable insertion remain planned |
| Agent Workflows | Optional local assessment and planning evidence; not geometry authority |
| Jobs | Read-only success, failure, and invalid evidence browser |
| Construct | Current linked object-scene and transform foundation only; general recipes and assemblies remain planned |
| Review | Planned as a real approval/version workflow |
| Export | Named verified continuation profiles remain planned |

## 7. Current interaction foundation through PR #80

Current merged and focused deterministic contracts include:

- direct 2D movement with click-offset preservation;
- direct 2D resize with one handle, minimum dimensions, and Square/Circle proportional constraints;
- paired 3D X/Y and planar-size synchronization;
- direct 3D movement and resize;
- explicit Select, Move, Rotate, Resize, and Orbit View modes;
- stable world/camera landmarks during selected-object transforms;
- front orthographic 3D Design View on entry;
- deliberate Perspective and Orbit controls;
- positioning guides, measurements, optional snapping, and separated wheel routes;
- Save Project transaction and project/document controls.

Fresh consolidated T1700 acceptance of the entire official runtime remains the next gate before new geometry work.

## 8. Active sequence

1. merge governance recovery after review;
2. create one final-runtime factory/fixture and consolidated Editor acceptance path;
3. run focused, complete, and T1700 live acceptance through PR #80 behaviour;
4. resolve any baseline regression without adding new feature scope;
5. begin Freeform Path Authority;
6. proceed to manual tracing, deterministic extraction, starter assets, review/Shape Library, and then general shape-to-component recipes.

The detailed gate requirements live in `docs/product/ACTIVE_ENGINEERING_PLAN.md`.

## 9. Current risks

- startup installer and patch order remains behaviourally significant;
- multiple shell and panel layers can cause wrong-class verification;
- current interaction contracts remain distributed across several modules;
- Source Truth manually lists many compile and verifier files;
- historical correction documents can confuse future agents unless clearly de-authorised;
- live acceptance must occur before merge for interaction-heavy changes;
- no freeform path authority exists yet, so source tracing and reusable asset generation remain blocked.

## 10. Evidence rule

No capability becomes verified solely because code is committed or merged.

Evidence may include:

- compile and import checks;
- schema and command replay;
- transaction, interruption, and rollback proof;
- final-runtime real Qt event delivery;
- minimum-window and layout geometry;
- pointer fidelity and camera-landmark comparison;
- save, close, reopen, and recovery;
- T1700 live interaction;
- downstream continuation or release installation.

## 11. Cross-project lesson

The reusable doctrine is:

```text
Recoup accepted decisions and working behaviour
→ Regroup authority, runtime composition, and invariants
→ Proceed with one complete verified user-value slice
```

Reliability is not separate from business progress. It protects founder attention, demonstration quality, support cost, truthful marketing, and the speed at which future assets can become sellable.