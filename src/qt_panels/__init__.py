#!/usr/bin/env python3
"""Side-effect-free Qt panel package for MXZTAR Forge.

Runtime compatibility contracts are installed explicitly by supported
application entrypoints before a window is constructed. Importing a panel
submodule must remain inert so startup guards can import panel classes without
recursively re-importing themselves through this package initializer.
"""

from __future__ import annotations


def install_panel_runtime_contracts() -> None:
    """Install idempotent runtime contracts required before any window is constructed.

    Must be called by every supported application entrypoint (e.g. mxztar_forge,
    qt_app, qt_editor_app) after importing panel classes and before showing UI.
    Calling it more than once is safe. Omitting the call leaves worker-ownership
    and source-compatibility guards uninstalled, which is only acceptable in
    non-UI contexts such as compile checks.
    """

    if getattr(install_panel_runtime_contracts, "_bootstrapping", False):
        return

    install_panel_runtime_contracts._bootstrapping = True
    try:
        from qt_startup_guards import install_my_library_refresh_guard
        from source_image_compatibility import install_source_image_compatibility

        install_my_library_refresh_guard()
        install_source_image_compatibility()
    finally:
        install_panel_runtime_contracts._bootstrapping = False


install_panel_runtime_contracts._bootstrapping = False
