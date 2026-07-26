# MXZTAR Forge v2.0 — Progress Ledger

**Ledger date:** 27 July 2026  
**Repository:** `M-TEKA-T-A-MXZTAR/MXZTAR-forge-v2.0`  
**Active product horizon:** integrated shape/object CAD, Stage One and Stage Two  
**Merged runtime baseline:** `6a0b558` through PR #62  
**Current delivery gate:** PR #63 live 3D output reveal and wheel-event routing  
**Current branch:** `agent/fix-live-3d-wheel-routing`

This ledger records current product truth and priority changes. Detailed commit history remains available in Git.

---

## 1. Status vocabulary

| Status | Meaning |
|---|---|
| VERIFIED | Required automated and recorded T1700 evidence exists for the stated boundary |
| DETERMINISTICALLY VERIFIED | Automated contracts pass; required visual or downstream acceptance may remain |
| MERGED | Code is on `main`; merge alone does not prove the complete product gate |
| PARTIAL | Useful implementation exists, but the complete user workflow does not |
| PLANNED | Required but not implemented |
| BLOCKED | A named dependency or founder decision prevents safe progress |
| DEFERRED | Outside the active product horizon |

---

## 2. Founder product direction

Forge is developing as a sophisticated but approachable local CAD workbench based on shapes and objects.

```text
Purpose
→ project
→ source image or blank document
→ editable shape
→ real 3D object
→ direct manipulation and positioning guidance
→ composition and construction
→ review and reusable library
→ portable outputs
```

Interaction controls must remain reachable while the user is working. A user must not be forced to drag a scrollbar or return to the top of a long Editor page merely to change output settings. Selecting a 2D or 3D output must bring that output into visible range, and an explicitly selected zoom mode must not also scroll the page.

This direction does not authorise fake perspective effects, unsupported automatic reconstruction, manufacturing claims, or a vague one-button merge operation.

---

## 3. Confirmed merged foundation

- PR #33 — canonical project manifest, required directories, history, atomic creation.
- PR #34 — one-writer lock and recovery classification.
- PR #35 — project session and Start Here create/open/close authority.
- PR #36 — project-contained source intake and processed lifecycle.
- PRs #39–#41 — asynchronous source intake and UI lifecycle corrections.
- PR #42 — project-owned model-call evidence.
- PR #44 — guided Next workflow and exact source handoff.
- PRs #45–#47 — stable My Library lifecycle and accepted image compatibility.
- PR #48 — Editor-first product reconciliation.
- PR #49 — native shape document and minimum reversible Editor.
- PR #50 — launcher import correction.
- PR #51 — Stage One–Two source-truth reconciliation.
- PR #52 — Purpose-driven Project Birth.
- PR #53 — Start Here default launch, project routing, Editor menus, and five reversible primitives.
- PR #54 — project-owned 3D object-scene foundation and CPU-rendered 3D workspace.
- PR #55 — single-object movement isolation, visible placement, immediate 3D synchronization, and stable layout.
- PR #56 — fresh project/document creation, project switching, and explicit paired deletion.
- PR #57 — restored Project Birth blank-document guidance and protected CodeQL Advanced.
- PR #58 — GitHub-generated CodeQL Advanced workflow for Actions and Python.
- PR #59 — reconciled README, Master Build Plan, Progress Ledger, capability boundary, and documentation-drift verification.
- PR #60 — transient positioning guides, measurements, optional snapping, rotation-aware bounds, and preserved empty-space orbit.
- PR #61 — default mouse-wheel page scrolling, selectable 3D zoom modes, and pinned Editor options.
- PR #62 — isolated wheel-verifier settings and guaranteed Qt background-thread cleanup.

---

## 4. Recorded T1700 evidence

### Established merged-main repository boundary

Status: **VERIFIED for the deterministic repository boundary**.

Recorded evidence includes:

- Project Birth focused verifier exit code `0`;
- complete Source Truth verification exit code `0`;
- required documentation files present;
- documentation runtime-state contract passes;
- listed Python files compile;
- CodeQL Advanced contract passes;
- launcher import contract passes;
- native shape, 3D object, single-object usability, project authoring, paired deletion, positioning-guide, and prompt contracts pass.

### PR #60 smart-guide evidence

