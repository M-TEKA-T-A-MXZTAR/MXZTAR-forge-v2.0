#!/usr/bin/env python3
"""Shared Qt-panel runtime bootstrap for every supported Forge entrypoint.

Importing any ``qt_panels`` submodule installs the panel-level runtime contracts
before a panel instance can be constructed. This keeps direct ``qt_app.py``
execution aligned with the official launcher.
"""

from __future__ import annotations

_BOOTSTRAPPING = False


def install_panel_runtime_contracts() -> None:
    """Install idempotent panel contracts without recursive package bootstrap."""

    global _BOOTSTRAPPING
    if _BOOTSTRAPPING:
        return

    _BOOTSTRAPPING = True
    try:
        from qt_startup_guards import install_my_library_refresh_guard
        from source_image_compatibility import install_source_image_compatibility

        install_my_library_refresh_guard()
        install_source_image_compatibility()
    finally:
        _BOOTSTRAPPING = False


install_panel_runtime_contracts()
