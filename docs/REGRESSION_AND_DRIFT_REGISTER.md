# MXZTAR Forge v2.0 — Regression and Drift Register

## Purpose

This register preserves causal learning from regressions, usability failures and source-of-truth drift.

It is not a blame log. Its purpose is to prevent repeated rediscovery by recording the assumption, architectural condition and verification gap that allowed a failure.

## Entry contract

Each entry records:

- ID and date;
- affected user action;
- observed failure;
- user and product impact;
- incorrect assumption;
- architectural condition;
- verification gap;
- correction;
- prevention rule;
- closing evidence and status.

Statuses: `OPEN`, `MITIGATED`, `CLOSED`, `SUPERSEDED`.

---

## RD-001 — Deterministic visibility did not prove usable layout

**Affected action:** access Editor commands while retaining useful canvas workspace.  
**Observed failure:** the always-open action tree introduced through PR #66 passed deterministic checks but consumed excessive live workspace. PR #67 restored a compact command strip.  
**Impact:** accepted interaction regressed despite passing tests; founder time was spent repairing a merged usability fault.  
**Incorrect assumption:** visible and persistent controls were equivalent to usable placement.  
**Architectural condition:** UI acceptance was represented mainly through widget presence and geometry contracts without the full workspace context.  
**Verification gap:** no pre-merge T1700 live acceptance for the complete Editor journey at supported window size.  
**Correction:** compact temporary-dropdown command row; preserve Project Trash and wheel routing.  
**Prevention rule:** layout changes must prove both control availability and retained task workspace in the official runtime; interaction-heavy changes require live acceptance before merge.  
**Closing evidence:** PR #67 deterministic evidence exists; final live acceptance status must remain explicit.  
**Status:** MITIGATED.

## RD-002 — Layered runtime corrections created competing final behaviour

**Affected action:** launch and use the official Editor.  
**Observed failure:** successive subclasses, panel replacements, signal rewiring and startup installers made correctness dependent on composition and import order.  
**Impact:** a fix could pass against an intermediate component while the launched application behaved differently; regressions were repaired by additional layers.  
**Incorrect assumption:** a narrow runtime patch remained isolated after installation.  
**Architectural condition:** multiple components could act as the “final” Editor, and installers could replace methods after class construction.  
**Verification gap:** tests did not consistently instantiate the official launcher after all installers ran.  
**Correction:** require a final-runtime map and official-launcher verification before adding capability; retire layers incrementally.  
**Prevention rule:** no feature is complete until the final composed runtime passes. New monkey patches require explicit justification and retirement plan.  
**Closing evidence:** pending Phase R1 runtime map and Phase R2 acceptance harness.  
**Status:** OPEN.

## RD-003 — 2D movement capability was assumed rather than implemented

**Affected action:** drag a 2D shape directly.  
**Observed failure:** the 2D canvas was effectively pan-oriented and displayed passive shapes without a durable move command.  
**Impact:** the interface suggested editable objects, but the fundamental direct-manipulation journey was incomplete.  
**Incorrect assumption:** displayed selectable geometry implied movable editable geometry.  
**Architectural condition:** rendering, selection and durable command state were not treated as one complete user-action contract.  
**Verification gap:** no real press-move-release test through the final runtime with save and reopen.  
**Correction:** add direct durable 2D movement and related replay/persistence behaviour.  
**Prevention rule:** every direct-manipulation feature must cover event delivery, command creation, canonical persistence, reopen and unaffected-object invariants.  
**Closing evidence:** PR #78 and related contracts; final-runtime regression coverage remains required.  
**Status:** MITIGATED.

## RD-004 — 3D pointer drift from mismatched transforms

**Affected action:** drag a selected 3D object while keeping it under the pointer.  
**Observed failure:** inverse movement calculations used an incomplete transform while rendering used yaw, pitch, zoom and perspective, causing visible pointer drift or floating.  
**Impact:** direct manipulation felt unreliable and broke the creator’s mental model.  
**Incorrect assumption:** updating world coordinates was sufficient proof of correct dragging.  
**Architectural condition:** screen-to-world and world-to-screen transforms did not share one authoritative transform model.  
**Verification gap:** prior tests asserted movement but not cursor/object lock across camera states.  
**Correction:** align inverse interaction transform with rendering and restore stable front orthographic Design View.  
**Prevention rule:** geometry interaction tests must assert round-trip transform consistency and pointer lock, not merely changed coordinates.  
**Closing evidence:** PR #78 and PR #79; full final-runtime camera-state matrix remains required.  
**Status:** MITIGATED.

