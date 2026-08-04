#!/usr/bin/env python3
"""Install direct, durable 2D shape resizing in the final Forge Editor."""

from __future__ import annotations

import copy
import math

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QPainter, QPen, QTransform

import core.object_scene as object_scene
import core.shape_document as shape_document
import qt_editor_authoring_app as authoring_app
from qt_panels import editor_authority_guard as guard


_BASE_GUARDED_PANEL = guard.GuardedProjectAwareEditorPanel
_MIN_SHAPE_SIZE = 12.0


def _geometry(value: object, label: str) -> dict[str, float]:
    if not isinstance(value, dict):
        raise shape_document.ShapeDocumentError(
            f"{label} geometry must be an object."
        )
    return {
        "x": shape_document._require_number(value.get("x"), f"{label} x"),
        "y": shape_document._require_number(value.get("y"), f"{label} y"),
        "width": shape_document._require_number(
            value.get("width"), f"{label} width", positive=True
        ),
        "height": shape_document._require_number(
            value.get("height"), f"{label} height", positive=True
        ),
    }


def _require_minimum_resize_geometry(
    geometry: dict[str, float],
    label: str,
) -> dict[str, float]:
    if (
        geometry["width"] < _MIN_SHAPE_SIZE
        or geometry["height"] < _MIN_SHAPE_SIZE
    ):
        raise shape_document.ShapeDocumentError(
            f"{label} width and height must each be at least {_MIN_SHAPE_SIZE:g}."
        )
    return geometry


