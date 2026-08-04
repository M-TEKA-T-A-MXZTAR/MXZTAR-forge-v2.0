#!/usr/bin/env python3
"""Mutation guard plus precise 2D/3D direct movement for the final Editor."""

from __future__ import annotations

import copy
import math

from PySide6.QtCore import QPointF, Qt
from PySide6.QtWidgets import QGraphicsView

import core.object_scene as object_scene
import core.shape_document as shape_document
from core.positioning_guides import calculate_positioning_guides
from qt_panels.editor_authoring_panel import ProjectAwareEditorPanel
from qt_panels.positioning_guides import GuidedObjectViewport, install_positioning_guides


def _install_shape_move_command_support() -> None:
    """Extend the established replay contract with one durable 2D move command."""
    if getattr(shape_document, "_mxztar_move_shape_installed", False):
        return

    def replay_commands_with_move(commands: object, history_cursor: int) -> list[dict]:
        if not isinstance(commands, list):
            raise shape_document.ShapeDocumentError(
                "Shape document commands must be a list."
            )
        if len(commands) > shape_document.MAX_COMMANDS:
            raise shape_document.ShapeDocumentError(
                f"Shape document exceeds the {shape_document.MAX_COMMANDS}-command limit."
            )
        if not isinstance(history_cursor, int) or isinstance(history_cursor, bool):
            raise shape_document.ShapeDocumentError(
                "Shape document history cursor must be an integer."
            )
        if history_cursor < 0 or history_cursor > len(commands):
            raise shape_document.ShapeDocumentError(
                "Shape document history cursor is outside command history."
            )

        ordered_ids: list[str] = []
        objects: dict[str, dict] = {}
        snapshot: list[dict] = [] if history_cursor == 0 else []
        seen_command_ids: set[str] = set()
        seen_object_ids: set[str] = set()

        for index, command in enumerate(commands):
            if not isinstance(command, dict):
                raise shape_document.ShapeDocumentError(
                    "Each editor command must be an object."
                )
            command_id = shape_document._require_non_empty_string(
                command, "command_id"
            )
            if command_id in seen_command_ids:
                raise shape_document.ShapeDocumentError(
                    "Shape document contains a duplicate command ID."
                )
            seen_command_ids.add(command_id)
            shape_document._require_non_empty_string(command, "created_at_utc")
            payload = command.get("payload")
            if not isinstance(payload, dict):
                raise shape_document.ShapeDocumentError(
                    "Editor command payload must be an object."
                )

            command_type = command.get("type")
            if command_type in shape_document.COMMAND_TO_PRIMITIVE:
                primitive = shape_document._primitive_from_command(command)
                object_id = primitive["object_id"]
                if object_id in seen_object_ids:
                    raise shape_document.ShapeDocumentError(
                        "Shape document contains a duplicate object ID."
                    )
                seen_object_ids.add(object_id)
                ordered_ids.append(object_id)
                objects[object_id] = primitive
            elif command_type == "move_shape":
                object_id = shape_document._require_non_empty_string(
                    payload, "object_id"
                )
                before = payload.get("before")
                after = payload.get("after")
                if not isinstance(before, dict) or not isinstance(after, dict):
                    raise shape_document.ShapeDocumentError(
                        "Shape move requires before and after coordinates."
                    )
                before_x = shape_document._require_number(
                    before.get("x"), "Shape move before x"
                )
                before_y = shape_document._require_number(
                    before.get("y"), "Shape move before y"
                )
                after_x = shape_document._require_number(
                    after.get("x"), "Shape move after x"
                )
                after_y = shape_document._require_number(
                    after.get("y"), "Shape move after y"
                )
                current = objects.get(object_id)
                if current is None:
                    raise shape_document.ShapeDocumentError(
                        "Shape move targets an unavailable object."
                    )
                if current["x"] != before_x or current["y"] != before_y:
                    raise shape_document.ShapeDocumentError(
                        "Shape move before-state does not match replayed state."
                    )
                current = copy.deepcopy(current)
                current["x"] = after_x
                current["y"] = after_y
                objects[object_id] = current
            else:
                raise shape_document.ShapeDocumentError(
                    f"Unsupported editor command: {command_type!r}"
                )

            if index + 1 == history_cursor:
                snapshot = [
                    copy.deepcopy(objects[object_id]) for object_id in ordered_ids
                ]

        return snapshot

    def move_shape(document: dict, object_id: str, *, x: float, y: float) -> dict:
        current = shape_document.validate_shape_document(document)
        selected = next(
            (
                item
                for item in current["objects"]
                if item.get("object_id") == object_id
            ),
            None,
        )
        if selected is None:
            raise shape_document.ShapeDocumentError(
                "The selected 2D shape is unavailable."
            )
        after_x = shape_document._require_number(x, "Shape move x")
        after_y = shape_document._require_number(y, "Shape move y")
        before_x = float(selected["x"])
        before_y = float(selected["y"])
        if before_x == after_x and before_y == after_y:
            return current

        commands = copy.deepcopy(
            current["commands"][: current["history_cursor"]]
        )
        commands.append(
            {
                "command_id": f"command_{shape_document.uuid.uuid4().hex}",
                "type": "move_shape",
                "created_at_utc": shape_document.utc_now_iso(),
                "payload": {
                    "object_id": object_id,
                    "before": {"x": before_x, "y": before_y},
                    "after": {"x": after_x, "y": after_y},
                },
            }
        )
        if len(commands) > shape_document.MAX_COMMANDS:
            raise shape_document.ShapeDocumentError(
                f"Shape document exceeds the {shape_document.MAX_COMMANDS}-command limit."
            )
        current["commands"] = commands
        current["history_cursor"] = len(commands)
        return shape_document.validate_shape_document(
            shape_document._refresh_derived_state(
                current,
                revision_increment=True,
            )
        )

    shape_document.replay_commands = replay_commands_with_move
    shape_document.move_shape = move_shape
    shape_document._mxztar_move_shape_installed = True


