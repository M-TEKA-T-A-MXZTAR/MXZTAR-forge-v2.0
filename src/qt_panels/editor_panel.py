#!/usr/bin/env python3
"""Minimum project-owned Forge Editor shell for native shape documents."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import (
    QComboBox,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.project_session import ProjectSession
from core.shape_document import (
    add_rectangle,
    can_redo,
    can_undo,
    create_blank_shape_document,
    list_shape_documents,
    load_shape_document,
    redo,
    save_shape_document,
    undo,
    write_shape_document_autosave,
)


class EditorPanel(QWidget):
    status_changed = Signal(str)

    def __init__(self, project_session: ProjectSession):
        super().__init__()
        self.project_session = project_session
        self.document: dict | None = None
        self._refreshing_documents = False

        title = QLabel("Editor")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")

        boundary = QLabel(
            "Native shape-document foundation. This milestone supports one real reversible "
            "operation: Add Rectangle. Extraction, free drawing, booleans, approval, 3D, and "
            "export are not exposed yet."
        )
        boundary.setWordWrap(True)
        boundary.setStyleSheet("color: #d6c27a;")

        self.document_selector = QComboBox()
        self.document_selector.setToolTip("Open a project-owned native shape document.")
        self.document_selector.currentIndexChanged.connect(self.open_selected_document)

        self.new_button = QPushButton("New Blank Document")
        self.new_button.clicked.connect(self.create_blank_document)

        self.add_rectangle_button = QPushButton("Add Rectangle")
        self.add_rectangle_button.clicked.connect(self.add_rectangle_command)

        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.undo_command)

        self.redo_button = QPushButton("Redo")
        self.redo_button.clicked.connect(self.redo_command)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_document)

        controls = QHBoxLayout()
        controls.addWidget(self.document_selector, 1)
        controls.addWidget(self.new_button)
        controls.addWidget(self.add_rectangle_button)
        controls.addWidget(self.undo_button)
        controls.addWidget(self.redo_button)
        controls.addWidget(self.save_button)

        self.scene = QGraphicsScene(self)
        self.canvas = QGraphicsView(self.scene)
        self.canvas.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.canvas.setMinimumHeight(360)
        self.canvas.setToolTip("Project-owned shape canvas. Mouse drag pans the view.")

        self.document_label = QLabel("No shape document is open.")
        self.document_label.setWordWrap(True)
        self.document_label.setStyleSheet("font-weight: 700;")

        self.status_label = QLabel("Open a writable project to create a blank shape document.")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("color: #d6c27a;")

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.addWidget(title)
        layout.addWidget(boundary)
        layout.addLayout(controls)
        layout.addWidget(self.document_label)
        layout.addWidget(self.canvas, 1)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        self.update_controls()

    def set_project_state(self, _state) -> None:
        self.document = None
        self.scene.clear()
        self.refresh_documents()

    def has_open_document(self) -> bool:
        return self.document is not None

    def refresh_documents(self, selected_document_id: str | None = None) -> None:
        self._refreshing_documents = True
        signals_were_blocked = self.document_selector.blockSignals(True)
        self.document_selector.clear()
        documents: tuple[dict, ...] = ()
        try:
            if self.project_session.state is None:
                self.set_status("Open a project before using the Editor.")
                return
            documents = list_shape_documents(self.project_session)
            for document in documents:
                self.document_selector.addItem(
                    f"{document['title']} — r{document['revision']}",
                    document["document_id"],
                )
            if not documents:
                self.document = None
                self.scene.clear()
                self.document_label.setText("No shape document is open.")
                self.set_status(
                    "This project has no native shape documents. Create one blank document to begin."
                )
                return
        except Exception as exc:
            self.document = None
            self.scene.clear()
            self.document_label.setText("Shape documents could not be loaded.")
            self.set_status(f"Editor document discovery failed: {exc}")
            return
        finally:
            self.document_selector.blockSignals(signals_were_blocked)
            self._refreshing_documents = False
            self.update_controls()

        index = self.document_selector.findData(selected_document_id)
        selection_signals_were_blocked = self.document_selector.blockSignals(True)
        try:
            self.document_selector.setCurrentIndex(index if index >= 0 else 0)
        finally:
            self.document_selector.blockSignals(selection_signals_were_blocked)
        self.open_selected_document()

    def open_selected_document(self, *_args) -> None:
        if self._refreshing_documents:
            return
        document_id = self.document_selector.currentData()
        if not isinstance(document_id, str):
            self.document = None
            self.render_document()
            return
        try:
            result = load_shape_document(self.project_session, document_id)
            self.document = result.document
            self.render_document()
            recovery_note = (
                " Recovered a newer autosave; use Save to make it canonical."
                if result.recovered_from_autosave
                else ""
            )
            self.set_status(
                f"Opened {self.document['title']} revision {self.document['revision']}.{recovery_note}"
            )
        except Exception as exc:
            self.document = None
            self.render_document()
            self.set_status(f"Could not open the selected shape document: {exc}")

    def create_blank_document(self, *_args) -> None:
        try:
            result = create_blank_shape_document(self.project_session)
            created_id = result.document["document_id"]
            self.document = result.document
            self.refresh_documents(created_id)
            self.set_status(f"Created project-owned blank document: {created_id}.")
        except Exception as exc:
            self.set_status(f"Could not create a blank shape document: {exc}")
        self.update_controls()

    def add_rectangle_command(self, *_args) -> None:
        if self.document is None:
            self.set_status("Create or open a shape document first.")
            return
        try:
            offset = 40.0 * len(self.document["objects"])
            self.document = add_rectangle(
                self.document,
                x=120.0 + offset,
                y=120.0 + offset,
            )
            autosave = write_shape_document_autosave(self.project_session, self.document)
            self.render_document()
            self.set_status(
                f"Added one rectangle and autosaved revision {self.document['revision']} to {autosave.name}."
            )
        except Exception as exc:
            self.set_status(f"Could not add the rectangle: {exc}")
        self.update_controls()

    def undo_command(self, *_args) -> None:
        if self.document is None:
            return
        try:
            self.document = undo(self.document)
            write_shape_document_autosave(self.project_session, self.document)
            self.render_document()
            self.set_status(f"Undo applied and autosaved at revision {self.document['revision']}.")
        except Exception as exc:
            self.set_status(f"Could not undo the last editor command: {exc}")
        self.update_controls()

    def redo_command(self, *_args) -> None:
        if self.document is None:
            return
        try:
            self.document = redo(self.document)
            write_shape_document_autosave(self.project_session, self.document)
            self.render_document()
            self.set_status(f"Redo applied and autosaved at revision {self.document['revision']}.")
        except Exception as exc:
            self.set_status(f"Could not redo the editor command: {exc}")
        self.update_controls()

    def save_document(self, *_args) -> None:
        if self.document is None:
            self.set_status("No shape document is open.")
            return
        try:
            document_id = self.document["document_id"]
            revision = self.document["revision"]
            path = save_shape_document(self.project_session, self.document)
            self.refresh_documents(document_id)
            self.set_status(f"Saved canonical shape document revision {revision}: {path.name}")
        except Exception as exc:
            self.set_status(f"Could not save the shape document: {exc}")
        self.update_controls()

    def render_document(self) -> None:
        self.scene.clear()
        if self.document is None:
            self.scene.setSceneRect(0, 0, 1024, 1024)
            self.document_label.setText("No shape document is open.")
            self.update_controls()
            return
        canvas = self.document["coordinate_space"]["canvas"]
        self.scene.setSceneRect(0, 0, canvas["width"], canvas["height"])
        for shape in self.document["objects"]:
            style = shape["style"]
            pen = QPen(QColor(style["stroke"]))
            pen.setWidthF(style["stroke_width"])
            brush = QBrush(QColor(style["fill"]))
            self.scene.addRect(
                shape["x"],
                shape["y"],
                shape["width"],
                shape["height"],
                pen,
                brush,
            )
        self.document_label.setText(
            f"{self.document['title']} | revision {self.document['revision']} | "
            f"{len(self.document['objects'])} visible object(s) | "
            f"{self.document['coordinate_space']['units']} | draft"
        )
        self.canvas.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.update_controls()

    def update_controls(self) -> None:
        writable = self.project_session.is_writable
        has_document = self.document is not None
        self.new_button.setEnabled(writable)
        self.document_selector.setEnabled(self.project_session.state is not None)
        self.add_rectangle_button.setEnabled(writable and has_document)
        self.undo_button.setEnabled(writable and can_undo(self.document))
        self.redo_button.setEnabled(writable and can_redo(self.document))
        self.save_button.setEnabled(writable and has_document)

    def set_status(self, message: str) -> None:
        self.status_label.setText(message)
        self.status_changed.emit(message)
