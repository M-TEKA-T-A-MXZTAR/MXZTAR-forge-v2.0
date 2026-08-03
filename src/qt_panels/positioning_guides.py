#!/usr/bin/env python3
"""Transient positioning guides, measurements, and optional snapping for Editor 3D."""

from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QAction, QPainter, QPalette, QPen
from PySide6.QtWidgets import QDoubleSpinBox, QLabel

from core.positioning_guides import (
    DEFAULT_SNAP_TOLERANCE,
    MAX_SNAP_TOLERANCE,
    MIN_SNAP_TOLERANCE,
    calculate_positioning_guides,
)
from qt_panels.editor_usability_panel import StableObjectViewport


class GuidedObjectViewport(StableObjectViewport):
    """Render transient alignment evidence while one selected object is moving."""

    def __init__(self):
        super().__init__()
        self.guides_enabled = True
        self.snap_enabled = False
        self.snap_tolerance = DEFAULT_SNAP_TOLERANCE
        self._guide_state: dict | None = None
        self.setToolTip(
            "3D object view: choose Select, Move, Rotate, Resize, or Orbit View. Position "
            "guides appear only while moving the selected object; Orbit View alone changes "
            "the camera and grid view."
        )

    def set_scene(self, scene: dict | None, selected_object_id: str | None = None) -> None:
        self.clear_positioning_guides()
        super().set_scene(scene, selected_object_id)

    def set_guide_options(
        self,
        *,
        guides_enabled: bool,
        snap_enabled: bool,
        tolerance: float,
    ) -> None:
        self.guides_enabled = bool(guides_enabled)
        self.snap_enabled = bool(snap_enabled and guides_enabled)
        self.snap_tolerance = max(
            MIN_SNAP_TOLERANCE,
            min(MAX_SNAP_TOLERANCE, float(tolerance)),
        )
        if not self.guides_enabled:
            self.clear_positioning_guides()
        self.update()

    def clear_positioning_guides(self) -> None:
        self._guide_state = None
        self.update()

    def guide_overlay_lines(self) -> list[str]:
        state = self._guide_state
        if not self.guides_enabled or not isinstance(state, dict):
            return []
        delta = state["scene_delta"]
        lines = [
            "Centre Δ  "
            f"X {delta['x']:+.1f}  Y {delta['y']:+.1f}  Z {delta['z']:+.1f}"
        ]
        nearest = state.get("nearest")
        if isinstance(nearest, dict):
            lines.append(
                f"Nearest {nearest['object_id']}  centre {nearest['center_distance']:.1f}  "
                f"surface {nearest['surface_distance']:.1f}  "
                f"ΔZ {nearest['axis_delta']['z']:+.1f}"
            )
        for alignment in state.get("alignments", []):
            reference = (
                "scene centre"
                if alignment["reference_kind"] == "scene_center"
                else alignment["reference_object_id"]
            )
            snapped = " • snapped" if alignment.get("snapped") else ""
            lines.append(
                f"Align {alignment['axis'].upper()}  {alignment['moving_feature']} → "
                f"{reference} {alignment['reference_feature']}  "
                f"Δ {alignment['delta']:+.1f}{snapped}"
            )
        return lines

    def _draw_positioning_guides(self, painter: QPainter) -> None:
        state = self._guide_state
        if not self.guides_enabled or not isinstance(state, dict) or self.scene_data is None:
            return
        selected = self.selected_object()
        if selected is None:
            return

        target = self._scene_target()
        highlight = self.palette().color(QPalette.ColorRole.Highlight)
        painter.setPen(QPen(highlight, 1.5, Qt.PenStyle.DashDotLine))
        extent = 1600.0
        selected_z = float(selected["position"]["z"])
        for alignment in state.get("alignments", []):
            axis = alignment["axis"]
            value = float(alignment["reference_value"])
            if axis == "x":
                first, _depth, _scale = self._project(
                    (value, target[1] - extent, selected_z), target
                )
                second, _depth, _scale = self._project(
                    (value, target[1] + extent, selected_z), target
                )
                painter.drawLine(first, second)
            elif axis == "y":
                first, _depth, _scale = self._project(
                    (target[0] - extent, value, selected_z), target
                )
                second, _depth, _scale = self._project(
                    (target[0] + extent, value, selected_z), target
                )
                painter.drawLine(first, second)

        lines = self.guide_overlay_lines()
        if not lines:
            return
        line_height = 18.0
        box_height = 10.0 + line_height * len(lines)
        box = QRectF(10.0, 34.0, max(200.0, self.width() - 20.0), box_height)
        background = self.palette().color(QPalette.ColorRole.Base)
        background.setAlpha(215)
        painter.fillRect(box, background)
        painter.setPen(self.palette().color(QPalette.ColorRole.Text))
        for index, line in enumerate(lines):
            painter.drawText(
                QRectF(16.0, 38.0 + index * line_height, box.width() - 12.0, line_height),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                line,
            )

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self._draw_positioning_guides(painter)

    def wheelEvent(self, event) -> None:
        """Honor the established explicit 3D-wheel-zoom route without enabling drag orbit."""
        previous_mode = self.interaction_mode
        try:
            self.interaction_mode = "orbit"
            super().wheelEvent(event)
        finally:
            self.interaction_mode = previous_mode
            self.update()

    def mousePressEvent(self, event) -> None:
        self.clear_positioning_guides()
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.interaction_mode in {"move", "rotate", "resize"}
            and self.selected_object_id is not None
            and self._hit_transform_handle(event.position()) is None
            and self._hit_object(event.position()) is None
        ):
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        drag_mode = self._drag_mode
        super().mouseMoveEvent(event)
        if drag_mode != "move" or self._drag_mode != "move":
            self.clear_positioning_guides()
            return
        selected = self.selected_object()
        if selected is None:
            self.clear_positioning_guides()
            return
        guided, guide_state = calculate_positioning_guides(
            selected,
            self._preview_objects,
            self._scene_target(),
            tolerance=self.snap_tolerance,
            snap_enabled=self.snap_enabled,
        )
        if guided != selected:
            self._replace_preview(guided)
        self._guide_state = guide_state if self.guides_enabled else None
        self.update()

    def mouseReleaseEvent(self, event) -> None:
        super().mouseReleaseEvent(event)
        self.clear_positioning_guides()