_install_shape_move_command_support()


class PreciseShapeCanvas(QGraphicsView):
    """Preserve 2D click offset and commit one movement command on release."""

    OBJECT_ID_ROLE = 0

    def __init__(self, scene, panel):
        super().__init__(scene)
        self.panel = panel
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setToolTip(
            "Project-owned shape canvas. Drag a shape to move it; drag empty space to pan."
        )
        self._items_by_object_id: dict[str, object] = {}
        self._drag_item = None
        self._drag_object_id: str | None = None
        self._drag_original_xy: tuple[float, float] | None = None
        self._drag_offset = QPointF()
        self._drag_preview_xy: tuple[float, float] | None = None

    def index_scene_items(self) -> None:
        self._items_by_object_id = {}
        document = self.panel.document
        if not isinstance(document, dict):
            return
        shapes = list(reversed(document.get("objects", [])))
        items = self.scene().items(Qt.SortOrder.DescendingOrder)
        for item, shape in zip(items, shapes):
            object_id = shape.get("object_id")
            if isinstance(object_id, str):
                item.setData(self.OBJECT_ID_ROLE, object_id)
                self._items_by_object_id[object_id] = item

    def _shape(self, object_id: str) -> dict | None:
        document = self.panel.document
        if not isinstance(document, dict):
            return None
        return next(
            (
                copy.deepcopy(item)
                for item in document.get("objects", [])
                if item.get("object_id") == object_id
            ),
            None,
        )

    def _clear_shape_drag(self) -> None:
        self._drag_item = None
        self._drag_object_id = None
        self._drag_original_xy = None
        self._drag_offset = QPointF()
        self._drag_preview_xy = None
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, event) -> None:
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.panel.project_session.is_writable
            and self.panel.document is not None
        ):
            item = self.itemAt(event.position().toPoint())
            object_id = (
                item.data(self.OBJECT_ID_ROLE) if item is not None else None
            )
            if isinstance(object_id, str):
                shape = self._shape(object_id)
                if shape is not None:
                    scene_point = self.mapToScene(event.position().toPoint())
                    self._drag_item = item
                    self._drag_object_id = object_id
                    self._drag_original_xy = (
                        float(shape["x"]),
                        float(shape["y"]),
                    )
                    self._drag_offset = QPointF(
                        scene_point.x() - float(shape["x"]),
                        scene_point.y() - float(shape["y"]),
                    )
                    self._drag_preview_xy = self._drag_original_xy
                    self.setCursor(Qt.CursorShape.ClosedHandCursor)
                    event.accept()
                    return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if (
            self._drag_item is not None
            and self._drag_original_xy is not None
            and self._drag_object_id is not None
        ):
            scene_point = self.mapToScene(event.position().toPoint())
            next_x = scene_point.x() - self._drag_offset.x()
            next_y = scene_point.y() - self._drag_offset.y()
            original_x, original_y = self._drag_original_xy
            self._drag_item.setPos(next_x - original_x, next_y - original_y)
            self._drag_preview_xy = (next_x, next_y)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self._drag_item is not None
            and self._drag_original_xy is not None
            and self._drag_object_id is not None
            and self._drag_preview_xy is not None
        ):
            object_id = self._drag_object_id
            original_x, original_y = self._drag_original_xy
            next_x, next_y = self._drag_preview_xy
            self._drag_item.setPos(0.0, 0.0)
            self._clear_shape_drag()
            if not (
                math.isclose(original_x, next_x, abs_tol=1.0e-9)
                and math.isclose(original_y, next_y, abs_tol=1.0e-9)
            ):
                self.panel.commit_2d_shape_move(object_id, next_x, next_y)
            event.accept()
            return
        super().mouseReleaseEvent(event)


