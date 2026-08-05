# AGENTS.md

Repository role: **MXZTAR Forge v2.0** is a local-first, human-governed creative concept-engineering forge. It converts source art and scratch-built shapes into inspectable, editable, reusable 2D assets, project-owned 3D blockouts, and later verified downstream handoffs.

Use this file as the compact operating contract for coding agents. Detailed authority lives in the documents linked below.

## 1. Read before changing anything

Read the applicable files in this order:

1. `docs/SOURCE_OF_TRUTH.md`
2. `docs/product/MASTER_BUILD_PLAN.md`
3. `docs/product/CURRENT_CAPABILITY_BOUNDARY.md`
4. `docs/product/ACTIVE_ENGINEERING_PLAN.md`
5. `docs/architecture/FINAL_RUNTIME_COMPOSITION.md`
6. `docs/architecture/REGRESSION_AND_DRIFT_PREVENTION.md`
7. `docs/PROGRESS_LEDGER.md`
8. the implementation and verifier files involved in the requested workflow

Do not rely on terminal scrollback, an old handoff, a historical correction document, an intermediate class, or a previously merged PR description as present-tense authority.

## 2. Product boundaries

- **Stage One — Forge Editor and portable 2D assets.**
- **Stage Two — Construct and portable 3D blockouts.**
- Stages One and Two together define MXZTAR Forge v2.0.
- Product Levels Three and Four are deferred vision. They do not authorise runtime controls, delivery claims, or engineering work.
- Forge is not a one-click production-ready 2D-to-3D converter, a manufacturing-certification tool, or a replacement for specialist creative applications.

## 3. Controlled-change protocol

Before editing, write down or encode in the PR:

- **User outcome:** what the user must be able to accomplish.
- **Final runtime:** the launcher, installers, shell, panel, controllers, and patched methods that actually run.
- **Authority owners:** which object owns project, document, shape, scene, camera, settings, autosave, history, and preview state.
- **Allowed change:** the exact behaviour that may change.
- **Preserved invariants:** every adjacent behaviour that must remain unchanged.
- **Failure result:** what remains authoritative if the operation fails or is interrupted.
- **Evidence:** the narrow verifier, complete suite, and live acceptance required.

A small diff is not necessarily a small change. The safe unit is one complete user action with all of its invariants.

## 4. Regression rules

- Test the **official final composed runtime**, not an intermediate parent class or unpatched panel.
- Use real Qt input delivery for interaction claims: mouse press/move/release, wheel propagation, menu activation, focus, geometry, and reopen behaviour.
- A widget being present or visible does not prove that it is usable, reachable, unclipped, correctly placed, or understandable.
- Preserve exact pointer offset for direct manipulation unless the contract explicitly changes it.
- Separate object transforms from camera navigation and screen-space behaviour from world-space behaviour.
- Keep 2D shapes and their paired 3D objects synchronized through edit, Undo, Redo, save, reopen, and deletion.
- Never change a verifier merely to match new output unless the prior requirement is explicitly superseded in current authority.
- Any new startup monkey-patch or class replacement requires a stated removal path. Prefer first-class commands and composition over further patch stacking.
- A regression-restoration PR must record the causal assumption and the missing proof—not only the symptom and fix.

## 5. State and data authority

- Durable validated project files are authoritative.
- SQLite, caches, previews, selectors, temporary geometry, and in-memory objects are rebuildable views unless a current contract states otherwise.
- Selection is not authority. An attached writable project, open document, selected object, camera mode, and pending preview are different states.
- Autosave is recoverable draft state, not silent canonical truth.
- Consequential commands require validated inputs, one defined transaction boundary, truthful failure, and confirmed rollback or authority revocation.
- External source files remain unchanged. Work on project-owned copies and declared derivatives.

## 6. Qt, local AI, and modest-hardware rules

- No heavy work on the Qt main thread.
- No dead UI, frozen UI, silent long job, or silent model download.
- One heavy local job at a time by default.
- Keep `OLLAMA_NUM_PARALLEL=1` and `max_heavy_jobs=1` unless a separately verified user-facing queue and resource policy authorises more.
- Use bounded image decoding, bounded collections, bounded timeouts, and clean worker shutdown.
- Success, saved failure, invalid evidence, timeout, cancellation, and failure-before-save remain distinct states.
- Ollama assessment is evidence or proposal—not authoritative editable geometry.

## 7. Human-governance boundary

Human approval is required for consequential or world-visible actions, including approval, publishing, destructive deletion, irreversible geometry operations, migration without confirmed rollback, release claims, and merge to the protected product baseline.

Silence is not approval. Do not merge a PR merely because automated checks pass.

## 8. Documentation discipline

- The Master Build Plan contains stable product scope and milestone logic, not current PR history.
- The Current Capability Boundary contains present-tense runtime truth, not aspirations.
- The Active Engineering Plan contains the current ordered gate, entry conditions, exit proof, and exclusions.
- The Progress Ledger records concise dated evidence and causal lessons; Git history retains exhaustive implementation detail.
- Historical correction documents are evidence only unless `docs/SOURCE_OF_TRUTH.md` explicitly promotes one.
- Update current authority in the same PR when capability, sequence, risk, or final runtime composition materially changes.
- Do not hard-code an old PR era into a drift verifier in a way that makes stale wording pass forever.

## 9. Verification ladder

Use the lowest applicable rung and every rung above it required by the risk:

1. Markdown, links, JSON/YAML syntax, and whitespace.
2. Python compile and import checks.
3. Pure state, schema, transaction, or command-replay contract.
4. Focused real-Qt contract against the final runtime.
5. Complete Source Truth suite.
6. T1700 live interaction acceptance for layout, pointer behaviour, timing, visibility, comprehension, or hardware-sensitive work.
7. Restart, interruption, rollback, migration, downstream continuation, or release-installation proof where applicable.

A merged PR is not proof by itself.

## 10. Required PR report

Every meaningful PR must state:

- user outcome;
- root cause or design purpose;
- changed files;
- authority and invariant impact;
- verification run and result;
- live acceptance status;
- remaining risk;
- documentation updated;
- next permitted gate.

Preserve working behaviour, reduce authority duplication, and make the next action clearer than the last one.