## RD-005 — Object and camera authority became entangled

**Affected action:** move or resize objects without unexpectedly changing the view.  
**Observed failure:** object transforms and camera navigation competed for mouse gestures and state.  
**Impact:** editing could alter viewing state or make object manipulation unpredictable.  
**Incorrect assumption:** gesture handlers could infer intent safely without explicit selection and empty-space rules.  
**Architectural condition:** object and camera state shared interaction pathways without a strict authority boundary.  
**Verification gap:** tests did not preserve non-target camera/object invariants through complete gestures.  
**Correction:** separate object transforms from camera navigation; selection acts on objects, empty-space drag acts on view; perspective/orbit are deliberate viewing controls.  
**Prevention rule:** each gesture must name its authority target and assert all non-target state remains unchanged.  
**Closing evidence:** PR #74 and PR #79; maintain in final-runtime interaction suite.  
**Status:** MITIGATED.

## RD-006 — Re-entry state changed the next user action

**Affected action:** return to Editor and continue working.  
**Observed failure:** re-entry could retain an interaction mode that made the next click act unexpectedly. PR #77 restored re-entry to Select.  
**Impact:** the interface lacked a safe, predictable starting state.  
**Incorrect assumption:** preserving the last tool was always helpful.  
**Architectural condition:** session convenience overrode safe document-entry defaults.  
**Verification gap:** no reopen/re-entry journey asserted the first actionable state.  
**Correction:** reset to Select at the defined entry boundary.  
**Prevention rule:** every workflow entry and recovery path must define a safe initial mode and test the first user action.  
**Closing evidence:** PR #77.  
**Status:** CLOSED.

## RD-007 — Current-capability documentation fossilised

**Affected action:** determine what Forge currently does and what work comes next.  
**Observed failure:** Current Capability remained at 27 July 2026 through PR #66/#67 while runtime advanced through PR #80. Documentation verification hard-coded old dates, PR numbers and phrases.  
**Impact:** agents could follow stale priorities, public claims could diverge from runtime, and a passing verifier could preserve drift.  
**Incorrect assumption:** checking exact historical phrases guaranteed current truth.  
**Architectural condition:** documentation tests encoded snapshots instead of authority relationships, recency and capability evidence.  
**Verification gap:** no rule compared current merged baseline with the documented baseline or required reconciliation after capability PRs.  
**Correction:** refresh current capability and replace frozen assertions with relationship-based checks.  
**Prevention rule:** current-state documents must declare a baseline that is not older than the latest capability-changing merged PR; historical detail belongs in the Progress Ledger and Git history.  
**Closing evidence:** governance-reset PR refreshes documents; verifier correction remains an immediate follow-up.  
**Status:** OPEN.

## RD-008 — Manual verifier inventory allowed omission

**Affected action:** rely on Source Truth as the complete verification gate.  
**Observed failure:** `verify_source_truth.sh` depended on manually maintained file and verifier lists; new modules or checks could be omitted.  
**Impact:** the suite could pass without running all intended contracts.  
**Incorrect assumption:** maintainers would always update every inventory list alongside new files.  
**Architectural condition:** discovery and inclusion were not generated or validated.  
**Verification gap:** no test proved that all required verifier modules were registered.  
**Correction:** introduce automatic discovery or a single manifest validated against repository conventions.  
**Prevention rule:** adding a verifier must make omission impossible or cause Source Truth to fail.  
**Closing evidence:** pending Phase R2.  
**Status:** OPEN.

---

## Register maintenance

- Add an entry when a merged or accepted behaviour regresses, a live usability test contradicts deterministic evidence, documentation materially drifts, or an architectural ambiguity causes repeated repair.
- Update status only when the prevention mechanism and closing evidence exist.
- Do not erase closed entries; they are durable project knowledge.
- Keep implementation chronology in `docs/PROGRESS_LEDGER.md`; keep causal mechanisms here.