# MXZTAR Forge v2.0 — Recovery and Completion Plan

## 1. Purpose

This document is the active recovery, consolidation and completion sequence for MXZTAR Forge v2.0.

It does not replace the finished-product boundary in `MASTER_BUILD_PLAN.md`. It converts that boundary into a safer engineering order after accumulated regressions, layered runtime corrections, stale documentation and verification gaps.

The objective is simple:

> Recoup the learning, regroup the architecture, preserve the working product, and proceed through a finite evidence-led sequence.

## 2. Recovery principles

1. Preserve accepted behaviour before simplifying architecture.
2. Correct governing truth before adding more capability.
3. Test the official final runtime, not intermediate classes.
4. Make state ownership explicit before expanding workflows.
5. Measure scope by the complete user action and invariants.
6. Require live acceptance before merging interaction-heavy changes.
7. Record causal learning so the same class of failure is not rediscovered.
8. Remove duplicate or obsolete authority only after its useful content has been reconciled.
9. Avoid sweeping rewrites; retire compatibility layers incrementally.
10. Tie every milestone to durable creator value and a truthful demonstration.

## 3. What may be omitted or retired

The following may be removed, archived or collapsed after reconciliation and verification:

- stale present-tense capability snapshots;
- exact-date and exact-PR documentation assertions that fossilise old state;
- duplicate descriptions of the same workflow with different authority;
- compatibility patches whose behaviour has moved into the canonical component;
- intermediate UI shells no longer used by the official launcher;
- direct-handler tests superseded by real-event tests;
- fake, disabled or premature controls;
- future-level plans that are not needed to complete Stage One and Stage Two;
- historical implementation commentary already preserved by Git history and the Progress Ledger.

The following must not be omitted:

- project and document authority;
- save, reopen, rollback and recovery behaviour;
- direct 2D and 3D interaction invariants;
- source provenance and editable-geometry authority;
- human approval boundaries;
- modest-hardware constraints;
- truthful failure states;
- verification evidence and known remaining risk.

## 4. Recovery phases

### Phase R0 — Governance reset

Deliverables:

- strengthened `AGENTS.md`;
- simplified `SOURCE_OF_TRUTH.md` authority order;
- this Recovery and Completion Plan;
- `REGRESSION_AND_DRIFT_REGISTER.md`;
- refreshed Current Capability Boundary through the latest merged baseline;
- removal of stale documentation-verifier assumptions.

Exit evidence:

- documents agree on product horizon, present capability and immediate sequence;
- no current-state verifier requires obsolete dates, PR numbers or phrases;
- no planned capability is described as implemented.

### Phase R1 — Final-runtime map

Create a durable map of:

- official launcher;
- final window and Editor composition;
- subclasses and replacements;
- startup installers and their order;
- signal rewiring;
- project, document, shape, object, camera and persistence state owners;
- compatibility layers and intended retirement targets.

Exit evidence:

- one diagram or table identifies the final path for each major user action;
- every runtime patch layer has a stated reason, owner and retirement status;
- tests can instantiate the same composition used by the official launcher.

### Phase R2 — Acceptance harness correction

Upgrade verification so it proves user experience:

- real mouse and wheel events;
- final composed runtime;
- geometry and visibility assertions;
- pointer/object lock during drag;
- save, close and reopen;
- interrupted-work and rollback checks where applicable;
- automatic verifier discovery or a manifest that fails when required verifiers are omitted.

Exit evidence:

- interaction regressions from PR #66–#80 are represented by durable contracts;
- T1700 live-acceptance checklist is attached to interaction-heavy PRs before merge;
- deterministic and live evidence are labelled separately.

### Phase R3 — Canonical interaction foundation

Consolidate accepted Editor behaviour without redesigning it:

- one canonical Editor composition;
- explicit select/move/resize/delete command boundaries;
- clear object-versus-camera interaction rules;
- stable front orthographic Design View as editing default;
- deliberate orbit and perspective viewing controls;
- exact 2D and 3D pointer-following;
- durable minimum geometry and paired-membership rules.

