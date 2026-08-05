# MXZTAR Forge v2.0 — Final Runtime Composition

## 1. Purpose

This document identifies the application that actually runs from the official repository launcher.

It prevents agents and verifiers from treating an intermediate class, uninstalled panel, direct event handler, or historical shell as the final product runtime.

This is a current composition map and technical-debt register. It does not endorse indefinite startup patching.

## 2. Official entry path

```text
run_mxztar_forge.sh
→ src/mxztar_forge.py
→ startup installers in declared order
→ qt_editor_authoring_app.main()
→ QApplication
→ AuthoringEditorForgeWindow
```

The launcher must remain relocatable and prefer the checkout-local virtual environment when available.

## 3. Startup installation order

`src/mxztar_forge.py` currently installs:

1. `install_source_image_compatibility()`
2. `install_my_library_refresh_guard()`
3. `install_live_acceptance_guards()`
4. `install_project_menu_and_rename()`
5. `install_project_menu_review_fixes()`
6. `install_direct_2d_resize()`
7. import and run `qt_editor_authoring_app.main`

This order is behaviourally significant because several installers replace or extend classes and methods before window construction.

Any change to the list or order must update this document and the launcher-import/final-runtime verifiers in the same PR.

## 4. Shell inheritance and replacement path

The live shell currently follows:

```text
AuthoringEditorForgeWindow
  inherits UsableEditorForgeWindow
    inherits EditorForgeWindow
      inherits the base Qt application shell
```

During construction:

1. `EditorForgeWindow` builds the initial application and Editor surface.
2. `UsableEditorForgeWindow` replaces the stacked page container with `CurrentPageStack` and replaces the Editor with `SingleObjectWorkspacePanel`.
3. `AuthoringEditorForgeWindow` replaces that Editor with `GuardedProjectAwareEditorPanel` and adds project authoring and mouse-wheel controllers.
4. Startup installers may have already extended or replaced methods on these classes and panel ancestors.
5. `install_direct_2d_resize()` extends final Editor behaviour and shape-command replay through the established installation pattern.

Therefore, testing `EditorForgeWindow`, `SingleObjectWorkspacePanel`, or an uninstalled `GuardedProjectAwareEditorPanel` alone does not prove the official application.

## 5. Final Editor target

For current interaction work, the required runtime target is:

```text
all startup installers applied
→ AuthoringEditorForgeWindow constructed
→ final window.editor_panel resolved
→ final viewport/controller objects resolved from that panel
```

A verifier must assert that the resolved classes and installed marker attributes match the expected final composition before testing behaviour.

## 6. Current composition risks

### Repeated panel replacement

Constructing and then replacing multiple Editor panels increases signal-rewiring, retained-state, cleanup, and wrong-class verification risk.

### Startup monkey-patching

Replacing class methods before construction makes import order part of correctness and can leave historical source bodies inconsistent with live behaviour.

### Ancestor alias retention

A module may retain a reference to a class before a later installer replaces or subclasses it. Tests can then pass against an alias that is not the live class.

### Distributed interaction ownership

Movement, resize, camera, guides, wheel routing, project authority, and persistence span multiple modules. A narrow change can bypass an adjacent contract.

### Documentation/runtime divergence

Source files may describe older interaction wording while startup patches produce different live behaviour.

## 7. Consolidation direction

Consolidation must be incremental and evidence-led.

Preferred destination:

- one official application shell;
- one deliberate Editor composition root;
- first-class commands for movement, resize, camera, project and document operations;
- explicit controller ownership rather than method replacement;
- one final-runtime factory used by the launcher and verifiers;
- startup installers limited to genuine compatibility boundaries;
- no duplicate controls or hidden intermediate panels.

## 8. Safe consolidation sequence

1. Add a final-runtime factory or fixture that applies the official installer sequence and constructs the live shell.
2. Make all interaction verifiers use that factory.
3. Inventory every patched method and the accepted behaviour it protects.
4. Select one complete user-action family.
5. Move that family into a first-class component without changing behaviour.
6. Run focused, complete, restart, and T1700 live acceptance.
7. Remove only the superseded patch for that family.
8. Update this map and the Capability Boundary.

Do not combine all families into one sweeping refactor.

## 9. Change checklist

A PR that changes runtime composition must answer:

- What is the official entry path after this PR?
- Which installers run and in what order?
- Which shell and panel are final?
- Which signals are connected, disconnected, or replaced?
- Which state survives panel replacement?
- Which cleanup occurs for discarded widgets and workers?
- Which verifier proves the same final composition?
- Which patch or replacement was removed, and which accepted behaviour remains protected?

## 10. Truth boundary

This map documents the repository baseline through merged PR #80 as assessed on 6 August 2026.

It does not claim that every interaction has completed fresh live acceptance after this governance recovery. Current evidence status belongs in `docs/product/CURRENT_CAPABILITY_BOUNDARY.md` and `docs/PROGRESS_LEDGER.md`.