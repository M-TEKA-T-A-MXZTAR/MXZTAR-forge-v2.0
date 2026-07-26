#!/usr/bin/env python3
"""Usability corrections for the integrated Forge shape/object CAD workspace."""

from __future__ import annotations

import copy

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QSizePolicy, QSplitter

from core.object_scene import save_object_scene, sync_scene_from_shape_document
from core.shape_document import (
    add_circle,
    add_ellipse,
    add_rectangle,
    add_square,
    add_star,
    write_shape_document_autosave,
)
from qt_panels.object_cad_panel import ObjectCadEditorPanel, ObjectViewport


class StableObjectViewport(ObjectViewport):
    """Keep a scene camera anchor stable while one selected object is transformed."""

    def __init__(self):
        super().__init__()
        self._anchor_scene_id: str | None = None
        self._scene_anchor: tuple[float, float, float] | None = None

    @staticmethod
    def _anchor_for_scene(scene: dict | None) -> tuple[float, float, float]:
        if not isinstance(scene, dict):
            return 512.0, 512.0, 0.0
        objects = scene.get("objects", [])
        if not isinstance(objects, list) or not objects:
            return 512.0, 512.0, 0.0
        count = len(objects)
        return (
            sum(float(item["position"]["x"]) for item in objects) / count,
            sum(float(item["position"]["y"]) for item in objects) / count,
            sum(float(item["position"]["z"]) for item in objects) / count,
        )

    def set_scene(self, scene: dict | None, selected_object_id: str | None = None) -> None:
        scene_id = scene.get("scene_id") if isinstance(scene, dict) else None
        if not isinstance(scene_id, str):
            self._anchor_scene_id = None
            self._scene_anchor = None
        elif scene_id != self._anchor_scene_id:
            self._anchor_scene_id = scene_id
            self._scene_anchor = self._anchor_for_scene(scene)
        super().set_scene(scene, selected_object_id)

    def _scene_target(self) -> tuple[float, float, float]:
        if self._scene_anchor is not None:
            return self._scene_anchor
        return super()._scene_target()