Compatibility installers may remain temporarily, but each consolidation change must retire at least one ambiguity or duplicate authority.

Exit evidence:

- create, select, move, resize, delete, undo/redo, save and reopen pass in the official runtime;
- nonselected objects, camera state and adjacent controls remain unchanged unless explicitly targeted;
- live T1700 acceptance passes.

### Phase R4 — Stage One asset workflow

Implement the smallest complete path from source or blank document to a reusable editable asset:

1. blank shape and freeform path foundation;
2. source-region selection;
3. manual trace baseline;
4. deterministic candidate extraction;
5. node and handle correction;
6. review, approval, rejection and supersession;
7. Shape Library insertion through reversible commands;
8. validated SVG and PNG continuation profiles;
9. Forge Pack packaging.

Exit evidence:

- a creator can produce, approve, reopen, reuse and export one portable 2D asset without AI or network access;
- AI evidence cannot silently become approved geometry;
- a demonstrable asset exists for product communication and user testing.

### Phase R5 — Stage Two component workflow

Implement the smallest complete path from approved shape to reversible 3D blockout:

1. reviewed shape-to-component recipe;
2. stable component identity and parent relationship;
3. object, surface, area, pivot and anchor records;
4. placement and snapping separated from camera navigation;
5. groups and recoverable assemblies;
6. explicit contact, seam, stitch/weld, join, boolean, separate and bake distinctions;
7. validated GLB/glTF or OBJ continuation profile.

Exit evidence:

- an approved 2D asset becomes a reversible 3D component;
- components can be placed into a recoverable assembly;
- one named downstream continuation test succeeds.

### Phase R6 — Release hardening

- clean install and launcher test;
- migration and recovery fixtures;
- bounded performance on the T1700;
- documentation and public claims reconciled;
- licence decision recorded before describing the repository as open source;
- support and commercial language remains truthful;
- backup and release evidence captured.

Exit evidence:

- a new user can install, create, save, reopen, recover and complete the demonstrated Stage One–Two journey;
- known limitations are explicit;
- no deferred feature appears as an active control or release claim.

## 5. Pull-request contract

Every meaningful PR must state:

- user action and product stage;
- problem and causal mechanism;
- final runtime path affected;
- authority owner affected;
- allowed change;
- preserved invariants;
- changed files;
- automated evidence;
- T1700 live-acceptance status when applicable;
- documentation updates;
- remaining risk;
- rollback or recovery path.

A PR that repairs a regression must also update the Regression and Drift Register.

## 6. Milestone priority rule

Work is prioritised in this order:

1. data loss, corruption, unsafe authority or unrecoverable state;
2. inability to complete a currently advertised user action;
3. interaction drift, regression or misleading UI;
4. verification gaps that permit recurrence;
5. consolidation that reduces competing runtime authority;
6. Stage One asset completion;
7. Stage Two component and assembly completion;
8. release, discovery and commercial refinement;
9. deferred future vision.

## 7. Commercial and user-value gate

Each milestone must answer:

- What durable asset can the creator make or improve?
- What time, confusion or rework does this remove?
- What truthful demonstration becomes possible?
- What reusable project knowledge is retained?
- What current public claim becomes more credible?

Feature count is not the success measure. Completed, recoverable and reusable creator outcomes are.

## 8. Immediate sequence

The authorised immediate order is:

1. merge the governance reset after review;
2. update the stale documentation verifier so it checks relationships and recency rather than frozen phrases;
3. produce the final-runtime and state-authority map;
4. convert PR #66–#80 regression lessons into final-runtime contracts;
5. run the complete Source Truth suite and T1700 interaction acceptance;
6. begin the Stage One editable-path and manual-trace foundation only after the interaction baseline is stable.

No new broad feature family should begin before steps 1–5 are complete.