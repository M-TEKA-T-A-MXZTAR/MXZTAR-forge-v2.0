#!/usr/bin/env python3
"""Pinned Editor options and explicit mouse-wheel routing."""

from __future__ import annotations

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QSizePolicy,
    QToolButton,
)


WHEEL_MODE_SCROLL = "scroll_page"
WHEEL_MODE_ZOOM = "zoom_3d"
WHEEL_MODE_SCROLL_CTRL_ZOOM = "scroll_page_ctrl_zoom"
WHEEL_MODE_SETTING = "editor/mouse_wheel_mode"
VALID_WHEEL_MODES = {
    WHEEL_MODE_SCROLL,
    WHEEL_MODE_ZOOM,
    WHEEL_MODE_SCROLL_CTRL_ZOOM,
}


class EditorMouseWheelController(QObject):
    """Keep Editor options visible and route output-wheel events deliberately."""

    def __init__(self, window, panel):
        super().__init__(window)
        self.window = window
        self.panel = panel
        self.page_scroll = window.page_scroll
        self._output_targets = (
            panel.canvas,
            panel.canvas.viewport(),
            panel.object_viewport,
        )

        self.bar = QFrame(window.centralWidget())
        self.bar.setObjectName("editorInteractionBar")
        self.bar.setFrameShape(QFrame.Shape.StyledPanel)
        self.bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.options_button = QToolButton(self.bar)
        self.options_button.setText("Editor Options")
        self.options_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.options_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.options_button.setToolTip(
            "Pinned access to the Editor action tree while the page is scrolled."
        )
        self.options_menu = QMenu(self.options_button)
        self._copy_editor_menus()
        self.options_button.setMenu(self.options_menu)

        self.mode_label = QLabel("Mouse wheel:", self.bar)
        self.mode_label.setStyleSheet("font-weight: 700;")
        self.mode_combo = QComboBox(self.bar)
        self.mode_combo.setObjectName("editorMouseWheelMode")
        self.mode_combo.addItem("Scroll page", WHEEL_MODE_SCROLL)
        self.mode_combo.addItem("Zoom 3D view", WHEEL_MODE_ZOOM)
        self.mode_combo.addItem(
            "Scroll page; Ctrl+wheel zoom",
            WHEEL_MODE_SCROLL_CTRL_ZOOM,
        )
        self.mode_combo.setToolTip(
            "Choose what the mouse wheel does over the 2D or 3D output. "
            "Page scrolling is the safe default."
        )

        self.mode_help = QLabel(self.bar)
        self.mode_help.setWordWrap(True)
        self.mode_help.setStyleSheet("color: #cfcfcf;")

        layout = QHBoxLayout()
        layout.setContentsMargins(8, 5, 8, 5)
        layout.setSpacing(8)
        layout.addWidget(self.options_button)
        layout.addSpacing(8)
        layout.addWidget(self.mode_label)
        layout.addWidget(self.mode_combo)
        layout.addWidget(self.mode_help, 1)
        self.bar.setLayout(layout)

        central_layout = window.centralWidget().layout()
        central_layout.insertWidget(1, self.bar)

        for target in self._output_targets:
            target.installEventFilter(self)
        self.mode_combo.currentIndexChanged.connect(self._mode_changed)
        window.pages.currentChanged.connect(self._update_visibility)

        stored_mode = str(window.settings.value(WHEEL_MODE_SETTING, WHEEL_MODE_SCROLL))
        self.set_mode(
            stored_mode if stored_mode in VALID_WHEEL_MODES else WHEEL_MODE_SCROLL,
            announce=False,
        )
        self._update_visibility()

    def _copy_editor_menus(self) -> None:
        menu_sources = (
            ("Document", self.panel.document_menu),
            ("Shape", self.panel.shape_menu),
            ("Edit", self.panel.edit_menu),
            ("Object", self.panel.object_menu),
            ("View", self.panel.view_menu),
        )
        for title, source in menu_sources:
            target = self.options_menu.addMenu(title)
            for action in source.actions():
                if action.isSeparator():
                    target.addSeparator()
                else:
                    target.addAction(action)

    def _update_visibility(self, *_args) -> None:
        self.bar.setVisible(self.window.pages.currentWidget() is self.panel)

    def current_mode(self) -> str:
        mode = self.mode_combo.currentData()
        return mode if mode in VALID_WHEEL_MODES else WHEEL_MODE_SCROLL

    def set_mode(self, mode: str, *, announce: bool = True) -> None:
        if mode not in VALID_WHEEL_MODES:
            mode = WHEEL_MODE_SCROLL
        index = self.mode_combo.findData(mode)
        signals_were_blocked = self.mode_combo.blockSignals(True)
        try:
            self.mode_combo.setCurrentIndex(max(0, index))
        finally:
            self.mode_combo.blockSignals(signals_were_blocked)
        self.window.settings.setValue(WHEEL_MODE_SETTING, mode)
        self._refresh_mode_copy()
        if announce:
            self.panel.set_status(self._status_text(mode))

    def _mode_changed(self, _index: int) -> None:
        self.set_mode(self.current_mode(), announce=True)

    @staticmethod
    def _status_text(mode: str) -> str:
        if mode == WHEEL_MODE_ZOOM:
            return (
                "Mouse wheel mode: zoom the 3D output; wheel over the 2D output still "
                "scrolls the page."
            )
        if mode == WHEEL_MODE_SCROLL_CTRL_ZOOM:
            return (
                "Mouse wheel mode: scroll the page; hold Ctrl over the 3D output to zoom."
            )
        return "Mouse wheel mode: scroll the Editor page from either output."

    def _refresh_mode_copy(self) -> None:
        mode = self.current_mode()
        if mode == WHEEL_MODE_ZOOM:
            help_text = "Wheel over 3D zooms; wheel over 2D scrolls."
            viewport_tip = (
                "3D object view: drag objects to move, drag empty space to orbit, "
                "and use the wheel to zoom in the selected wheel mode."
            )
        elif mode == WHEEL_MODE_SCROLL_CTRL_ZOOM:
            help_text = "Wheel scrolls; hold Ctrl over 3D to zoom."
            viewport_tip = (
                "3D object view: wheel scrolls the page; hold Ctrl while wheeling to zoom."
            )
        else:
            help_text = "Wheel scrolls the page from the 2D or 3D output."
            viewport_tip = (
                "3D object view: wheel scrolls the Editor page. Choose Zoom 3D view "
                "or Ctrl+wheel zoom in the pinned selector when needed."
            )
        self.mode_help.setText(help_text)
        self.panel.object_viewport.setToolTip(viewport_tip)
        self.panel.canvas.setToolTip(
            "Project-owned shape canvas. Drag pans the canvas; wheel follows the pinned "
            "Editor mouse-wheel setting."
        )

    def _should_zoom_3d(self, watched, event) -> bool:
        if watched is not self.panel.object_viewport:
            return False
        mode = self.current_mode()
        if mode == WHEEL_MODE_ZOOM:
            return True
        return bool(
            mode == WHEEL_MODE_SCROLL_CTRL_ZOOM
            and event.modifiers() & Qt.KeyboardModifier.ControlModifier
        )

    def _scroll_page(self, event) -> None:
        scrollbar = self.page_scroll.verticalScrollBar()
        pixel_delta = event.pixelDelta().y()
        if pixel_delta:
            distance = float(pixel_delta)
        else:
            angle_delta = event.angleDelta().y()
            step = max(48.0, float(scrollbar.singleStep()) * 3.0)
            distance = (float(angle_delta) / 120.0) * step
        scrollbar.setValue(scrollbar.value() - round(distance))
        event.accept()

    def eventFilter(self, watched, event) -> bool:
        if event.type() != QEvent.Type.Wheel or watched not in self._output_targets:
            return False
        if self._should_zoom_3d(watched, event):
            return False
        self._scroll_page(event)
        return True
