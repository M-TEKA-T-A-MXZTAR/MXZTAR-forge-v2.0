#!/usr/bin/env python3
"""Shared Qt-panel runtime bootstrap for every supported Forge entrypoint.

Importing any ``qt_panels`` submodule installs the panel-level runtime contracts
before a panel instance can be constructed. This keeps direct ``qt_app.py``
execution aligned with the official launcher.
"""

from __future__ import annotations


def install_panel_runtime_contracts() -> None:
    """Install idempotent panel contracts without recursive package bootstrap."""

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
install_panel_runtime_contracts()