class PreciseGuidedObjectViewport(GuidedObjectViewport):
    """Map pointer positions through the exact camera transform onto fixed-Z XY."""

    FOCAL_LENGTH = 1100.0

    def __init__(self):
        super().__init__()
        self._precise_anchor_world: tuple[float, float] | None = None
        self._precise_plane_z: float | None = None

    def _camera_vector_to_world(
        self, vector: tuple[float, float, float]
    ) -> tuple[float, float, float]:
        view = self.scene_data["view"]
        x_camera, y_camera, z_camera = vector
        pitch = math.radians(view["pitch_deg"])
        y_yaw = y_camera * math.cos(pitch) + z_camera * math.sin(pitch)
        z_world = -y_camera * math.sin(pitch) + z_camera * math.cos(pitch)

        yaw_rotation = math.radians(-view["yaw_deg"])
        x_world = (
            x_camera * math.cos(yaw_rotation)
            + y_yaw * math.sin(yaw_rotation)
        )
        y_world = (
            -x_camera * math.sin(yaw_rotation)
            + y_yaw * math.cos(yaw_rotation)
        )
        return x_world, y_world, z_world

    def _camera_point_to_world(
        self, point: tuple[float, float, float]
    ) -> tuple[float, float, float]:
        rotated = self._camera_vector_to_world(point)
        target = self._scene_target()
        return (
            rotated[0] + target[0],
            rotated[1] + target[1],
            rotated[2] + target[2],
        )

    def _screen_to_world_on_z(
        self,
        screen: QPointF,
        world_z: float,
    ) -> tuple[float, float] | None:
        if self.scene_data is None:
            return None
        view = self.scene_data["view"]
        scale = max(
            0.02,
            view["zoom"]
            * min(max(self.width(), 1), max(self.height(), 1))
            / 900.0,
        )
        camera_x = (screen.x() - self.width() / 2.0) / scale
        camera_y = (screen.y() - self.height() / 2.0) / scale

        if view["perspective"]:
            camera_origin = (0.0, 0.0, -self.FOCAL_LENGTH)
            camera_direction = (
                camera_x,
                camera_y,
                self.FOCAL_LENGTH,
            )
        else:
            camera_origin = (
                camera_x,
                camera_y,
                -self.FOCAL_LENGTH,
            )
            camera_direction = (0.0, 0.0, 1.0)

        world_origin = self._camera_point_to_world(camera_origin)
        world_direction = self._camera_vector_to_world(camera_direction)
        if abs(world_direction[2]) < 1.0e-9:
            return None
        distance = (world_z - world_origin[2]) / world_direction[2]
        return (
            world_origin[0] + world_direction[0] * distance,
            world_origin[1] + world_direction[1] * distance,
        )

    def mousePressEvent(self, event) -> None:
        direct_move = (
            event.button() == Qt.MouseButton.LeftButton
            and self.interaction_mode == "select"
            and self._direct_resize_enabled()
            and not self._resize_handle.contains(event.position())
        )
        if direct_move:
            object_id = self._hit_object(event.position())
            if object_id is not None:
                self.selected_object_id = object_id
                self.selection_changed.emit(object_id)
                selected = self.selected_object()
                if selected is not None:
                    plane_z = float(selected["position"]["z"])
                    anchor = self._screen_to_world_on_z(
                        event.position(),
                        plane_z,
                    )
                    if anchor is not None:
                        self._drag_start = event.position()
                        self._begin_object_drag(
                            "move",
                            "precise_xy",
                            selected,
                        )
                        self._precise_anchor_world = anchor
                        self._precise_plane_z = plane_z
                        self.update()
                        return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if (
            self.scene_data is not None
            and self._drag_mode == "move"
            and self._drag_constraint == "precise_xy"
            and self._drag_original_object is not None
            and self._precise_anchor_world is not None
            and self._precise_plane_z is not None
        ):
            current = self._screen_to_world_on_z(
                event.position(),
                self._precise_plane_z,
            )
            if current is None:
                return
            updated = copy.deepcopy(self._drag_original_object)
            updated["position"]["x"] += (
                current[0] - self._precise_anchor_world[0]
            )
            updated["position"]["y"] += (
                current[1] - self._precise_anchor_world[1]
            )
            self._replace_preview(updated)

            guided, guide_state = calculate_positioning_guides(
                updated,
                self._preview_objects,
                self._scene_target(),
                tolerance=self.snap_tolerance,
                snap_enabled=self.snap_enabled,
            )
            if guided != updated:
                self._replace_preview(guided)
            self._guide_state = guide_state if self.guides_enabled else None
            self.update()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        precise_drag = (
            self._drag_mode == "move"
            and self._drag_constraint == "precise_xy"
        )
        super().mouseReleaseEvent(event)
        if precise_drag:
            self._precise_anchor_world = None
            self._precise_plane_z = None


