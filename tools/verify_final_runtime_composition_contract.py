#!/usr/bin/env python3
"""Verify the official Forge launcher and final runtime composition.

This contract is deliberately narrow. It proves the current launcher path,
installer order, final window hierarchy and final Editor-panel binding without
changing runtime behaviour or claiming live interaction acceptance.
"""

from __future__ import annotations

import ast
import inspect
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAUNCHER_SCRIPT = PROJECT_ROOT / "run_mxztar_forge.sh"
ENTRY_POINT = PROJECT_ROOT / "src" / "mxztar_forge.py"
MAP_PATH = (
    PROJECT_ROOT
    / "docs"
    / "architecture"
    / "FINAL_RUNTIME_AND_STATE_AUTHORITY_MAP.md"
)

EXPECTED_INSTALLERS = [
    "install_source_image_compatibility",
    "install_my_library_refresh_guard",
    "install_live_acceptance_guards",
    "install_project_menu_and_rename",
    "install_project_menu_review_fixes",
    "install_direct_2d_resize",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"Required file is missing: {path.relative_to(PROJECT_ROOT)}")
    return path.read_text(encoding="utf-8")


def module_call_order(source: str) -> list[str]:
    tree = ast.parse(source)
    calls: list[str] = []
    for node in tree.body:
        if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
            continue
        function = node.value.func
        if isinstance(function, ast.Name):
            calls.append(function.id)
    return calls


def main() -> int:
    launcher = read(LAUNCHER_SCRIPT)
    entry_source = read(ENTRY_POINT)
    runtime_map = read(MAP_PATH)

    require(
        'src/mxztar_forge.py' in launcher or 'src/mxztar_forge.py"' in launcher,
        "The shell launcher no longer executes src/mxztar_forge.py",
    )

    ordered_calls = module_call_order(entry_source)
    installed_calls = [name for name in ordered_calls if name in EXPECTED_INSTALLERS]
    require(
        installed_calls == EXPECTED_INSTALLERS,
        "Official installer order changed without updating the final-runtime contract",
    )
    require(
        "from qt_editor_authoring_app import main" in entry_source,
        "The official entry point no longer delegates to qt_editor_authoring_app.main",
    )

    # Importing the official entry point installs the composed runtime but does not
    # enter the event loop because mxztar_forge.py is imported rather than executed.
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    import mxztar_forge  # noqa: F401
    import qt_direct_2d_resize as direct_resize
    import qt_editor_authoring_app as authoring_app
    import qt_editor_app as editor_app
    import qt_editor_usability_app as usability_app
    import qt_live_acceptance_guards as live_guards
    import qt_project_menu_and_rename as project_menu
    import qt_project_menu_review_fixes as review_fixes
    import qt_startup_guards
    import source_image_compatibility
    from qt_app import MXZTARForgeWindow
    from qt_panels import editor_authority_guard as guard
    from qt_panels.editor_authoring_panel import ProjectAwareEditorPanel

    require(
        source_image_compatibility.install_source_image_compatibility._installed,
        "Source-image compatibility was not installed by the official entry point",
    )
    require(
        getattr(
            qt_startup_guards.MyLibraryPanel.refresh_library,
            "_mxztar_worker_ownership_guard",
            False,
        ),
        "My Library worker-ownership refresh guard is not active",
    )
    require(
        live_guards.install_live_acceptance_guards._installed,
        "Live-acceptance compatibility guards were not installed",
    )
    require(
        project_menu.install_project_menu_and_rename._installed,
        "Unified project-menu and rename contract was not installed",
    )
    require(
        getattr(
            review_fixes.install_project_menu_review_fixes,
            "_mxztar_codex_review_corrections",
            False,
        ),
        "Project-menu review corrections are not registered",
    )
    require(
        direct_resize.install_direct_2d_resize._installed,
        "Direct 2D resize was not installed by the official entry point",
    )

    require(
        issubclass(authoring_app.AuthoringEditorForgeWindow, usability_app.UsableEditorForgeWindow),
        "AuthoringEditorForgeWindow no longer extends the usability shell",
    )
    require(
        issubclass(usability_app.UsableEditorForgeWindow, editor_app.EditorForgeWindow),
        "UsableEditorForgeWindow no longer extends the Editor shell",
    )
    require(
        issubclass(editor_app.EditorForgeWindow, MXZTARForgeWindow),
        "EditorForgeWindow no longer extends the base Forge window",
    )

    final_panel = direct_resize.DirectResizeProjectAwareEditorPanel
    require(
        authoring_app.GuardedProjectAwareEditorPanel is final_panel,
        "The authoring shell no longer resolves its Editor binding to the direct-resize panel",
    )
    require(
        guard.GuardedProjectAwareEditorPanel is final_panel,
        "The guard module no longer exposes the same final Editor-panel binding",
    )
    require(
        issubclass(final_panel, ProjectAwareEditorPanel),
        "The final Editor panel lost project/document authority behaviour",
    )
    mro_names = [item.__name__ for item in final_panel.__mro__]
    for required_name in (
        "DirectResizeProjectAwareEditorPanel",
        "GuardedProjectAwareEditorPanel",
        "ProjectAwareEditorPanel",
    ):
        require(
            required_name in mro_names,
            f"Final Editor MRO omits required layer: {required_name}",
        )

    authoring_main_source = inspect.getsource(authoring_app.main)
    require(
        "AuthoringEditorForgeWindow()" in authoring_main_source,
        "The final authoring main function no longer constructs AuthoringEditorForgeWindow",
    )

    for required_text in (
        "run_mxztar_forge.sh",
        "install_source_image_compatibility()",
        "install_my_library_refresh_guard()",
        "install_live_acceptance_guards()",
        "install_project_menu_and_rename()",
        "install_project_menu_review_fixes()",
        "install_direct_2d_resize()",
        "AuthoringEditorForgeWindow",
        "DirectResizeProjectAwareEditorPanel",
        "State-authority table",
        "Current retirement status",
        "ProjectSession",
        "shape-document JSON",
        "object-scene JSON",
        "R2",
    ):
        require(
            required_text in runtime_map,
            f"Final-runtime map omits required composition or authority term: {required_text}",
        )

    print("PASS: shell launcher targets src/mxztar_forge.py")
    print("PASS: six startup installers remain in the declared order")
    print("PASS: official entry-point import installs the current compatibility layers")
    print("PASS: final window hierarchy resolves to AuthoringEditorForgeWindow")
    print("PASS: final Editor binding resolves to DirectResizeProjectAwareEditorPanel")
    print("PASS: runtime map records installer, state-owner and retirement boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
