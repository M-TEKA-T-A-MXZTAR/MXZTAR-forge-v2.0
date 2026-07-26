#!/usr/bin/env python3
"""Persistent Editor options and explicit mouse-wheel routing."""

from __future__ import annotations

from PySide6.QtCore import QEvent, QObject, QPoint, QTimer, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QSizePolicy,
    QTreeWidget,
    QTreeWidgetItem,
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
    """Keep Editor options continuously visible and route wheel events explicitly."""

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
        self._tree_actions: dict[int, object] = {}
        self._tree_items_by_action: dict[int, list[QTreeWidgetItem]] = {}

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

        self.options_label = QLabel("Editor Options", self.bar)
        self.options_label.setStyleSheet("font-weight: 700;")
        self.options_label.setToolTip(
            "The complete Editor action tree remains open and mouse-reachable while the "
            "Editor page or active output moves."
        )

        self.options_tree = QTreeWidget(self.bar)
        self.options_tree.setObjectName("persistentEditorOptionsTree")
        self.options_tree.setHeaderHidden(True)
        self.options_tree.setColumnCount(1)
        self.options_tree.setRootIsDecorated(True)
        self.options_tree.setExpandsOnDoubleClick(False)
        self.options_tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.options_tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.options_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.options_tree.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.options_tree.setMinimumHeight(155)
        self.options_tree.setMaximumHeight(210)
        self.options_tree.setMinimumWidth(310)
        self.options_tree.setToolTip(
            "Persistent Editor commands. Selecting a command never closes this tree or "
            "moves it out of mouse range."
        )
        self.options_tree.itemClicked.connect(self._activate_option_item)

        # Keep a non-popup menu mirror for compatibility with existing verification and
        # action discovery. The user-facing authority is the persistent tree above.
        self.options_menu = QMenu(self.bar)
        self._copy_editor_actions()

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

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)
        header_layout.addWidget(self.options_label)
        header_layout.addSpacing(8)
        header_layout.addWidget(self.mode_label)
        header_layout.addWidget(self.mode_combo)
        header_layout.addWidget(self.mode_help, 1)

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 5, 8, 5)
        layout.setSpacing(5)
        layout.addLayout(header_layout)
        layout.addWidget(self.options_tree)
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
        """Keep the control bar fixed above the scroll viewport, not inside the page."""
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

    def _copy_editor_actions(self) -> None:
        menu_sources = (
            ("Document", self.panel.document_menu),
            ("Shape", self.panel.shape_menu),
            ("Edit", self.panel.edit_menu),
            ("Object", self.panel.object_menu),
            ("View", self.panel.view_menu),
        )
        for title, source in menu_sources:
            mirrored_menu = self.options_menu.addMenu(title)
            group = QTreeWidgetItem([title])
            group.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.options_tree.addTopLevelItem(group)
            for action in source.actions():
                if action.isSeparator():
                    mirrored_menu.addSeparator()
                    continue
                mirrored_menu.addAction(action)
                item = QTreeWidgetItem(group)
                item.setFlags(
                    Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
                )
                self._tree_actions[id(item)] = action
                self._tree_items_by_action.setdefault(id(action), []).append(item)
                self._sync_option_item(item, action)
                action.changed.connect(
                    lambda item=item, action=action: self._sync_option_item(item, action)
                )
        self.options_tree.expandAll()

    @staticmethod
    def _clean_action_text(text: str) -> str:
        return text.replace("&", "").strip()

    def _sync_option_item(self, item: QTreeWidgetItem, action) -> None:
        """Mirror enabled, visible, checked, text, and tooltip state without closing."""
        flags = item.flags() | Qt.ItemFlag.ItemIsSelectable
        flags &= ~Qt.ItemFlag.ItemIsUserCheckable
        if action.isEnabled():
            flags |= Qt.ItemFlag.ItemIsEnabled
        else:
            flags &= ~Qt.ItemFlag.ItemIsEnabled
        item.setFlags(flags)
        base_text = self._clean_action_text(action.text())
        if action.isCheckable():
            prefix = "✓ " if action.isChecked() else "○ "
        else:
            prefix = ""
        item.setText(0, f"{prefix}{base_text}")
        item.setToolTip(0, action.toolTip() or action.statusTip() or base_text)
        item.setHidden(not action.isVisible())

    def _activate_option_item(self, item: QTreeWidgetItem, _column: int = 0) -> None:
        """Trigger one real QAction while preserving the persistent tree and selection."""
        action = self._tree_actions.get(id(item))
        if action is None or not action.isEnabled() or not action.isVisible():
            return
        self.options_tree.setCurrentItem(item)
        action.trigger()
        # Output-reveal commands may move the page, but the tree remains fixed and the
        # selected command remains mouse-reachable inside its own viewport.
        QTimer.singleShot(0, lambda: self.options_tree.scrollToItem(item))

    def option_item_for_action(self, action) -> QTreeWidgetItem | None:
        """Return the first persistent-tree item mirroring an Editor QAction."""
        items = self._tree_items_by_action.get(id(action), ())
        return items[0] if items else None

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
                "or Ctrl+wheel zoom in the persistent selector when needed."
            )
        self.mode_help.setText(help_text)
        self.panel.object_viewport.setToolTip(viewport_tip)
        self.panel.canvas.setToolTip(
            "Project-owned shape canvas. Drag pans the canvas; wheel follows the persistent "
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
