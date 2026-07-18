#!/usr/bin/env python3
"""
MXZTAR Forge v2.0 Qt shell.

Known-good shell wiring:
- Dashboard page
- Start Here page
- Agent Workflows page wired to AgentPanel
- My Library placeholder
- Shape Library placeholder
- Jobs placeholder
- collapsible sidebar with icon-only state
- screen-safe resizable main window
- saved window size and position
- scrollable page area for smaller displays
- no duplicate visible app title
"""

import sys
from pathlib import Path

from PySide6.QtCore import QSettings, QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from core.hardware_profile import apply_local_ai_policy, policy_summary
from core.paths import ensure_project_dirs
from qt_panels.start_here_panel import StartHerePanel
from qt_panels.agent_panel import AgentPanel


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SETTINGS_ORG = "MXZTAR"
SETTINGS_APP = "MXZTAR-Forge-v2.0"
DEFAULT_WINDOW_SIZE = QSize(1080, 680)
MINIMUM_WINDOW_SIZE = QSize(760, 520)
SCREEN_MARGIN_PX = 80


NAV_ITEMS = [
    {
        "icon": "⌂",
        "label": "Dashboard",
        "tooltip": "Dashboard: next step, workflow selection, ZCVIOS levers, and system guidance.",
    },
    {
        "icon": "✎",
        "label": "Start Here",
        "tooltip": "Start Here: project profile, notes, and workflow rules.",
    },
    {
        "icon": "◆",
        "label": "Agent Workflows",
        "tooltip": "Agent Workflows: source discovery and workflow definitions.",
    },
    {
        "icon": "▤",
        "label": "My Library — planned",
        "tooltip": "Planned: concept folders, prompt library, drafts, previews, copy text, open folder.",
    },
    {
        "icon": "◇",
        "label": "Shape Library — planned",
        "tooltip": "Planned: extracted shapes, structures, layers, reusable components.",
    },
    {
        "icon": "⏱",
        "label": "Jobs — planned",
        "tooltip": "Planned: running jobs, elapsed time, logs, failures, retry options.",
    },
]


WORKFLOW_GUIDANCE = {
    "Rebuild foundation": {
        "next": "Next: keep the app shell stable, verify each restored page, then back up working stages.",
        "lever": "ZCVIOS lever: reliability before expansion.",
        "status": "Working. The shell, launcher, and basic persistent folders are restored.",
    },
    "Restore Agent Workflows": {
        "next": "Next: confirm the Agent Workflows page shows source dropdown, workflow selector, and value contracts.",
        "lever": "ZCVIOS lever: useful automation with visible progress.",
        "status": "In progress. Source discovery and workflow definitions should now be visible.",
    },
    "Restore Safe AI Runner": {
        "next": "Next: rebuild Ollama call, QThread worker, elapsed timer, progress messages, and saved outputs.",
        "lever": "ZCVIOS lever: no silent freeze; adaptive hardware-kind AI.",
        "status": "Working baseline. One background-thread workflow can run with truthful final states.",
    },
    "Restore Concept Folders": {
        "next": "Next: create README, source, prompts, notes, and agent_output.json from AI output.",
        "lever": "ZCVIOS lever: reusable production output.",
        "status": "Planned after safe AI runner.",
    },
    "Restore My Library": {
        "next": "Next: scan concept folders, prompt files, web copy drafts, and agent outputs into one panel.",
        "lever": "ZCVIOS lever: reduce lost work and file hunting.",
        "status": "Planned.",
    },
}


def screen_safe_default_size() -> QSize:
    """Return a default size that should fit inside the current primary screen."""
    screen = QApplication.primaryScreen()

    if screen is None:
        return DEFAULT_WINDOW_SIZE

    available = screen.availableGeometry()
    max_width = max(MINIMUM_WINDOW_SIZE.width(), available.width() - SCREEN_MARGIN_PX)
    max_height = max(MINIMUM_WINDOW_SIZE.height(), available.height() - SCREEN_MARGIN_PX)

    return QSize(
        min(DEFAULT_WINDOW_SIZE.width(), max_width),
        min(DEFAULT_WINDOW_SIZE.height(), max_height),
    )


class DashboardPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.workflow_selector = QComboBox()
        self.workflow_selector.addItems(WORKFLOW_GUIDANCE.keys())
        self.workflow_selector.currentTextChanged.connect(self.update_guidance)

        self.next_label = QLabel()
        self.next_label.setWordWrap(True)
        self.next_label.setStyleSheet("font-size: 17px; font-weight: 700; color: #f0e1a0;")

        self.lever_label = QLabel()
        self.lever_label.setWordWrap(True)
        self.lever_label.setStyleSheet("font-size: 14px; color: #d6d6d6;")

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("font-size: 14px; color: #cfcfcf;")

        ai_policy = apply_local_ai_policy()
        policy_label = QLabel(f"Adaptive hardware policy: {policy_summary(ai_policy)}")
        policy_label.setWordWrap(True)
        policy_label.setStyleSheet("font-size: 13px; color: #bfbfbf;")

        selector_row = QHBoxLayout()
        selector_title = QLabel("Workflow:")
        selector_title.setStyleSheet("font-weight: 700;")
        selector_row.addWidget(selector_title)
        selector_row.addWidget(self.workflow_selector, 1)

        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet(
            "QFrame {"
            "background-color: #252525;"
            "border: 1px solid #3a3a3a;"
            "border-radius: 10px;"
            "padding: 12px;"
            "}"
        )

        card_layout = QVBoxLayout()
        card_layout.addLayout(selector_row)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.next_label)
        card_layout.addWidget(self.lever_label)
        card_layout.addWidget(self.status_label)
        card_layout.addSpacing(8)
        card_layout.addWidget(policy_label)
        card.setLayout(card_layout)

        zcvios_title = QLabel("ZCVIOS lever identification")
        zcvios_title.setStyleSheet("font-size: 18px; font-weight: 700;")

        zcvios_body = QLabel(
            "Each workflow must serve a clear lever: reliability, safe automation, useful output, "
            "audit trail, hardware kindness, reusable assets, market/audience value, or reduced friction."
        )
        zcvios_body.setWordWrap(True)
        zcvios_body.setStyleSheet("color: #cfcfcf;")

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.addWidget(card)
        layout.addSpacing(16)
        layout.addWidget(zcvios_title)
        layout.addWidget(zcvios_body)
        layout.addStretch(1)
        self.setLayout(layout)

        self.update_guidance(self.workflow_selector.currentText())

    def update_guidance(self, workflow_name: str):
        guidance = WORKFLOW_GUIDANCE.get(workflow_name, {})
        self.next_label.setText(guidance.get("next", "Next: choose a workflow."))
        self.lever_label.setText(guidance.get("lever", "ZCVIOS lever: not identified."))
        self.status_label.setText(guidance.get("status", "Status: unknown."))


class PlaceholderPanel(QWidget):
    def __init__(self, title: str, detail: str):
        super().__init__()

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: 700;")

        detail_label = QLabel(detail)
        detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        detail_label.setWordWrap(True)
        detail_label.setStyleSheet("font-size: 14px; color: #cfcfcf;")

        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(title_label)
        layout.addWidget(detail_label)
        layout.addStretch(1)
        self.setLayout(layout)


class MXZTARForgeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ensure_project_dirs()
        self.ai_policy = apply_local_ai_policy()

        self.settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
        self.sidebar_collapsed = False

        self.setWindowTitle("MXZTAR Forge v2.0")
        self.setMinimumSize(MINIMUM_WINDOW_SIZE)
        self.resize(screen_safe_default_size())

        self.pages = QStackedWidget()

        self.dashboard_panel = DashboardPanel()

        self.start_here_panel = StartHerePanel()
        self.start_here_panel.status_changed.connect(self.set_status)

        self.agent_panel = AgentPanel()
        self.agent_panel.status_changed.connect(self.set_status)

        self.library_panel = PlaceholderPanel(
            "My Library",
            "Planned: concept folders, my prompts, web copy drafts, agent outputs, preview, copy text, and open folder."
        )

        self.shape_panel = PlaceholderPanel(
            "Shape / Structure Extraction",
            "Planned: extract shapes, layers, structures, visual systems, reusable modules, and component candidates."
        )

        self.jobs_panel = PlaceholderPanel(
            "Jobs",
            "Planned: visible job state, elapsed time, logs, failures, retry options, and completed output records."
        )

        self.pages.addWidget(self.dashboard_panel)
        self.pages.addWidget(self.start_here_panel)
        self.pages.addWidget(self.agent_panel)
        self.pages.addWidget(self.library_panel)
        self.pages.addWidget(self.shape_panel)
        self.pages.addWidget(self.jobs_panel)

        self.page_scroll = QScrollArea()
        self.page_scroll.setWidgetResizable(True)
        self.page_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.page_scroll.setWidget(self.pages)

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setToolTip("Navigation. Planned panels are marked clearly.")
        self.sidebar.currentRowChanged.connect(self.pages.setCurrentIndex)

        for nav in NAV_ITEMS:
            item = QListWidgetItem(f"{nav['icon']}  {nav['label']}")
            item.setToolTip(nav["tooltip"])
            self.sidebar.addItem(item)

        self.sidebar.setCurrentRow(0)

        self.collapse_button = QPushButton("‹")
        self.collapse_button.setFixedWidth(34)
        self.collapse_button.setToolTip("Collapse sidebar to icon-only navigation.")
        self.collapse_button.clicked.connect(self.toggle_sidebar)

        sidebar_top = QHBoxLayout()
        sidebar_top.addStretch(1)
        sidebar_top.addWidget(self.collapse_button)

        side_layout = QVBoxLayout()
        side_layout.setContentsMargins(6, 6, 6, 6)
        side_layout.addLayout(sidebar_top)
        side_layout.addWidget(self.sidebar)

        self.side_container = QWidget()
        self.side_container.setLayout(side_layout)
        self.side_container.setStyleSheet("background-color: #181818;")

        self.status_label = QLabel(
            f"Ready. Adaptive AI policy: {policy_summary(self.ai_policy)}. Root: {PROJECT_ROOT}"
        )
        self.status_label.setStyleSheet("padding: 8px; color: #d6c27a;")

        main_row = QHBoxLayout()
        main_row.addWidget(self.side_container)
        main_row.addWidget(self.page_scroll, 1)

        main_column = QVBoxLayout()
        main_column.addLayout(main_row, 1)
        main_column.addWidget(self.status_label)

        root = QWidget()
        root.setLayout(main_column)
        root.setStyleSheet(
            "background-color: #202020;"
            "color: #f2f2f2;"
            "font-family: Sans Serif;"
        )

        self.setCentralWidget(root)
        self.restore_window_geometry()

    def closeEvent(self, event):
        if self.agent_panel.has_active_job():
            self.set_status(
                "A local AI workflow is still running. Wait for it to finish before closing."
            )
            event.ignore()
            return

        self.settings.setValue("main_window/geometry", self.saveGeometry())
        event.accept()

    def restore_window_geometry(self) -> None:
        saved_geometry = self.settings.value("main_window/geometry")

        if saved_geometry is not None and self.restoreGeometry(saved_geometry):
            return

        self.resize(screen_safe_default_size())
        self.center_on_primary_screen()

    def center_on_primary_screen(self) -> None:
        screen = QApplication.primaryScreen()

        if screen is None:
            return

        available = screen.availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(available.center())
        self.move(frame.topLeft())

    def closeEvent(self, event):
        self.settings.setValue("main_window/geometry", self.saveGeometry())
        super().closeEvent(event)

    def toggle_sidebar(self):
        self.sidebar_collapsed = not self.sidebar_collapsed

        if self.sidebar_collapsed:
            self.sidebar.setFixedWidth(52)
            self.side_container.setFixedWidth(64)
            self.collapse_button.setText("›")
            self.collapse_button.setToolTip("Restore full sidebar navigation.")

            for index, nav in enumerate(NAV_ITEMS):
                item = self.sidebar.item(index)
                item.setText(nav["icon"])
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setToolTip(nav["tooltip"])
        else:
            self.sidebar.setFixedWidth(220)
            self.side_container.setFixedWidth(232)
            self.collapse_button.setText("‹")
            self.collapse_button.setToolTip("Collapse sidebar to icon-only navigation.")

            for index, nav in enumerate(NAV_ITEMS):
                item = self.sidebar.item(index)
                item.setText(f"{nav['icon']}  {nav['label']}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                item.setToolTip(nav["tooltip"])

    def set_status(self, message: str):
        self.status_label.setText(
            f"{message} Adaptive AI policy: {policy_summary(self.ai_policy)}."
        )


def main() -> int:
    app = QApplication(sys.argv)
    app.setOrganizationName(SETTINGS_ORG)
    app.setApplicationName(SETTINGS_APP)
    window = MXZTARForgeWindow()
    window.show()
    return app.exec()
