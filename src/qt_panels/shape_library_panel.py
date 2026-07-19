#!/usr/bin/env python3
"""Read-only Shape Library baseline for existing raw harvest evidence."""

from __future__ import annotations

import subprocess

from PySide6.QtCore import QThread, Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.job_records import JobRecord, JobScanResult, read_job_record, scan_job_records


SHAPE_WORKFLOW = "shape_structure_harvest"


def is_shape_evidence(record: JobRecord) -> bool:
    return record.workflow_key == SHAPE_WORKFLOW or record.path.name.startswith(
        (f"{SHAPE_WORKFLOW}-", f"{SHAPE_WORKFLOW}__")
    )


class ShapeEvidenceScanThread(QThread):
    evidence_ready = Signal(object)

    def run(self):
        scan = scan_job_records(self.isInterruptionRequested)
        if self.isInterruptionRequested():
            return
        filtered = tuple(record for record in scan.records if is_shape_evidence(record))
        self.evidence_ready.emit(
            JobScanResult(filtered, scan.diagnostics, scan.omitted_for_byte_budget)
        )


class ShapeLibraryPanel(QWidget):
    status_changed = Signal(str)
    background_idle = Signal()

    def __init__(self):
        super().__init__()
        self._scan_thread = None
        self._loaded_once = False

        title = QLabel("Shape Library")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")

        self.boundary_label = QLabel(
            "Approved shapes: 0. The approval and extraction workflows are not implemented yet. "
            "Existing shape-harvest reports below remain raw evidence; they are not SVGs, masks, "
            "geometry, or approved reusable components."
        )
        self.boundary_label.setWordWrap(True)
        self.boundary_label.setStyleSheet("color: #d6c27a;")

        self.refresh_button = QPushButton("Refresh Raw Evidence")
        self.refresh_button.clicked.connect(self.refresh_evidence)

        self.open_folder_button = QPushButton("Open Containing Folder")
        self.open_folder_button.clicked.connect(self.open_containing_folder)
        self.open_folder_button.setEnabled(False)

        actions = QHBoxLayout()
        actions.addWidget(self.refresh_button)
        actions.addWidget(self.open_folder_button)
        actions.addStretch(1)

        self.evidence_list = QListWidget()
        self.evidence_list.setMinimumWidth(310)
        self.evidence_list.currentItemChanged.connect(self.update_selection)

        self.details = QTextEdit()
        self.details.setReadOnly(True)

        body = QHBoxLayout()
        body.addWidget(self.evidence_list, 1)
        body.addWidget(self.details, 2)

        self.status_label = QLabel("Open Shape Library to scan existing raw evidence.")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("color: #d6c27a;")

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.addWidget(title)
        layout.addWidget(self.boundary_label)
        layout.addLayout(actions)
        layout.addLayout(body, 1)
        layout.addWidget(self.status_label)
        self.setLayout(layout)
        self.clear_selection()

    def ensure_loaded(self):
        if not self._loaded_once:
            self.refresh_evidence()

    def selected_record(self) -> JobRecord | None:
        item = self.evidence_list.currentItem()
        if item is None:
            return None
        record = item.data(Qt.ItemDataRole.UserRole)
        return record if isinstance(record, JobRecord) else None

    def refresh_evidence(self, *_):
        if self.has_active_scan():
            self.set_status("A raw-evidence scan is already running.")
            return
        self._loaded_once = True
        self.refresh_button.setEnabled(False)
        self.set_status("Scanning existing shape-harvest evidence in the background…")
        self._scan_thread = ShapeEvidenceScanThread(self)
        self._scan_thread.evidence_ready.connect(self.apply_evidence)
        self._scan_thread.finished.connect(self.scan_finished)
        self._scan_thread.start()

    def apply_evidence(self, result: JobScanResult):
        self.evidence_list.clear()
        for record in result.records:
            item = QListWidgetItem(
                f"RAW {record.status}  |  {record.created_utc or 'time unavailable'}"
            )
            item.setData(Qt.ItemDataRole.UserRole, record)
            item.setToolTip(str(record.path))
            self.evidence_list.addItem(item)

        if self.evidence_list.count():
            self.evidence_list.setCurrentRow(0)
        else:
            self.clear_selection()

        message = (
            f"Showing {len(result.records)} raw shape-harvest record(s); approved shapes remain 0."
        )
        if result.diagnostics:
            message += " Scan warning: " + " | ".join(result.diagnostics)
        if result.omitted_for_byte_budget:
            message += (
                f" {result.omitted_for_byte_budget} candidate(s) omitted by the Jobs read budget."
            )
        self.set_status(message)

    def scan_finished(self):
        thread = self._scan_thread
        self._scan_thread = None
        if thread is not None:
            thread.deleteLater()
        self.refresh_button.setEnabled(True)
        self.background_idle.emit()

    def update_selection(self, *_):
        record = self.selected_record()
        if record is None:
            self.clear_selection()
            return
        self.open_folder_button.setEnabled(True)
        record = read_job_record(record.path)
        evidence = record.output_text or record.error or "No evidence text was recorded."
        self.details.setPlainText(
            "Authority: RAW SHAPE-HARVEST EVIDENCE — NOT AN APPROVED SHAPE\n"
            f"Record status: {record.status}\n"
            f"Created: {record.created_utc or 'Unavailable'}\n"
            f"Model: {record.model or 'Unavailable'}\n"
            f"Source: {record.source_path or 'Unavailable'}\n"
            f"Record: {record.path}\n\n"
            f"Evidence:\n{evidence}"
        )

    def clear_selection(self):
        self.open_folder_button.setEnabled(False)
        self.details.setPlainText(
            "No raw shape-harvest evidence is selected. A successful AI report is still raw "
            "until a future review workflow creates a durable approval derivative."
        )

    def open_containing_folder(self):
        record = self.selected_record()
        if record is None:
            self.set_status("Select a raw evidence record first.")
            return
        try:
            subprocess.Popen(["xdg-open", str(record.path.parent)])
            self.set_status(f"Opened raw-evidence folder: {record.path.parent}")
        except Exception as exc:
            self.set_status(f"Could not open raw-evidence folder: {exc}")

    def has_active_scan(self) -> bool:
        return self._scan_thread is not None and self._scan_thread.isRunning()

    def request_scan_shutdown(self) -> None:
        if not self.has_active_scan():
            self.background_idle.emit()
            return
        self._scan_thread.requestInterruption()

    def set_status(self, message: str):
        self.status_label.setText(message)
        self.status_changed.emit(message)
