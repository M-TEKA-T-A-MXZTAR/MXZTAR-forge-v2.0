#!/usr/bin/env python3
"""Verify direct, durable 2D resizing in the final live Forge Editor."""

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
from PySide6.QtGui import QTransform  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from core.object_scene import load_object_scene  # noqa: E402
from core.project_session import ProjectSession  # noqa: E402
from core.shape_document import load_shape_document  # noqa: E402
from qt_direct_2d_resize import (  # noqa: E402
    DirectResizeProjectAwareEditorPanel,
    DirectResizeShapeCanvas,
    install_direct_2d_resize,
)

install_direct_2d_resize()

from qt_panels.editor_authority_guard import (  # noqa: E402
    GuardedProjectAwareEditorPanel,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def close_enough(first: float, second: float, tolerance: float = 0.03) -> bool:
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


def click_shape(canvas, shape: dict) -> None:
    centre_scene = QPointF(
        float(shape["x"]) + float(shape["width"]) / 2.0,
        float(shape["y"]) + float(shape["height"]) / 2.0,
    )
    centre_view = QPointF(canvas.mapFromScene(centre_scene))
    canvas.mousePressEvent(
        FakeMouseEvent(centre_view, Qt.MouseButton.LeftButton)
    )
    canvas.mouseReleaseEvent(
        FakeMouseEvent(centre_view, Qt.MouseButton.LeftButton)
    )


def main() -> int:
    app = QApplication.instance() or QApplication([])
    with tempfile.TemporaryDirectory(prefix="mxztar-direct-2d-resize-") as temporary:
        session = ProjectSession(Path(temporary) / "projects")
        state = session.create_and_open(
            "Direct 2D Resize",
            "Verify one visible resize handle and durable paired geometry",
        )
        require(state.writable, "resize test project has writable authority")

        panel = GuardedProjectAwareEditorPanel(session)
        require(
            isinstance(panel, DirectResizeProjectAwareEditorPanel),
            "official final Editor class is replaced by the direct-resize panel",
        )
        panel.set_project_state(session.state)
        panel.create_blank_document()
        panel.add_rectangle_command()
        panel.add_square_command()
        app.processEvents()

        require(
            isinstance(panel.canvas, DirectResizeShapeCanvas),
            "final live Editor installs the direct-resize 2D canvas",
        )
        require(
            panel.document is not None
            and len(panel.document["objects"]) == 2
            and panel.object_scene is not None
            and len(panel.object_scene["objects"]) == 2,
            "rectangle and square each have a paired 3D object",
        )

        panel.show_2d_view()
        panel.canvas.resize(900, 560)
        panel.canvas.show()
        panel.render_document()
        app.processEvents()
        canvas = panel.canvas

        rectangle = copy.deepcopy(panel.document["objects"][0])
        rectangle_id = rectangle["object_id"]
        paired_before = copy.deepcopy(
            scene_object_by_source(panel.object_scene, rectangle_id)
        )
        other_before = copy.deepcopy(
            next(
                item
                for item in panel.object_scene["objects"]
                if item["source_shape_id"] != rectangle_id
            )
        )

        click_shape(canvas, rectangle)
        canvas.grab()
        handle = canvas.current_resize_handle()
        require(
            canvas._selected_shape_id == rectangle_id
            and not handle.isNull()
            and not handle.isEmpty(),
            "clicking a 2D shape displays one clear bottom-right resize handle",
        )
        require(
            panel.selected_object_id == paired_before["object_id"],
            "2D selection identifies the exact paired 3D object",
        )

        history_before = panel.document["history_cursor"]
        start = handle.center()
        target = start + QPointF(84.0, 53.0)
        delivered_target_scene = canvas.mapToScene(target.toPoint())
        expected_width = max(
            canvas.MIN_SHAPE_SIZE,
            delivered_target_scene.x() - float(rectangle["x"]),
        )
        expected_height = max(
            canvas.MIN_SHAPE_SIZE,
            delivered_target_scene.y() - float(rectangle["y"]),
        )
        item = canvas._items_by_object_id[rectangle_id]

        canvas.mousePressEvent(
            FakeMouseEvent(start, Qt.MouseButton.LeftButton)
        )
        require(
            canvas._resize_shape_id == rectangle_id
            and canvas._resize_original_geometry is not None,
            "pressing the visible handle starts resize rather than body movement",
        )
        canvas.mouseMoveEvent(FakeMouseEvent(target))
        preview = copy.deepcopy(canvas._resize_preview_geometry)
        require(
            preview is not None
            and close_enough(preview["x"], rectangle["x"])
            and close_enough(preview["y"], rectangle["y"])
            and close_enough(preview["width"], expected_width)
            and close_enough(preview["height"], expected_height)
            and item.transform() != QTransform(),
            "handle preview keeps the opposite corner fixed and follows delivered geometry",
        )
        canvas.mouseReleaseEvent(
            FakeMouseEvent(target, Qt.MouseButton.LeftButton)
        )
        app.processEvents()

        resized = copy.deepcopy(shape_by_id(panel.document, rectangle_id))
        require(
            close_enough(resized["x"], rectangle["x"])
            and close_enough(resized["y"], rectangle["y"])
            and close_enough(resized["width"], expected_width)
            and close_enough(resized["height"], expected_height)
            and panel.document["history_cursor"] == history_before + 1
            and panel.document["commands"][-1]["type"] == "resize_shape",
            "2D release commits exactly one durable resize_shape command",
        )

        recovered = load_shape_document(
            session,
            panel.document["document_id"],
        )
        recovered_shape = shape_by_id(recovered.document, rectangle_id)
        require(
            recovered.recovered_from_autosave
            and close_enough(recovered_shape["width"], resized["width"])
            and close_enough(recovered_shape["height"], resized["height"]),
            "2D resize is present in the project-owned autosave",
        )

        paired_after = copy.deepcopy(
            scene_object_by_source(panel.object_scene, rectangle_id)
        )
        other_after = next(
            item
            for item in panel.object_scene["objects"]
            if item["object_id"] == other_before["object_id"]
        )
        require(
            close_enough(paired_after["size"]["x"], resized["width"])
            and close_enough(paired_after["size"]["y"], resized["height"])
            and close_enough(
                paired_after["position"]["x"],
                resized["x"] + resized["width"] / 2.0,
            )
            and close_enough(
                paired_after["position"]["y"],
                resized["y"] + resized["height"] / 2.0,
            )
            and paired_after["position"]["z"] == paired_before["position"]["z"]
            and paired_after["size"]["z"] == paired_before["size"]["z"]
            and paired_after["rotation_deg"] == paired_before["rotation_deg"]
            and paired_after["appearance"] == paired_before["appearance"]
            and other_after == other_before,
            "resize synchronizes only paired 3D centre and width/height",
        )
        persisted_scene = load_object_scene(
            session,
            panel.document["document_id"],
        )
        require(
            scene_object_by_source(persisted_scene, rectangle_id) == paired_after,
            "paired 3D resize synchronization is persisted",
        )

        panel.undo_command()
        app.processEvents()
        undone = shape_by_id(panel.document, rectangle_id)
        undone_object = scene_object_by_source(panel.object_scene, rectangle_id)
        require(
            close_enough(undone["x"], rectangle["x"])
            and close_enough(undone["y"], rectangle["y"])
            and close_enough(undone["width"], rectangle["width"])
            and close_enough(undone["height"], rectangle["height"])
            and close_enough(undone_object["size"]["x"], paired_before["size"]["x"])
            and close_enough(undone_object["size"]["y"], paired_before["size"]["y"]),
            "Undo restores both 2D geometry and paired 3D geometry",
        )

        panel.redo_command()
        app.processEvents()
        redone = shape_by_id(panel.document, rectangle_id)
        redone_object = scene_object_by_source(panel.object_scene, rectangle_id)
        require(
            close_enough(redone["width"], resized["width"])
            and close_enough(redone["height"], resized["height"])
            and close_enough(redone_object["size"]["x"], paired_after["size"]["x"])
            and close_enough(redone_object["size"]["y"], paired_after["size"]["y"]),
            "Redo reapplies both 2D geometry and paired 3D geometry",
        )

        canvas = panel.canvas
        canvas.grab()
        click_shape(canvas, redone)
        move_start_scene = QPointF(
            redone["x"] + 25.0,
            redone["y"] + 22.0,
        )
        move_target_scene = move_start_scene + QPointF(37.0, 29.0)
        move_start = QPointF(canvas.mapFromScene(move_start_scene))
        move_target = QPointF(canvas.mapFromScene(move_target_scene))
        size_before_move = (redone["width"], redone["height"])
        move_history_before = panel.document["history_cursor"]
        canvas.mousePressEvent(
            FakeMouseEvent(move_start, Qt.MouseButton.LeftButton)
        )
        canvas.mouseMoveEvent(FakeMouseEvent(move_target))
        canvas.mouseReleaseEvent(
            FakeMouseEvent(move_target, Qt.MouseButton.LeftButton)
        )
        app.processEvents()
        moved_after_resize = shape_by_id(panel.document, rectangle_id)
        require(
            panel.document["history_cursor"] == move_history_before + 1
            and panel.document["commands"][-1]["type"] == "move_shape"
            and close_enough(moved_after_resize["width"], size_before_move[0])
            and close_enough(moved_after_resize["height"], size_before_move[1]),
            "existing direct body movement remains unchanged after resizing",
        )

        square = copy.deepcopy(
            next(item for item in panel.document["objects"] if item["type"] == "square")
        )
        square_id = square["object_id"]
        click_shape(panel.canvas, square)
        panel.canvas.grab()
        square_handle = panel.canvas.current_resize_handle()
        square_target_scene = QPointF(
            float(square["x"]) - 60.0,
            float(square["y"]) - 60.0,
        )
        square_target = QPointF(panel.canvas.mapFromScene(square_target_scene))
        square_history_before = panel.document["history_cursor"]
        panel.canvas.mousePressEvent(
            FakeMouseEvent(square_handle.center(), Qt.MouseButton.LeftButton)
        )
        panel.canvas.mouseMoveEvent(FakeMouseEvent(square_target))
        square_preview = copy.deepcopy(panel.canvas._resize_preview_geometry)
        require(
            square_preview is not None
            and close_enough(
                square_preview["width"], panel.canvas.MIN_SHAPE_SIZE
            )
            and close_enough(
                square_preview["height"], panel.canvas.MIN_SHAPE_SIZE
            ),
            "minimum size prevents inversion or disappearance during handle drag",
        )
        panel.canvas.mouseReleaseEvent(
            FakeMouseEvent(square_target, Qt.MouseButton.LeftButton)
        )
        app.processEvents()
        resized_square = shape_by_id(panel.document, square_id)
        resized_square_object = scene_object_by_source(panel.object_scene, square_id)
        require(
            panel.document["history_cursor"] == square_history_before + 1
            and panel.document["commands"][-1]["type"] == "resize_shape"
            and close_enough(resized_square["x"], square["x"])
            and close_enough(resized_square["y"], square["y"])
            and close_enough(
                resized_square["width"], panel.canvas.MIN_SHAPE_SIZE
            )
            and close_enough(
                resized_square["height"], panel.canvas.MIN_SHAPE_SIZE
            )
            and close_enough(
                resized_square_object["size"]["x"], resized_square["width"]
            )
            and close_enough(
                resized_square_object["size"]["y"], resized_square["height"]
            ),
            "square resize remains proportional and synchronizes its paired object",
        )

        panel.deleteLater()
        app.processEvents()
        session.close()

    print("PASS: direct 2D resize contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
