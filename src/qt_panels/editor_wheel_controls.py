#!/usr/bin/env python3
"""Compact Editor command strip and explicit mouse-wheel routing."""

from __future__ import annotations

from PySide6.QtCore import QEvent, QObject, QPoint, QTimer, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
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
    """Keep compact Editor menus visible and route wheel events explicitly."""

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

        self.viewport_column = QWidget(window.centralWidget())
        self.viewport_column.setObjectName("editorViewportColumn")
        self.viewport_column.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.bar = QFrame(self.viewport_column)
        self.bar.setObjectName("editorInteractionBar")
        self.bar.setFrameShape(QFrame.Shape.StyledPanel)
        self.bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.bar.setMaximumHeight(48)

        # Preserve a non-visual aggregate menu for action discovery and compatibility,
        # while the user-facing authority is the compact row of category buttons.
        self.options_menu = QMenu(self.bar)
        self.menu_buttons: dict[str, QToolButton] = {}
        self._build_editor_menu_buttons()

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
        self.mode_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        layout = QHBoxLayout()
        layout.setContentsMargins(6, 3, 6, 3)
        layout.setSpacing(4)
        for title in ("Document", "Shape", "Edit", "Object", "View"):
            layout.addWidget(self.menu_buttons[title])
        layout.addStretch(1)
        layout.addWidget(self.mode_label)
        layout.addWidget(self.mode_combo)
        self.bar.setLayout(layout)

        self._install_sticky_viewport_column()

        for target in self._output_targets:
            target.installEventFilter(self)
        self.mode_combo.currentIndexChanged.connect(self._mode_changed)
        window.pages.currentChanged.connect(self._update_visibility)
        panel.view_stack.currentChanged.connect(self._active_output_changed)
        # currentChanged is silent when an already-active stacked widget is selected.
        # Listen to the explicit View actions as well so every user selection reveals
        # the requested output, even when the output itself did not change.
        panel.view_2d_action.triggered.connect(self._active_output_selected)
        panel.view_3d_action.triggered.connect(self._active_output_selected)

        stored_mode = str(window.settings.value(WHEEL_MODE_SETTING, WHEEL_MODE_SCROLL))
        self.set_mode(
            stored_mode if stored_mode in VALID_WHEEL_MODES else WHEEL_MODE_SCROLL,
            announce=False,
        )
        self._update_visibility()

    def _install_sticky_viewport_column(self) -> None:
        """Keep the compact strip fixed above the scroll viewport, not inside the page."""
        central = self.window.centralWidget()
        central_layout = central.layout()
        main_row_item = central_layout.itemAt(0) if central_layout is not None else None
        main_row = main_row_item.layout() if main_row_item is not None else None
        if main_row is None:
            raise RuntimeError("Forge main content row is unavailable for sticky Editor controls.")

        page_index = main_row.indexOf(self.page_scroll)
        if page_index < 0:
            raise RuntimeError("Forge page scroll area is not present in the main content row.")

        main_row.removeWidget(self.page_scroll)

        column_layout = QVBoxLayout()
        column_layout.setContentsMargins(0, 0, 0, 0)
        column_layout.setSpacing(0)
        column_layout.addWidget(self.bar)
        column_layout.addWidget(self.page_scroll, 1)
        self.viewport_column.setLayout(column_layout)

        main_row.insertWidget(page_index, self.viewport_column, 1)

    def _build_editor_menu_buttons(self) -> None:
        menu_sources = (
            ("Document", self.panel.document_menu),
            ("Shape", self.panel.shape_menu),
            ("Edit", self.panel.edit_menu),
            ("Object", self.panel.object_menu),
            ("View", self.panel.view_menu),
        )
        for title, source in menu_sources:
            button = QToolButton(self.bar)
            button.setObjectName(f"editor{title}MenuButton")
            button.setText(title)
            button.setAutoRaise(True)
            button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
            button.setMenu(source)
            button.setToolTip(f"Open {title} commands. The menu closes after selection.")
            self.menu_buttons[title] = button

            mirrored_menu = self.options_menu.addMenu(title)
            for action in source.actions():
                if action.isSeparator():
                    mirrored_menu.addSeparator()
                else:
                    mirrored_menu.addAction(action)

    def menu_button(self, title: str) -> QToolButton | None:
        """Return one compact top-level Editor menu button for verification and access."""
        return self.menu_buttons.get(title)

    def _update_visibility(self, *_args) -> None:
        editor_active = self.window.pages.currentWidget() is self.panel
        self.bar.setVisible(editor_active)
        if editor_active:
            QTimer.singleShot(0, self._reveal_active_output)

    def _active_output_changed(self, *_args) -> None:
        """Bring a newly selected 2D or 3D output into the visible page range."""
        QTimer.singleShot(0, self._reveal_active_output)

    def _active_output_selected(self, *_args) -> None:
        """Reveal an explicitly selected output even when it was already active."""
        QTimer.singleShot(0, self._reveal_active_output)

    def _reveal_active_output(self) -> None:
        if self.window.pages.currentWidget() is not self.panel:
            return
        target = self.panel.view_stack.currentWidget()
        content = self.page_scroll.widget()
        if target is None or content is None:
            return
        target_top = target.mapTo(content, QPoint(0, 0)).y()
        scrollbar = self.page_scroll.verticalScrollBar()
        desired = target_top - 12
        scrollbar.setValue(
            max(scrollbar.minimum(), min(scrollbar.maximum(), desired))
        )

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
                "or Ctrl+wheel zoom in the compact selector when needed."
            )
        self.mode_combo.setToolTip(
            f"{help_text} Page scrolling is the safe default."
        )
        self.panel.object_viewport.setToolTip(viewport_tip)
        self.panel.canvas.setToolTip(
            "Project-owned shape canvas. Drag pans the canvas; wheel follows the compact "
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

    def _zoom_3d(self, event) -> None:
        """Deliver zoom once and consume it before the page scroll area sees it."""
        self.panel.object_viewport.wheelEvent(event)
        event.accept()

    def eventFilter(self, watched, event) -> bool:
        if event.type() != QEvent.Type.Wheel or watched not in self._output_targets:
            return False
        if self._should_zoom_3d(watched, event):
            self._zoom_3d(event)
            return True
        self._scroll_page(event)
        return True