def _connect_viewport(panel, viewport: GuidedObjectViewport) -> None:
    panel._connect_object_viewport(viewport)


def install_positioning_guides(panel) -> None:
    """Replace the official viewport and install explicit guide controls."""
    old_viewport = panel.object_viewport
    viewport_index = panel.view_stack.indexOf(old_viewport)
    panel.view_stack.removeWidget(old_viewport)
    viewport = GuidedObjectViewport()
    viewport.setMinimumHeight(old_viewport.minimumHeight())
    _connect_viewport(panel, viewport)
    panel.view_stack.insertWidget(max(0, viewport_index), viewport)
    panel.object_viewport = viewport
    if panel.object_scene is not None:
        viewport.set_scene(panel.object_scene, panel.selected_object_id)
    old_viewport.deleteLater()

    panel.guides_action = QAction("Position Guides", panel.view_menu)
    panel.guides_action.setCheckable(True)
    panel.guides_action.setChecked(True)
    panel.guides_action.setToolTip(
        "Show transient centre, edge, nearest-object, and distance evidence only while moving."
    )
    panel.snap_guides_action = QAction("Snap to Guides", panel.view_menu)
    panel.snap_guides_action.setCheckable(True)
    panel.snap_guides_action.setChecked(False)
    panel.snap_guides_action.setToolTip(
        "Explicitly snap X/Y movement within the configured tolerance. Off means guidance only."
    )
    panel.view_menu.addSeparator()
    panel.view_menu.addActions([panel.guides_action, panel.snap_guides_action])

    panel.guide_tolerance_label = QLabel("Guide tolerance")
    panel.guide_tolerance_label.setStyleSheet("font-weight: 600;")
    panel.guide_tolerance_spin = QDoubleSpinBox()
    panel.guide_tolerance_spin.setRange(MIN_SNAP_TOLERANCE, MAX_SNAP_TOLERANCE)
    panel.guide_tolerance_spin.setValue(DEFAULT_SNAP_TOLERANCE)
    panel.guide_tolerance_spin.setDecimals(1)
    panel.guide_tolerance_spin.setSingleStep(1.0)
    panel.guide_tolerance_spin.setSuffix(" units")
    panel.guide_tolerance_spin.setToolTip(
        "Scene-unit threshold used for alignment detection and optional X/Y snapping."
    )
    inspector_layout = panel.inspector.layout()
    inspector_layout.addWidget(panel.guide_tolerance_label, 6, 0)
    inspector_layout.addWidget(panel.guide_tolerance_spin, 6, 1, 1, 3)
    inspector_layout.setRowStretch(7, 1)

    panel.guides_action.triggered.connect(
        lambda _checked=False: apply_positioning_guide_options(panel, announce=True)
    )
    panel.snap_guides_action.triggered.connect(
        lambda _checked=False: apply_positioning_guide_options(panel, announce=True)
    )
    panel.guide_tolerance_spin.valueChanged.connect(
        lambda _value: apply_positioning_guide_options(panel, announce=False)
    )

    original_update_cad_controls = panel._update_cad_controls

    def update_cad_controls_with_guides() -> None:
        original_update_cad_controls()
        update_positioning_guide_controls(panel)

    panel._update_cad_controls = update_cad_controls_with_guides
    apply_positioning_guide_options(panel, announce=False)
    update_positioning_guide_controls(panel)


def apply_positioning_guide_options(panel, *, announce: bool) -> None:
    guides_enabled = panel.guides_action.isChecked()
    if not guides_enabled and panel.snap_guides_action.isChecked():
        panel.snap_guides_action.setChecked(False)
    snap_enabled = guides_enabled and panel.snap_guides_action.isChecked()
    panel.snap_guides_action.setEnabled(guides_enabled and panel.object_scene is not None)
    panel.guide_tolerance_spin.setEnabled(guides_enabled and panel.object_scene is not None)
    panel.object_viewport.set_guide_options(
        guides_enabled=guides_enabled,
        snap_enabled=snap_enabled,
        tolerance=panel.guide_tolerance_spin.value(),
    )
    if announce:
        mode = "guidance with snapping" if snap_enabled else "visual guidance only"
        if not guides_enabled:
            mode = "guides off; snapping off"
        panel.set_status(
            f"Positioning mode: {mode}; tolerance {panel.guide_tolerance_spin.value():.1f} units."
        )


def update_positioning_guide_controls(panel) -> None:
    if not hasattr(panel, "guides_action"):
        return
    has_scene = panel.object_scene is not None
    panel.guides_action.setEnabled(has_scene)
    if not has_scene:
        panel.snap_guides_action.setChecked(False)
        panel.object_viewport.clear_positioning_guides()
    apply_positioning_guide_options(panel, announce=False)
