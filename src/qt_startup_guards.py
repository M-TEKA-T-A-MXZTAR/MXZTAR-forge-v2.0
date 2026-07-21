#!/usr/bin/env python3
"""Live Qt startup guards for MXZTAR Forge.

The real desktop event loop can briefly report a newly started QThread as not
running before its queued completion callback is delivered. During that small
window, a duplicate My Library refresh must not replace the tracked worker.
"""

from __future__ import annotations

from qt_panels.my_library_panel import MyLibraryPanel


def defer_refresh_for_existing_worker(panel) -> bool:
    """Serialize refresh behind any worker object still owned by the panel.

    Worker-object ownership is the authority here, not ``isRunning()``. A
    finished worker remains owned until its queued ``finished`` callback clears
    the panel field. Replacing it earlier lets the stale callback delete a newer
    live QThread.
    """

    if panel.has_active_intake():
        return False

    discovery = panel._discovery_thread
    if discovery is not None:
        panel._refresh_pending = True
        discovery.requestInterruption()
        panel.set_status("Stopping the current source discovery before refreshing…")
        return True

    loader = panel._thumbnail_loader
    if loader is not None:
        panel._refresh_pending = True
        loader.requestInterruption()
        panel.set_status("Stopping the current thumbnail scan before refreshing…")
        return True

    return False


def install_my_library_refresh_guard() -> None:
    """Install the startup guard once before ``qt_app`` constructs the window."""

    current = MyLibraryPanel.refresh_library
    if getattr(current, "_mxztar_worker_ownership_guard", False):
        return

    original_refresh = current

    def guarded_refresh(self):
        if defer_refresh_for_existing_worker(self):
            return None
        return original_refresh(self)

    guarded_refresh._mxztar_worker_ownership_guard = True
    guarded_refresh.__name__ = original_refresh.__name__
    guarded_refresh.__doc__ = original_refresh.__doc__
    MyLibraryPanel.refresh_library = guarded_refresh
