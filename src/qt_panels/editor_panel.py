#!/usr/bin/env python3
"""Project-owned Forge Editor with bounded menu-driven primitive workflows."""

from __future__ import annotations

import math

from PySide6.QtCore import QPointF, Qt, Signal
from PySide6.QtGui import QAction, QBrush, QColor, QPen, QPolygonF
from PySide6.QtWidgets import (
    QComboBox,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QMenu,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from core.project_session import ProjectSession
from core.shape_document import (
    add_circle,
    add_ellipse,
    add_rectangle,
    add_square,
    add_star,
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

        self.header_label = QLabel(
            "EDITOR; native shape-document workspace. Document manages project files, "
            "Shape adds reversible primitives, and Edit manages command history."
        )
        self.header_label.setWordWrap(True)
        self.header_label.setStyleSheet(
            "font-size: 18px; font-weight: 700; color: #d6c27a; padding: 0px;"
        )

        self.document_button = self._make_menu_button("Document")
        self.document_menu = QMenu(self.document_button)
        self.load_project_action = QAction("Load Project", self.document_menu)
        self.new_document_action = QAction("New Blank Document", self.document_menu)
        self.save_document_action = QAction("Save Document", self.document_menu)
        self.load_project_action.triggered.connect(self.load_project_build)
        self.new_document_action.triggered.connect(self.create_blank_document)
        self.save_document_action.triggered.connect(self.save_document)
        self.document_menu.addActions(
            [
                self.load_project_action,
                self.new_document_action,
                self.save_document_action,
            ]
        )
        self.document_button.setMenu(self.document_menu)

        self.shape_button = self._make_menu_button("Shape")
        self.shape_menu = QMenu(self.shape_button)
        self.rectangle_action = QAction("Rectangle", self.shape_menu)
        self.square_action = QAction("Square", self.shape_menu)
        self.circle_action = QAction("Circle", self.shape_menu)
        self.ellipse_action = QAction("Ellipse", self.shape_menu)
        self.star_action = QAction("Star", self.shape_menu)
        self.rectangle_action.triggered.connect(self.add_rectangle_command)
        self.square_action.triggered.connect(self.add_square_command)
        self.circle_action.triggered.connect(self.add_circle_command)
        self.ellipse_action.triggered.connect(self.add_ellipse_command)
        self.star_action.triggered.connect(self.add_star_command)
        self.shape_menu.addActions(
            [
                self.rectangle_action,
                self.square_action,
                self.circle_action,
                self.ellipse_action,
                self.star_action,
            ]
        )
        self.shape_button.setMenu(self.shape_menu)

        self.edit_button = self._make_menu_button("Edit")
        self.edit_menu = QMenu(self.edit_button)
        self.undo_action = QAction("Undo", self.edit_menu)
        self.redo_action = QAction("Redo", self.edit_menu)
        self.undo_action.triggered.connect(self.undo_command)
        self.redo_action.triggered.connect(self.redo_command)
        self.edit_menu.addActions([self.undo_action, self.redo_action])
        self.edit_button.setMenu(self.edit_menu)

        self.document_selector_label = QLabel("Current document:")
        self.document_selector_label.setStyleSheet("font-weight: 600;")
        self.document_selector = QComboBox()
        self.document_selector.setToolTip("Open a project-owned native shape document.")
        self.document_selector.currentIndexChanged.connect(self.open_selected_document)

        self.menu_row = QHBoxLayout()
        self.menu_row.setSpacing(8)
        self.menu_row.addWidget(self.document_button)
        self.menu_row.addWidget(self.shape_button)
        self.menu_row.addWidget(self.edit_button)
        self.menu_row.addSpacing(10)
        self.menu_row.addWidget(self.document_selector_label)
        self.menu_row.addWidget(self.document_selector, 1)

        self.scene = QGraphicsScene(self)
        self.canvas = QGraphicsView(self.scene)
        self.canvas.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.canvas.setMinimumHeight(360)
        self.canvas.setToolTip("Project-owned shape canvas. Mouse drag pans the view.")

        self.document_label = QLabel("No project build is loaded.")
        self.document_label.setWordWrap(True)
        self.document_label.setStyleSheet("font-weight: 700;")

        self.status_label = QLabel("Open a project from Start Here to use the Editor.")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("color: #d6c27a;")

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 4, 10, 10)
        layout.setSpacing(7)
        layout.addWidget(self.header_label)
        layout.addLayout(self.menu_row)
        layout.addWidget(self.document_label)
        layout.addWidget(self.canvas, 1)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        self.update_controls()

    @staticmethod
    def _make_menu_button(text: str) -> QToolButton:
        button = QToolButton()
        button.setText(text)
        button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        return button

    def set_project_state(self, _state) -> None:
        self.document = None
        self.scene.clear()
        self.load_project_build()

    def has_open_document(self) -> bool:
        return self.document is not None

    def load_project_build(self, *_args) -> None:
        state = self.project_session.state
        if state is None:
            self.document = None
            self.scene.clear()
            self.document_selector.clear()
            self.document_label.setText("No project build is loaded.")
            self.set_status("Open a project from Start Here before loading the Editor build.")
            self.update_controls()
            return

        project_name = state.assessment.manifest.get(
            "project_name", state.assessment.project_dir.name
        )
        selected_document_id = (
            self.document.get("document_id")
            if isinstance(self.document, dict)
            else self.document_selector.currentData()
        )
        outcome = self.refresh_documents(
            selected_document_id
            if isinstance(selected_document_id, str)
            else None
        )
        if outcome == "empty":
            self.document_label.setText(
                f"Project: {project_name} | No native shape document exists yet."
            )
            self.set_status(
                f"Loaded project build: {project_name}. Use Document → New Blank Document to begin."
            )
        self.update_controls()

    def refresh_documents(self, selected_document_id: str | None = None) -> str:
        self._refreshing_documents = True
        signals_were_blocked = self.document_selector.blockSignals(True)
        self.document_selector.clear()
        documents: tuple[dict, ...] = ()
        try:
            if self.project_session.state is None:
                self.document = None
                self.scene.clear()
                self.document_label.setText("No project build is loaded.")
                self.set_status("Open a project before using the Editor.")
                return "detached"
            documents = list_shape_documents(self.project_session)
            for document in documents:
                self.document_selector.addItem(
                    f"{document['title']} — r{document['revision']}",
                    document["document_id"],
                )
            if not documents:
                self.document = None
                self.scene.clear()
                project_name = self.project_session.state.assessment.manifest.get(
                    "project_name", self.project_session.state.assessment.project_dir.name
                )
                self.document_label.setText(
                    f"Project: {project_name} | No native shape document exists yet."
                )
                self.set_status(
                    "This project has no native shape documents. Use Document → New Blank Document."
                )
                return "empty"
        except Exception as exc:
            self.document = None
            self.scene.clear()
            self.document_label.setText("Project build could not be loaded.")
            self.set_status(f"Editor document discovery failed: {exc}")
            return "error"
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
        return "loaded"

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
                " Recovered a newer autosave; use Document → Save Document to make it canonical."
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

    def _add_primitive(self, primitive_type: str) -> None:
        if self.document is None:
            self.set_status("Create or open a shape document first.")
            return
        try:
            offset = 28.0 * len(self.document["objects"])
            x = 110.0 + offset
            y = 110.0 + offset
            if primitive_type == "rectangle":
                self.document = add_rectangle(self.document, x=x, y=y)
            elif primitive_type == "square":
                self.document = add_square(self.document, x=x, y=y)
            elif primitive_type == "circle":
                self.document = add_circle(self.document, x=x, y=y)
            elif primitive_type == "ellipse":
                self.document = add_ellipse(self.document, x=x, y=y)
            elif primitive_type == "star":
                self.document = add_star(self.document, x=x, y=y)
            else:
                raise ValueError(f"Unsupported primitive: {primitive_type}")
            autosave = write_shape_document_autosave(self.project_session, self.document)
            self.render_document()
            self.set_status(
                f"Added one {primitive_type} and autosaved revision "
                f"{self.document['revision']} to {autosave.name}."
            )
        except Exception as exc:
            self.set_status(f"Could not add the {primitive_type}: {exc}")
        self.update_controls()

    def add_rectangle_command(self, *_args) -> None:
        self._add_primitive("rectangle")

    def add_square_command(self, *_args) -> None:
        self._add_primitive("square")

    def add_circle_command(self, *_args) -> None:
        self._add_primitive("circle")

    def add_ellipse_command(self, *_args) -> None:
        self._add_primitive("ellipse")

    def add_star_command(self, *_args) -> None:
        self._add_primitive("star")

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
            self.set_status(
                f"Saved canonical shape document revision {revision}: {path.name}"
            )
        except Exception as exc:
            self.set_status(f"Could not save the shape document: {exc}")
        self.update_controls()

    @staticmethod
    def _star_polygon(shape: dict) -> QPolygonF:
        center_x = shape["x"] + (shape["width"] / 2.0)
        center_y = shape["y"] + (shape["height"] / 2.0)
        radius_x = shape["width"] / 2.0
        radius_y = shape["height"] / 2.0
        point_count = shape.get("points", 5)
        inner_ratio = shape.get("inner_ratio", 0.45)
        vertices = []
        for index in range(point_count * 2):
            angle = (-math.pi / 2.0) + (index * math.pi / point_count)
            ratio = 1.0 if index % 2 == 0 else inner_ratio
            vertices.append(
                QPointF(
                    center_x + math.cos(angle) * radius_x * ratio,
                    center_y + math.sin(angle) * radius_y * ratio,
                )
            )
        return QPolygonF(vertices)

    def render_document(self) -> None:
        self.scene.clear()
        if self.document is None:
            self.scene.setSceneRect(0, 0, 1024, 1024)
            if self.project_session.state is None:
                self.document_label.setText("No project build is loaded.")
            self.update_controls()
            return
        canvas = self.document["coordinate_space"]["canvas"]
        self.scene.setSceneRect(0, 0, canvas["width"], canvas["height"])
        for shape in self.document["objects"]:
            style = shape["style"]
            pen = QPen(QColor(style["stroke"]))
            pen.setWidthF(style["stroke_width"])
            brush = QBrush(QColor(style["fill"]))
            if shape["type"] in {"rectangle", "square"}:
                self.scene.addRect(
                    shape["x"],
                    shape["y"],
                    shape["width"],
                    shape["height"],
                    pen,
                    brush,
                )
            elif shape["type"] in {"circle", "ellipse"}:
                self.scene.addEllipse(
                    shape["x"],
                    shape["y"],
                    shape["width"],
                    shape["height"],
                    pen,
                    brush,
                )
            elif shape["type"] == "star":
                self.scene.addPolygon(self._star_polygon(shape), pen, brush)
            else:
                raise ValueError(f"Unsupported rendered shape: {shape['type']}")
        project_name = self.project_session.state.assessment.manifest.get(
            "project_name", self.project_session.state.assessment.project_dir.name
        )
        self.document_label.setText(
            f"Project: {project_name} | {self.document['title']} | "
            f"revision {self.document['revision']} | "
            f"{len(self.document['objects'])} visible object(s) | "
            f"{self.document['coordinate_space']['units']} | draft"
        )
        self.canvas.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.update_controls()

    def update_controls(self) -> None:
        attached = self.project_session.state is not None
        writable = self.project_session.is_writable
        has_document = self.document is not None

        self.document_button.setEnabled(attached)
        self.load_project_action.setEnabled(attached)
        self.new_document_action.setEnabled(writable)
        self.save_document_action.setEnabled(writable and has_document)
        self.document_selector.setEnabled(attached and self.document_selector.count() > 0)

        self.shape_button.setEnabled(writable and has_document)
        for action in (
            self.rectangle_action,
            self.square_action,
            self.circle_action,
            self.ellipse_action,
            self.star_action,
        ):
            action.setEnabled(writable and has_document)

        self.edit_button.setEnabled(has_document)
        self.undo_action.setEnabled(writable and can_undo(self.document))
        self.redo_action.setEnabled(writable and can_redo(self.document))

    def set_status(self, message: str) -> None:
        self.status_label.setText(message)
        self.status_changed.emit(message)
