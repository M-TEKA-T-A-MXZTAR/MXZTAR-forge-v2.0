# MXZTAR Forge v2.0 — Source of Truth Policy

## 1. Leading software-project authority

This Git repository and its history are the leading source of truth for the MXZTAR Forge v2.0 software project.

Priority order:

1. committed Git repository history;
2. current reviewed branch or pull-request state;
3. current local working tree;
4. dated VX12 safety backups;
5. terminal scrollback.

Terminal scrollback is not project truth. Important decisions, verification evidence, contracts, and results must be saved to durable files or GitHub records.

---

## 2. User creative-work authority

For a user’s Forge project, validated durable files inside the project directory are authoritative.

SQLite, cached UI state, previews, queues, and in-memory objects may accelerate or display project state, but they must remain rebuildable and cannot silently override validated project files.

The detailed project authority hierarchy is defined in:

- `docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md`;
- `docs/product/OUTPUT_ARTIFACT_CONTRACTS.md`.

---

## 3. Product-document authority

The active documentation hierarchy is:

1. **`docs/product/MASTER_BUILD_PLAN.md`** — finished-product boundary, product principles, 18 workflow families, architecture, acceptance criteria, milestones, and engineering sequence.
2. **`docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md`** — workflow readiness, input, output, failure, blocking, and next-action rules.
3. **`docs/PROGRESS_LEDGER.md`** — current verified, merged, partial, planned, blocked, and deferred implementation state.
4. **`docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md`** — project truth, recovery, and index hierarchy.
5. **`docs/product/OUTPUT_ARTIFACT_CONTRACTS.md`** — durable workflow, approval, diagnostic, and export artifact requirements.
6. **`README.md`** — public product explanation and repository orientation. It must remain accurate but does not override detailed product contracts.
7. **`docs/product/FIRST_RENTABLE_RELEASE.md`** — historical planning notice only; it is not current scope authority.
8. **Future-vision documents** — deferred concepts only and never current implementation instructions without a separate founder-approved source-of-truth revision.

When two documents appear to conflict, the higher applicable authority wins. The conflict should then be corrected in a dedicated documentation change rather than allowed to persist.

---

## 4. Active product horizon

The current product horizon is:

- **Stage One — Forge Editor and portable 2D assets**;
- **Stage Two — Construct and portable 3D blockouts**.

Stage One and Stage Two together define the planned finished MXZTAR Forge v2.0 product.

Future Product Levels Three and Four remain deferred. Their documents preserve lore and long-term direction but do not authorise runtime work, delivery dates, public claims, or dead UI controls.

---

## 5. Change rule

Every meaningful change should record:

- what changed;
- why it changed;
- affected workflow family or product stage;
- affected authoritative artifacts;
- reversible and irreversible boundaries where applicable;
- affected files;
- verification command;
- verification result;
- live acceptance status where required;
- backup status when relevant.

No verification pass may be claimed without evidence from the environment that actually ran it.

---

## 6. Drift prevention

Before working:

1. check the current branch;
2. check Git status;
3. pull or fetch the latest remote state;
4. confirm the intended product stage and workflow family;
5. inspect the current Master Build Plan and Progress Ledger;
6. verify the application still compiles, imports, or launches at the relevant gate.

After working:

1. compile changed code files where applicable;
2. run the targeted verifier;
3. run source-truth and whitespace checks;
4. perform required live acceptance;
5. update the Progress Ledger truthfully;
6. commit and review known-good state through a pull request;
7. create a dated VX12 backup only when a stable stage warrants it.

---

## 7. Public-claim rule

The README and repository metadata are product-discovery surfaces. They should clearly state:

- the user problem;
- the intended users;
- the value Forge adds to existing workflows;
- the current Stage One–Two boundary;
- the actual implementation state;
- the local-first and human-governed model;
- limitations and deferred scope.

Discoverability language must remain natural and accurate. Keyword stuffing, unsupported compatibility claims, invented release status, and calling public source “open source” before a recognised `LICENSE` is selected are prohibited.
