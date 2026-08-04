#!/usr/bin/env python3
"""Usability corrections for the integrated Forge shape/object CAD workspace."""

from __future__ import annotations

import copy

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QSizePolicy, QSplitter

from core.object_scene import (
    save_object_scene,
    set_scene_view,
    sync_scene_from_shape_document,
)
from core.object_scene_membership import reconcile_scene_membership
from core.shape_document import (
    add_circle,
    add_ellipse,
    add_rectangle,
    add_square,
    add_star,
    redo as redo_shape,
    undo as undo_shape,
    write_shape_document_autosave,
)
from qt_panels.object_cad_panel import ObjectCadEditorPanel, ObjectViewport


class StableObjectViewport(ObjectViewport):
    """Keep the world origin, grid, and camera target stable during object transforms."""

    @staticmethod
    def _anchor_for_scene(_scene: dict | None) -> tuple[float, float, float]:
        return ObjectViewport.WORLD_ORIGIN

    def _scene_target(self) -> tuple[float, float, float]:
        return self._anchor_for_scene(self.scene_data)


class SingleObjectWorkspacePanel(ObjectCadEditorPanel):
    """Present visible non-overlapping shapes and isolate one object transform at a time."""

    GRID_COLUMNS = 3
    GRID_ROWS = 3
    GRID_CAPACITY = GRID_COLUMNS * GRID_ROWS
    GRID_LEFT = 70.0
    GRID_TOP = 70.0
    GRID_STEP_X = 310.0
    GRID_STEP_Y = 300.0
    DESIGN_VIEW_ZOOM = 900.0 / 1024.0

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
        self._connect_object_viewport(stable_viewport)
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

    def _activate_design_view(self) -> None:
        """Use one front orthographic canvas view without changing object authority."""
        if self.object_scene is None:
            return
        self._cancel_pending_view_state()
        current_view = self.object_scene["view"]
        design_view = {
            **current_view,
            "yaw_deg": 0.0,
            "pitch_deg": 0.0,
            "zoom": self.DESIGN_VIEW_ZOOM,
            "perspective": False,
        }
        if design_view != current_view:
            self.object_scene = set_scene_view(self.object_scene, **design_view)
        self.object_viewport.set_scene(
            self.object_scene,
            self.selected_object_id,
        )
        self._load_view_controls()

    def show_3d_view(self, *_args) -> None:
        """Enter a centred front design view; Orbit remains an explicit operation."""
        if self.object_scene is None:
            self.ensure_object_scene(switch_to_3d=False)
        if self.object_scene is not None:
            self._activate_design_view()
        super().show_3d_view(*_args)
        if self.object_scene is not None:
            self.set_status(
                "3D Design View active: front orthographic canvas centred on world origin. "
                "Objects move without perspective growth, shrinkage, skew, or camera drift; "
                "use Orbit View or Perspective deliberately when needed."
            )

    def _next_primitive_position(self) -> tuple[float, float]:
        count = len(self.document.get("objects", [])) if isinstance(self.document, dict) else 0
        if count >= self.GRID_CAPACITY:
            raise ValueError(
                "The visible 3×3 placement grid is full. Undo a shape or create another document."
            )
        column = count % self.GRID_COLUMNS
        row = count // self.GRID_COLUMNS
        return (
            self.GRID_LEFT + column * self.GRID_STEP_X,
            self.GRID_TOP + row * self.GRID_STEP_Y,
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

            if len(self.document["objects"]) >= self.GRID_CAPACITY:
                detail += " The visible placement grid is now full."
            self.set_status(detail)
        except Exception as exc:
            self.set_status(f"Could not add the {primitive_type}: {exc}")
        self.update_controls()

    @staticmethod
    def _source_ids(document: dict | None) -> set[str]:
        if not isinstance(document, dict):
            return set()
        return {
            item["object_id"]
            for item in document.get("objects", [])
            if isinstance(item, dict) and isinstance(item.get("object_id"), str)
        }

    def _restore_workspace_state(
        self,
        document: dict,
        scene: dict | None,
        selected_object_id: str | None,
    ) -> None:
        self.document = copy.deepcopy(document)
        self.object_scene = copy.deepcopy(scene) if scene is not None else None
        self.selected_object_id = selected_object_id
        self.render_document()
        self.object_viewport.set_scene(self.object_scene, self.selected_object_id)
        self._update_inspector()
        self._update_cad_controls()
        self.update_controls()

    def _apply_shape_history_change(self, change, action_label: str) -> None:
        if self.document is None:
            return

        original_document = copy.deepcopy(self.document)
        original_scene = copy.deepcopy(self.object_scene)
        original_selection = self.selected_object_id
        original_sources = self._source_ids(original_document)
        shape_written = False
        scene_written = False

        try:
            updated_document = change(original_document)
            reconciled_scene = original_scene
            added = removed = 0
            if original_scene is not None:
                reconciled_scene, added, removed = reconcile_scene_membership(
                    original_scene,
                    updated_document,
                )

            write_shape_document_autosave(self.project_session, updated_document)
            shape_written = True
            if reconciled_scene is not None and reconciled_scene != original_scene:
                save_object_scene(self.project_session, reconciled_scene)
                scene_written = True

            desired_sources = self._source_ids(updated_document)
            available_ids = {
                item["object_id"]
                for item in reconciled_scene.get("objects", [])
            } if reconciled_scene is not None else set()
            selected = original_selection if original_selection in available_ids else None
            newly_visible = desired_sources - original_sources
            if newly_visible and reconciled_scene is not None:
                selected = next(
                    (
                        item["object_id"]
                        for item in reversed(reconciled_scene["objects"])
                        if item["source_shape_id"] in newly_visible
                    ),
                    selected,
                )
            if selected is None and reconciled_scene is not None and reconciled_scene["objects"]:
                selected = reconciled_scene["objects"][-1]["object_id"]

            self._restore_workspace_state(updated_document, reconciled_scene, selected)
            membership = []
            if added:
                membership.append(f"added {added} 3D object(s)")
            if removed:
                membership.append(f"removed {removed} orphaned 3D object(s)")
            detail = ", ".join(membership) if membership else "3D membership unchanged"
            self.set_status(
                f"{action_label} applied and autosaved at revision "
                f"{updated_document['revision']}; {detail}."
            )
        except Exception as exc:
            rollback_errors = []
            if scene_written and original_scene is not None:
                try:
                    save_object_scene(self.project_session, original_scene)
                except Exception as rollback_exc:
                    rollback_errors.append(f"3D rollback failed: {rollback_exc}")
            if shape_written:
                try:
                    write_shape_document_autosave(self.project_session, original_document)
                except Exception as rollback_exc:
                    rollback_errors.append(f"2D rollback failed: {rollback_exc}")
            self._restore_workspace_state(
                original_document,
                original_scene,
                original_selection,
            )
            suffix = f" {'; '.join(rollback_errors)}" if rollback_errors else ""
            self.set_status(f"Could not apply {action_label.lower()}: {exc}.{suffix}")

    def undo_command(self, *_args) -> None:
        self._apply_shape_history_change(undo_shape, "Undo")

    def redo_command(self, *_args) -> None:
        self._apply_shape_history_change(redo_shape, "Redo")

    def select_cad_object(self, object_id) -> None:
        super().select_cad_object(object_id)
        self.object_viewport.update()
        if isinstance(object_id, str):
            item = self._selected_scene_object()
            if item is not None:
                self.set_status(
                    f"Selected one {item['primitive_type']} object. Only this object can be transformed."
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