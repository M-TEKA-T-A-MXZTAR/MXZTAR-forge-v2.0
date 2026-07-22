#!/usr/bin/env python3
"""Integrated shape/object CAD editor with a CPU-safe 3D viewport."""

from __future__ import annotations

import copy
import math

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import (
    QAction,
    QActionGroup,
    QBrush,
    QColor,
    QPainter,
    QPalette,
    QPen,
    QPolygonF,
)
from PySide6.QtWidgets import (
    QColorDialog,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QLabel,
    QMenu,
    QPushButton,
    QStackedWidget,
    QWidget,
)

from core.object_scene import (
    can_redo_scene,
    can_undo_scene,
    load_or_create_object_scene,
    redo_scene,
    save_object_scene,
    set_scene_view,
    sync_scene_from_shape_document,
    undo_scene,
    update_scene_object,
)
from qt_panels.editor_panel import EditorPanel


class ObjectViewport(QWidget):
    """Small CPU-rendered 3D viewport for project-owned extruded shape objects."""

    selection_changed = Signal(object)
    object_committed = Signal(str, object)
    view_committed = Signal(object)
    status_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.scene_data: dict | None = None
        self.selected_object_id: str | None = None
        self._preview_objects: list[dict] = []
        self._projected_faces: list[tuple[float, str, QPolygonF]] = []
        self._resize_handle = QRectF()
        self._drag_mode: str | None = None
        self._drag_start = QPointF()
        self._drag_original_object: dict | None = None
        self._drag_original_view: dict | None = None
        self.setMinimumHeight(360)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setToolTip(
            "3D object view: click an object to select, drag it to move, drag the square "
            "handle to resize, drag empty space to orbit, and use the wheel to zoom."
        )

    def set_scene(self, scene: dict | None, selected_object_id: str | None = None) -> None:
        self.scene_data = copy.deepcopy(scene) if scene is not None else None
        self._preview_objects = (
            copy.deepcopy(self.scene_data.get("objects", []))
            if self.scene_data is not None
            else []
        )
        available = {item["object_id"] for item in self._preview_objects}
        if selected_object_id in available:
            self.selected_object_id = selected_object_id
        elif self.selected_object_id not in available:
            self.selected_object_id = (
                self._preview_objects[0]["object_id"] if self._preview_objects else None
            )
        self.update()

    def selected_object(self) -> dict | None:
        return next(
            (
                copy.deepcopy(item)
                for item in self._preview_objects
                if item["object_id"] == self.selected_object_id
            ),
            None,
        )

    @staticmethod
    def _rotate_point(
        point: tuple[float, float, float], rotation: dict
    ) -> tuple[float, float, float]:
        x, y, z = point
        rx = math.radians(rotation["x"])
        ry = math.radians(rotation["y"])
        rz = math.radians(rotation["z"])

        cosine, sine = math.cos(rx), math.sin(rx)
        y, z = y * cosine - z * sine, y * sine + z * cosine

        cosine, sine = math.cos(ry), math.sin(ry)
        x, z = x * cosine + z * sine, -x * sine + z * cosine

        cosine, sine = math.cos(rz), math.sin(rz)
        x, y = x * cosine - y * sine, x * sine + y * cosine
        return x, y, z

    @staticmethod
    def _base_polygon(item: dict) -> list[tuple[float, float]]:
        width = item["size"]["x"]
        height = item["size"]["y"]
        primitive = item["primitive_type"]
        if primitive in {"rectangle", "square"}:
            return [
                (-width / 2.0, -height / 2.0),
                (width / 2.0, -height / 2.0),
                (width / 2.0, height / 2.0),
                (-width / 2.0, height / 2.0),
            ]
        if primitive in {"circle", "ellipse"}:
            return [
                (
                    math.cos(index * math.tau / 24.0) * width / 2.0,
                    math.sin(index * math.tau / 24.0) * height / 2.0,
                )
                for index in range(24)
            ]
        if primitive == "star":
            points = int(item.get("primitive_parameters", {}).get("points", 5))
            inner_ratio = float(
                item.get("primitive_parameters", {}).get("inner_ratio", 0.45)
            )
            result = []
            for index in range(points * 2):
                angle = -math.pi / 2.0 + index * math.pi / points
                ratio = 1.0 if index % 2 == 0 else inner_ratio
                result.append(
                    (
                        math.cos(angle) * width / 2.0 * ratio,
                        math.sin(angle) * height / 2.0 * ratio,
                    )
                )
            return result
        return []

    def _object_faces(self, item: dict) -> list[list[tuple[float, float, float]]]:
        polygon = self._base_polygon(item)
        depth = item["size"]["z"]
        lower = [(x, y, -depth / 2.0) for x, y in polygon]
        upper = [(x, y, depth / 2.0) for x, y in polygon]
        faces = [list(reversed(lower)), upper]
        for index in range(len(polygon)):
            next_index = (index + 1) % len(polygon)
            faces.append(
                [
                    lower[index],
                    lower[next_index],
                    upper[next_index],
                    upper[index],
                ]
            )
        position = item["position"]
        transformed = []
        for face in faces:
            points = []
            for point in face:
                x, y, z = self._rotate_point(point, item["rotation_deg"])
                points.append(
                    (
                        x + position["x"],
                        y + position["y"],
                        z + position["z"],
                    )
                )
            transformed.append(points)
        return transformed

    def _scene_target(self) -> tuple[float, float, float]:
        if not self._preview_objects:
            return 512.0, 512.0, 0.0
        count = len(self._preview_objects)
        return (
            sum(item["position"]["x"] for item in self._preview_objects) / count,
            sum(item["position"]["y"] for item in self._preview_objects) / count,
            sum(item["position"]["z"] for item in self._preview_objects) / count,
        )

    def _project(
        self,
        point: tuple[float, float, float],
        target: tuple[float, float, float],
    ) -> tuple[QPointF, float, float]:
        view = self.scene_data["view"]
        x = point[0] - target[0]
        y = point[1] - target[1]
        z = point[2] - target[2]

        yaw = math.radians(-view["yaw_deg"])
        x, y = (
            x * math.cos(yaw) - y * math.sin(yaw),
            x * math.sin(yaw) + y * math.cos(yaw),
        )
        pitch = math.radians(view["pitch_deg"])
        y, z = (
            y * math.cos(pitch) - z * math.sin(pitch),
            y * math.sin(pitch) + z * math.cos(pitch),
        )

        base_scale = min(max(self.width(), 1), max(self.height(), 1)) / 900.0
        scale = max(0.02, view["zoom"] * base_scale)
        perspective_factor = 1.0
        if view["perspective"]:
            focal = 1100.0
            perspective_factor = focal / max(250.0, focal + z)
        screen = QPointF(
            self.width() / 2.0 + x * scale * perspective_factor,
            self.height() / 2.0 + y * scale * perspective_factor,
        )
        return screen, z, scale

    def _draw_grid(self, painter: QPainter, target: tuple[float, float, float]) -> None:
        if not self.scene_data["view"]["grid_visible"]:
            return
        pen = QPen(self.palette().color(QPalette.ColorRole.Mid))
        pen.setStyle(Qt.PenStyle.DotLine)
        pen.setWidthF(1.0)
        painter.setPen(pen)
        extent = 1200
        step = 100
        for value in range(-extent, extent + step, step):
            first, _depth, _scale = self._project(
                (target[0] - extent, target[1] + value, 0.0),
                target,
            )
            second, _depth, _scale = self._project(
                (target[0] + extent, target[1] + value, 0.0),
                target,
            )
            painter.drawLine(first, second)
            first, _depth, _scale = self._project(
                (target[0] + value, target[1] - extent, 0.0),
                target,
            )
            second, _depth, _scale = self._project(
                (target[0] + value, target[1] + extent, 0.0),
                target,
            )
            painter.drawLine(first, second)

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.fillRect(self.rect(), self.palette().color(QPalette.ColorRole.Base))
        self._projected_faces = []
        self._resize_handle = QRectF()
        if self.scene_data is None:
            painter.setPen(self.palette().color(QPalette.ColorRole.Text))
            painter.drawText(
                self.rect(),
                Qt.AlignmentFlag.AlignCenter,
                "Create or open a shape document to begin the 3D object scene.",
            )
            return

        target = self._scene_target()
        self._draw_grid(painter, target)
        faces_to_draw: list[tuple[float, dict, QPolygonF, int]] = []
        selected_points: list[QPointF] = []

        for item in self._preview_objects:
            for face_index, face in enumerate(self._object_faces(item)):
                projected = []
                depths = []
                for point in face:
                    screen, depth, _scale = self._project(point, target)
                    projected.append(screen)
                    depths.append(depth)
                    if item["object_id"] == self.selected_object_id:
                        selected_points.append(screen)
                polygon = QPolygonF(projected)
                average_depth = sum(depths) / max(1, len(depths))
                faces_to_draw.append((average_depth, item, polygon, face_index))

        faces_to_draw.sort(key=lambda entry: entry[0], reverse=True)
        edges_visible = self.scene_data["view"]["edges_visible"]
        for depth, item, polygon, face_index in faces_to_draw:
            color = QColor(item["appearance"]["color"])
            if not color.isValid():
                color = self.palette().color(QPalette.ColorRole.Highlight)
            shade = (
                118
                if face_index == 1
                else 88
                if face_index == 0
                else 98 + (face_index % 3) * 6
            )
            color = color.lighter(shade)
            color.setAlpha(round(item["appearance"]["opacity"] * 220))
            painter.setBrush(QBrush(color))
            if edges_visible:
                edge = self.palette().color(QPalette.ColorRole.Text)
                edge.setAlpha(175)
                painter.setPen(QPen(edge, 1.0))
            else:
                painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPolygon(polygon)
            self._projected_faces.append((depth, item["object_id"], polygon))

        if selected_points:
            bounds = QPolygonF(selected_points).boundingRect()
            highlight = self.palette().color(QPalette.ColorRole.Highlight)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(highlight, 2.0, Qt.PenStyle.DashLine))
            painter.drawRect(bounds)
            self._resize_handle = QRectF(
                bounds.right() - 6.0,
                bounds.bottom() - 6.0,
                12.0,
                12.0,
            )
            painter.fillRect(self._resize_handle, highlight)

        painter.setPen(self.palette().color(QPalette.ColorRole.Text))
        painter.drawText(
            QRectF(10.0, 8.0, self.width() - 20.0, 24.0),
            Qt.AlignmentFlag.AlignLeft,
            "3D: drag object to move • drag square handle to resize • drag empty space to orbit",
        )

    def _hit_object(self, point: QPointF) -> str | None:
        for _depth, object_id, polygon in reversed(self._projected_faces):
            if polygon.containsPoint(point, Qt.FillRule.OddEvenFill):
                return object_id
        return None

    def _replace_preview(self, updated: dict) -> None:
        self._preview_objects = [
            copy.deepcopy(updated) if item["object_id"] == updated["object_id"] else item
            for item in self._preview_objects
        ]
        self.update()

    def mousePressEvent(self, event) -> None:
        if self.scene_data is None:
            return
        self._drag_start = event.position()
        self._drag_original_view = copy.deepcopy(self.scene_data["view"])
        selected = self.selected_object()
        if (
            event.button() == Qt.MouseButton.LeftButton
            and selected is not None
            and self._resize_handle.contains(event.position())
        ):
            self._drag_mode = "resize"
            self._drag_original_object = selected
            return

        object_id = self._hit_object(event.position())
        if event.button() == Qt.MouseButton.LeftButton and object_id is not None:
            self.selected_object_id = object_id
            self.selection_changed.emit(object_id)
            self._drag_mode = "move"
            self._drag_original_object = self.selected_object()
            self.update()
            return

        if event.button() in {
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.MiddleButton,
            Qt.MouseButton.RightButton,
        }:
            self._drag_mode = "orbit"
            if event.button() == Qt.MouseButton.LeftButton:
                self.selected_object_id = None
                self.selection_changed.emit(None)
                self.update()

    def mouseMoveEvent(self, event) -> None:
        if self.scene_data is None or self._drag_mode is None:
            return
        delta = event.position() - self._drag_start
        if self._drag_mode == "orbit" and self._drag_original_view is not None:
            view = copy.deepcopy(self._drag_original_view)
            view["yaw_deg"] = view["yaw_deg"] + delta.x() * 0.45
            view["pitch_deg"] = max(
                -89.0,
                min(89.0, view["pitch_deg"] + delta.y() * 0.35),
            )
            self.scene_data["view"] = view
            self.update()
            return
        if self._drag_original_object is None:
            return

        updated = copy.deepcopy(self._drag_original_object)
        view = self.scene_data["view"]
        scale = max(
            0.02,
            view["zoom"]
            * min(max(self.width(), 1), max(self.height(), 1))
            / 900.0,
        )
        if self._drag_mode == "move":
            yaw = math.radians(view["yaw_deg"])
            dx = delta.x() / scale
            dy = delta.y() / scale
            updated["position"]["x"] += dx * math.cos(yaw) + dy * math.sin(yaw)
            updated["position"]["y"] += -dx * math.sin(yaw) + dy * math.cos(yaw)
        elif self._drag_mode == "resize":
            updated["size"]["x"] = max(
                10.0,
                self._drag_original_object["size"]["x"] + delta.x() / scale,
            )
            updated["size"]["y"] = max(
                10.0,
                self._drag_original_object["size"]["y"] + delta.y() / scale,
            )
        self._replace_preview(updated)

    def mouseReleaseEvent(self, _event) -> None:
        if self.scene_data is None:
            return
        if self._drag_mode in {"move", "resize"} and self._drag_original_object is not None:
            updated = self.selected_object()
            if updated is not None and updated != self._drag_original_object:
                self.object_committed.emit(updated["object_id"], updated)
        elif self._drag_mode == "orbit" and self._drag_original_view is not None:
            if self.scene_data["view"] != self._drag_original_view:
                self.view_committed.emit(copy.deepcopy(self.scene_data["view"]))
        self._drag_mode = None
        self._drag_original_object = None
        self._drag_original_view = None

    def wheelEvent(self, event) -> None:
        if self.scene_data is None:
            return
        factor = 1.12 if event.angleDelta().y() > 0 else 1.0 / 1.12
        view = copy.deepcopy(self.scene_data["view"])
        view["zoom"] = max(0.05, min(20.0, view["zoom"] * factor))
        self.scene_data["view"] = view
        self.view_committed.emit(copy.deepcopy(view))
        self.update()


