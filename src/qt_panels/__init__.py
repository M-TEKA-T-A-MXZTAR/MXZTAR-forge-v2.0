#!/usr/bin/env python3
"""Side-effect-free Qt panel package for MXZTAR Forge.

Importing a panel submodule must remain inert so startup guards can import panel
classes without recursively re-importing themselves through this package
initializer. The official launcher installs its runtime guards explicitly before
it imports the editor shell.
"""

from __future__ import annotations


def install_panel_runtime_contracts() -> None:
    """Install both idempotent panel contracts after package initialization.

    The official ``mxztar_forge`` launcher currently installs the underlying
    startup and source-compatibility guards directly before importing the Qt
    shell. This helper supports tests or alternate callers that have already
    imported panel classes and then need to install the same contracts. Calling
    it repeatedly is safe; importing ``qt_panels`` never calls it automatically.
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