Status: **DETERMINISTICALLY VERIFIED on merged `main`; final live acceptance remains coupled to the corrected viewport interaction gate**.

Recorded evidence:

- focused positioning-guide contract exit code `0`;
- complete Source Truth exit code `0`;
- rotation-aware 90-degree and 45-degree bounds pass;
- guidance-only movement does not force position;
- snapping remains separate and off by default;
- nonselected objects remain unchanged;
- empty-space drag remains orbit.

### PR #61 and PR #62 interaction evidence

Status: **MERGED and deterministically verified; live acceptance found two remaining defects**.

Recorded evidence:

- focused isolated wheel verifier exit code `0`;
- complete T1700 Source Truth exit code `0`;
- page scrolling is the first-run default;
- pinned Editor options remain outside the scroll area;
- settings persistence and Qt thread cleanup pass.

Live T1700 inspection then found:

1. switching to `3D Object View` left the object viewport below the current visible page range;
2. selecting `Zoom 3D view` still allowed the real wheel event to scroll the outer page.

The earlier verifier called handlers directly and therefore did not prove real Qt event delivery or parent propagation. These are interaction defects, not project-authority, geometry, or object-scene failures.

No downstream export, production mesh, manufacturing, tracing, approved library, or advanced assembly acceptance is implied.

---

## 5. Current workspace truth

| Workspace | Current truth |
|---|---|
| Start Here | Purpose-driven Project Birth, discovery, open/switch, close, and guided blank-document path are implemented |
| Editor | Primary integrated 2D shape and 3D object workspace; PR #63 corrects live output reveal and real wheel-event consumption |
| My Library | Verified bounded source intake, previews, exact handoff, and guarded lifecycle |
| Shape Library | Evidence browser only; approved editable lifecycle and insertion are not implemented |
| Agent Workflows | Optional local-AI assessment and planning foundation; not geometry authority |
| Jobs | Verified read-only evidence browser |
| Construct | Advanced construction and assembly workspace is not yet a complete exposed workflow |
| Review | Planned |
| Export | Verified SVG, PNG, GLB/glTF, and OBJ adapters are not implemented |

---

## 6. Implemented shape and object boundary

### Native 2D shape creation

Status: **PARTIAL / DETERMINISTICALLY VERIFIED**.

Implemented shapes:

- Rectangle;
- Square;
- Circle;
- Ellipse;
- Star.

Implemented authority:

- native versioned shape document;
- durable command replay;
- Undo and Redo;
- autosave and canonical save;
- transaction rollback;
- reopen and recovery;
- explicit deletion requiring a valid selection.

Not implemented:

- pen or Bezier paths;
- freehand drawing;
- node and handle editing;
- layers, groups, locking, visibility, arrays, mirrors, 2D snapping, or 2D booleans.

### Project-owned 3D object scene

Status: **DETERMINISTICALLY VERIFIED foundation**.

Implemented on merged `main`:

- five native shapes become real extruded 3D objects;
- source shape and object membership remain linked;
- XYZ position, width, height, depth, and three-axis rotation;
- colour and opacity;
- object selection, drag movement, resize, and numeric inspector;
- empty-space orbit;
- perspective, grid, line, camera, and zoom persistence;
- reversible object edits;
- paired membership during Undo, Redo, and deletion;
- atomic save, rollback, and restart restoration;
- moving one selected object leaves nonselected objects unchanged.

### Smart positioning gate

Status: **DETERMINISTICALLY VERIFIED on merged `main`**.

Implemented:

- transient X/Y alignment lines while moving one selected object;
- scene-centre and neighbouring-object centre/edge comparison;
- live X/Y/Z centre deltas;
- nearest-object centre distance, rotation-aware surface distance, and Z difference;
- separate `Position Guides` and `Snap to Guides` controls;
- snapping off by default;
- bounded tolerance from 1 to 50 scene units;
- guides off forces snapping off;
- guide state disappears immediately on release;
- final movement uses the existing reversible object command;
- empty-space drag remains perspective orbit.

Not included:

- equal-gap distribution guidance;
- transform gizmos;
- anchors, connectors, hierarchy, or assemblies;
- stitch, weld, join mesh, 3D booleans, separate, or bake;
- revolve, sweep, loft, shell, relief, bevel, vertex/face editing, or sculpting;
- verified 3D export.

---

## 7. PR #63 live viewport interaction correction

