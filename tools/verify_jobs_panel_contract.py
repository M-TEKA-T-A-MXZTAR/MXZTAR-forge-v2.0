#!/usr/bin/env python3
"""Verify truthful legacy job recovery and the read-only Jobs panel."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PySide6.QtWidgets import QApplication  # noqa: E402

from core import agent_runner  # noqa: E402
from core.job_records import JobScanResult, read_job_record, scan_job_records  # noqa: E402
from qt_panels import jobs_panel as jobs_module  # noqa: E402
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
        "output_text": detail if ok else "raw diagnostic response",
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
            project = root / "project"
            (project / "logs").mkdir(parents=True)
            (project / "diagnostics").mkdir()
            project_evidence = project / "logs" / "run.workflow-run.json"
            project_evidence.write_text(
                json.dumps(
                    {
                        "schema_name": "mxztar_forge_workflow_run_evidence",
                        "schema_version": "1.0.0",
                        "run_id": "run_fixture",
                        "project_id": "project_fixture",
                        "workflow_key": "source_art_intelligence",
                        "status": "model_call_succeeded",
                        "workflow_complete": False,
                        "approval_state": "not_applicable",
                        "started_at_utc": "2026-07-19T12:00:00+00:00",
                        "completed_at_utc": "2026-07-19T12:00:01+00:00",
                        "execution": {"model_name": "fixture-model"},
                        "provenance": {"source_path": "source/originals/fixture.png"},
                        "raw_model_output": "unvalidated model evidence",
                        "error": None,
                    }
                ),
                encoding="utf-8",
            )

            agent_runner.WORKFLOW_OUTPUT_DIRS.clear()
            agent_runner.WORKFLOW_OUTPUT_DIRS["fixture"] = root

            require(read_job_record(success_path).status == "SUCCESS", "success misclassified")
            require(read_job_record(failure_path).status == "FAILED", "failure misclassified")
            require(read_job_record(invalid_path).status == "INVALID", "invalid record hidden")

            scan = scan_job_records(project_dir=project)
            require(len(scan.records) == 4, "scanner did not recover every record")
            require({record.status for record in scan.records} == {"SUCCESS", "MODEL_OK", "FAILED", "INVALID"},
                    "scanner collapsed truthful record states")

            panel = JobsPanel(SimpleNamespace(project_dir=project))
            wait_for_scan(app, panel)
            require(panel.job_list.count() == 4, "Jobs panel did not show every record")
            require(not hasattr(panel, "retry_button"), "Jobs panel exposed an unimplemented retry")
            require(not hasattr(panel, "delete_button"), "Jobs panel exposed destructive delete")

            labels = [panel.job_list.item(i).text() for i in range(panel.job_list.count())]
            require(any("SUCCESS" in label for label in labels), "success state not visible")
            require(any("FAILED" in label for label in labels), "failure state not visible")
            require(any("INVALID" in label for label in labels), "invalid state not visible")

            panel.job_list.setCurrentRow(labels.index(next(x for x in labels if "FAILED" in x)))
            require("model failure" in panel.details.toPlainText(), "saved failure detail was hidden")
            require(
                "raw diagnostic response" in panel.details.toPlainText(),
                "failed record's saved output text was hidden",
            )

            success_path.unlink()
            failure_path.unlink()
            invalid_path.unlink()
            project_evidence.unlink()
            panel.refresh_jobs()
            wait_for_scan(app, panel)
            require(panel.job_list.count() == 0, "empty state retained stale jobs")
            require(not panel.open_folder_button.isEnabled(), "empty state enabled folder action")

            deep_path = root / "deep.json"
            deep_path.write_text("[" * 1200 + "]" * 1200, encoding="utf-8")
            require(read_job_record(deep_path).status == "INVALID", "deep JSON escaped invalid classification")

            inaccessible = root / "not-a-directory"
            inaccessible.write_text("fixture", encoding="utf-8")
            agent_runner.WORKFLOW_OUTPUT_DIRS["inaccessible"] = inaccessible
            diagnostic_scan = scan_job_records()
            require(
                any("Could not scan job directory" in item for item in diagnostic_scan.diagnostics),
                "directory scan failure was hidden",
            )

            original_scan = jobs_module.scan_job_records

            def slow_scan(should_stop, **_):
                while not should_stop():
                    time.sleep(0.01)
                return JobScanResult(())

            jobs_module.scan_job_records = slow_scan
            stopping_panel = JobsPanel()
            require(stopping_panel._scan_thread.isRunning(), "shutdown fixture scan did not start")
            stopping_panel.request_scan_shutdown()
            wait_for_scan(app, stopping_panel)
            require(not stopping_panel.has_active_scan(), "Jobs scan survived shutdown request")
            jobs_module.scan_job_records = original_scan

            print("PASS: saved success, failure, and invalid records remain distinct")
            print("PASS: Jobs scans legacy and active-project records outside the Qt main thread")
            print("PASS: Jobs shows every recovered record and its truthful detail")
            print("PASS: Jobs exposes no fake retry, delete, cancel, or approval action")
            print("PASS: empty Jobs state is safe and disables record actions")
            print("PASS: deep malformed JSON is classified INVALID")
            print("PASS: inaccessible job history produces a visible scan diagnostic")
            print("PASS: active Jobs scan stops before application shutdown")
            print("PASS: read-only Jobs panel baseline verified")
    finally:
        agent_runner.WORKFLOW_OUTPUT_DIRS.clear()
        agent_runner.WORKFLOW_OUTPUT_DIRS.update(original_dirs)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
