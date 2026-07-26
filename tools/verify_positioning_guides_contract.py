#!/usr/bin/env python3
"""Verify transient guides, measurements, optional snapping, and orbit isolation."""

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

from core.positioning_guides import (  # noqa: E402
    MAX_SNAP_TOLERANCE,
    MIN_SNAP_TOLERANCE,
    calculate_positioning_guides,
    clamp_snap_tolerance,
)
from core.project_session import ProjectSession  # noqa: E402
from qt_panels.editor_authority_guard import GuardedProjectAwareEditorPanel  # noqa: E402
from qt_panels.positioning_guides import (  # noqa: E402
    GuidedObjectViewport,
    apply_positioning_guide_options,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


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


def sample_object(
    object_id: str,
    x: float,
    y: float,
    z: float = 40.0,
    *,
    size: dict | None = None,
    rotation: dict | None = None,
) -> dict:
    return {
        "object_id": object_id,
        "source_shape_id": f"object_{object_id.removeprefix('cad_')}",
        "primitive_type": "rectangle",
        "position": {"x": x, "y": y, "z": z},
        "size": copy.deepcopy(size or {"x": 80.0, "y": 60.0, "z": 80.0}),
        "rotation_deg": copy.deepcopy(
            rotation or {"x": 0.0, "y": 0.0, "z": 0.0}
        ),
        "appearance": {"color": "#4477aa", "opacity": 1.0},
        "primitive_parameters": {},
    }


def main() -> int:
    require(
        clamp_snap_tolerance(-20.0) == MIN_SNAP_TOLERANCE
        and clamp_snap_tolerance(500.0) == MAX_SNAP_TOLERANCE,
        "snap tolerance is bounded before guide calculations",
    )

    moving = sample_object("cad_moving", 205.0, 200.0)
    neighbour = sample_object("cad_neighbour", 290.0, 200.0)
    unsnapped, guidance = calculate_positioning_guides(
        moving,
        [moving, neighbour],
        (250.0, 250.0, 40.0),
        tolerance=10.0,
        snap_enabled=False,
    )
    require(
        unsnapped["position"] == moving["position"]
        and guidance["snap_applied"] is False,
        "guidance-only movement never forces object position",
    )
    require(
        guidance["nearest"]["object_id"] == neighbour["object_id"]
        and guidance["nearest"]["center_distance"] > 0.0
        and guidance["nearest"]["surface_distance"] >= 0.0,
        "nearest-object centre and surface distances are calculated",
    )
    require(
        {item["axis"] for item in guidance["alignments"]}.issuperset({"x", "y", "z"}),
        "centre and edge alignment detection reports all applicable axes",
    )

    snapped, snapped_guidance = calculate_positioning_guides(
        moving,
        [moving, neighbour],
        (250.0, 250.0, 40.0),
        tolerance=10.0,
        snap_enabled=True,
    )
    require(
        snapped["position"]["x"] == 210.0
        and snapped["position"]["y"] == moving["position"]["y"]
        and snapped_guidance["snap_applied"] is True,
        "explicit snapping adjusts only the selected object's X/Y movement",
    )
    require(
        neighbour == sample_object("cad_neighbour", 290.0, 200.0),
        "guide and snap calculations never mutate a neighbouring object",
    )

    slender_size = {"x": 100.0, "y": 20.0, "z": 20.0}
    small_size = {"x": 20.0, "y": 20.0, "z": 20.0}
    quarter_turn = {"x": 0.0, "y": 0.0, "z": 90.0}
    rotated = sample_object(
        "cad_rotated",
        0.0,
        0.0,
        0.0,
        size=slender_size,
        rotation=quarter_turn,
    )
    rotated_neighbour = sample_object(
        "cad_rotated_neighbour",
        35.0,
        0.0,
        0.0,
        size=small_size,
    )
    rotated_unsnapped, rotated_guidance = calculate_positioning_guides(
        rotated,
        [rotated, rotated_neighbour],
        (500.0, 500.0, 500.0),
        tolerance=10.0,
        snap_enabled=True,
    )
    require(
        math.isclose(
            rotated_guidance["nearest"]["surface_distance"],
            15.0,
            abs_tol=1.0e-6,
        ),
        "90-degree rotation changes surface distance to match rendered bounds",
    )
    require(
        rotated_unsnapped["position"] == rotated["position"]
        and not any(
            alignment["axis"] == "x"
            for alignment in rotated_guidance["alignments"]
        ),
        "rotated bounds prevent a false X-edge snap between visibly separated objects",
    )

    near_rotated_edge = sample_object(
        "cad_rotated_edge",
        14.0,
        0.0,
        0.0,
        size=slender_size,
        rotation=quarter_turn,
    )
    edge_snapped, edge_guidance = calculate_positioning_guides(
        near_rotated_edge,
        [near_rotated_edge, rotated_neighbour],
        (500.0, 500.0, 500.0),
        tolerance=2.0,
        snap_enabled=True,
    )
    require(
        math.isclose(edge_snapped["position"]["x"], 15.0, abs_tol=1.0e-6)
        and edge_guidance["snap_applied"] is True,
        "rotation-aware edge snapping uses the visible 90-degree object extent",
    )

    angled = sample_object(
        "cad_angled",
        0.0,
        0.0,
        0.0,
        size=slender_size,
        rotation={"x": 0.0, "y": 0.0, "z": 45.0},
    )
    angled_neighbour = sample_object(
        "cad_angled_neighbour",
        100.0,
        0.0,
        0.0,
        size=small_size,
    )
    _angled_result, angled_guidance = calculate_positioning_guides(
        angled,
        [angled, angled_neighbour],
        (500.0, 500.0, 500.0),
        tolerance=1.0,
        snap_enabled=False,
    )
    expected_angled_gap = 100.0 - (
        50.0 * math.cos(math.radians(45.0))
        + 10.0 * math.sin(math.radians(45.0))
        + 10.0
    )
    require(
        math.isclose(
            angled_guidance["nearest"]["surface_distance"],
            expected_angled_gap,
            abs_tol=1.0e-6,
        ),
        "angled rotation derives surface gaps from rotated geometry rather than raw size",
    )

    app = QApplication.instance() or QApplication([])
    with tempfile.TemporaryDirectory(prefix="mxztar-position-guides-") as temporary:
        session = ProjectSession(Path(temporary) / "projects")
        state = session.create_and_open(
            "Position Guides",
            "Verify transient object alignment and viewport orbit",
        )
        require(state.writable, "position-guide test project opens with writable authority")

        panel = GuardedProjectAwareEditorPanel(session)
        panel.set_project_state(session.state)
        panel.create_blank_document()
        panel.add_rectangle_command()
        panel.add_square_command()
        app.processEvents()

        viewport = panel.object_viewport
        require(
            isinstance(viewport, GuidedObjectViewport)
            and panel.guides_action.isChecked()
            and not panel.snap_guides_action.isChecked(),
            "official authoring Editor uses visual guides with snapping off by default",
        )
        require(
            panel.guide_tolerance_spin.minimum() == MIN_SNAP_TOLERANCE
            and panel.guide_tolerance_spin.maximum() == MAX_SNAP_TOLERANCE,
            "Editor exposes a bounded configurable guide tolerance",
        )

        viewport.resize(900, 560)
        viewport.set_scene(panel.object_scene, panel.selected_object_id)
        selected = viewport.selected_object()
        require(selected is not None, "one explicit CAD object is selected for guided movement")
        other_before = {
            item["object_id"]: copy.deepcopy(item)
            for item in panel.object_scene["objects"]
            if item["object_id"] != selected["object_id"]
        }

        viewport._drag_mode = "move"
        viewport._drag_start = QPointF(0.0, 0.0)
        viewport._drag_original_object = copy.deepcopy(selected)
        viewport._drag_original_view = copy.deepcopy(panel.object_scene["view"])
        viewport.mouseMoveEvent(FakeMouseEvent(QPointF(24.0, 16.0)))
        overlay = viewport.guide_overlay_lines()
        require(
            viewport._guide_state is not None
            and any(
                "Centre" in line and "X" in line and "Y" in line and "Z" in line
                for line in overlay
            )
            and any("Nearest" in line for line in overlay),
            "active object movement exposes live X/Y/Z and nearest-object measurements",
        )
        require(
            all(
                item == other_before[item["object_id"]]
                for item in viewport._preview_objects
                if item["object_id"] in other_before
            ),
            "guided viewport movement leaves every nonselected preview object unchanged",
        )

        viewport.mouseReleaseEvent(FakeMouseEvent(QPointF(24.0, 16.0)))
        app.processEvents()
        require(
            viewport._guide_state is None and viewport.guide_overlay_lines() == [],
            "position guides disappear immediately when movement is released",
        )

        panel.guides_action.setChecked(False)
        panel.snap_guides_action.setChecked(True)
        apply_positioning_guide_options(panel, announce=False)
        require(
            not panel.snap_guides_action.isChecked()
            and not panel.snap_guides_action.isEnabled()
            and not viewport.guides_enabled
            and not viewport.snap_enabled,
            "turning guides off also prevents invisible snapping",
        )

        panel.guides_action.setChecked(True)
        panel.snap_guides_action.setChecked(True)
        apply_positioning_guide_options(panel, announce=False)
        require(
            viewport.guides_enabled and viewport.snap_enabled,
            "snapping activates only through its separate explicit control",
        )

        original_view = copy.deepcopy(viewport.scene_data["view"])
        viewport.mousePressEvent(
            FakeMouseEvent(QPointF(-100.0, -100.0), Qt.MouseButton.LeftButton)
        )
        require(
            viewport._drag_mode == "orbit" and viewport.selected_object_id is None,
            "left-drag beginning in empty space enters orbit instead of moving an object",
        )
        viewport.mouseMoveEvent(FakeMouseEvent(QPointF(-55.0, -70.0)))
        require(
            viewport.scene_data["view"]["yaw_deg"] != original_view["yaw_deg"]
            and viewport.scene_data["view"]["pitch_deg"] != original_view["pitch_deg"]
            and viewport._guide_state is None,
            "empty-space drag reorients perspective without showing movement guides",
        )
        viewport.mouseReleaseEvent(FakeMouseEvent(QPointF(-55.0, -70.0)))
        require(
            viewport._drag_mode is None and viewport._guide_state is None,
            "orbit release clears interaction state without changing guide authority",
        )

        panel.deleteLater()
        app.processEvents()
        session.close()

    print("PASS: transient positioning guides and viewport navigation contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
