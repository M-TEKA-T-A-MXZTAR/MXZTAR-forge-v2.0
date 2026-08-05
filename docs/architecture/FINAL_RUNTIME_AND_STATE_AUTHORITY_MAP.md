# MXZTAR Forge v2.0 — Final Runtime and State Authority Map

**Map date:** 6 August 2026  
**Assessed merged baseline:** `main` through PR #81 at `e8659d5`  
**Recovery phase:** R1 — Final-runtime map  
**Change boundary:** documentation and executable composition verification only; no runtime behaviour is changed by this map

## 1. Purpose

This document identifies the application that actually launches, the order in which compatibility installers alter it, the final window and Editor-panel composition, and the authoritative owner of each mutable state family.

It exists because isolated classes and direct handler tests do not necessarily represent the official Forge application. Import order, installer order, class rebinding, panel replacement and signal rewiring are currently architectural dependencies.

This map is therefore part of the verification boundary. Runtime work must update it whenever the official launcher, installer order, final class binding, state owner or retirement status materially changes.

## 2. Official launch path

```text
run_mxztar_forge.sh
→ choose .venv/bin/python when executable, otherwise python3
→ execute src/mxztar_forge.py
→ set bounded Ollama defaults
→ add src/ to sys.path
→ import installer modules and qt_editor_authoring_app dependencies
→ run six installers in declared order
→ import qt_editor_authoring_app.main
→ create QApplication
→ create AuthoringEditorForgeWindow
→ show window
→ enter Qt event loop
```

The official executable path is not any module-level `main()` below the final authoring shell. `qt_app.py`, `qt_editor_app.py` and `qt_editor_usability_app.py` contain useful intermediate entry points, but `run_mxztar_forge.sh` does not launch them.

## 3. Startup installer order

`src/mxztar_forge.py` installs the following contracts before it calls the final authoring `main()`:

| Order | Installer | Primary mutation surface | Reason it exists | Current retirement status |
|---:|---|---|---|---|
| 1 | `install_source_image_compatibility()` | `core.source_library`, `core.project_source_intake`, `MyLibraryPanel`, `AgentPanel` | Preserve accepted source originals, bounded previews and fail-closed model readiness across image formats | Compatibility layer; retire only after canonical source-library, intake and agent methods own the same contract directly |
| 2 | `install_my_library_refresh_guard()` | `MyLibraryPanel.refresh_library` | Use worker-object ownership rather than a transient `isRunning()` result so stale callbacks cannot destroy a newer worker | Compatibility guard; retire after the canonical panel serialises refresh through one explicit worker authority |
| 3 | `install_live_acceptance_guards()` | `EditorPanel`, `ProjectAwareEditorPanel`, `AuthoringEditorForgeWindow`, `StartHereProjectController`, sticky/wheel presentation surfaces | Correct live deletion visibility, deliberate no-document state, Project Trash feedback and unclipped Editor entry without replacing durable transactions | Broad compatibility layer; split into canonical components during R3 after final-runtime contracts cover every preserved behaviour |
| 4 | `install_project_menu_and_rename()` | project save command, Start Here and Editor selectors, controller constructors, project menus, rename surfaces and control synchronisation | Provide one visible project interaction model while preserving canonical project/session authority | Broad compatibility layer; consolidate into first-class project command/controller ownership during R3 |
| 5 | `install_project_menu_review_fixes()` | project-open assessment references, rename helpers, selector metadata, shared selection and controller initialisation | Close review-discovered recovery, lock-cleanup, name-collision and cross-panel selection faults | Corrective compatibility layer; integrate into project access, rename and selector controllers before removal |
| 6 | `install_direct_2d_resize()` | `core.shape_document` replay/resize support plus final Editor-panel class bindings | Add durable primitive resize while preserving the previously accepted guarded Editor behaviour | Active final binding; becomes canonical only after R3 removes class rebinding and instantiates one explicit Editor composition |

Installer order is significant:

- source and worker guards must exist before panels begin background work;
- live-acceptance corrections wrap methods that later menu installers also extend;
- review fixes depend on the base project-menu contract;
- direct resize captures the already-guarded panel as its base, then rebinds the final panel name used by the authoring shell.

A new installer must not be added merely because it is convenient. The preferred direction is to move verified behaviour into explicit canonical classes and commands, then remove one layer at a time.

## 4. Final window composition

The final window class hierarchy is:

