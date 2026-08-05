# MXZTAR Forge v2.0 — Regression and Drift Prevention

## 1. Purpose

This document converts the Forge build history into a reusable engineering control system.

A regression is not treated only as a defective line of code. The review must identify the condition that allowed a previously accepted user outcome, invariant, authority boundary, or product truth to disappear.

The objective is:

```text
observe failure
→ identify causal assumption
→ repair the user workflow
→ strengthen proof
→ reduce the chance of recurrence across every project
```

## 2. Recurring causal classes

### A. Final-runtime mismatch

A verifier or change targets an intermediate class, unpatched panel, direct handler, or different import order from the official launcher.

Control: every interaction contract must name and instantiate the final runtime composition documented in `FINAL_RUNTIME_COMPOSITION.md`.

### B. Assertion-to-experience gap

A narrow assertion is technically true but does not prove usability. Examples include testing `isVisible()` without viewport placement, checking coordinates without pointer fidelity, or confirming a control exists without proving the workflow is understandable.

Control: express acceptance as an observable user outcome plus measurable layout, event, persistence, and recovery evidence.

### C. Competing state ownership

Selection, attachment, canonical state, autosave, preview, camera, object, and document state are conflated.

Control: identify one owner for every state domain and reject writes from non-authoritative views.

### D. Patch-order dependency

Multiple startup installers, class replacements, and monkey-patches make import order part of behaviour.

Control: document the order, verify it, prevent new patches without a retirement path, and consolidate proven behaviour into first-class components one bounded slice at a time.

### E. Fragmented user-story delivery

A complete action is divided into several PRs without preserving its full interaction contract. A later feature then removes the direct path restored by an earlier feature.

Control: use a vertical user-action slice as the change unit. Include direct manipulation, persistence, paired synchronization, Undo/Redo, and mode transitions where applicable.

### F. Verification-environment mismatch

Fast hardware, fake events, unisolated settings, premature idle checks, or incomplete Qt shutdown create false passes or false failures.

Control: use hardware-kind deadlines, consecutive-idle checks, isolated settings before `QApplication`, real Qt events, final cleanup in `finally`, and T1700 evidence for hardware-sensitive work.

### G. Documentation fossilisation

A drift test hard-codes an old PR range or exact historical wording. Stale documentation then passes because the verifier protects the obsolete snapshot.

Control: verify structural relationships, current baseline metadata, prohibited authority duplication, and required status distinctions—not an indefinitely frozen paragraph.

### H. Merge-before-acceptance

A PR reaches `main` before live interaction proves layout, pointer, timing, or comprehension requirements.

Control: live acceptance is a pre-merge gate for interaction-heavy work unless the PR is explicitly marked as deterministic-only and is not merged into the accepted baseline.

## 3. Change packet

Every meaningful change must carry this packet in the PR body or a linked issue:

### User outcome

One sentence describing what the user can complete.

### Final runtime target

Exact launcher, installer chain, shell, panel, controller, and command path.

### Authority map

| Domain | Owner | Rebuildable views |
|---|---|---|
| Project | Project session and validated project files | selectors, labels, recent-project state |
| Shape document | canonical shape document and command history | canvas items, selection handles, autosave preview |
| 3D scene | project-owned object-scene document | projected faces, inspector controls |
| Camera/view | declared scene view state | screen projection and transient drag state |
| Job/evidence | saved job or diagnostic record | progress labels and browser cards |

Extend the table when a change introduces another state domain.

### Allowed change

The exact behaviour that may differ after the PR.

### Preserved invariants

List all adjacent accepted behaviour. “Unrelated behaviour remains unchanged” is insufficient when the affected surface contains known interactions.

### Failure contract

State what remains authoritative after validation failure, interruption, partial write, rollback failure, or shutdown.

### Proof plan

Name focused, complete, live, restart, interruption, and downstream evidence as applicable.

## 4. Interaction proof rules

For Qt interaction claims:

