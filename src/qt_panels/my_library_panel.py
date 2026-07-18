#!/usr/bin/env python3
"""My Library source-art baseline for MXZTAR Forge v2.0.

This first library stage is intentionally read-only. It discovers supported
source art through the shared source-library service, previews the selected
file, and hands the exact SourceArtItem to Agent Workflows without copying,
moving, renaming, or modifying the source.
"""

from __future__ import annotations

import subprocess

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.source_library import (
    SourceArtItem,
    format_size,
    known_source_dirs,
    scan_source_art,
)


class MyLibraryPanel(QWidget):
    status_changed = Signal(str)
    source_selected = Signal(object)

    def __init__(self):
        super().__init__()
        self.source_items = []

        title = QLabel("My Library")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")

        intro = QLabel(
            "Browse known source art, inspect it safely, and send one deliberate selection "
            "to Agent Workflows. This stage is read-only and does not alter source files."
        )
        intro.setWordWrap(True)
        intro.setStyleSheet("color: #cfcfcf;")

        boundary = QLabel(
            "Library stage: Source Art. Workflow outputs and approved reusable artifacts "
            "will appear here only after their durable project contracts are implemented."
        )
        boundary.setWordWrap(True)
        boundary.setStyleSheet("color: #d6c27a;")

        self.source_combo = QComboBox()
        self.source_combo.setToolTip(
            "Supported images discovered in workspace/input, workspace/imports, "
            "and workspace/test_inputs."
        )
        self.source_combo.currentIndexChanged.connect(self.update_selection)

        refresh_button = QPushButton("Refresh Library")
        refresh_button.setToolTip("Rescan known source folders without changing their contents.")
        refresh_button.clicked.connect(self.refresh_library)

        self.open_folder_button = QPushButton("Open Containing Folder")
        self.open_folder_button.clicked.connect(self.open_containing_folder)

        self.use_button = QPushButton("Use in Agent Workflows")
        self.use_button.setToolTip(
            "Select this exact source in Agent Workflows without copying or moving it."
        )
        self.use_button.clicked.connect(self.use_in_agent_workflows)

        source_row = QHBoxLayout()
        source_row.addWidget(QLabel("Source art:"))
        source_row.addWidget(self.source_combo, 1)
        source_row.addWidget(refresh_button)

        action_row = QHBoxLayout()
        action_row.addWidget(self.use_button)
        action_row.addWidget(self.open_folder_button)
        action_row.addStretch(1)

        self.preview_label = QLabel("No source preview available.")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(320, 240)
        self.preview_label.setStyleSheet(
            "background-color: #181818; border: 1px solid #3a3a3a; padding: 8px;"
        )

        self.details = QTextEdit()
        self.details.setReadOnly(True)
        self.details.setMinimumHeight(180)

        preview_frame = QFrame()
        preview_frame.setFrameShape(QFrame.Shape.StyledPanel)
        preview_layout = QHBoxLayout()
        preview_layout.addWidget(self.preview_label, 1)
        preview_layout.addWidget(self.details, 1)
        preview_frame.setLayout(preview_layout)

        self.status_label = QLabel("Ready.")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("color: #d6c27a;")

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.addWidget(title)
        layout.addWidget(intro)
        layout.addWidget(boundary)
        layout.addSpacing(10)
        layout.addLayout(source_row)
        layout.addLayout(action_row)
        layout.addWidget(preview_frame, 1)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        self.refresh_library()

    def selected_source(self) -> SourceArtItem | None:
        item = self.source_combo.currentData()
        return item if isinstance(item, SourceArtItem) else None

    def refresh_library(self):
        previous_path = self.selected_source().path if self.selected_source() else None

        self.source_combo.blockSignals(True)
        self.source_combo.clear()
        self.source_items = scan_source_art()

        if not self.source_items:
            self.source_combo.addItem("No supported source art found", None)
            self.source_combo.blockSignals(False)
            self.clear_selection()
            self.set_status("No source art found. Add a supported image to a known source folder.")
            return

        selected_index = 0
        for index, item in enumerate(self.source_items):
            self.source_combo.addItem(item.label, item)
            if previous_path is not None and item.path == previous_path:
                selected_index = index

        self.source_combo.setCurrentIndex(selected_index)
        self.source_combo.blockSignals(False)
        self.update_selection()
        self.set_status(f"Found {len(self.source_items)} source-art file(s).")

    def update_selection(self):
        item = self.selected_source()

        if item is None:
            self.clear_selection()
            return

        self.use_button.setEnabled(True)
        self.open_folder_button.setEnabled(True)
        self.details.setPlainText(
            "Selected source art\n"
            "-------------------\n"
            f"Name: {item.path.name}\n"
            f"Path: {item.path}\n"
            f"Library section: {item.folder_name}\n"
            f"Type: {item.suffix}\n"
            f"Size: {format_size(item.size_bytes)}\n\n"
            "Authority boundary:\n"
            "- The original file remains in place.\n"
            "- Selection does not imply approval or ownership verification.\n"
            "- Agent output will be stored separately from this source."
        )
        self.load_preview(item)

    def load_preview(self, item: SourceArtItem):
        pixmap = QPixmap(str(item.path))

        if pixmap.isNull():
            self.preview_label.setPixmap(QPixmap())
            self.preview_label.setText(
                "Preview unavailable for this file.\nThe source remains selectable."
            )
            return

        target = self.preview_label.size()
        scaled = pixmap.scaled(
            max(1, target.width() - 16),
            max(1, target.height() - 16),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.preview_label.setText("")
        self.preview_label.setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        item = self.selected_source()
        if item is not None:
            self.load_preview(item)

    def clear_selection(self):
        self.use_button.setEnabled(False)
        self.open_folder_button.setEnabled(False)
        self.preview_label.setPixmap(QPixmap())
        self.preview_label.setText("No source preview available.")
        folders = "\n".join(f"- {path}" for path in known_source_dirs())
        self.details.setPlainText(
            "Supported source types:\n"
            ".png, .jpg, .jpeg, .webp, .bmp, .tif, .tiff\n\n"
            "Known source folders:\n"
            f"{folders}"
        )

    def use_in_agent_workflows(self):
        item = self.selected_source()

        if item is None:
            self.set_status("Select a source image before opening Agent Workflows.")
            return

        if not item.path.exists():
            self.set_status(f"Selected source no longer exists: {item.path}")
            return

        self.source_selected.emit(item)
        self.set_status(f"Sent source to Agent Workflows: {item.path.name}")

    def open_containing_folder(self):
        item = self.selected_source()

        if item is None:
            self.set_status("Select a source image before opening its folder.")
            return

        try:
            subprocess.Popen(["xdg-open", str(item.path.parent)])
            self.set_status(f"Opened source folder: {item.path.parent}")
        except Exception as exc:
            self.set_status(f"Could not open source folder: {exc}")

    def set_status(self, message: str):
        self.status_label.setText(message)
        self.status_changed.emit(message)