```text
QMainWindow
└── MXZTARForgeWindow
    └── EditorForgeWindow
        └── UsableEditorForgeWindow
            └── AuthoringEditorForgeWindow   ← official constructed window
```

Responsibilities currently accumulate through the hierarchy:

| Class | Current responsibility in the final application |
|---|---|
| `MXZTARForgeWindow` | base project session, Dashboard, Start Here, Agent Workflows, My Library, Shape Library, Jobs, navigation, scroll surface, status and guided-next-step shell |
| `EditorForgeWindow` | inserts the Editor navigation/page and routes current-project and guided actions into the Editor |
| `UsableEditorForgeWindow` | replaces the page stack with current-page sizing and replaces the first Editor panel with the single-object workspace |
| `AuthoringEditorForgeWindow` | replaces the Editor again with the project-aware guarded binding, adds project/document authoring, static guidance and explicit wheel controller |

The inheritance chain is part of current behaviour, but it is not the desired permanent architecture. R3 should consolidate it incrementally rather than rewrite it wholesale.

## 5. Final Editor-panel composition

The construction path contains three panel generations:

```text
EditorForgeWindow.__init__
→ creates ObjectCadEditorPanel

UsableEditorForgeWindow.__init__
→ removes ObjectCadEditorPanel
→ creates SingleObjectWorkspacePanel

AuthoringEditorForgeWindow.__init__
→ removes SingleObjectWorkspacePanel
→ creates the name GuardedProjectAwareEditorPanel

install_direct_2d_resize()
→ rebinds authoring_app.GuardedProjectAwareEditorPanel
  to DirectResizeProjectAwareEditorPanel before window construction

final live panel
→ DirectResizeProjectAwareEditorPanel
```

`DirectResizeProjectAwareEditorPanel` inherits the guarded project-aware panel captured before rebinding. It therefore preserves the existing project/document, movement, object/camera and positioning-guide behaviour while adding direct durable 2D resize.

This final binding must be asserted after all installers run. Testing only `ProjectAwareEditorPanel`, the original guarded class, `SingleObjectWorkspacePanel` or `ObjectCadEditorPanel` is insufficient evidence for the launched Editor.

## 6. Important signal and replacement wiring

The final shell intentionally disconnects and replaces earlier connections while preserving their user-visible purpose.

Key current paths include:

- `StartHerePanel.project_changed` updates Agent Workflows, My Library, Jobs and the final Editor panel;
- `StartHerePanel.go_to_project_requested` routes into the Editor;
- final Editor `project_authority_changed` updates Start Here and the guided next step;
- Agent and source-intake activity mark project mutation as active in Start Here and the Editor;
- project-menu review fixes maintain one selected project target across Start Here and Editor selectors without silently switching authoritative open-project state;
- Jobs refreshes after an Agent job record is saved;
- background-idle signals participate in safe deferred application close;
- the authoring shell owns an explicit `EditorMouseWheelController` after the final panel replacement.

When a panel is replaced, old signal connections must be disconnected before deletion and equivalent required connections must be recreated against the new instance.

## 7. State-authority table