- send real mouse and wheel events through Qt;
- prove target priority when handles and object bodies overlap;
- prove the grabbed point remains beneath the pointer where direct manipulation promises that behaviour;
- compare fixed world or screen landmarks to prove camera stability;
- verify mode entry, exit, re-entry, and the first action after re-entry;
- verify minimum supported window geometry and clipping;
- verify controls remain reachable after scrolling and output reveal;
- verify one durable command per completed action;
- verify preview state is not mistaken for canonical state;
- verify Undo, Redo, save, close, reopen, and paired 2D/3D synchronization.

## 5. Runtime-composition control

The official launcher composition is a temporary compatibility architecture, not a preferred permanent pattern.

Rules:

1. The runtime map must be updated when installer order, shell inheritance, panel replacement, or monkey-patched methods change.
2. A new startup patch requires:
   - a reason first-class composition is not yet safe;
   - an idempotence guard;
   - a focused final-runtime verifier;
   - a named consolidation or removal target.
3. No patch may silently retain an alias to a superseded class and then verify the alias instead of the live class.
4. Consolidation occurs one accepted workflow at a time; no sweeping rewrite is authorised merely because patch debt exists.

## 6. Documentation authority control

Each current document has one job:

- `MASTER_BUILD_PLAN.md`: stable product boundary and milestone logic.
- `CURRENT_CAPABILITY_BOUNDARY.md`: present-tense implemented, partial, planned, and deferred truth.
- `ACTIVE_ENGINEERING_PLAN.md`: current ordered gate and exit evidence.
- `PROGRESS_LEDGER.md`: concise dated evidence and causal learning.
- `SOURCE_OF_TRUTH.md`: authority hierarchy and conflict resolution.

A current-state change is incomplete until these responsibilities remain synchronized.

Historical correction documents may preserve evidence, but they do not outrank current authority unless explicitly promoted.

## 7. Root-cause record

When a regression is found, record:

```text
Observed failure:
Previously accepted outcome:
Change that exposed or caused it:
Causal assumption:
Architecture condition:
Why existing verification passed:
Immediate repair:
Stronger invariant:
New or strengthened evidence:
Consolidation debt:
Cross-project lesson:
```

Do not attribute every defect to one person or model. Separate founder-directed requirement changes, implementation mistakes, inadequate tests, architecture debt, and documentation drift.

## 8. Merge gates by risk

### Documentation-only

- authority conflict review;
- links and syntax;
- documentation contract;
- no unsupported capability claim.

### Core state or persistence

- schema and command replay;
- transaction and rollback;
- interruption and restart;
- authority remains explicit.

### Qt interaction

- final-runtime real-event verifier;
- complete Source Truth;
- minimum-window and workflow-comprehension check;
- T1700 live acceptance before merge.

### AI or long-running job

- no main-thread work;
- one-job guard;
- visible progress and terminal state;
- bounded timeout and resources;
- saved success/failure evidence;
- clean shutdown.

### Export or release claim

- named profile;
- validation fixture;
- downstream continuation/import proof;
- limitations recorded;
- installation and recovery evidence.

## 9. Quality indicators

Review these trends periodically:

- number of restoration PRs after feature PRs;
- number of live defects found after merge;
- days between runtime change and capability-document update;
- number of startup patches and panel replacements;
- tests using intermediate rather than final runtime classes;
- repeated defects in the same interaction family;
- founder hours spent repairing versus advancing user value.

The purpose is not blame or vanity metrics. The purpose is to expose where engineering effort is failing to compound.

## 10. Recovery doctrine

Forge proceeds by:

1. **Recoup:** recover decisions, accepted behaviour, evidence, and useful architecture.
2. **Regroup:** remove competing authority, identify the final runtime, and define the next complete gate.
3. **Proceed:** deliver one verified user-value slice while preserving every named invariant.

Reliability, truthful product claims, and a comprehensible workflow are commercial capabilities. They protect founder time and make future features easier to demonstrate, support, and sell.