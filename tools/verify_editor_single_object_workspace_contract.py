#!/usr/bin/env python3
"""Verify visible placement, synchronized history, isolated edits, and Editor sizing."""

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

from PySide6.QtCore import QPointF, QSize, Qt  # noqa: E402
from PySide6.QtWidgets import QApplication, QWidget  # noqa: E402

from core.object_scene import load_object_scene  # noqa: E402
from core.project_session import ProjectSession  # noqa: E402
from qt_editor_usability_app import CurrentPageStack  # noqa: E402
from qt_panels.editor_authority_guard import GuardedProjectAwareEditorPanel  # noqa: E402
from qt_panels.editor_usability_panel import (  # noqa: E402
    SingleObjectWorkspacePanel,
    StableObjectViewport,
)
from qt_panels.positioning_guides import GuidedObjectViewport  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def overlaps(first: dict, second: dict) -> bool:
    return not (
        first["x"] + first["width"] <= second["x"]
        or second["x"] + second["width"] <= first["x"]
        or first["y"] + first["height"] <= second["y"]
        or second["y"] + second["height"] <= first["y"]
    )


class HintWidget(QWidget):
    def __init__(self, size: QSize):
        super().__init__()
        self._hint = size

    def sizeHint(self) -> QSize:
        return self._hint

    def minimumSizeHint(self) -> QSize:
        return self._hint


class FakeMouseEvent:
    def __init__(
        self,
        position: QPointF,
        button: Qt.MouseButton = Qt.MouseButton.NoButton,
    ):
        self._position = position
        self._button = button

    def position(self) -> QPointF:
        return self._position

    def button(self) -> Qt.MouseButton:
        return self._button


def grid_landmarks(viewport) -> tuple[tuple[float, float], ...]:
    target = viewport._scene_target()
    world_points = (
        (target[0], target[1], 0.0),
        (target[0] + 100.0, target[1], 0.0),
        (target[0], target[1] + 100.0, 0.0),
    )
    return tuple(
        (screen.x(), screen.y())
        for screen, _depth, _scale in (
            viewport._project(point, target) for point in world_points
        )
    )


def landmarks_match(
    first: tuple[tuple[float, float], ...],
    second: tuple[tuple[float, float], ...],
) -> bool:
    return all(
        math.isclose(first_x, second_x, abs_tol=1.0e-9)
        and math.isclose(first_y, second_y, abs_tol=1.0e-9)
        for (first_x, first_y), (second_x, second_y) in zip(first, second)
    )


