# AGENTS.md

MXZTAR Forge v2.0 is a local-first Ubuntu creative-construction workbench for producing editable, reusable 2D assets and reversible 3D blockouts on modest hardware.

This file is the compact operating contract for every coding agent working in this repository. Product scope comes from `docs/product/MASTER_BUILD_PLAN.md`; recovery sequencing comes from `docs/product/RECOVERY_AND_COMPLETION_PLAN.md`; present capability comes from `docs/product/CURRENT_CAPABILITY_BOUNDARY.md`.

## Non-negotiable change rule

Upgrade only the named behaviour. Preserve every adjacent accepted behaviour unless the task explicitly authorises its replacement.

Before editing, record:

1. the user action being changed;
2. the final runtime path that serves it;
3. the authoritative state owner;
4. the allowed change;
5. the invariants that must remain exact;
6. the failure and recovery behaviour;
7. the evidence required before the change may be called complete.

A small diff is not automatically a small change. Scope is measured by the complete user action and its invariants, not by file count.

## Final-runtime rule

Forge currently contains layered subclasses, installers, signal rewiring and compatibility guards. Never prove a feature only against an intermediate class, isolated handler or pre-install state.

For every runtime change:

- trace the official launcher from `src/mxztar_forge.py` to the final composed window;
- identify every installer, subclass and method replacement touching the behaviour;
- test the final composed runtime after all installers have run;
- treat import or installation order as an architectural dependency until it is removed;
- do not introduce another monkey patch when a first-class command, state owner or composed component can solve the problem safely.

No sweeping runtime refactor is authorised by this rule. First map the composition, preserve behaviour, then retire layers incrementally through verified changes.

## Interaction and geometry rule

UI correctness means the real user action works in the official application.

Do not substitute:

- direct handler calls for real Qt event delivery;
- widget existence for visible and useful placement;
- coordinate mutation for pointer-lock accuracy;
- isolated panel tests for official-launcher tests;
- deterministic checks for required T1700 live acceptance.

For direct manipulation, verify press, move, release, selection, cursor/object lock, transforms, camera state, persistence, reopen and interruption as applicable.

## State-authority rule

Every mutable concept must have one named authority. Common boundaries include:

- selected project versus authoritative open project;
- selected document versus canonical document;
- preview/autosave versus canonical save;
- object transform versus camera transform;
- screen coordinates versus world coordinates;
- 2D shape membership versus paired 3D object membership;
- raw evidence versus user-approved asset truth.

Do not add duplicate authority fields, implicit synchronization or vague status strings. Cached UI state, SQLite indexes and previews must remain rebuildable from durable project files.

## Product and workflow guardrails

- Stage One is Forge Editor and portable editable 2D assets.
- Stage Two is Construct and portable reversible 3D blockouts.
- Stage One and Stage Two together define the active finished-product boundary.
- Future Levels Three and Four remain deferred until a founder-approved source-of-truth revision.
- Preserve the source-image → editable geometry → reviewed asset → reversible component → assembly → verified export value path.
- AI may assess, classify, explain and propose; it does not become geometry or approval authority.
- Every visible control must have a complete workflow: handler, state transition, persistence, failure path, user feedback and verification.
- No dead UI, frozen UI, fake controls or planned capability presented as current capability.
- One heavy local-AI job at a time by default; no AI work on the Qt main thread; bounded CPU and memory use; no silent downloads.

## Verification ladder

Use the narrowest useful check first, then the checks required by risk.

1. Documentation-only change: check links, authority order, dates and present-tense claims.
2. Python change: compile changed files.
3. Prompt-contract change: run `PYTHONPATH=src python tools/verify_prompts.py`.
4. Workflow or source-truth change: run `./scripts/verify_source_truth.sh`.
5. Qt interaction change: deliver real Qt events through the final composed runtime.
6. Persistence change: save, close, reopen and verify canonical state.
7. Recovery-sensitive change: test interruption, rollback or read-only recovery.
8. Interaction-heavy change: complete T1700 live acceptance before merge.
9. Export claim: prove named downstream import or continuation.

A verifier must prove the current contract, not preserve an old snapshot through hard-coded dates, PR numbers or obsolete phrases.

## Causal learning rule

When correcting a regression, record in `docs/REGRESSION_AND_DRIFT_REGISTER.md`:

- observed failure;
- user impact;
- incorrect assumption;
- architectural condition that allowed it;
- verification gap;
- corrective action;
- prevention rule;
- evidence closing the entry.

A repair without causal learning is incomplete.

## Agent workflow

1. Inspect relevant source, governing documents and recent related history.
2. Reconstruct the complete user journey.
3. Map the final runtime and state owners.
4. Declare change boundary and preserved invariants.
5. Make the smallest complete, reversible change.
6. Run final-runtime and persistence/recovery checks appropriate to the risk.
7. Update Current Capability and Progress Ledger truthfully when capability changes.
8. Add causal learning when the work corrects drift or regression.
9. Report changed files, commands, results, live-acceptance status and remaining risk.

## Conduct and public claims

- Follow New Zealand legal and compliance assumptions unless repository authority says otherwise.
- Do not add occult, obscene, hateful, grooming, criminal, exploitative or unsafe material.
- Do not expose secrets, credentials, buyer data or unnecessary tracking.
- Official use is free of charge; founder support is voluntary.
- Do not claim a recognised open-source licence before one is selected.
- Do not advertise GST handling until registration and checkout/accounting support are ready.
- Do not overstate model certainty, compatibility, release readiness or engineering safety.

Never leave hidden drift, stale capability claims, broken authority, dead UI, frozen UI, incomplete workflows or verification that proves only an implementation detail rather than the real user experience.