def _install_precise_viewport(panel) -> None:
    old_viewport = panel.object_viewport
    viewport_index = panel.view_stack.indexOf(old_viewport)
    panel.view_stack.removeWidget(old_viewport)

    viewport = PreciseGuidedObjectViewport()
    viewport.setMinimumHeight(old_viewport.minimumHeight())
    viewport.guides_enabled = old_viewport.guides_enabled
    viewport.snap_enabled = old_viewport.snap_enabled
    viewport.snap_tolerance = old_viewport.snap_tolerance
    viewport.set_interaction_mode(old_viewport.interaction_mode)
    viewport.setProperty(
        "mxztar_direct_resize_enabled",
        old_viewport.property("mxztar_direct_resize_enabled"),
    )
    panel._connect_object_viewport(viewport)
    panel.view_stack.insertWidget(max(0, viewport_index), viewport)
    panel.object_viewport = viewport
    if panel.object_scene is not None:
        viewport.set_scene(panel.object_scene, panel.selected_object_id)
    old_viewport.deleteLater()


class GuardedProjectAwareEditorPanel(ProjectAwareEditorPanel):
    """Block authority changes and preserve precise direct movement."""

    def __init__(self, project_session):
        self._project_mutation_sources: set[str] = set()
        super().__init__(project_session)
        install_positioning_guides(self)
        _install_precise_viewport(self)
        self._install_precise_shape_canvas()
        self.header_label.setText(
            "EDITOR; project/document shape-CAD workspace. Drag a 2D shape or a "
            "3D object precisely while the canvas, grid, camera, and other objects remain fixed."
        )
        self.project_selector.currentIndexChanged.connect(
            lambda _index: self._update_project_controls()
        )
        self._update_project_controls()
        self._update_cad_controls()

    def _install_precise_shape_canvas(self) -> None:
        old_canvas = self.canvas
        canvas_index = self.view_stack.indexOf(old_canvas)
        self.view_stack.removeWidget(old_canvas)
        canvas = PreciseShapeCanvas(self.scene, self)
        canvas.setMinimumHeight(old_canvas.minimumHeight())
        self.view_stack.insertWidget(max(0, canvas_index), canvas)
        self.canvas = canvas
        old_canvas.deleteLater()
        self.render_document()

    def render_document(self) -> None:
        super().render_document()
        if isinstance(getattr(self, "canvas", None), PreciseShapeCanvas):
            self.canvas.index_scene_items()

    def show_3d_view(self, *_args) -> None:
        """Enter 3D in direct object-manipulation mode, never stale Orbit View mode."""
        self.set_interaction_mode("select")
        super().show_3d_view(*_args)

    @staticmethod
    def _shape_by_id(document: dict, object_id: str) -> dict | None:
        return next(
            (
                copy.deepcopy(item)
                for item in document.get("objects", [])
                if item.get("object_id") == object_id
            ),
            None,
        )

    @staticmethod
    def _scene_after_2d_delta(
        scene: dict | None,
        source_shape_id: str,
        delta_x: float,
        delta_y: float,
    ) -> tuple[dict | None, str | None]:
        if scene is None:
            return None, None
        paired = next(
            (
                copy.deepcopy(item)
                for item in scene.get("objects", [])
                if item.get("source_shape_id") == source_shape_id
            ),
            None,
        )
        if paired is None:
            raise object_scene.ObjectSceneError(
                "The paired 3D object is unavailable for this 2D shape."
            )
        updated = copy.deepcopy(paired)
        updated["position"]["x"] += delta_x
        updated["position"]["y"] += delta_y
        return (
            object_scene.update_scene_object(
                scene,
                paired["object_id"],
                updated,
            ),
            paired["object_id"],
        )

    def _apply_2d_move_state(
        self,
        updated_document: dict,
        source_shape_id: str,
        delta_x: float,
        delta_y: float,
        action_label: str,
    ) -> bool:
        original_document = copy.deepcopy(self.document)
        original_scene = copy.deepcopy(self.object_scene)
        original_selection = self.selected_object_id
        shape_written = False
        scene_written = False

        try:
            updated_scene, paired_id = self._scene_after_2d_delta(
                original_scene,
                source_shape_id,
                delta_x,
                delta_y,
            )
            shape_document.write_shape_document_autosave(
                self.project_session,
                updated_document,
            )
            shape_written = True
            if updated_scene is not None and updated_scene != original_scene:
                object_scene.save_object_scene(
                    self.project_session,
                    updated_scene,
                )
                scene_written = True

            selected = paired_id or original_selection
            self._restore_workspace_state(
                updated_document,
                updated_scene,
                selected,
            )
            self.set_status(
                f"{action_label} committed one 2D move command and moved only the paired "
                "3D object's X/Y; depth, size, rotation, appearance, camera, and grid were unchanged."
            )
            return True
        except Exception as exc:
            rollback_errors: list[str] = []
            if scene_written and original_scene is not None:
                try:
                    object_scene.save_object_scene(
                        self.project_session,
                        original_scene,
                    )
                except Exception as rollback_exc:
                    rollback_errors.append(
                        f"3D rollback failed: {rollback_exc}"
                    )
            if shape_written and original_document is not None:
                try:
                    shape_document.write_shape_document_autosave(
                        self.project_session,
                        original_document,
                    )
                except Exception as rollback_exc:
                    rollback_errors.append(
                        f"2D rollback failed: {rollback_exc}"
                    )
            self._restore_workspace_state(
                original_document,
                original_scene,
                original_selection,
            )
            if rollback_errors:
                self.project_session.revoke_writable_authority(
                    "Precise movement rollback failed; explicit recovery is required."
                )
            suffix = (
                f" {'; '.join(rollback_errors)}"
                if rollback_errors
                else ""
            )
            self.set_status(
                f"Could not apply precise movement: {exc}.{suffix}"
            )
            return False

    def commit_2d_shape_move(
        self,
        source_shape_id: str,
        x: float,
        y: float,
    ) -> bool:
        if (
            self.document is None
            or not self.project_session.is_writable
        ):
            self.set_status(
                "A writable shape document is required before moving a 2D shape."
            )
            return False
        before = self._shape_by_id(self.document, source_shape_id)
        if before is None:
            self.set_status("The selected 2D shape is unavailable.")
            return False
        updated_document = shape_document.move_shape(
            self.document,
            source_shape_id,
            x=x,
            y=y,
        )
        after = self._shape_by_id(updated_document, source_shape_id)
        if after is None:
            self.set_status("The moved 2D shape could not be replayed.")
            return False
        return self._apply_2d_move_state(
            updated_document,
            source_shape_id,
            float(after["x"]) - float(before["x"]),
            float(after["y"]) - float(before["y"]),
            "2D drag",
        )

    def undo_command(self, *_args) -> None:
        if (
            self.document is not None
            and self.document.get("history_cursor", 0) > 0
        ):
            command = self.document["commands"][
                self.document["history_cursor"] - 1
            ]
            if command.get("type") == "move_shape":
                source_shape_id = command["payload"]["object_id"]
                before = self._shape_by_id(
                    self.document,
                    source_shape_id,
                )
                updated_document = shape_document.undo(self.document)
                after = self._shape_by_id(
                    updated_document,
                    source_shape_id,
                )
                if before is not None and after is not None:
                    self._apply_2d_move_state(
                        updated_document,
                        source_shape_id,
                        float(after["x"]) - float(before["x"]),
                        float(after["y"]) - float(before["y"]),
                        "Undo 2D move",
                    )
                    self.update_controls()
                    return
        super().undo_command(*_args)

    def redo_command(self, *_args) -> None:
        if (
            self.document is not None
            and self.document.get("history_cursor", 0)
            < len(self.document.get("commands", []))
        ):
            command = self.document["commands"][
                self.document["history_cursor"]
            ]
            if command.get("type") == "move_shape":
                source_shape_id = command["payload"]["object_id"]
                before = self._shape_by_id(
                    self.document,
                    source_shape_id,
                )
                updated_document = shape_document.redo(self.document)
                after = self._shape_by_id(
                    updated_document,
                    source_shape_id,
                )
                if before is not None and after is not None:
                    self._apply_2d_move_state(
                        updated_document,
                        source_shape_id,
                        float(after["x"]) - float(before["x"]),
                        float(after["y"]) - float(before["y"]),
                        "Redo 2D move",
                    )
                    self.update_controls()
                    return
        super().redo_command(*_args)

    def _authority_unlocked(self) -> bool:
        return not self._project_mutation_sources

    def _update_project_controls(self) -> None:
        if not hasattr(self, "project_selector"):
            return
        unlocked = self._authority_unlocked()
        selected = self.project_selector.currentData()
        current = (
            str(self.project_session.project_dir)
            if self.project_session.project_dir
            else None
        )
        self.switch_project_button.setEnabled(
            bool(unlocked and selected and selected != current)
        )
        self.delete_project_button.setEnabled(bool(unlocked and selected))
        self.new_project_document_button.setEnabled(unlocked)
        self.refresh_projects_button.setEnabled(unlocked)
        self.project_selector.setEnabled(
            unlocked and self.project_selector.count() > 0
        )

    def _update_delete_controls(self) -> None:
        if not hasattr(self, "delete_selected_action"):
            return
        enabled = bool(
            self._authority_unlocked()
            and self.project_session.is_writable
            and self.document is not None
            and self._selected_source_shape_id() is not None
        )
        self.delete_selected_action.setEnabled(enabled)
        self.delete_selected_button.setEnabled(enabled)

    def set_project_mutation_active(self, active: bool, source: str) -> None:
        if active:
            self._project_mutation_sources.add(source)
        else:
            self._project_mutation_sources.discard(source)
        self._update_project_controls()
        self._update_delete_controls()
        if active:
            self.set_status(
                f"{source.capitalize()} is active; project switching and deletion are paused."
            )

    def switch_selected_project(self, *_args):
        if not self._authority_unlocked():
            self.set_status(
                "Finish active project work before switching projects."
            )
            return None
        return super().switch_selected_project(*_args)

    def delete_selected_project(self, *, confirm: bool = True) -> bool:
        if not self._authority_unlocked():
            self.set_status(
                "Finish active project work before deleting a project."
            )
            return False
        return super().delete_selected_project(confirm=confirm)

    delete_selected_project._mxztar_selection_confirmation = True

    def create_fresh_project_and_document(self, *_args):
        if not self._authority_unlocked():
            self.set_status(
                "Finish active project work before creating a fresh project."
            )
            return None
        return super().create_fresh_project_and_document(*_args)

    def delete_selected_shape_object(
        self,
        *,
        confirm: bool = True,
    ) -> bool:
        if not self._authority_unlocked():
            self.set_status(
                "Finish active project work before deleting a shape/object."
            )
            return False
        return super().delete_selected_shape_object(confirm=confirm)
