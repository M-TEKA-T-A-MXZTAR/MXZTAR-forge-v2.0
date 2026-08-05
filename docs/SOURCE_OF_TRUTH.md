# MXZTAR Forge v2.0 — Source of Truth Policy

## 1. Repository authority

This Git repository and its reviewed history are the leading software-project authority for MXZTAR Forge v2.0.

Priority order:

1. committed repository history;
2. current reviewed branch or pull-request state;
3. current local working tree;
4. dated safety backups;
5. terminal scrollback or chat recollection.

Terminal output and conversation history are useful evidence, but important decisions, accepted behaviour, verification, and current product truth must be promoted into durable repository records.

## 2. User-project authority

For a Forge user project, validated durable files inside the project directory are authoritative.

SQLite, caches, thumbnails, selectors, queues, settings, previews, autosave, and in-memory objects may accelerate, recover, or display state. They do not silently override canonical project files.

The detailed project hierarchy and recovery rules live in:

- `docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md`;
- `docs/product/OUTPUT_ARTIFACT_CONTRACTS.md`.

## 3. Current document hierarchy

Each current document has one responsibility.

### Tier 1 — Stable product authority

1. **`docs/product/MASTER_BUILD_PLAN.md`** — finished Stage One–Two product boundary, principles, workflow families, authority model, milestone dependencies, and release acceptance.

The Master Build Plan changes only when the intended finished product changes. It does not track current PRs or the immediate queue.

### Tier 2 — Present execution authority

2. **`docs/product/CURRENT_CAPABILITY_BOUNDARY.md`** — present-tense implemented, partial, planned, deferred, and evidence truth.
3. **`docs/product/ACTIVE_ENGINEERING_PLAN.md`** — current ordered gate, entry conditions, preserved invariants, exit proof, and exclusions.
4. **`docs/architecture/FINAL_RUNTIME_COMPOSITION.md`** — official launcher, installer order, shell/panel composition, and current consolidation debt.
5. **`docs/architecture/REGRESSION_AND_DRIFT_PREVENTION.md`** — change packets, invariant rules, proof fidelity, causal records, and merge gates.
6. **`AGENTS.md`** — compact operating rules for coding agents, subordinate to the detailed authorities above.

### Tier 3 — Evidence and detailed architecture

7. **`docs/PROGRESS_LEDGER.md`** — concise dated evidence, sequencing decisions, and causal learning.
8. **`docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md`** — project data, locking, recovery, and index hierarchy.
9. **`docs/product/OUTPUT_ARTIFACT_CONTRACTS.md`** — durable workflow, diagnostic, approval, component, assembly, and export artifacts.
10. **`docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md`** — workflow readiness, input, output, failure, and blocking rules.
11. **`docs/product/ASSET_GENERATION_AND_CONSTRUCT_ARCHITECTURE.md`** — detailed design possibilities and dependencies for asset generation and Construct, interpreted through the current Master Plan and Active Engineering Plan.
12. **`README.md`** — public product explanation and repository orientation. It must remain accurate but does not override detailed authority.

### Tier 4 — Historical evidence and deferred vision

- correction documents tied to a specific PR or live defect;
- `docs/product/FIRST_RENTABLE_RELEASE.md`;
- older roadmap snapshots;
- future Construct, World, and Level Four vision documents.

These preserve useful history and design lore. They are **not current engineering instructions** unless explicitly promoted into Tier 1 or Tier 2 by a reviewed source-of-truth change.

## 4. Conflict resolution

When documents conflict:

1. apply the highest relevant tier;
2. prefer the document whose assigned responsibility matches the question;
3. treat present runtime claims from historical correction documents as stale evidence;
4. correct the conflict in a dedicated documentation change;
5. do not allow several documents to remain competing authorities.

Examples:

- Finished product question → Master Build Plan.
- What exists now → Current Capability Boundary.
- What happens next → Active Engineering Plan.
- Which class actually runs → Final Runtime Composition.
- Why a regression occurred and how to prevent it → Regression and Drift Prevention.
- What happened and what evidence exists → Progress Ledger and Git history.

## 5. Active product horizon

The active horizon is:

- **Stage One — Forge Editor and portable 2D assets**;
- **Stage Two — Construct and portable 3D blockouts**.

