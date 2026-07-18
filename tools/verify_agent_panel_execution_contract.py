#!/usr/bin/env python3
"""Verify the safe AgentPanel/QThread execution lifecycle without calling Ollama."""

from __future__ import annotations

import os
import sys
import tempfile
import time
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PySide6.QtCore import QObject, QThread, QTimer, Signal, Slot  # noqa: E402
from PySide6.QtGui import QCloseEvent  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

import qt_app  # noqa: E402
from core.source_library import SourceArtItem  # noqa: E402
from qt_panels import agent_panel as panel_module  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


class FakeWorker(QObject):
    progress = Signal(str)
    finished = Signal(bool, str, str)

    result = (True, "/tmp/mxztar-success.json", "")
    ran_off_main_thread = False

    def __init__(self, workflow_key: str, source_path: str, user_notes: str = ""):
        super().__init__()
        self.workflow_key = workflow_key
        self.source_path = source_path
        self.user_notes = user_notes

    @Slot()
    def run(self) -> None:
        type(self).ran_off_main_thread = QThread.currentThread() is not QApplication.instance().thread()
        self.progress.emit("Fake worker running.")
        QTimer.singleShot(20, self.emit_result)

    @Slot()
    def emit_result(self) -> None:
        self.finished.emit(*type(self).result)


def wait_until_idle(app: QApplication, panel, timeout_seconds: float = 2.0) -> None:
    deadline = time.monotonic() + timeout_seconds
    while panel.has_active_job() and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.005)
    require(not panel.has_active_job(), "worker lifecycle did not return to idle")


def set_source(panel, source_path: Path) -> None:
    item = SourceArtItem(
        label=source_path.name,
        path=source_path,
        folder_name=source_path.parent.name,
        suffix=source_path.suffix,
        size_bytes=source_path.stat().st_size,
    )
    panel.source_combo.clear()
    panel.source_combo.addItem(item.label, item)
    panel.source_combo.setCurrentIndex(0)


def run_case(app: QApplication, panel, result, expected_status: str) -> None:
    FakeWorker.result = result
    panel.start_selected_workflow()
    require(panel.has_active_job(), "panel did not enter active-job state")
    require(not panel.run_button.isEnabled(), "run button remained enabled during active job")

    panel.start_selected_workflow()
    require("already running" in panel.status_label.text(), "second job was not rejected")

    wait_until_idle(app, panel)
    require(panel.run_button.isEnabled(), "run button was not restored after completion")
    require(expected_status in panel.status_label.text(), "final UI state was not truthful")


def main() -> int:
    app = QApplication.instance() or QApplication([])
    original_worker = panel_module.AgentWorker
    panel_module.AgentWorker = FakeWorker

    try:
        with tempfile.TemporaryDirectory(prefix="mxztar-agent-panel-") as temp_dir:
            source_path = Path(temp_dir) / "source.png"
            source_path.write_bytes(b"fixture")

            panel = panel_module.AgentPanel()
            set_source(panel, source_path)

            panel._elapsed_seconds = 14
            panel.update_elapsed_time()
            require("00:15" in panel.elapsed_label.text(), "elapsed display did not advance")
            require("Still working locally" in panel.progress_output.toPlainText(), "heartbeat was not visible")

            run_case(
                app,
                panel,
                (True, "/tmp/mxztar-success.json", ""),
                "Workflow succeeded",
            )
            require(FakeWorker.ran_off_main_thread, "worker ran on the Qt main thread")

            run_case(
                app,
                panel,
                (False, "/tmp/mxztar-failure.json", "simulated model failure"),
                "Diagnostic saved",
            )
            require("simulated model failure" in panel.status_label.text(), "failure reason was hidden")

            run_case(
                app,
                panel,
                (False, "", "simulated unsaved exception"),
                "failed before saving",
            )

            window = qt_app.MXZTARForgeWindow()
            window.agent_panel._job_active = True
            blocked_close = QCloseEvent()
            window.closeEvent(blocked_close)
            require(not blocked_close.isAccepted(), "window closed while a job was active")

            window.agent_panel._job_active = False
            allowed_close = QCloseEvent()
            window.closeEvent(allowed_close)
            require(allowed_close.isAccepted(), "window did not close when idle")

            print("PASS: worker executes outside the Qt main thread")
            print("PASS: elapsed timer and heartbeat remain visible")
            print("PASS: one-active-job guard rejects a second launch")
            print("PASS: success, saved failure, and unsaved failure remain distinct")
            print("PASS: controls return to idle after every final state")
            print("PASS: active workflow blocks unsafe window close")
            print("PASS: AgentPanel execution contract verified")
    finally:
        panel_module.AgentWorker = original_worker

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