def _install_shape_resize_command_support() -> None:
    """Extend the established replay contract with one durable resize command."""
    if getattr(shape_document, "_mxztar_resize_shape_installed", False):
        return

    def replay_commands_with_resize(
        commands: object,
        history_cursor: int,
    ) -> list[dict]:
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
        snapshot: list[dict] = []
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
            elif command_type == "resize_shape":
                object_id = shape_document._require_non_empty_string(
                    payload, "object_id"
                )
                before = _geometry(payload.get("before"), "Shape resize before")
                after = _require_minimum_resize_geometry(
                    _geometry(payload.get("after"), "Shape resize after"),
                    "Shape resize after",
                )
                current = objects.get(object_id)
                if current is None:
                    raise shape_document.ShapeDocumentError(
                        "Shape resize targets an unavailable object."
                    )
                current_geometry = {
                    key: float(current[key])
                    for key in ("x", "y", "width", "height")
                }
                if current_geometry != before:
                    raise shape_document.ShapeDocumentError(
                        "Shape resize before-state does not match replayed state."
                    )
                if (
                    current["type"] in {"square", "circle"}
                    and not math.isclose(
                        after["width"], after["height"], abs_tol=1.0e-9
                    )
                ):
                    raise shape_document.ShapeDocumentError(
                        f"{current['type'].title()} resize must preserve equal sides."
                    )
                current = copy.deepcopy(current)
                current.update(after)
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

    def resize_shape(
        document: dict,
        object_id: str,
        *,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> dict:
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

        before = {
            key: float(selected[key])
            for key in ("x", "y", "width", "height")
        }
        after = _require_minimum_resize_geometry(
            {
                "x": shape_document._require_number(x, "Shape resize x"),
                "y": shape_document._require_number(y, "Shape resize y"),
                "width": shape_document._require_number(
                    width, "Shape resize width", positive=True
                ),
                "height": shape_document._require_number(
                    height, "Shape resize height", positive=True
                ),
            },
            "Shape resize",
        )
        if (
            selected["type"] in {"square", "circle"}
            and not math.isclose(
                after["width"], after["height"], abs_tol=1.0e-9
            )
        ):
            raise shape_document.ShapeDocumentError(
                f"{selected['type'].title()} resize must preserve equal sides."
            )
        if before == after:
            return current

        commands = copy.deepcopy(
            current["commands"][: current["history_cursor"]]
        )
        commands.append(
            {
                "command_id": f"command_{shape_document.uuid.uuid4().hex}",
                "type": "resize_shape",
                "created_at_utc": shape_document.utc_now_iso(),
                "payload": {
                    "object_id": object_id,
                    "before": before,
                    "after": after,
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

    shape_document.replay_commands = replay_commands_with_resize
    shape_document.resize_shape = resize_shape
    shape_document._mxztar_resize_shape_installed = True


class DirectResizeShapeCanvas(guard.PreciseShapeCanvas):
    """Add one visible bottom-right resize handle without changing body movement."""

    HANDLE_SIZE = 14.0
    MIN_SHAPE_SIZE = _MIN_SHAPE_SIZE

    def __init__(self, scene, panel):
        super().__init__(scene, panel)
        self.setToolTip(
            "Click a shape to select it. Drag its body to move it, drag the square "
            "bottom-right handle to resize it, or drag empty space to pan."
        )
        self._selected_shape_id: str | None = None
        self._resize_item = None
        self._resize_shape_id: str | None = None
        self._resize_original_geometry: dict[str, float] | None = None
        self._resize_preview_geometry: dict[str, float] | None = None
        self._resize_handle_rect = QRectF()

    def index_scene_items(self) -> None:
        super().index_scene_items()
        selected_scene_object = None
        if callable(getattr(self.panel, "_selected_scene_object", None)):
            selected_scene_object = self.panel._selected_scene_object()
        paired_source = (
            selected_scene_object.get("source_shape_id")
            if isinstance(selected_scene_object, dict)
            else None
        )
        if isinstance(paired_source, str) and paired_source in self._items_by_object_id:
            self._selected_shape_id = paired_source
        elif self._selected_shape_id not in self._items_by_object_id:
            self._selected_shape_id = None
        self.viewport().update()

    def selected_shape(self) -> dict | None:
        if self._selected_shape_id is None:
            return None
        return self._shape(self._selected_shape_id)

    def select_shape(self, object_id: str | None) -> None:
        self._selected_shape_id = (
            object_id if object_id in self._items_by_object_id else None
        )
        if self._selected_shape_id is not None:
            self.panel.select_2d_shape(self._selected_shape_id)
        self.viewport().update()

    def _selection_view_rect(self) -> QRectF:
        shape = self.selected_shape()
        if shape is None:
            return QRectF()
        top_left = QPointF(
            self.mapFromScene(QPointF(float(shape["x"]), float(shape["y"])))
        )
        bottom_right = QPointF(
            self.mapFromScene(
                QPointF(
                    float(shape["x"]) + float(shape["width"]),
                    float(shape["y"]) + float(shape["height"]),
                )
            )
        )
        return QRectF(top_left, bottom_right).normalized()

    def current_resize_handle(self) -> QRectF:
        selection = self._selection_view_rect()
        if selection.isNull() or selection.isEmpty():
            self._resize_handle_rect = QRectF()
            return QRectF()
        half = self.HANDLE_SIZE / 2.0
        corner = selection.bottomRight()
        self._resize_handle_rect = QRectF(
            corner.x() - half,
            corner.y() - half,
            self.HANDLE_SIZE,
            self.HANDLE_SIZE,
        )
        return QRectF(self._resize_handle_rect)

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        selection = self._selection_view_rect()
        if selection.isNull() or selection.isEmpty():
            self._resize_handle_rect = QRectF()
            return
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        highlight = self.palette().highlight().color()
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(highlight, 2.0))
        painter.drawRect(selection)
        handle = self.current_resize_handle()
        painter.fillRect(handle, highlight)
        painter.setPen(QPen(self.palette().base().color(), 1.0))
        painter.drawRect(handle)

    def _clear_resize_drag(self) -> None:
        self._resize_item = None
        self._resize_shape_id = None
        self._resize_original_geometry = None
        self._resize_preview_geometry = None
        self.unsetCursor()
        self.viewport().update()

    @staticmethod
    def _preview_transform(
        original: dict[str, float],
        preview: dict[str, float],
    ) -> QTransform:
        transform = QTransform()
        transform.translate(original["x"], original["y"])
        transform.scale(
            preview["width"] / original["width"],
            preview["height"] / original["height"],
        )
        transform.translate(-original["x"], -original["y"])
        return transform

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self.panel.document is not None:
            if (
                self.panel.project_session.is_writable
                and self._selected_shape_id is not None
                and self.current_resize_handle().contains(event.position())
            ):
                shape = self.selected_shape()
                item = self._items_by_object_id.get(self._selected_shape_id)
                if shape is not None and item is not None:
                    self._resize_item = item
                    self._resize_shape_id = self._selected_shape_id
                    self._resize_original_geometry = {
                        key: float(shape[key])
                        for key in ("x", "y", "width", "height")
                    }
                    self._resize_preview_geometry = copy.deepcopy(
                        self._resize_original_geometry
                    )
                    self.setCursor(Qt.CursorShape.SizeFDiagCursor)
                    event.accept()
                    return

            item = self.itemAt(event.position().toPoint())
            object_id = item.data(self.OBJECT_ID_ROLE) if item is not None else None
            if isinstance(object_id, str):
                self.select_shape(object_id)
                if self.panel.project_session.is_writable:
                    super().mousePressEvent(event)
                else:
                    event.accept()
                return
            self.select_shape(None)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if (
            self._resize_item is not None
            and self._resize_shape_id is not None
            and self._resize_original_geometry is not None
        ):
            shape = self._shape(self._resize_shape_id)
            if shape is None:
                self._resize_item.setTransform(QTransform())
                self._clear_resize_drag()
                return
            scene_point = self.mapToScene(event.position().toPoint())
            original = self._resize_original_geometry
            width = max(
                self.MIN_SHAPE_SIZE,
                scene_point.x() - original["x"],
            )
            height = max(
                self.MIN_SHAPE_SIZE,
                scene_point.y() - original["y"],
            )
            if shape["type"] in {"square", "circle"}:
                side = max(self.MIN_SHAPE_SIZE, width, height)
                width = height = side
            preview = {
                "x": original["x"],
                "y": original["y"],
                "width": width,
                "height": height,
            }
            self._resize_item.setTransform(
                self._preview_transform(original, preview)
            )
            self._resize_preview_geometry = preview
            self.viewport().update()
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self._resize_item is not None
            and self._resize_shape_id is not None
            and self._resize_original_geometry is not None
            and self._resize_preview_geometry is not None
        ):
            item = self._resize_item
            object_id = self._resize_shape_id
            original = self._resize_original_geometry
            preview = self._resize_preview_geometry
            item.setTransform(QTransform())
            self._clear_resize_drag()
            if any(
                not math.isclose(original[key], preview[key], abs_tol=1.0e-9)
                for key in ("x", "y", "width", "height")
            ):
                self.panel.commit_2d_shape_resize(
                    object_id,
                    x=preview["x"],
                    y=preview["y"],
                    width=preview["width"],
                    height=preview["height"],
                )
            event.accept()
            return
        super().mouseReleaseEvent(event)


class DirectResizeProjectAwareEditorPanel(_BASE_GUARDED_PANEL):
    """Preserve existing movement while adding direct durable 2D resizing."""

    def __init__(self, project_session):
        super().__init__(project_session)
        self.header_label.setText(
            "EDITOR; project/document shape-CAD workspace. Select a 2D shape, drag its "
            "body to move it, or drag its bottom-right handle to resize it precisely."
        )

    def _install_precise_shape_canvas(self) -> None:
        old_canvas = self.canvas
        canvas_index = self.view_stack.indexOf(old_canvas)
        self.view_stack.removeWidget(old_canvas)
        canvas = DirectResizeShapeCanvas(self.scene, self)
        canvas.setMinimumHeight(old_canvas.minimumHeight())
        self.view_stack.insertWidget(max(0, canvas_index), canvas)
        self.canvas = canvas
        old_canvas.deleteLater()
        self.render_document()

    def select_2d_shape(self, source_shape_id: str) -> None:
        if self.object_scene is None:
            return
        paired = next(
            (
                item
                for item in self.object_scene.get("objects", [])
                if item.get("source_shape_id") == source_shape_id
            ),
            None,
        )
        if paired is not None:
            self.select_cad_object(paired["object_id"])

    @staticmethod
    def _scene_after_2d_resize(
        scene: dict | None,
        source_shape_id: str,
        shape: dict,
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
        updated["position"]["x"] = float(shape["x"]) + float(shape["width"]) / 2.0
        updated["position"]["y"] = float(shape["y"]) + float(shape["height"]) / 2.0
        updated["size"]["x"] = float(shape["width"])
        updated["size"]["y"] = float(shape["height"])
        return (
            object_scene.update_scene_object(
                scene,
                paired["object_id"],
                updated,
            ),
            paired["object_id"],
        )

    def _apply_2d_resize_state(
        self,
        updated_document: dict,
        source_shape_id: str,
        action_label: str,
    ) -> bool:
        original_document = copy.deepcopy(self.document)
        original_scene = copy.deepcopy(self.object_scene)
        original_selection = self.selected_object_id
        shape_written = False
        scene_written = False

        try:
            resized_shape = self._shape_by_id(
                updated_document,
                source_shape_id,
            )
            if resized_shape is None:
                raise shape_document.ShapeDocumentError(
                    "The resized 2D shape could not be replayed."
                )
            updated_scene, paired_id = self._scene_after_2d_resize(
                original_scene,
                source_shape_id,
                resized_shape,
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

            self._restore_workspace_state(
                updated_document,
                updated_scene,
                paired_id or original_selection,
            )
            self.set_status(
                f"{action_label} committed one 2D resize command and synchronized only "
                "the paired 3D object's X/Y centre and width/height; depth, Z, rotation, "
                "appearance, camera, grid, and other objects were unchanged."
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
                    "Direct 2D resize rollback failed; explicit recovery is required."
                )
            suffix = f" {'; '.join(rollback_errors)}" if rollback_errors else ""
            self.set_status(f"Could not apply direct 2D resize: {exc}.{suffix}")
            return False

    def commit_2d_shape_resize(
        self,
        source_shape_id: str,
        *,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> bool:
        if self.document is None or not self.project_session.is_writable:
            self.set_status(
                "A writable shape document is required before resizing a 2D shape."
            )
            return False
        if self._shape_by_id(self.document, source_shape_id) is None:
            self.set_status("The selected 2D shape is unavailable.")
            return False
        updated_document = shape_document.resize_shape(
            self.document,
            source_shape_id,
            x=x,
            y=y,
            width=width,
            height=height,
        )
        return self._apply_2d_resize_state(
            updated_document,
            source_shape_id,
            "2D resize",
        )

    def undo_command(self, *_args) -> None:
        if self.document is not None and self.document.get("history_cursor", 0) > 0:
            command = self.document["commands"][
                self.document["history_cursor"] - 1
            ]
            if command.get("type") == "resize_shape":
                source_shape_id = command["payload"]["object_id"]
                updated_document = shape_document.undo(self.document)
                self._apply_2d_resize_state(
                    updated_document,
                    source_shape_id,
                    "Undo 2D resize",
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
            command = self.document["commands"][self.document["history_cursor"]]
            if command.get("type") == "resize_shape":
                source_shape_id = command["payload"]["object_id"]
                updated_document = shape_document.redo(self.document)
                self._apply_2d_resize_state(
                    updated_document,
                    source_shape_id,
                    "Redo 2D resize",
                )
                self.update_controls()
                return
        super().redo_command(*_args)


def install_direct_2d_resize() -> None:
    """Install the final Editor resize contract exactly once."""
    if getattr(install_direct_2d_resize, "_installed", False):
        return
    _install_shape_resize_command_support()
    guard.DirectResizeShapeCanvas = DirectResizeShapeCanvas
    guard.DirectResizeProjectAwareEditorPanel = DirectResizeProjectAwareEditorPanel
    guard.GuardedProjectAwareEditorPanel = DirectResizeProjectAwareEditorPanel
    authoring_app.GuardedProjectAwareEditorPanel = DirectResizeProjectAwareEditorPanel
    install_direct_2d_resize._installed = True


install_direct_2d_resize._installed = False