class SingleObjectWorkspacePanel(ObjectCadEditorPanel):
    """Present visible non-overlapping shapes and isolate one object transform at a time."""

    GRID_COLUMNS = 3
    GRID_ROWS = 3
    GRID_LEFT = 70.0
    GRID_TOP = 70.0
    GRID_STEP_X = 310.0
    GRID_STEP_Y = 300.0

    def __init__(self, project_session):
        super().__init__(project_session)
        self.header_label.setText(
            "EDITOR; single-object shape/CAD workspace. Add visible shapes, select one object, "
            "then move, resize, rotate, style, inspect, and save it locally."
        )
        self._install_stable_viewport()
        self._install_compact_workspace()
        self._update_inspector()
        self._update_cad_controls()

    def _install_stable_viewport(self) -> None:
        old_viewport = self.object_viewport
        viewport_index = self.view_stack.indexOf(old_viewport)
        self.view_stack.removeWidget(old_viewport)

        stable_viewport = StableObjectViewport()
        stable_viewport.selection_changed.connect(self.select_cad_object)
        stable_viewport.object_committed.connect(self.commit_viewport_object)
        stable_viewport.view_committed.connect(self.commit_view_state)
        stable_viewport.view_previewed.connect(self.schedule_view_state_commit)
        stable_viewport.status_changed.connect(self.set_status)
        self.view_stack.insertWidget(max(0, viewport_index), stable_viewport)
        self.object_viewport = stable_viewport

        if self.object_scene is not None:
            self.object_viewport.set_scene(self.object_scene, self.selected_object_id)
        old_viewport.deleteLater()

    @staticmethod
    def _detach_control(widget) -> None:
        widget.setParent(None)

    def _install_compact_workspace(self) -> None:
        outer_layout = self.layout()
        old_inspector = self.inspector

        retained_widgets = [
            self.inspector_title,
            *self.position_spins.values(),
            *self.size_spins.values(),
            *self.rotation_spins.values(),
            self.opacity_spin,
            self.color_button,
        ]
        for widget in retained_widgets:
            self._detach_control(widget)

        outer_layout.removeWidget(old_inspector)
        outer_layout.removeWidget(self.view_stack)
        old_inspector.deleteLater()

        inspector = QFrame()
        inspector.setFrameShape(QFrame.Shape.StyledPanel)
        inspector.setMinimumWidth(360)
        inspector.setMaximumWidth(520)
        inspector.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        inspector_layout = QGridLayout()
        inspector_layout.setContentsMargins(10, 8, 10, 8)
        inspector_layout.setHorizontalSpacing(6)
        inspector_layout.setVerticalSpacing(6)
        inspector_layout.addWidget(self.inspector_title, 0, 0, 1, 4)

        rows = (
            (1, "Position", self.position_spins),
            (2, "Size", self.size_spins),
            (3, "Rotation", self.rotation_spins),
        )
        for row, title, controls in rows:
            label = QLabel(title)
            label.setStyleSheet("font-weight: 600;")
            inspector_layout.addWidget(label, row, 0)
            for column, axis in enumerate(("x", "y", "z"), start=1):
                inspector_layout.addWidget(controls[axis], row, column)

        opacity_label = QLabel("Opacity")
        opacity_label.setStyleSheet("font-weight: 600;")
        inspector_layout.addWidget(opacity_label, 4, 0)
        inspector_layout.addWidget(self.opacity_spin, 4, 1)
        inspector_layout.addWidget(self.color_button, 4, 2, 1, 2)
        inspector_layout.setRowStretch(5, 1)
        inspector.setLayout(inspector_layout)
        self.inspector = inspector

        self.canvas.setMinimumHeight(260)
        self.object_viewport.setMinimumHeight(260)
        self.view_stack.setMinimumHeight(260)
        self.view_stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        splitter.addWidget(self.view_stack)
        splitter.addWidget(self.inspector)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 2)
        splitter.setSizes([720, 380])
        outer_layout.insertWidget(3, splitter, 1)
        self.workspace_splitter = splitter

        self.setMinimumHeight(0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def _next_primitive_position(self) -> tuple[float, float]:
        count = len(self.document.get("objects", [])) if isinstance(self.document, dict) else 0
        slots_per_page = self.GRID_COLUMNS * self.GRID_ROWS
        slot = count % slots_per_page
        page = count // slots_per_page
        column = slot % self.GRID_COLUMNS
        row = slot // self.GRID_COLUMNS
        cascade = float(page * 14)
        return (
            self.GRID_LEFT + column * self.GRID_STEP_X + cascade,
            self.GRID_TOP + row * self.GRID_STEP_Y + cascade,
        )

    def _add_primitive(self, primitive_type: str) -> None:
        if self.document is None:
            self.set_status("Create or open a shape document first.")
            return
        try:
            x, y = self._next_primitive_position()
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
            new_shape = self.document["objects"][-1]
            detail = (
                f"Added one visible {primitive_type} in grid position and autosaved revision "
                f"{self.document['revision']} to {autosave.name}."
            )

            if self.object_scene is not None:
                synchronized, added = sync_scene_from_shape_document(
                    self.object_scene,
                    self.document,
                )
                if added:
                    save_object_scene(self.project_session, synchronized)
                    self.object_scene = synchronized
                    self.selected_object_id = (
                        f"cad_{new_shape['object_id'].removeprefix('object_')}"
                    )
                    self.object_viewport.set_scene(
                        self.object_scene,
                        self.selected_object_id,
                    )
                    self._update_inspector()
                    self._update_cad_controls()
                    detail += " The new shape was synchronized into 3D and selected."

            self.set_status(detail)
        except Exception as exc:
            self.set_status(f"Could not add the {primitive_type}: {exc}")
        self.update_controls()

    def select_cad_object(self, object_id) -> None:
        super().select_cad_object(object_id)
        self.object_viewport.update()
        if isinstance(object_id, str):
            item = self._selected_scene_object()
            if item is not None:
                self.set_status(
                    f"Selected one {item['primitive_type']} object. Only this object will move or resize."
                )

    def commit_viewport_object(self, object_id: str, updated_object: dict) -> None:
        before = None
        if self.object_scene is not None:
            before = {
                item["object_id"]: copy.deepcopy(item)
                for item in self.object_scene.get("objects", [])
            }
        super().commit_viewport_object(object_id, updated_object)
        if before is None or self.object_scene is None:
            return
        unchanged = all(
            item["object_id"] == object_id or item == before.get(item["object_id"])
            for item in self.object_scene.get("objects", [])
        )
        if not unchanged:
            self.set_status(
                "Object isolation check failed: an unselected object changed unexpectedly."
            )