Stages One and Two together define MXZTAR Forge v2.0.

Product Levels Three and Four remain deferred and do not authorise runtime work, public capability claims, delivery dates, or dead UI.

## 6. Planning versus implementation

Planning documents may describe intended capability and permitted sequence. They do not prove that controls, schemas, assets, operations, effects, or exports exist.

The Current Capability Boundary must label meaningful capability as:

- live verified;
- deterministically verified;
- merged foundation;
- partial;
- planned;
- deferred.

The README must not present planned capability as current capability.

## 7. Runtime evidence classes

A merged PR is not sufficient evidence by itself.

Applicable evidence classes include:

1. documentation, syntax, and compile checks;
2. schema, command-replay, and pure state contracts;
3. transaction, interruption, rollback, and restart tests;
4. focused real-Qt verification against the official final runtime;
5. complete Source Truth verification;
6. T1700 live interaction acceptance;
7. downstream continuation or round-trip evidence;
8. release installation and recovery evidence.

Layout, pointer behaviour, focus, visibility, event propagation, timing, comprehension, and hardware-sensitive work normally require live acceptance before merge.

## 8. Final-runtime rule

Runtime interaction claims must target the official composition documented in `FINAL_RUNTIME_COMPOSITION.md`.

Testing an intermediate class, uninstalled panel, direct event handler, retained alias, or different import order does not prove the official application.

When installer order, shell inheritance, panel replacement, or patched methods change, update the runtime map and final-runtime verifier in the same PR.

## 9. Controlled-change rule

Every meaningful change records:

- user outcome;
- final runtime target;
- authority owners;
- allowed change;
- preserved invariants;
- failure and rollback result;
- changed files;
- verification performed and result;
- live acceptance status;
- documentation impact;
- remaining risk;
- next permitted gate.

A narrow file diff is not automatically a narrow user-impact change.

## 10. Drift-prevention rule

Documentation verification must protect current authority structure and status distinctions without fossilising one historical PR era.

Good checks verify:

- required current documents exist;
- each document performs its assigned role;
- the Master Plan does not contain current branch or PR history;
- the Capability Boundary and Progress Ledger share the current assessed baseline;
- the Active Engineering Plan names one ordered active gate;
- the runtime map matches the official launcher composition;
- planned capability remains labelled planned;
- historical correction documents are not promoted accidentally;
- README claims remain within current capability.

Bad checks require an indefinitely frozen date, old PR range, rejected control wording, or exact paragraph merely because it was once current.

## 11. Omission and archival rule

To reduce drift and maintenance cost:

- keep exhaustive implementation detail in Git and PR discussions;
- keep only concise evidence and causal learning in the Progress Ledger;
- remove temporary branch state from the Master Plan;
- keep the immediate queue only in the Active Engineering Plan;
- de-authorise superseded correction documents rather than stacking them indefinitely;
- archive or delete obsolete documents only through a reviewed change that preserves any unique useful evidence;
- do not duplicate the same status table across several current documents.

## 12. Before work

1. confirm repository and branch;
2. inspect Git status and latest remote state;
3. read the current authority documents;
4. identify the active gate and workflow family;
5. resolve the official final runtime;
6. identify state owners and preserved invariants;
7. run the lowest useful baseline check before editing.

## 13. After work

1. run focused verification;
2. run complete Source Truth where required;
3. perform live, restart, interruption, downstream, or release acceptance as applicable;
4. update current capability, active sequence, runtime map, and ledger where materially affected;
5. report remaining risk truthfully;
6. open a reviewable PR;
7. do not treat silence or passing automation as merge approval.

## 14. Public-claim rule

Public documentation should clearly state:

- the user problem;
- intended users;
- durable value;
- Stage One–Two boundary;
- actual current foundation;
- limitations and deferred scope;
- local-first and human-governed model.

Unsupported compatibility, invented release status, engineering certainty, open-source licensing, pricing, tax, or manufacturing claims are prohibited.

## 15. Recovery doctrine

The current recovery method is:

```text
Recoup accepted decisions, evidence, and working behaviour
→ Regroup authority, runtime composition, and priorities
→ Proceed with one complete verified user-value slice
```

This policy exists to make engineering progress compound rather than repeatedly consume founder time repairing unintentional damage.