Status: **DETERMINISTICALLY VERIFIED on the PR #63 branch; T1700 live acceptance pending**.

Correction:

- 2D/3D stacked-view changes use the existing outer `QScrollArea` authority;
- after layout settles, the newly active output is repositioned into the visible page range;
- authorized 3D zoom is delivered exactly once to the object viewport;
- the zoom event is explicitly accepted and consumed before it can propagate to page scrolling;
- `Scroll page` continues to scroll over 2D or 3D output;
- `Zoom 3D view` zooms over 3D while 2D wheel input still scrolls;
- modifier mode scrolls normally and uses Ctrl+wheel for 3D zoom;
- project files, geometry, object-scene schema, and saved user preference authority remain unchanged.

Strengthened deterministic evidence:

- real `QWheelEvent` objects are sent through Qt rather than calling fake handlers directly;
- switching from 2D to 3D places the object viewport inside the visible scroll viewport;
- real wheel delivery in zoom mode changes zoom and leaves the page scrollbar unchanged;
- real Ctrl+wheel zoom changes zoom and leaves the page scrollbar unchanged;
- Python Compile Check passes;
- Security & Code Scan passes;
- Source Truth Check passes;
- CodeQL Advanced passes for Actions and Python.

---

## 8. Source-image and Ollama boundary

Status: **PARTIAL evidence foundation**.

Implemented:

- project-owned source copy;
- source identity and hash;
- bounded preview;
- supported source intake;
- optional Ollama assessment and raw findings.

Not implemented:

- source-region geometry selection;
- manual tracing into editable paths;
- deterministic contour, threshold, mask, or silhouette extraction;
- model-generated editable geometry;
- review and approval of extracted candidates.

Ollama findings remain evidence or guidance. They do not become editable or approved geometry automatically.

---

## 9. Shape Library boundary

Status: **PARTIAL evidence browser**.

The current Shape Library does not provide approved editable shape records, approval/version authority, `Insert into Current Document`, reversible insertion, document compatibility validation, or reusable component and assembly insertion.

---

## 10. Security and repository controls

Current PR #63 evidence:

- Python Compile Check: passing;
- Security & Code Scan: passing;
- Source Truth Check: passing with real wheel-event delivery and output-reveal assertions;
- CodeQL Advanced: passing for Actions and Python.

The root source-truth gate compiles the wheel controller and executes the complete real-event routing contract.

---

## 11. Next permitted engineering sequence

After PR #63 review, merge, T1700 synchronization, focused output, complete Source Truth output, and live acceptance:

1. freeform editable paths, nodes, and handles;
2. source-region selection and manual tracing;
3. bounded deterministic contour and mask candidates;
4. Ollama-assisted candidate assessment through the same editable path;
5. review, approval, versioning, and real Shape Library insertion;
6. 2D composition, alignment, groups, arrays, and explicit booleans;
7. advanced reversible 3D construction recipes;
8. assemblies, anchors, connectors, hierarchy, and distinct merge operations;
9. verified SVG, PNG, GLB/glTF, and OBJ output profiles;
10. release installation, migration, backup, recovery, licence, and documentation gates.

```text
focused branch
→ deterministic verifier
→ Source Truth
→ review comments
→ merge confirmation
→ T1700 sync
→ focused output and inspection
→ complete Source Truth output and inspection
→ applicable live acceptance
→ ledger and capability-boundary update
```

---

## 12. Current non-claims

Forge does not currently claim:

- a completed CAD release;
- editable tracing from arbitrary source images;
- automatic production-ready reconstruction;
- approved Shape Library insertion;
- advanced assembly or constraint solving;
- equal-gap or distribution guides;
- engineering-grade dimensions or tolerances;
- manufacturing safety;
- watertight or repaired meshes;
- stitch, weld, join mesh, booleans, topology repair, rigging, UVs, LODs, collision, or production materials;
- verified SVG, PNG, GLB/glTF, or OBJ continuation;
- universal downstream compatibility;
- an open-source licence.

---

## 13. Verification rule

No capability becomes VERIFIED solely because code was committed or merged.

Evidence may include compile and import checks, schema and command replay, project integrity, interruption and rollback, Qt lifecycle and offscreen rendering, real event delivery, manual T1700 interaction, and downstream continuation tests.
