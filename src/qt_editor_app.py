#!/usr/bin/env python3
"""Editor-first MXZTAR Forge shell built on the verified Qt application baseline."""

from __future__ import annotations

import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QListWidgetItem

from qt_app import MXZTARForgeWindow, NAV_ITEMS, SETTINGS_APP, SETTINGS_ORG
from qt_panels.editor_panel import EditorPanel


EDITOR_PAGE_INDEX = 2
AGENT_PAGE_INDEX = 3
LIBRARY_PAGE_INDEX = 4
SHAPE_LIBRARY_PAGE_INDEX = 5
JOBS_PAGE_INDEX = 6
EDITOR_NAV = {
    "icon": "✦",
    "label": "Editor",
    "tooltip": "Editor: create and edit project-owned native shape documents.",
}


def _install_editor_navigation_contract() -> None:
    if any(item.get("label") == "Editor" for item in NAV_ITEMS):
        return
    NAV_ITEMS.insert(EDITOR_PAGE_INDEX, EDITOR_NAV)


class EditorForgeWindow(MXZTARForgeWindow):
    """Add the Level One Editor without weakening the verified legacy workspaces."""

    def __init__(self, project_session=None):
        _install_editor_navigation_contract()
        super().__init__(project_session)

        self.editor_panel = EditorPanel(self.project_session)
        self.editor_panel.status_changed.connect(self.set_status)
        self.pages.insertWidget(EDITOR_PAGE_INDEX, self.editor_panel)
        self.start_here_panel.project_changed.connect(self.editor_panel.set_project_state)
        self.editor_panel.set_project_state(self.project_session.state)

        editor_item = self.sidebar.item(EDITOR_PAGE_INDEX)
        if editor_item is None or "Editor" not in editor_item.text():
            item = QListWidgetItem(f"{EDITOR_NAV['icon']}  {EDITOR_NAV['label']}")
            item.setToolTip(EDITOR_NAV["tooltip"])
            self.sidebar.insertItem(EDITOR_PAGE_INDEX, item)

    def open_guided_import(self) -> None:
        self._open_guided_page(LIBRARY_PAGE_INDEX)
        QTimer.singleShot(0, self.library_panel.choose_project_source)

    def run_guided_workflow(self) -> None:
        self._open_guided_page(AGENT_PAGE_INDEX)
        self.agent_panel.start_selected_workflow()

    def open_guided_jobs(self) -> None:
        self._guided_evidence_ready = False
        self._open_guided_page(JOBS_PAGE_INDEX)
        self.jobs_panel.refresh_jobs()
        self.refresh_guided_next_step()

    def accept_reopened_project_sources(self, sources) -> None:
        if not self._awaiting_project_resume:
            return
        self._awaiting_project_resume = False
        if not sources:
            self.refresh_guided_next_step()
            return
        item = sources[0]
        if self.agent_panel.select_source_item(item):
            self._open_guided_page(AGENT_PAGE_INDEX)
            self.refresh_guided_next_step()
            self.set_status(f"Resumed project source in Agent Workflows: {item.path.name}.")

    def accept_guided_project_source(self, item) -> None:
        if self.agent_panel.select_source_item(item):
            self._guided_evidence_ready = False
            self._open_guided_page(AGENT_PAGE_INDEX)
            self.refresh_guided_next_step()
            self.set_status(
                f"Imported source selected in Agent Workflows: {item.path.name}. "
                "Choose any workflow, then use the pulsing Next control."
            )

    def open_library_source_in_agent_panel(self, item):
        if self.agent_panel.select_source_item(item):
            self._guided_evidence_ready = False
            self.pages.setCurrentIndex(AGENT_PAGE_INDEX)
            self.sidebar.setCurrentRow(AGENT_PAGE_INDEX)
            self.set_status(f"Opened library source in Agent Workflows: {item.path.name}")
            self.refresh_guided_next_step()

    def open_page(self, index: int):
        self.pages.setCurrentIndex(index)
        if index == EDITOR_PAGE_INDEX:
            self.editor_panel.refresh_documents()
        elif index == SHAPE_LIBRARY_PAGE_INDEX:
            self.shape_panel.ensure_loaded()


def main() -> int:
    app = QApplication(sys.argv)
    app.setOrganizationName(SETTINGS_ORG)
    app.setApplicationName(SETTINGS_APP)
    window = EditorForgeWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
