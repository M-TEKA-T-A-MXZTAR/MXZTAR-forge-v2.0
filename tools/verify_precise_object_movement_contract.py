#!/usr/bin/env python3
"""Verify cursor-locked 2D and 3D movement in the final live Editor."""

from __future__ import annotations

import copy
import math
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PySide6.QtCore import QPointF, Qt  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

import core.object_scene as object_scene  # noqa: E402
from core.object_scene import load_object_scene  # noqa: E402
from core.project_session import ProjectSession  # noqa: E402
from core.shape_document import load_shape_document  # noqa: E402
from qt_panels.editor_authority_guard import (  # noqa: E402
    GuardedProjectAwareEditorPanel,
    PreciseGuidedObjectViewport,
    PreciseShapeCanvas,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def close_enough(first: float, second: float, tolerance: float = 0.02) -> bool:
    return math.isclose(first, second, abs_tol=tolerance)


class FakeMouseEvent:
    def __init__(
        self,
        position: QPointF,
        button: Qt.MouseButton = Qt.MouseButton.NoButton,
    ):
        self._position = QPointF(position)
        self._button = button
        self.accepted = False

    def position(self) -> QPointF:
        return QPointF(self._position)

    def button(self) -> Qt.MouseButton:
        return self._button

    def accept(self) -> None:
        self.accepted = True


def shape_by_id(document: dict, object_id: str) -> dict:
    return next(
        item
        for item in document["objects"]
        if item["object_id"] == object_id
    )


def scene_object_by_source(scene: dict, source_shape_id: str) -> dict:
    return next(
        item
        for item in scene["objects"]
        if item["source_shape_id"] == source_shape_id
    )


def grid_landmarks(viewport) -> tuple[tuple[float, float], ...]:
    target = viewport._scene_target()
    points = (
        (target[0], target[1], 0.0),
        (target[0] + 100.0, target[1], 0.0),
        (target[0], target[1] + 100.0, 0.0),
    )
    return tuple(
        (screen.x(), screen.y())
        for screen, _depth, _scale in (
            viewport._project(point, target) for point in points
        )
    )


def landmarks_match(
    first: tuple[tuple[float, float], ...],
    second: tuple[tuple[float, float], ...],
) -> bool:
    return all(
        close_enough(first_x, second_x, 1.0e-8)
        and close_enough(first_y, second_y, 1.0e-8)
        for (first_x, first_y), (second_x, second_y) in zip(first, second)
    )


def main() -> int:
    app = QApplication.instance() or QApplication([])
    with tempfile.TemporaryDirectory(
        prefix="mxztar-precise-movement-"
    ) as temporary:
        session = ProjectSession(Path(temporary) / "projects")
        state = session.create_and_open(
            "Precise Movement",
            "Verify direct 2D and 3D pointer-locked object movement",
        )
        require(state.writable, "movement test project has writable authority")

        panel = GuardedProjectAwareEditorPanel(session)
        panel.set_project_state(session.state)
        panel.create_blank_document()
        panel.add_rectangle_command()
        panel.add_square_command()
        app.processEvents()

        require(
            isinstance(panel.canvas, PreciseShapeCanvas),
            "final live Editor installs the precise 2D shape canvas",
        )
        require(
            isinstance(panel.object_viewport, PreciseGuidedObjectViewport),
            "final live Editor installs the precise guided 3D viewport",
        )
        require(
            panel.document is not None
            and len(panel.document["objects"]) == 2
            and panel.object_scene is not None
            and len(panel.object_scene["objects"]) == 2,
            "two paired shapes and CAD objects are available",
        )

        panel.show_2d_view()
        panel.canvas.resize(900, 560)
        panel.canvas.show()
        panel.render_document()
        app.processEvents()

        source_shape = copy.deepcopy(panel.document["objects"][0])
        source_shape_id = source_shape["object_id"]
        paired_before = copy.deepcopy(
            scene_object_by_source(panel.object_scene, source_shape_id)
        )
        other_before = copy.deepcopy(
            next(
                item
                for item in panel.object_scene["objects"]
                if item["source_shape_id"] != source_shape_id
            )
        )
        history_before = panel.document["history_cursor"]

        click_offset = QPointF(31.0, 27.0)
        start_scene = QPointF(
            source_shape["x"] + click_offset.x(),
            source_shape["y"] + click_offset.y(),
        )
        target_scene = start_scene + QPointF(73.0, 41.0)
        start_view = QPointF(panel.canvas.mapFromScene(start_scene))
        target_view = QPointF(panel.canvas.mapFromScene(target_scene))
        delivered_start_scene = panel.canvas.mapToScene(start_view.toPoint())
        delivered_target_scene = panel.canvas.mapToScene(target_view.toPoint())
        delivered_delta = delivered_target_scene - delivered_start_scene
        item = panel.canvas._items_by_object_id[source_shape_id]

        panel.canvas.mousePressEvent(
            FakeMouseEvent(start_view, Qt.MouseButton.LeftButton)
        )
        panel.canvas.mouseMoveEvent(FakeMouseEvent(target_view))
        require(
            close_enough(item.pos().x(), delivered_delta.x())
            and close_enough(item.pos().y(), delivered_delta.y()),
            "2D preview follows the delivered pointer by the exact scene-space delta",
        )
        preview_x, preview_y = panel.canvas._drag_preview_xy
        require(
            close_enough(
                preview_x + panel.canvas._drag_offset.x(),
                delivered_target_scene.x(),
            )
            and close_enough(
                preview_y + panel.canvas._drag_offset.y(),
                delivered_target_scene.y(),
            ),
            "2D drag preserves the exact clicked offset instead of jumping to centre",
        )
        panel.canvas.mouseReleaseEvent(
            FakeMouseEvent(target_view, Qt.MouseButton.LeftButton)
        )
        app.processEvents()

        moved_shape = copy.deepcopy(
            shape_by_id(panel.document, source_shape_id)
        )
        require(
            close_enough(
                moved_shape["x"],
                source_shape["x"] + delivered_delta.x(),
            )
            and close_enough(
                moved_shape["y"],
                source_shape["y"] + delivered_delta.y(),
            )
            and panel.document["history_cursor"] == history_before + 1
            and panel.document["commands"][-1]["type"] == "move_shape",
            "2D release commits exactly one durable move command",
        )

        recovered = load_shape_document(
            session,
            panel.document["document_id"],
        )
        recovered_shape = shape_by_id(
            recovered.document,
            source_shape_id,
        )
        require(
            recovered.recovered_from_autosave
            and close_enough(recovered_shape["x"], moved_shape["x"])
            and close_enough(recovered_shape["y"], moved_shape["y"]),
            "2D movement is present in the project-owned autosave",
        )

        paired_after_2d = copy.deepcopy(
            scene_object_by_source(panel.object_scene, source_shape_id)
        )
        other_after_2d = next(
            item
            for item in panel.object_scene["objects"]
            if item["object_id"] == other_before["object_id"]
        )
        require(
            close_enough(
                paired_after_2d["position"]["x"],
                paired_before["position"]["x"] + delivered_delta.x(),
            )
            and close_enough(
                paired_after_2d["position"]["y"],
                paired_before["position"]["y"] + delivered_delta.y(),
            )
            and paired_after_2d["position"]["z"]
            == paired_before["position"]["z"]
            and paired_after_2d["size"] == paired_before["size"]
            and paired_after_2d["rotation_deg"]
            == paired_before["rotation_deg"]
            and paired_after_2d["appearance"]
            == paired_before["appearance"]
            and other_after_2d == other_before,
            "2D movement changes only paired 3D X/Y and preserves all adjacent state",
        )
        persisted_after_2d = load_object_scene(
            session,
            panel.document["document_id"],
        )
        require(
            scene_object_by_source(
                persisted_after_2d,
                source_shape_id,
            )
            == paired_after_2d,
            "paired 3D X/Y synchronization is persisted",
        )

        panel.undo_command()
        app.processEvents()
        undone_shape = shape_by_id(panel.document, source_shape_id)
        undone_object = scene_object_by_source(
            panel.object_scene,
            source_shape_id,
        )
        require(
            close_enough(undone_shape["x"], source_shape["x"])
            and close_enough(undone_shape["y"], source_shape["y"])
            and close_enough(
                undone_object["position"]["x"],
                paired_before["position"]["x"],
            )
            and close_enough(
                undone_object["position"]["y"],
                paired_before["position"]["y"],
            ),
            "Undo restores both 2D position and paired 3D X/Y",
        )

        panel.redo_command()
        app.processEvents()
        redone_shape = shape_by_id(panel.document, source_shape_id)
        redone_object = scene_object_by_source(
            panel.object_scene,
            source_shape_id,
        )
        require(
            close_enough(redone_shape["x"], moved_shape["x"])
            and close_enough(redone_shape["y"], moved_shape["y"])
            and close_enough(
                redone_object["position"]["x"],
                paired_after_2d["position"]["x"],
            )
            and close_enough(
                redone_object["position"]["y"],
                paired_after_2d["position"]["y"],
            ),
            "Redo reapplies both 2D position and paired 3D X/Y",
        )

        panel.object_scene = object_scene.set_scene_view(
            panel.object_scene,
            yaw_deg=35.0,
            pitch_deg=28.0,
            zoom=0.75,
            perspective=True,
            grid_visible=True,
            edges_visible=True,
        )
        object_scene.save_object_scene(
            session,
            panel.object_scene,
        )
        cad_object = copy.deepcopy(
            scene_object_by_source(panel.object_scene, source_shape_id)
        )
        panel.selected_object_id = cad_object["object_id"]
        panel.object_viewport.resize(900, 560)
        panel.object_viewport.set_scene(
            panel.object_scene,
            cad_object["object_id"],
        )
        panel.snap_guides_action.setChecked(False)
        panel.show_3d_view()
        panel.object_viewport.show()
        panel.object_viewport.grab()
        app.processEvents()

        viewport = panel.object_viewport
        bounds = viewport._selected_projected_bounds()
        require(bounds is not None, "selected 3D object has projected hit bounds")
        start = bounds.center()
        require(
            viewport._hit_object(start) == cad_object["object_id"]
            and not viewport._resize_handle.contains(start),
            "3D drag begins on the object body away from resize",
        )

        camera_before = copy.deepcopy(viewport.scene_data["view"])
        grid_before = grid_landmarks(viewport)
        other_3d_before = copy.deepcopy(
            next(
                item
                for item in viewport._preview_objects
                if item["object_id"] != cad_object["object_id"]
            )
        )
        scene_history_before = panel.object_scene["history_cursor"]

        viewport.mousePressEvent(
            FakeMouseEvent(start, Qt.MouseButton.LeftButton)
        )
        require(
            viewport._drag_mode == "move"
            and viewport._drag_constraint == "precise_xy"
            and viewport._precise_anchor_world is not None,
            "Select-mode press starts fixed-Z precise XY movement",
        )
        original_drag_object = copy.deepcopy(
            viewport._drag_original_object
        )
        anchor_world = viewport._precise_anchor_world
        plane_z = viewport._precise_plane_z
        target_pointer = start + QPointF(76.0, -33.0)
        viewport.mouseMoveEvent(FakeMouseEvent(target_pointer))

        preview = viewport.selected_object()
        anchor_offset_x = (
            anchor_world[0] - original_drag_object["position"]["x"]
        )
        anchor_offset_y = (
            anchor_world[1] - original_drag_object["position"]["y"]
        )
        moved_anchor_world = (
            preview["position"]["x"] + anchor_offset_x,
            preview["position"]["y"] + anchor_offset_y,
            plane_z,
        )
        moved_anchor_screen, _depth, _scale = viewport._project(
            moved_anchor_world,
            viewport._scene_target(),
        )
        require(
            close_enough(moved_anchor_screen.x(), target_pointer.x())
            and close_enough(moved_anchor_screen.y(), target_pointer.y()),
            "the grabbed 3D point remains directly beneath the pointer",
        )
        require(
            viewport.scene_data["view"] == camera_before
            and landmarks_match(grid_before, grid_landmarks(viewport)),
            "3D movement leaves camera and fixed grid stationary",
        )
        require(
            preview["position"]["z"] == original_drag_object["position"]["z"]
            and preview["size"] == original_drag_object["size"]
            and preview["rotation_deg"]
            == original_drag_object["rotation_deg"]
            and preview["appearance"]
            == original_drag_object["appearance"]
            and next(
                item
                for item in viewport._preview_objects
                if item["object_id"] == other_3d_before["object_id"]
            )
            == other_3d_before,
            "3D drag changes only selected-object X/Y",
        )

        viewport.mouseReleaseEvent(
            FakeMouseEvent(target_pointer, Qt.MouseButton.LeftButton)
        )
        app.processEvents()
        require(
            panel.object_scene["history_cursor"]
            == scene_history_before + 1,
            "3D release commits exactly one object-scene command",
        )
        persisted_3d = load_object_scene(
            session,
            panel.document["document_id"],
        )
        persisted_selected = scene_object_by_source(
            persisted_3d,
            source_shape_id,
        )
        require(
            close_enough(
                persisted_selected["position"]["x"],
                preview["position"]["x"],
            )
            and close_enough(
                persisted_selected["position"]["y"],
                preview["position"]["y"],
            )
            and persisted_selected["position"]["z"]
            == original_drag_object["position"]["z"],
            "precise 3D movement persists with unchanged depth",
        )

        panel.close()
        session.close()

    print("PASS: precise 2D/3D movement contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