| Mutable concept | Authoritative owner | Rebuildable or transient surfaces | Non-negotiable rule |
|---|---|---|---|
| Open project and writer lease | `core.project_session.ProjectSession` plus project lock/recovery assessment | selector choice, labels and status text | Selected project is not automatically the authoritative open project |
| Project identity and purpose | project-owned `project.json` manifest | editable combo text and labels | Display-name edits must preserve directory and immutable project ID |
| Project recovery classification | `core.project_access` assessment plus transaction markers and lock evidence | dialogs and status labels | Recovery blockers cannot be hidden by UI state |
| Project deletion | `core.project_trash.move_project_to_trash` transaction and receipt | confirmation and near-field feedback | No permanent-delete command; active work and locked projects remain protected |
| Native 2D document | canonical project-owned shape-document JSON | autosave, rendered scene, selectors and labels | Commands and history replay define durable geometry; UI items are not authority |
| 2D preview/autosave | shape-document autosave file | in-memory `panel.document` and graphics items | Autosave must not silently outrank canonical save or survive as unexplained stale state |
| 3D object scene | canonical project-owned object-scene JSON | rendered viewport and inspector controls | Object membership remains linked to source shape IDs |
| 2D/3D membership | shape document plus object-scene reconciliation contract | selected item and visible pairing | Create, resize, delete, undo and redo must preserve paired membership rules |
| Camera, grid and view state | object-scene `view` state when saved | pending panel view state and viewport transforms | Object transforms and camera transforms are separate authorities |
| Current 2D selection | final Editor panel selection state | graphics highlight | Selection is transient and must reference an available canonical object ID |
| Current 3D selection | final Editor panel `selected_object_id` | viewport/inspector highlight | Selection may change without mutating unrelated objects or camera state |
| Project target shared between selectors | `StartHereProjectController._mxztar_shared_project_path` compatibility controller | Start Here and Editor combo indices | Shared target selection must not itself open or switch project authority |
| Source originals | project-owned imported source files and provenance | My Library previews and cache | Accepted originals remain unchanged; previews are bounded and rebuildable |
| Local-AI evidence | project-owned job/model-call evidence | Agent status and Jobs display | AI output is evidence, not editable geometry or approval authority |
| Job activity | Agent worker/job lifecycle and saved job record | progress/status controls | One heavy job at a time; no silent main-thread work |
| My Library discovery/thumbnail work | worker objects owned by `MyLibraryPanel` | `isRunning()` and visual status | Worker-object ownership governs replacement until queued completion clears it |
| Window size and position | `QSettings` for the Forge organisation/application | live widget geometry | Window settings do not become project or document truth |
| Guided next action | final window controller state | highlighted control and button text | Guidance may route the user but may not execute heavy work without explicit action |

## 8. Final user-action paths

### Launch

```text
shell launcher
→ Python entry point
→ installer sequence
→ final authoring window
→ final direct-resize project-aware Editor
→ Qt event loop
```

### Project create/open/switch

```text
Start Here or Editor project command
→ ProjectSession / project-authoring workflow
→ validated manifest and writer authority
→ project_changed / project_authority_changed propagation
→ final Editor loads project-owned documents and scene
```

### Project rename

```text
editable selector or Rename action
→ normalisation and mutation lock check
→ writable ProjectSession authority
→ transactional rename and recovery marker
→ refresh both project surfaces
→ preserve directory and project ID
```

### Project Trash

```text
selected canonical project
→ confirmation
→ active-work and lock validation
→ project-trash transaction and receipt
→ refresh selectors and detach if active
→ recoverable project remains outside active list
```

### Document create/open/close/delete/save/reopen

```text
final Editor document command
→ ProjectAwareEditorPanel command boundary
→ shape-document and object-scene authority
→ autosave/canonical save or transactional deletion
→ deliberate no-document state where requested
→ save / close / reopen verification
```

### Direct 2D move and resize

```text
real Qt pointer event on final canvas
→ select canonical shape ID
→ preview without authority transfer
→ one durable command on release
→ update paired 3D object only as contract permits
→ autosave / object-scene persistence
→ render final canonical state
```

### 3D object manipulation and viewing

```text
real Qt event in final viewport
→ distinguish object hit from empty-space camera action
→ mutate selected object or pending camera state, never both implicitly
→ preserve nonselected objects
→ save into object-scene authority when committed
```

## 9. Verification boundary

R1 verification must prove at minimum:

1. `run_mxztar_forge.sh` executes `src/mxztar_forge.py`;
2. the six installers remain in the declared order;
3. importing the launcher installs all six contracts;
4. the official main function constructs `AuthoringEditorForgeWindow`;
5. the final window inheritance chain remains intact;
6. `authoring_app.GuardedProjectAwareEditorPanel` and the guard-module binding both resolve to `DirectResizeProjectAwareEditorPanel` after installation;
7. the final panel inherits the pre-existing guarded project-aware behaviour;
8. this document names every installer, final class path, major state owner and retirement status.

The executable contract is `tools/verify_final_runtime_composition_contract.py`.

## 10. R1 exit status and next gate

This map closes the discovery portion of R1 and gives tests one explicit composition target. It does not authorise immediate runtime consolidation.

The next recovery work is R2:

- convert PR #66–#80 interaction failures into official-launcher contracts;
- deliver real mouse and wheel events through the final composition;
- verify geometry, visibility and pointer/object lock;
- prove save, close and reopen;
- add automatic verifier discovery or a manifest that cannot silently omit required checks;
- complete applicable T1700 live acceptance before interaction-heavy merges.

R3 consolidation may begin only after R2 protects the accepted behaviour named here.