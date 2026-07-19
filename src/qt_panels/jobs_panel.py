#!/usr/bin/env python3
"""Read-only Jobs panel for truthful recovery of existing agent records."""

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
from core.project_session import ProjectSession


class JobScanThread(QThread):
    records_ready = Signal(object)

    def __init__(self, project_dir=None, parent=None):
        super().__init__(parent)
        self._project_dir = project_dir

    def run(self):
        result = scan_job_records(
            self.isInterruptionRequested, project_dir=self._project_dir
        )
        if not self.isInterruptionRequested():
            self.records_ready.emit(result)


class JobsPanel(QWidget):
    status_changed = Signal(str)
    background_idle = Signal()

    def __init__(self, project_session: ProjectSession | None = None):
        super().__init__()
        self.project_session = project_session or ProjectSession()
        self._scan_thread = None
        self._refresh_pending = False

        title = QLabel("Jobs")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")

        intro = QLabel(
            "Inspect existing local workflow records. This baseline is read-only: it does not "
            "retry, cancel, delete, approve, or alter recorded work."
        )
        intro.setWordWrap(True)
        intro.setStyleSheet("color: #cfcfcf;")

        self.refresh_button = QPushButton("Refresh Jobs")
        self.refresh_button.clicked.connect(self.refresh_jobs)

        self.open_folder_button = QPushButton("Open Containing Folder")
        self.open_folder_button.clicked.connect(self.open_containing_folder)
        self.open_folder_button.setEnabled(False)

        actions = QHBoxLayout()
        actions.addWidget(self.refresh_button)
        actions.addWidget(self.open_folder_button)
        actions.addStretch(1)

        self.job_list = QListWidget()
        self.job_list.setMinimumWidth(310)
        self.job_list.currentItemChanged.connect(self.update_selection)

        self.details = QTextEdit()
        self.details.setReadOnly(True)

        body = QHBoxLayout()
        body.addWidget(self.job_list, 1)
        body.addWidget(self.details, 2)

        self.status_label = QLabel("Ready.")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("color: #d6c27a;")

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.addWidget(title)
        layout.addWidget(intro)
        layout.addLayout(actions)
        layout.addLayout(body, 1)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        self.refresh_jobs()

    def selected_record(self) -> JobRecord | None:
        item = self.job_list.currentItem()
        if item is None:
            return None
        record = item.data(Qt.ItemDataRole.UserRole)
        return record if isinstance(record, JobRecord) else None

    def refresh_jobs(self, *_):
        if self._scan_thread is not None and self._scan_thread.isRunning():
            self._refresh_pending = True
            self._scan_thread.requestInterruption()
            self.set_status("Restarting the background job-record scan…")
            return

        self.refresh_button.setEnabled(False)
        self.set_status("Scanning existing job records in the background…")
        self._scan_thread = JobScanThread(self.project_session.project_dir, self)
        self._scan_thread.records_ready.connect(self.apply_records)
        self._scan_thread.finished.connect(self.scan_finished)
        self._scan_thread.start()

    def set_project_state(self, _state=None):
        self.refresh_jobs()

    def apply_records(self, result: JobScanResult):
        records = result.records
        previous = self.selected_record()
        previous_path = previous.path if previous else None
        self.job_list.clear()
        selected = None

        for record in records:
            workflow = record.workflow_key or record.path.stem
            created = record.created_utc or "time unavailable"
            item = QListWidgetItem(f"{record.status}  |  {workflow}\n{created}")
            item.setData(Qt.ItemDataRole.UserRole, record)
            item.setToolTip(str(record.path))
            self.job_list.addItem(item)
            if selected is None or record.path == previous_path:
                selected = item

        if selected is not None:
            self.job_list.setCurrentItem(selected)
        else:
            self.clear_selection()
        message = f"Showing {len(records)} existing job record(s)."
        warnings = list(result.diagnostics)
        if result.omitted_for_byte_budget:
            warnings.append(
                f"{result.omitted_for_byte_budget} older candidate(s) omitted by the "
                "16 MiB decoded-record budget."
            )
        if warnings:
            message += " Scan warning: " + " | ".join(warnings)
        self.set_status(message)

    def scan_finished(self):
        thread = self._scan_thread
        self._scan_thread = None
        if thread is not None:
            thread.deleteLater()
        self.refresh_button.setEnabled(True)
        if self._refresh_pending:
            self._refresh_pending = False
            self.refresh_jobs()
            return
        self.background_idle.emit()

    def update_selection(self, *_):
        record = self.selected_record()
        if record is None:
            self.clear_selection()
            return

        self.open_folder_button.setEnabled(True)
        record = read_job_record(record.path)
        evidence = []
        if record.error:
            evidence.append(f"Error:\n{record.error}")
        if record.output_text:
            evidence.append(f"Saved output text:\n{record.output_text}")
        if not evidence:
            evidence.append("No result or error text was recorded.")
        self.details.setPlainText(
            f"Status: {record.status}\n"
            f"Created: {record.created_utc or 'Unavailable in this record'}\n"
            f"Workflow: {record.workflow_key or 'Unavailable'}\n"
            f"Model: {record.model or 'Unavailable'}\n"
            f"Source: {record.source_path or 'Unavailable'}\n"
            f"Record: {record.path}\n\n"
            f"{'Saved evidence' if record.status in ('SUCCESS', 'MODEL_OK') else 'Failure / validation evidence'}:\n"
            + "\n\n".join(evidence)
        )

    def has_active_scan(self) -> bool:
        thread = self._scan_thread
        return thread is not None and thread.isRunning()

    def request_scan_shutdown(self) -> None:
        """Request non-blocking scan shutdown; completion emits background_idle."""
        thread = self._scan_thread
        if thread is None or not thread.isRunning():
            self.background_idle.emit()
            return
        self._refresh_pending = False
        thread.requestInterruption()

    def clear_selection(self):
        self.open_folder_button.setEnabled(False)
        self.details.setPlainText(
            "No saved job record is selected. New records appear after Agent Workflows "
            "successfully saves either an output or a failure diagnostic."
        )

    def open_containing_folder(self):
        record = self.selected_record()
        if record is None:
            self.set_status("Select a job record first.")
            return
        try:
            subprocess.Popen(["xdg-open", str(record.path.parent)])
            self.set_status(f"Opened job-record folder: {record.path.parent}")
        except Exception as exc:
            self.set_status(f"Could not open job-record folder: {exc}")

    def set_status(self, message: str):
        self.status_label.setText(message)
        self.status_changed.emit(message)