def main() -> int:
    app = QApplication.instance() or QApplication([])
    with tempfile.TemporaryDirectory(prefix="mxztar-single-object-") as temporary:
        session = ProjectSession(Path(temporary) / "projects")
        state = session.create_and_open(
            "Single Object Workspace",
            "Verify one-object editing and visible Editor layout",
        )
        require(state.writable, "single-object test project opens with writable authority")

        panel = SingleObjectWorkspacePanel(session)
        panel.set_project_state(session.state)
        panel.create_blank_document()
        panel.add_rectangle_command()
        panel.add_square_command()
        panel.add_circle_command()
        panel.add_ellipse_command()
        panel.add_star_command()
        app.processEvents()

        shapes = panel.document["objects"]
        require(len(shapes) == 5, "all five requested shapes exist in the native document")
        require(
            not any(
                overlaps(shapes[first], shapes[second])
                for first in range(len(shapes))
                for second in range(first + 1, len(shapes))
            ),
            "new shapes use non-overlapping visible grid positions",
        )
        require(
            panel.object_scene is not None
            and len(panel.object_scene["objects"]) == 5
            and len(panel.object_viewport._preview_objects) == 5,
            "each new shape appears in the 3D Editor immediately without manual resynchronization",
        )
        newest_shape = shapes[-1]
        newest_source_id = newest_shape["object_id"]
        expected_selected = f"cad_{newest_source_id.removeprefix('object_')}"
        require(
            panel.selected_object_id == expected_selected,
            "the newest created object becomes the single active selection",
        )

        require(
            panel.layout().indexOf(panel.workspace_splitter) == 3
            and panel.workspace_splitter.widget(0) is panel.view_stack
            and panel.workspace_splitter.widget(1) is panel.inspector,
            "visual output and Object Inspector share one side-by-side Editor workspace",
        )

        five_object_anchor = panel.object_viewport._scene_target()
        panel.undo_command()
        app.processEvents()
        require(
            len(panel.document["objects"]) == 4
            and len(panel.object_scene["objects"]) == 4
            and all(
                item["source_shape_id"] != newest_source_id
                for item in panel.object_scene["objects"]
            ),
            "shape Undo removes the matching object from both 2D and 3D authority",
        )
        persisted_after_undo = load_object_scene(
            session,
            panel.document["document_id"],
        )
        require(
            len(persisted_after_undo["objects"]) == 4
            and all(
                item["source_shape_id"] != newest_source_id
                for item in persisted_after_undo["objects"]
            ),
            "shape Undo persists without a ghost object after reload",
        )
        four_object_anchor = panel.object_viewport._scene_target()
        require(
            four_object_anchor == five_object_anchor
            == StableObjectViewport._anchor_for_scene(panel.object_scene),
            "world-origin anchor remains stationary when Undo removes a scene member",
        )

        panel.redo_command()
        app.processEvents()
        require(
            len(panel.document["objects"]) == 5
            and len(panel.object_scene["objects"]) == 5
            and any(
                item["source_shape_id"] == newest_source_id
                for item in panel.object_scene["objects"]
            ),
            "shape Redo restores matching membership in both 2D and 3D authority",
        )
        persisted_after_redo = load_object_scene(
            session,
            panel.document["document_id"],
        )
        require(
            len(persisted_after_redo["objects"]) == 5,
            "shape Redo persists the restored 3D membership",
        )
        require(
            panel.object_viewport._scene_target() == four_object_anchor
            == StableObjectViewport._anchor_for_scene(panel.object_scene),
            "world-origin anchor remains stationary when Redo restores a scene member",
        )

        target_before = panel.object_viewport._scene_target()
        objects_before = {
            item["object_id"]: copy.deepcopy(item)
            for item in panel.object_scene["objects"]
        }
        selected = panel._selected_scene_object()
        updated = copy.deepcopy(selected)
        updated["position"]["x"] += 85.0
        updated["position"]["y"] += 45.0
        panel.commit_viewport_object(selected["object_id"], updated)
        app.processEvents()

        require(
            panel.object_viewport._scene_target() == target_before,
            "moving one object does not recenter the camera or make every object slide",
        )
        require(
            all(
                item["object_id"] == selected["object_id"]
                or item == objects_before[item["object_id"]]
                for item in panel.object_scene["objects"]
            ),
            "moving the selected object leaves every nonselected object unchanged",
        )

        guarded_panel = GuardedProjectAwareEditorPanel(session)
        guarded_panel.set_project_state(session.state)
        app.processEvents()
        guarded_viewport = guarded_panel.object_viewport
        require(
            isinstance(guarded_viewport, GuidedObjectViewport),
            "final live Editor installs the guided stable 3D viewport",
        )
        guarded_viewport.resize(900, 560)
        guarded_viewport.show()
        guarded_viewport.set_scene(
            guarded_panel.object_scene,
            guarded_panel.selected_object_id,
        )
        guarded_viewport.grab()

        guarded_panel.set_interaction_mode("orbit")
        guarded_panel.show_2d_view()
        view_before_reentry = copy.deepcopy(guarded_viewport.scene_data["view"])
        guarded_panel.show_3d_view()
        app.processEvents()
        require(
            guarded_panel.view_stack.currentWidget() is guarded_viewport
            and guarded_panel.interaction_mode == "select"
            and guarded_viewport.interaction_mode == "select"
            and guarded_panel.interaction_actions["select"].isChecked(),
            "Orbit to 2D to 3D re-entry always restores Select mode",
        )
        require(
            guarded_viewport.scene_data["view"] == view_before_reentry,
            "3D re-entry changes interaction mode without changing the camera view",
        )

        guarded_viewport.grab()
        selected = guarded_viewport.selected_object()
        require(selected is not None, "one object remains selected after 3D re-entry")
        bounds = guarded_viewport._selected_projected_bounds()
        require(bounds is not None, "selected object has visible projected bounds after re-entry")
        drag_start = bounds.center()
        require(
            not guarded_viewport._resize_handle.contains(drag_start),
            "re-entry movement begins on the object body rather than the resize handle",
        )
        grid_before_drag = grid_landmarks(guarded_viewport)
        camera_before_drag = copy.deepcopy(guarded_viewport.scene_data["view"])
        selected_before_drag = copy.deepcopy(selected)
        history_before_drag = guarded_panel.object_scene["history_cursor"]

        guarded_viewport.mousePressEvent(
            FakeMouseEvent(drag_start, Qt.MouseButton.LeftButton)
        )
        require(
            guarded_viewport._drag_mode == "move"
            and guarded_viewport._drag_constraint == "plane_xy",
            "first object drag after 3D re-entry begins movement rather than orbit",
        )
        drag_end = QPointF(drag_start.x() + 42.0, drag_start.y() + 19.0)
        guarded_viewport.mouseMoveEvent(FakeMouseEvent(drag_end))
        moved_preview = guarded_viewport.selected_object()
        grid_during_drag = grid_landmarks(guarded_viewport)
        require(
            moved_preview["position"]["x"] != selected_before_drag["position"]["x"]
            and moved_preview["position"]["y"] != selected_before_drag["position"]["y"]
            and moved_preview["position"]["z"] == selected_before_drag["position"]["z"],
            "re-entry drag changes only the selected object's X/Y position",
        )
        require(
            guarded_viewport.scene_data["view"] == camera_before_drag
            and landmarks_match(grid_before_drag, grid_during_drag),
            "camera state and fixed grid landmarks remain stationary during object movement",
        )

        guarded_viewport.mouseReleaseEvent(FakeMouseEvent(drag_end))
        app.processEvents()
        grid_after_drag = grid_landmarks(guarded_viewport)
        require(
            guarded_panel.object_scene["history_cursor"] == history_before_drag + 1
            and guarded_panel.object_scene["view"] == camera_before_drag
            and guarded_viewport.scene_data["view"] == camera_before_drag
            and landmarks_match(grid_before_drag, grid_after_drag),
            "object release commits once while camera and grid remain stationary",
        )

        guarded_panel.deleteLater()
        app.processEvents()

        panel.add_rectangle_command()
        panel.add_square_command()
        panel.add_circle_command()
        panel.add_ellipse_command()
        app.processEvents()
        nine_shapes = panel.document["objects"]
        require(
            len(nine_shapes) == panel.GRID_CAPACITY
            and len(panel.object_scene["objects"]) == panel.GRID_CAPACITY,
            "the visible placement grid accepts exactly nine synchronized objects",
        )
        require(
            not any(
                overlaps(nine_shapes[first], nine_shapes[second])
                for first in range(len(nine_shapes))
                for second in range(first + 1, len(nine_shapes))
            ),
            "all nine capacity slots remain non-overlapping",
        )
        revision_before_rejected_add = panel.document["revision"]
        scene_revision_before_rejected_add = panel.object_scene["revision"]
        panel.add_star_command()
        app.processEvents()
        require(
            len(panel.document["objects"]) == panel.GRID_CAPACITY
            and len(panel.object_scene["objects"]) == panel.GRID_CAPACITY
            and panel.document["revision"] == revision_before_rejected_add
            and panel.object_scene["revision"] == scene_revision_before_rejected_add
            and "placement grid is full" in panel.status_label.text().lower(),
            "a tenth primitive is rejected clearly without overlap or state mutation",
        )

        pages = CurrentPageStack()
        tall_hidden_page = HintWidget(QSize(900, 1400))
        compact_editor_page = HintWidget(QSize(900, 430))
        pages.addWidget(tall_hidden_page)
        pages.addWidget(compact_editor_page)
        pages.setCurrentWidget(compact_editor_page)
        require(
            pages.minimumSizeHint().height() == 430
            and pages.sizeHint().height() == 430,
            "page sizing follows the visible Editor instead of a taller hidden page",
        )

        panel.deleteLater()
        pages.deleteLater()
        app.processEvents()
        session.close()

    print("PASS: single-object Editor workspace contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
