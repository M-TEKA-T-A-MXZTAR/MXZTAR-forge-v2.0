#!/usr/bin/env python3
"""Verify the honest read-only Shape Library evidence baseline."""

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
from core.job_records import JobScanResult  # noqa: E402
from qt_panels import shape_library_panel as shape_module  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def write_record(path: Path, workflow: str, ok: bool, text: str) -> None:
    path.write_text(
        json.dumps(
            {
                "created_utc": "2026-07-19T13:00:00+00:00",
                "model": "qwen2.5vl:3b",
                "workflow_key": workflow,
                "source_path": "/tmp/source.png",
                "ok": ok,
                "error": "" if ok else text,
                "output_text": text if ok else "raw failed response",
            }
        ),
        encoding="utf-8",
    )


def wait_for_scan(app: QApplication, panel, timeout: float = 5) -> None:
    deadline = time.monotonic() + timeout
    while panel.has_active_scan() and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()
    require(not panel.has_active_scan(), "Shape Library scan did not finish")


def main() -> int:
    app = QApplication.instance() or QApplication([])
    original_dirs = dict(agent_runner.WORKFLOW_OUTPUT_DIRS)
    original_scan = shape_module.scan_job_records

    try:
        with tempfile.TemporaryDirectory(prefix="mxztar-shapes-") as temp_dir:
            root = Path(temp_dir)
            write_record(
                root / "shape_structure_harvest-success.json",
                "shape_structure_harvest",
                True,
                "raw silhouette candidate",
            )
            write_record(
                root / "shape_structure_harvest-failure.json",
                "shape_structure_harvest",
                False,
                "shape workflow failed",
            )
            (root / "shape_structure_harvest-invalid.json").write_text("{bad", encoding="utf-8")
            write_record(root / "source-art.json", "source_art_intelligence", True, "not a shape report")
            for index in range(510):
                write_record(
                    root / f"source_art_intelligence-{index:03d}.json",
                    "source_art_intelligence",
                    True,
                    "newer unrelated evidence",
                )

            agent_runner.WORKFLOW_OUTPUT_DIRS.clear()
            agent_runner.WORKFLOW_OUTPUT_DIRS["fixture"] = root

            panel = shape_module.ShapeLibraryPanel()
            require(not panel.has_active_scan(), "Shape Library scanned before it was opened")
            panel.ensure_loaded()
            wait_for_scan(app, panel)

            require(panel.evidence_list.count() == 3, "Shape Library did not filter raw evidence")
            labels = [panel.evidence_list.item(i).text() for i in range(3)]
            require(any("SUCCESS" in label for label in labels), "raw success is not visible")
            require(any("FAILED" in label for label in labels), "raw failure is not visible")
            require(any("INVALID" in label for label in labels), "invalid shape evidence is hidden")
            require("Approved shapes: 0" in panel.boundary_label.text(), "approval boundary is hidden")
            require("NOT AN APPROVED SHAPE" in panel.details.toPlainText(), "raw evidence was promoted")
            panel.evidence_list.setCurrentRow(labels.index(next(x for x in labels if "FAILED" in x)))
            require("shape workflow failed" in panel.details.toPlainText(), "failure reason was hidden")
            require("Saved output text" in panel.details.toPlainText(), "failed saved output was hidden")
            for forbidden in ("approve_button", "extract_button", "morph_button", "make_3d_button", "delete_button"):
                require(not hasattr(panel, forbidden), f"Shape Library exposed fake control: {forbidden}")

            def slow_scan(should_stop, **_):
                while not should_stop():
                    time.sleep(0.01)
                return JobScanResult(())

            shape_module.scan_job_records = slow_scan
            stopping_panel = shape_module.ShapeLibraryPanel()
            stopping_panel.ensure_loaded()
            require(stopping_panel.has_active_scan(), "shutdown fixture scan did not start")
            stopping_panel.request_scan_shutdown()
            wait_for_scan(app, stopping_panel)

            print("PASS: Shape Library loads only when opened")
            print("PASS: raw success, failure, and invalid shape evidence remain distinct")
            print("PASS: unrelated workflow records are excluded")
            print("PASS: unrelated records cannot crowd shape evidence out of bounded discovery")
            print("PASS: failed evidence shows both error and saved output text")
            print("PASS: raw evidence is never represented as an approved shape")
            print("PASS: no fake approval, extraction, Morph, Make 3D, or delete action exists")
            print("PASS: Shape Library scan stops asynchronously before shutdown")
            print("PASS: read-only Shape Library evidence baseline verified")
    finally:
        shape_module.scan_job_records = original_scan
        agent_runner.WORKFLOW_OUTPUT_DIRS.clear()
        agent_runner.WORKFLOW_OUTPUT_DIRS.update(original_dirs)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
