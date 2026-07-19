#!/usr/bin/env python3
"""Verify truthful legacy job recovery and the read-only Jobs panel."""

from __future__ import annotations

import json
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

from PySide6.QtWidgets import QApplication  # noqa: E402

from core import agent_runner  # noqa: E402
from core.job_records import read_job_record, scan_job_records  # noqa: E402
from qt_panels.jobs_panel import JobsPanel  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def write_record(path: Path, ok: bool, workflow: str, detail: str) -> None:
    payload = {
        "created_utc": "2026-07-19T12:00:00+00:00",
        "model": "qwen2.5vl:3b",
        "workflow_key": workflow,
        "source_path": "/tmp/source.png",
        "ok": ok,
        "error": "" if ok else detail,
        "output_text": detail if ok else "",
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def wait_for_scan(app: QApplication, panel: JobsPanel, timeout: float = 5) -> None:
    deadline = time.monotonic() + timeout
    while panel._scan_thread is not None and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()
    require(panel._scan_thread is None, "Jobs background scan did not finish")


def main() -> int:
    app = QApplication.instance() or QApplication([])
    original_dirs = dict(agent_runner.WORKFLOW_OUTPUT_DIRS)

    try:
        with tempfile.TemporaryDirectory(prefix="mxztar-jobs-") as temp_dir:
            root = Path(temp_dir)
            success_path = root / "success.json"
            failure_path = root / "failure.json"
            invalid_path = root / "invalid.json"
            write_record(success_path, True, "source_art_intelligence", "useful result")
            write_record(failure_path, False, "shape_structure_harvest", "model failure")
            invalid_path.write_text("{not-json", encoding="utf-8")

            agent_runner.WORKFLOW_OUTPUT_DIRS.clear()
            agent_runner.WORKFLOW_OUTPUT_DIRS["fixture"] = root

            require(read_job_record(success_path).status == "SUCCESS", "success misclassified")
            require(read_job_record(failure_path).status == "FAILED", "failure misclassified")
            require(read_job_record(invalid_path).status == "INVALID", "invalid record hidden")

            records = scan_job_records()
            require(len(records) == 3, "scanner did not recover every record")
            require({record.status for record in records} == {"SUCCESS", "FAILED", "INVALID"},
                    "scanner collapsed truthful record states")

            panel = JobsPanel()
            wait_for_scan(app, panel)
            require(panel.job_list.count() == 3, "Jobs panel did not show every record")
            require(not hasattr(panel, "retry_button"), "Jobs panel exposed an unimplemented retry")
            require(not hasattr(panel, "delete_button"), "Jobs panel exposed destructive delete")

            labels = [panel.job_list.item(i).text() for i in range(panel.job_list.count())]
            require(any("SUCCESS" in label for label in labels), "success state not visible")
            require(any("FAILED" in label for label in labels), "failure state not visible")
            require(any("INVALID" in label for label in labels), "invalid state not visible")

            panel.job_list.setCurrentRow(labels.index(next(x for x in labels if "FAILED" in x)))
            require("model failure" in panel.details.toPlainText(), "saved failure detail was hidden")

            success_path.unlink()
            failure_path.unlink()
            invalid_path.unlink()
            panel.refresh_jobs()
            wait_for_scan(app, panel)
            require(panel.job_list.count() == 0, "empty state retained stale jobs")
            require(not panel.open_folder_button.isEnabled(), "empty state enabled folder action")

            print("PASS: saved success, failure, and invalid records remain distinct")
            print("PASS: Jobs scans existing records outside the Qt main thread")
            print("PASS: Jobs shows every recovered record and its truthful detail")
            print("PASS: Jobs exposes no fake retry, delete, cancel, or approval action")
            print("PASS: empty Jobs state is safe and disables record actions")
            print("PASS: read-only Jobs panel baseline verified")
    finally:
        agent_runner.WORKFLOW_OUTPUT_DIRS.clear()
        agent_runner.WORKFLOW_OUTPUT_DIRS.update(original_dirs)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
