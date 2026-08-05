# MXZTAR Forge v2.0 — Source of Truth Policy

## 1. Purpose

This policy defines which records govern MXZTAR Forge v2.0, how conflicts are resolved, and what evidence is required before a capability claim is accepted.

The repository must have one coherent authority chain. Historical corrections and addenda may explain decisions, but they must not remain permanent competing sources of current instruction.

## 2. Software-project authority

Priority order:

1. committed Git history on the reviewed target branch;
2. current reviewed pull-request state;
3. current local working tree;
4. dated VX12 safety backups;
5. terminal scrollback.

Terminal scrollback is not project truth. Decisions, contracts, verification evidence and results must be saved in repository documents, code, tests or GitHub records.

## 3. User creative-work authority

For a Forge project, validated durable files inside the project directory are authoritative.

SQLite, indexes, previews, caches, queues, settings and in-memory state may accelerate or display project state, but must remain rebuildable and must not silently override canonical project files.

Detailed data authority is defined by:

- `docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md`;
- `docs/product/OUTPUT_ARTIFACT_CONTRACTS.md`.

## 4. Governing document hierarchy

1. **`docs/product/MASTER_BUILD_PLAN.md`** — finished Stage One–Two product boundary, workflow families, architecture and acceptance intent.
2. **`docs/product/RECOVERY_AND_COMPLETION_PLAN.md`** — active consolidation, recovery and engineering sequence until the runtime and verification baseline is stable.
3. **`docs/product/CURRENT_CAPABILITY_BOUNDARY.md`** — concise present-tense truth about merged capability, partial foundations, limitations and next gate.
4. **`docs/architecture/FINAL_RUNTIME_AND_STATE_AUTHORITY_MAP.md`** — official launcher, installer order, final window and Editor composition, mutable-state owners and compatibility-layer retirement status.
5. **`docs/PROGRESS_LEDGER.md`** — dated implementation and verification chronology.
6. **`docs/REGRESSION_AND_DRIFT_REGISTER.md`** — causal learning and recurrence-prevention status.
7. **`docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md`** — workflow readiness, inputs, outputs, failures, blockers and next-action rules.
8. **`docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md`** — project truth, recovery and index authority.
9. **`docs/product/OUTPUT_ARTIFACT_CONTRACTS.md`** — durable artifact, approval, diagnostic, component, assembly and export contracts.
10. **`README.md`** — public explanation and repository orientation; it may not exceed current capability truth.

Other product notes, corrections, addenda and future-vision documents are supporting evidence only. Their still-valid requirements must be reconciled into the governing documents above. They do not override the hierarchy by remaining newer or more specific indefinitely.

When documents conflict:

1. obey the highest applicable authority;
2. preserve working and recoverable behaviour;
3. record the conflict;
4. correct or retire the lower document in a dedicated change.

## 5. Active product horizon

The active finished-product boundary is:

- **Stage One — Forge Editor and portable editable 2D assets**;
- **Stage Two — Construct and portable reversible 3D blockouts**.

Stage One and Stage Two together define MXZTAR Forge v2.0.

Future Product Levels Three and Four are deferred. They do not authorise runtime work, controls, delivery claims or public promises without a founder-approved revision to this authority chain.

## 6. Planning versus current state

The Master Build Plan states what the finished product is permitted to become.

The Recovery and Completion Plan states the active engineering order.

The Current Capability Boundary states what users can do now.

The Final Runtime and State Authority Map states which launcher, installers, classes and state owners actually serve those current user actions.

The Progress Ledger states what changed and when.

The Regression and Drift Register states why important failures occurred and how recurrence is prevented.

Planned capability must never appear in the README, interface or marketing as implemented capability.

## 7. Final-runtime evidence rule

A merged PR, isolated unit result or intermediate-widget test is not sufficient proof of user capability.

Runtime claims must identify applicable evidence:

- syntax or import check;
- deterministic contract;
- final composed-runtime contract;
- real Qt event delivery;
- canonical save and reopen;
- interruption, rollback or recovery;
- T1700 live interaction;
- downstream import or continuation;
- clean release installation.

The official launcher and all installed runtime corrections are part of the tested system. A feature that passes only before final composition is not verified.

The Final Runtime and State Authority Map is the composition reference. Runtime work must update it when the launcher, installer order, final class binding, state owner or compatibility-layer retirement status materially changes.

Deterministic verification and live acceptance must be labelled separately. Interaction-heavy changes require T1700 live acceptance before merge unless the PR remains explicitly draft or blocked.

## 8. Change contract

Every meaningful change records:

- user action and product stage;
- final runtime path;
- authoritative state owner;
- allowed change;
- preserved invariants;
- failure and recovery behaviour;
- affected files and artifacts;
- verification commands and actual results;
- live-acceptance status where required;
- remaining risk;
- documentation impact.

A regression repair also records causal learning in `docs/REGRESSION_AND_DRIFT_REGISTER.md`.

No pass may be claimed without evidence from the environment that ran the check.

## 9. Drift-prevention workflow

Before work:

1. confirm branch, status and latest remote state;
2. identify product stage and complete user action;
3. inspect Master Plan, Recovery Plan, Current Capability and recent related history;
4. trace the official final runtime and state owners through `docs/architecture/FINAL_RUNTIME_AND_STATE_AUTHORITY_MAP.md` and current source;
5. declare preserved invariants;
6. verify the relevant baseline still launches or passes.

After work:

1. compile changed code where applicable;
2. run targeted checks;
3. run final-runtime, persistence and recovery checks appropriate to risk;
4. complete required T1700 live acceptance;
5. run Source Truth and whitespace checks;
6. update the Final Runtime and State Authority Map when composition or ownership changes;
7. update Current Capability and Progress Ledger when capability changes;
8. update the Regression and Drift Register when correcting failure;
9. reconcile README claims when public capability changes;
10. review through a pull request;
11. create a dated VX12 backup when a stable milestone warrants it.

## 10. Documentation-verification contract

Documentation checks must prove current relationships and prevent known contradictions. They must not fossilise old state through exact historical dates, PR numbers or obsolete phrases.

At minimum, Source Truth should verify:

- all governing documents exist and link to one another correctly;
- Current Capability declares a merged baseline no older than the latest capability-changing merged PR;
- planned, partial and verified states remain distinct;
- Stage One and Stage Two remain the active horizon;
- AI evidence is not described as editable geometry or user approval;
- the official final runtime is the verification target;
- the Final Runtime and State Authority Map names the current launcher, installer order, final class composition, state owners and retirement status;
- interaction-heavy changes require explicit live-acceptance status;
- regression repairs update the causal register;
- verifier discovery or registration cannot silently omit required checks;
- README claims do not exceed Current Capability.

Historical PR detail belongs in Git history and the Progress Ledger, not as frozen current-state assertions.

## 11. Public-claim rule

Public surfaces must state accurately:

- the creator problem;
- the durable asset value;
- the Stage One–Two boundary;
- present implementation state;
- local-first and human-governed authority;
- modest-hardware assumptions;
- known limitations and deferred scope.

Do not use unsupported compatibility claims, invented release status, keyword stuffing, engineering-safety claims or the phrase “open source” before a recognised licence is selected.
