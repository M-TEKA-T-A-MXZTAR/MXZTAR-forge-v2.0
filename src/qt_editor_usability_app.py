#!/usr/bin/env python3
"""Official Forge shell with current-page sizing and the single-object CAD workspace."""

from __future__ import annotations

import sys

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QStackedWidget

from qt_app import SETTINGS_APP, SETTINGS_ORG
from qt_editor_app import START_HERE_PAGE_INDEX, EditorForgeWindow
from qt_panels.editor_usability_panel import SingleObjectWorkspacePanel


class CurrentPageStack(QStackedWidget):
    """Report geometry for the visible page instead of the tallest hidden page."""

    def __init__(self):
        super().__init__()
        self.currentChanged.connect(lambda _index: self.updateGeometry())

    def sizeHint(self) -> QSize:
        current = self.currentWidget()
        if current is not None:
            hint = current.sizeHint()
            if hint.isValid():
                return hint
        return super().sizeHint()

    def minimumSizeHint(self) -> QSize:
        current = self.currentWidget()
        if current is not None:
            hint = current.minimumSizeHint()
            if hint.isValid():
                return hint
        return super().minimumSizeHint()


class UsableEditorForgeWindow(EditorForgeWindow):
    """Use current-page sizing and a pinned, single-object Editor workspace."""

    def __init__(self, project_session=None):
        super().__init__(project_session)
        self._install_current_page_stack()
        self._replace_editor_panel()
        self.pages.setCurrentIndex(START_HERE_PAGE_INDEX)
        self.sidebar.setCurrentRow(START_HERE_PAGE_INDEX)
        self.page_scroll.verticalScrollBar().setValue(0)
        self.refresh_guided_next_step()

    def _install_current_page_stack(self) -> None:
        old_pages = self.pages
        current_index = old_pages.currentIndex()
        widgets = []
        while old_pages.count():
            widget = old_pages.widget(0)
            old_pages.removeWidget(widget)
            widgets.append(widget)

        detached = self.page_scroll.takeWidget()
        pages = CurrentPageStack()
        for widget in widgets:
            pages.addWidget(widget)
        self.page_scroll.setWidget(pages)
        self.pages = pages
        self.pages.setCurrentIndex(max(0, current_index))
        if detached is not None:
            detached.deleteLater()

    def _replace_editor_panel(self) -> None:
        old_editor = self.editor_panel
        editor_index = self.pages.indexOf(old_editor)
        try:
            self.start_here_panel.project_changed.disconnect(old_editor.set_project_state)
        except (RuntimeError, TypeError):
            # Safe during replacement: the connection may already be absent or its QObject destroyed.
            pass

        self.pages.removeWidget(old_editor)
        editor = SingleObjectWorkspacePanel(self.project_session)
        editor.status_changed.connect(self.set_status)
        self.pages.insertWidget(editor_index, editor)
        self.editor_panel = editor
        self.start_here_panel.project_changed.connect(editor.set_project_state)
        editor.set_project_state(self.project_session.state)
        old_editor.deleteLater()

    def _reset_page_scroll(self) -> None:
        self.pages.updateGeometry()
        self.page_scroll.verticalScrollBar().setValue(0)
        self.page_scroll.horizontalScrollBar().setValue(0)

    def _open_guided_page(self, page_index: int) -> None:
        super()._open_guided_page(page_index)
        self._reset_page_scroll()

    def open_page(self, index: int):
        super().open_page(index)
        self._reset_page_scroll()


def main() -> int:
    app = QApplication(sys.argv)
    app.setOrganizationName(SETTINGS_ORG)
    app.setApplicationName(SETTINGS_APP)
    window = UsableEditorForgeWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