class ObjectCadEditorPanel(EditorPanel):
    """Extend the native shape editor into a direct-manipulation object CAD workspace."""

    def __init__(self, project_session):
        super().__init__(project_session)
        self.object_scene: dict | None = None
        self.selected_object_id: str | None = None
        self._updating_inspector = False
        self._loading_scene_controls = False

        self.header_label.setText(
            "EDITOR; shape/object CAD workspace. Create reusable shapes, construct real 3D "
            "objects, then move, resize, rotate, style, inspect, and save them locally."
        )

        self.object_button = self._make_menu_button("Object")
        self.object_menu = QMenu(self.object_button)
        self.sync_3d_action = QAction("Sync Shapes to 3D", self.object_menu)
        self.object_undo_action = QAction("Undo Object Change", self.object_menu)
        self.object_redo_action = QAction("Redo Object Change", self.object_menu)
        self.reset_object_action = QAction("Reset Selected Object", self.object_menu)
        self.color_object_action = QAction("Change Selected Color…", self.object_menu)
        self.sync_3d_action.triggered.connect(self.sync_shapes_to_3d)
        self.object_undo_action.triggered.connect(self.undo_object_change)
        self.object_redo_action.triggered.connect(self.redo_object_change)
        self.reset_object_action.triggered.connect(self.reset_selected_object)
        self.color_object_action.triggered.connect(self.choose_selected_color)
        self.object_menu.addActions(
            [
                self.sync_3d_action,
                self.object_undo_action,
                self.object_redo_action,
                self.reset_object_action,
                self.color_object_action,
            ]
        )
        self.object_button.setMenu(self.object_menu)

        self.view_button = self._make_menu_button("View")
        self.view_menu = QMenu(self.view_button)
        self.view_group = QActionGroup(self.view_menu)
        self.view_group.setExclusive(True)
        self.view_2d_action = QAction("2D Shape View", self.view_group)
        self.view_3d_action = QAction("3D Object View", self.view_group)
        self.view_group.addAction(self.view_2d_action)
        self.view_group.addAction(self.view_3d_action)
        self.view_2d_action.setCheckable(True)
        self.view_3d_action.setCheckable(True)
        self.view_2d_action.setChecked(True)
        self.view_2d_action.triggered.connect(self.show_2d_view)
        self.view_3d_action.triggered.connect(self.show_3d_view)
        self.perspective_action = QAction("Perspective", self.view_menu)
        self.grid_action = QAction("Grid", self.view_menu)
        self.lines_action = QAction("Lines", self.view_menu)
        for action in (self.perspective_action, self.grid_action, self.lines_action):
            action.setCheckable(True)
            action.triggered.connect(self.commit_view_options)
        self.view_menu.addActions([self.view_2d_action, self.view_3d_action])
        self.view_menu.addSeparator()
        self.view_menu.addActions(
            [self.perspective_action, self.grid_action, self.lines_action]
        )
        self.view_button.setMenu(self.view_menu)

        self.menu_row.insertWidget(3, self.object_button)
        self.menu_row.insertWidget(4, self.view_button)

        self.object_viewport = ObjectViewport()
        self.object_viewport.selection_changed.connect(self.select_cad_object)
        self.object_viewport.object_committed.connect(self.commit_viewport_object)
        self.object_viewport.view_committed.connect(self.commit_view_state)
        self.object_viewport.status_changed.connect(self.set_status)

        layout = self.layout()
        layout.removeWidget(self.canvas)
        self.view_stack = QStackedWidget()
        self.view_stack.addWidget(self.canvas)
        self.view_stack.addWidget(self.object_viewport)
        layout.insertWidget(3, self.view_stack, 1)

        self.inspector = QFrame()
        self.inspector.setFrameShape(QFrame.Shape.StyledPanel)
        inspector_layout = QGridLayout()
        inspector_layout.setContentsMargins(8, 5, 8, 5)
        inspector_layout.setHorizontalSpacing(7)
        inspector_layout.setVerticalSpacing(4)
        self.inspector_title = QLabel("Object Inspector — no object selected")
        self.inspector_title.setStyleSheet("font-weight: 700;")
        inspector_layout.addWidget(self.inspector_title, 0, 0, 1, 12)

        self.position_spins = self._add_vector_controls(
            inspector_layout,
            row=1,
            start_column=0,
            label="Position",
            minimum=-100000.0,
            maximum=100000.0,
        )
        self.size_spins = self._add_vector_controls(
            inspector_layout,
            row=2,
            start_column=0,
            label="Size",
            minimum=1.0,
            maximum=100000.0,
        )
        self.rotation_spins = self._add_vector_controls(
            inspector_layout,
            row=1,
            start_column=6,
            label="Rotation",
            minimum=-3600.0,
            maximum=3600.0,
        )
        opacity_label = QLabel("Opacity")
        self.opacity_spin = QDoubleSpinBox()
        self.opacity_spin.setRange(0.0, 1.0)
        self.opacity_spin.setSingleStep(0.05)
        self.opacity_spin.setDecimals(2)
        self.opacity_spin.editingFinished.connect(self.commit_inspector)
        self.color_button = QPushButton("Color…")
        self.color_button.clicked.connect(self.choose_selected_color)
        inspector_layout.addWidget(opacity_label, 2, 6)
        inspector_layout.addWidget(self.opacity_spin, 2, 7)
        inspector_layout.addWidget(self.color_button, 2, 8)
        inspector_layout.setColumnStretch(11, 1)
        self.inspector.setLayout(inspector_layout)
        layout.insertWidget(3, self.inspector)

        self._update_cad_controls()

    def _add_vector_controls(
        self,
        layout: QGridLayout,
        *,
        row: int,
        start_column: int,
        label: str,
        minimum: float,
        maximum: float,
    ) -> dict[str, QDoubleSpinBox]:
        layout.addWidget(QLabel(label), row, start_column)
        controls = {}
        for offset, axis in enumerate(("x", "y", "z"), start=1):
            spin = QDoubleSpinBox()
            spin.setRange(minimum, maximum)
            spin.setDecimals(1)
            spin.setSingleStep(5.0)
            spin.setPrefix(axis.upper() + " ")
            spin.editingFinished.connect(self.commit_inspector)
            layout.addWidget(spin, row, start_column + offset)
            controls[axis] = spin
        return controls

    def open_selected_document(self, *_args) -> None:
        super().open_selected_document(*_args)
        document_status = self.status_label.text()
        if self.document is None:
            self.clear_object_scene()
            return
        self.ensure_object_scene()
        if "Recovered a newer autosave" in document_status:
            self.set_status(document_status)

    def load_project_build(self, *_args) -> None:
        super().load_project_build(*_args)
        if self.document is None:
            self.clear_object_scene()

    def clear_object_scene(self) -> None:
        self.object_scene = None
        self.selected_object_id = None
        if hasattr(self, "object_viewport"):
            self.object_viewport.set_scene(None)
            self.view_stack.setCurrentWidget(self.canvas)
            self.view_2d_action.setChecked(True)
            self._update_inspector()
            self._update_cad_controls()

    def ensure_object_scene(self, *, switch_to_3d: bool | None = None) -> None:
        if self.document is None or not hasattr(self, "object_viewport"):
            return
        try:
            scene, created, added = load_or_create_object_scene(
                self.project_session,
                self.document,
            )
            self.object_scene = scene
            available = {item["object_id"] for item in scene["objects"]}
            if self.selected_object_id not in available:
                self.selected_object_id = (
                    scene["objects"][0]["object_id"] if scene["objects"] else None
                )
            self.object_viewport.set_scene(scene, self.selected_object_id)
            self._load_view_controls()
            self._update_inspector()
            self._update_cad_controls()
            should_switch = (
                bool(scene["objects"]) if switch_to_3d is None else switch_to_3d
            )
            if should_switch:
                self.show_3d_view()
            detail = (
                f"Created 3D object scene with {len(scene['objects'])} object(s)."
                if created
                else f"Loaded 3D object scene with {len(scene['objects'])} object(s)."
            )
            if added and not created:
                detail += f" Synchronized {added} new shape(s)."
            self.set_status(detail)
        except Exception as exc:
            self.object_scene = None
            self.object_viewport.set_scene(None)
            self._update_inspector()
            self._update_cad_controls()
            self.set_status(f"Could not load the 3D object scene: {exc}")

    def sync_shapes_to_3d(self, *_args) -> None:
        if self.document is None:
            self.set_status(
                "Create or open a shape document before synchronizing 3D objects."
            )
            return
        if self.object_scene is None:
            self.ensure_object_scene(switch_to_3d=True)
            return
        try:
            synchronized, added = sync_scene_from_shape_document(
                self.object_scene,
                self.document,
            )
            if added:
                save_object_scene(self.project_session, synchronized)
                self.object_scene = synchronized
            self.object_viewport.set_scene(self.object_scene, self.selected_object_id)
            self.show_3d_view()
            self._update_cad_controls()
            self.set_status(
                f"Synchronized {added} new shape(s) into the 3D object scene."
                if added
                else "The 3D object scene already contains every visible shape."
            )
        except Exception as exc:
            self.set_status(f"Could not synchronize shapes into 3D: {exc}")

    def show_2d_view(self, *_args) -> None:
        self.view_stack.setCurrentWidget(self.canvas)
        self.view_2d_action.setChecked(True)
        self.set_status("2D shape view active.")

    def show_3d_view(self, *_args) -> None:
        if self.object_scene is None:
            self.ensure_object_scene(switch_to_3d=False)
        if self.object_scene is None:
            self.view_2d_action.setChecked(True)
            return
        self.view_stack.setCurrentWidget(self.object_viewport)
        self.view_3d_action.setChecked(True)
        self.object_viewport.setFocus()
        self.set_status(
            "3D object view active. Drag objects to move, drag the square handle to resize, "
            "or drag empty space to orbit."
        )

    def _load_view_controls(self) -> None:
        if self.object_scene is None:
            return
        self._loading_scene_controls = True
        try:
            view = self.object_scene["view"]
            self.perspective_action.setChecked(view["perspective"])
            self.grid_action.setChecked(view["grid_visible"])
            self.lines_action.setChecked(view["edges_visible"])
        finally:
            self._loading_scene_controls = False

    def commit_view_options(self, *_args) -> None:
        if self._loading_scene_controls or self.object_scene is None:
            return
        self.commit_view_state(
            {
                **self.object_scene["view"],
                "perspective": self.perspective_action.isChecked(),
                "grid_visible": self.grid_action.isChecked(),
                "edges_visible": self.lines_action.isChecked(),
            }
        )

    def commit_view_state(self, view: dict) -> None:
        if self.object_scene is None:
            return
        try:
            self.object_scene = set_scene_view(self.object_scene, **view)
            save_object_scene(self.project_session, self.object_scene)
            self.object_viewport.set_scene(self.object_scene, self.selected_object_id)
            self._load_view_controls()
            self.set_status("Saved the 3D perspective, grid, lines, and camera view.")
        except Exception as exc:
            self.object_viewport.set_scene(self.object_scene, self.selected_object_id)
            self._load_view_controls()
            self.set_status(f"Could not save the 3D view: {exc}")

    def select_cad_object(self, object_id) -> None:
        self.selected_object_id = object_id if isinstance(object_id, str) else None
        self.object_viewport.selected_object_id = self.selected_object_id
        self._update_inspector()
        self._update_cad_controls()

    def _selected_scene_object(self) -> dict | None:
        if self.object_scene is None or self.selected_object_id is None:
            return None
        return next(
            (
                copy.deepcopy(item)
                for item in self.object_scene["objects"]
                if item["object_id"] == self.selected_object_id
            ),
            None,
        )

    def _update_inspector(self) -> None:
        if not hasattr(self, "inspector_title"):
            return
        item = self._selected_scene_object()
        self._updating_inspector = True
        try:
            enabled = item is not None and self.project_session.is_writable
            self.inspector.setEnabled(enabled)
            if item is None:
                self.inspector_title.setText("Object Inspector — no object selected")
                return
            self.inspector_title.setText(
                f"Object Inspector — {item['primitive_type'].title()} — {item['object_id']}"
            )
            for axis, spin in self.position_spins.items():
                spin.setValue(item["position"][axis])
            for axis, spin in self.size_spins.items():
                spin.setValue(item["size"][axis])
            for axis, spin in self.rotation_spins.items():
                spin.setValue(item["rotation_deg"][axis])
            self.opacity_spin.setValue(item["appearance"]["opacity"])
        finally:
            self._updating_inspector = False

    def commit_inspector(self) -> None:
        if self._updating_inspector:
            return
        item = self._selected_scene_object()
        if item is None:
            return
        updated = copy.deepcopy(item)
        updated["position"] = {
            axis: spin.value() for axis, spin in self.position_spins.items()
        }
        updated["size"] = {
            axis: spin.value() for axis, spin in self.size_spins.items()
        }
        updated["rotation_deg"] = {
            axis: spin.value() for axis, spin in self.rotation_spins.items()
        }
        updated["appearance"]["opacity"] = self.opacity_spin.value()
        self.commit_viewport_object(item["object_id"], updated)

    def commit_viewport_object(self, object_id: str, updated_object: dict) -> None:
        if self.object_scene is None:
            return
        try:
            self.object_scene = update_scene_object(
                self.object_scene,
                object_id,
                updated_object,
            )
            save_object_scene(self.project_session, self.object_scene)
            self.selected_object_id = object_id
            self.object_viewport.set_scene(self.object_scene, object_id)
            self._update_inspector()
            self._update_cad_controls()
            self.set_status(
                "Saved the selected object's position, size, rotation, color, and opacity."
            )
        except Exception as exc:
            self.object_viewport.set_scene(self.object_scene, self.selected_object_id)
            self._update_inspector()
            self.set_status(f"Could not save the object change: {exc}")

    def choose_selected_color(self, *_args) -> None:
        item = self._selected_scene_object()
        if item is None:
            self.set_status("Select a 3D object before changing its color.")
            return
        current = QColor(item["appearance"]["color"])
        chosen = QColorDialog.getColor(current, self, "Choose object color")
        if not chosen.isValid():
            return
        updated = copy.deepcopy(item)
        updated["appearance"]["color"] = chosen.name()
        self.commit_viewport_object(item["object_id"], updated)

    def reset_selected_object(self, *_args) -> None:
        item = self._selected_scene_object()
        if item is None:
            self.set_status("Select a 3D object before resetting it.")
            return
        source = next(
            (
                shape
                for shape in self.document.get("objects", [])
                if shape.get("object_id") == item["source_shape_id"]
            ),
            None,
        )
        if source is None:
            self.set_status("The selected object's source shape is unavailable.")
            return
        width = float(source["width"])
        height = float(source["height"])
        depth = max(24.0, min(180.0, (width + height) / 5.0))
        updated = copy.deepcopy(item)
        updated["position"] = {
            "x": float(source["x"]) + width / 2.0,
            "y": float(source["y"]) + height / 2.0,
            "z": depth / 2.0,
        }
        updated["size"] = {"x": width, "y": height, "z": depth}
        updated["rotation_deg"] = {"x": 0.0, "y": 0.0, "z": 0.0}
        updated["appearance"]["color"] = source["style"]["fill"]
        updated["appearance"]["opacity"] = 1.0
        self.commit_viewport_object(item["object_id"], updated)

    def undo_object_change(self, *_args) -> None:
        if self.object_scene is None:
            return
        try:
            self.object_scene = undo_scene(self.object_scene)
            save_object_scene(self.project_session, self.object_scene)
            self.object_viewport.set_scene(self.object_scene, self.selected_object_id)
            self._update_inspector()
            self._update_cad_controls()
            self.set_status("Undid the latest 3D object change.")
        except Exception as exc:
            self.set_status(f"Could not undo the object change: {exc}")

    def redo_object_change(self, *_args) -> None:
        if self.object_scene is None:
            return
        try:
            self.object_scene = redo_scene(self.object_scene)
            save_object_scene(self.project_session, self.object_scene)
            self.object_viewport.set_scene(self.object_scene, self.selected_object_id)
            self._update_inspector()
            self._update_cad_controls()
            self.set_status("Redid the latest 3D object change.")
        except Exception as exc:
            self.set_status(f"Could not redo the object change: {exc}")

    def _update_cad_controls(self) -> None:
        if not hasattr(self, "object_button"):
            return
        attached = self.project_session.state is not None
        writable = self.project_session.is_writable
        has_document = self.document is not None
        has_scene = self.object_scene is not None
        has_object = self._selected_scene_object() is not None

        self.object_button.setEnabled(attached and has_document)
        self.sync_3d_action.setEnabled(writable and has_document)
        self.object_undo_action.setEnabled(writable and can_undo_scene(self.object_scene))
        self.object_redo_action.setEnabled(writable and can_redo_scene(self.object_scene))
        self.reset_object_action.setEnabled(writable and has_object)
        self.color_object_action.setEnabled(writable and has_object)

        self.view_button.setEnabled(attached and has_document)
        self.view_3d_action.setEnabled(has_scene)
        self.perspective_action.setEnabled(has_scene)
        self.grid_action.setEnabled(has_scene)
        self.lines_action.setEnabled(has_scene)
