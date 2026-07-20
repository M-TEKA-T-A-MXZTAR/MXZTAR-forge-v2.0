#!/usr/bin/env python3
"""
MXZTAR Forge v2.0 Qt shell.

Known-good shell wiring:
- Dashboard page
- Start Here page
- Agent Workflows page wired to AgentPanel
- My Library source-art browser wired to Agent Workflows
- read-only Shape Library evidence browser
- read-only Jobs record browser
- collapsible sidebar with icon-only state
- screen-safe resizable main window
- saved window size and position
- scrollable page area for smaller displays
- no duplicate visible app title
"""

import sys
from pathlib import Path

from PySide6.QtCore import QSettings, QSize, Qt, QTimer
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
from core.project_session import ProjectSession
from core.source_library import SourceArtItem
from qt_panels.start_here_panel import StartHerePanel
from qt_panels.agent_panel import AgentPanel
from qt_panels.my_library_panel import MyLibraryPanel
from qt_panels.jobs_panel import JobsPanel
from qt_panels.shape_library_panel import ShapeLibraryPanel


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
        "label": "My Library",
        "tooltip": "My Library: preview known source art and send a deliberate selection to Agent Workflows.",
    },
    {
        "icon": "◇",
        "label": "Shape Library",
        "tooltip": "Shape Library: inspect raw shape-harvest evidence and its approval boundary.",
    },
    {
        "icon": "⏱",
        "label": "Jobs",
        "tooltip": "Jobs: inspect saved successes, failure diagnostics, and invalid legacy records.",
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
        "next": "Next: verify the threaded runner with a compatible source, then address image preflight and cooperative cancellation.",
        "lever": "ZCVIOS lever: no silent freeze; adaptive hardware-kind AI.",
        "status": "Working baseline. One background-thread workflow can run with truthful final states.",
    },
    "Restore Concept Folders": {
        "next": "Next: create README, source, prompts, notes, and agent_output.json from AI output.",
        "lever": "ZCVIOS lever: reusable production output.",
        "status": "Planned after safe AI runner.",
    },
    "Restore My Library": {
        "next": "Next: choose known source art in My Library and send it to Agent Workflows.",
        "lever": "ZCVIOS lever: deliberate source selection without file duplication.",
        "status": "Working source-art baseline. Durable workflow outputs remain a later project-contract stage.",
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


class MXZTARForgeWindow(QMainWindow):
    def __init__(self, project_session: ProjectSession | None = None):
        super().__init__()

        ensure_project_dirs()
        self.ai_policy = apply_local_ai_policy()

        self.settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
        self.sidebar_collapsed = False
        self._close_when_background_idle = False
        self._guided_action = None
        self._guided_target = None
        self._guided_target_style = ""
        self._guided_pulse_on = False
        self._guided_evidence_ready = False
        self._guided_project_name_edited = False
        self._awaiting_project_resume = bool(
            project_session is not None and project_session.state is not None
        )
        self.project_session = project_session or ProjectSession()

        self.setWindowTitle("MXZTAR Forge v2.0")
        self.setMinimumSize(MINIMUM_WINDOW_SIZE)
        self.resize(screen_safe_default_size())

        self.pages = QStackedWidget()

        self.dashboard_panel = DashboardPanel()

        self.start_here_panel = StartHerePanel(self.project_session)
        self.start_here_panel.status_changed.connect(self.set_status)
        self.start_here_panel.profile_fields["project_name"].textChanged.connect(
            self.handle_guided_project_name_edited
        )
        self.start_here_panel.project_selector.currentIndexChanged.connect(
            lambda _index: self.refresh_guided_next_step()
        )

        self.agent_panel = AgentPanel(self.project_session)
        self.agent_panel.status_changed.connect(self.set_status)
        self.agent_panel.job_active_changed.connect(
            lambda active: self.start_here_panel.set_project_mutation_active(
                active, "local AI workflow"
            )
        )

        self.library_panel = MyLibraryPanel(self.project_session)
        self.library_panel.status_changed.connect(self.set_status)
        self.library_panel.source_selected.connect(self.open_library_source_in_agent_panel)
        self.library_panel.background_idle.connect(self.finish_deferred_close)
        self.library_panel.background_idle.connect(self.refresh_guided_next_step)
        self.library_panel.background_active.connect(self.refresh_guided_next_step)
        self.library_panel.intake_active_changed.connect(
            lambda _active: self.refresh_guided_next_step()
        )
        self.library_panel.project_source_ready.connect(
            self.accept_guided_project_source
        )
        self.library_panel.project_sources_discovered.connect(
            self.accept_reopened_project_sources
        )
        self.library_panel.intake_active_changed.connect(
            self.start_here_panel.set_project_mutation_active
        )
        self.library_panel.project_authority_changed.connect(
            self.start_here_panel.refresh_attached_project_state
        )
        self.start_here_panel.project_changed.connect(self.library_panel.set_project_state)
        self.start_here_panel.project_changed.connect(self.agent_panel.set_project_state)
        self.start_here_panel.project_changed.connect(self.handle_guided_project_changed)
        self.agent_panel.set_project_state(self.project_session.state)

        self.shape_panel = ShapeLibraryPanel()
        self.shape_panel.status_changed.connect(self.set_status)
        self.shape_panel.background_idle.connect(self.finish_deferred_close)

        self.jobs_panel = JobsPanel(self.project_session)
        self.jobs_panel.status_changed.connect(self.set_status)
        self.jobs_panel.background_idle.connect(self.finish_deferred_close)
        self.agent_panel.job_record_saved.connect(self.jobs_panel.refresh_jobs)
        self.agent_panel.job_record_saved.connect(self.guide_to_saved_evidence)
        self.agent_panel.job_active_changed.connect(self.handle_guided_job_active)
        self.agent_panel.workflow_combo.currentTextChanged.connect(
            lambda _text: self.refresh_guided_next_step()
        )
        self.start_here_panel.project_changed.connect(self.jobs_panel.set_project_state)

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
        self.sidebar.currentRowChanged.connect(self.open_page)

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

        self.next_step_button = QPushButton("Next: Start Here")
        self.next_step_button.setToolTip(
            "Guided next action. Heavy AI work still requires this explicit click."
        )
        self.next_step_button.clicked.connect(self.perform_guided_next_step)
        self.guided_pulse_timer = QTimer(self)
        self.guided_pulse_timer.setInterval(800)
        self.guided_pulse_timer.timeout.connect(self.toggle_guided_pulse)
        self.guided_pulse_timer.start()

        main_row = QHBoxLayout()
        main_row.addWidget(self.side_container)
        main_row.addWidget(self.page_scroll, 1)

        main_column = QVBoxLayout()
        main_column.addLayout(main_row, 1)
        guidance_row = QHBoxLayout()
        guidance_row.addWidget(self.status_label, 1)
        guidance_row.addWidget(self.next_step_button)
        main_column.addLayout(guidance_row)

        root = QWidget()
        root.setLayout(main_column)
        root.setStyleSheet(
            "background-color: #202020;"
            "color: #f2f2f2;"
            "font-family: Sans Serif;"
        )

        self.setCentralWidget(root)
        self.restore_window_geometry()
        QTimer.singleShot(0, self.refresh_guided_next_step)

    def _open_guided_page(self, page_index: int) -> None:
        self.pages.setCurrentIndex(page_index)
        self.sidebar.setCurrentRow(page_index)

    def set_guidance(self, text: str, action=None, target=None) -> None:
        if self._guided_target is not None:
            self._guided_target.setStyleSheet(self._guided_target_style)
        self._guided_target = target
        self._guided_target_style = target.styleSheet() if target is not None else ""
        if target is not None:
            target.setStyleSheet(
                self._guided_target_style
                + " border: 2px solid #d6c27a; font-weight: 700;"
            )
        self._guided_action = action
        self.next_step_button.setText(text)
        self.next_step_button.setEnabled(action is not None)

    def toggle_guided_pulse(self) -> None:
        if not self.next_step_button.isEnabled():
            self.next_step_button.setStyleSheet("")
            return
        self._guided_pulse_on = not self._guided_pulse_on
        if self._guided_pulse_on:
            self.next_step_button.setStyleSheet(
                "background-color: #6b5b24; border: 3px solid #f0d76b; "
                "font-weight: 800; padding: 8px 14px;"
            )
        else:
            self.next_step_button.setStyleSheet(
                "background-color: #3a3420; border: 2px solid #9f8d49; "
                "font-weight: 700; padding: 8px 14px;"
            )

    def perform_guided_next_step(self) -> None:
        action = self._guided_action
        if action is not None:
            action()

    def focus_project_name(self) -> None:
        self._open_guided_page(1)
        self.start_here_panel.profile_fields["project_name"].setFocus()
        self.set_status("Enter a project name, then use the pulsing Next control.")

    def open_guided_import(self) -> None:
        self._open_guided_page(3)
        QTimer.singleShot(0, self.library_panel.choose_project_source)

    def run_guided_workflow(self) -> None:
        self._open_guided_page(2)
        self.agent_panel.start_selected_workflow()

    def open_guided_jobs(self) -> None:
        self._guided_evidence_ready = False
        self._open_guided_page(5)
        self.jobs_panel.refresh_jobs()
        self.refresh_guided_next_step()

    def handle_guided_project_name_edited(self, _text: str) -> None:
        self._guided_project_name_edited = True
        self.refresh_guided_next_step()

    def handle_guided_project_changed(self, state) -> None:
        self._guided_evidence_ready = False
        self._guided_project_name_edited = False
        self._awaiting_project_resume = bool(state is not None and state.writable)
        self.refresh_guided_next_step()

    def handle_guided_job_active(self, active: bool) -> None:
        if active:
            self._guided_evidence_ready = False
            self.set_guidance("Working locally…", None)
        elif self._guided_evidence_ready:
            self.guide_to_saved_evidence()
        else:
            self.refresh_guided_next_step()

    def guide_to_saved_evidence(self, *_args) -> None:
        self._guided_evidence_ready = True
        self.set_guidance(
            "Next: Inspect saved evidence",
            self.open_guided_jobs,
            self.sidebar,
        )

    def accept_reopened_project_sources(self, sources) -> None:
        if not self._awaiting_project_resume:
            return
        self._awaiting_project_resume = False
        if not sources:
            self.refresh_guided_next_step()
            return
        item = sources[0]
        if self.agent_panel.select_source_item(item):
            self._open_guided_page(2)
            self.refresh_guided_next_step()
            self.set_status(
                f"Resumed project source in Agent Workflows: {item.path.name}."
            )

    def accept_guided_project_source(self, item) -> None:
        if self.agent_panel.select_source_item(item):
            self._guided_evidence_ready = False
            self._open_guided_page(2)
            self.refresh_guided_next_step()
            self.set_status(
                f"Imported source selected in Agent Workflows: {item.path.name}. "
                "Choose any workflow, then use the pulsing Next control."
            )

    def refresh_guided_next_step(self) -> None:
        if self.agent_panel.has_active_job():
            self.set_guidance("Working locally…", None)
            return
        if self._guided_evidence_ready:
            self.guide_to_saved_evidence()
            return
        state = self.project_session.state
        if state is None:
            typed_name = self.start_here_panel.profile_fields["project_name"].text().strip()
            if self._guided_project_name_edited and typed_name:
                self.set_guidance(
                    "Next: Create project",
                    self.start_here_panel.create_current_project,
                    self.start_here_panel.create_project_button,
                )
            elif self.start_here_panel.project_selector.currentData():
                self.set_guidance(
                    "Next: Open selected project",
                    self.start_here_panel.open_selected_project,
                    self.start_here_panel.open_project_button,
                )
            elif typed_name:
                self.set_guidance(
                    "Next: Create project",
                    self.start_here_panel.create_current_project,
                    self.start_here_panel.create_project_button,
                )
            else:
                self.set_guidance(
                    "Next: Enter project name",
                    self.focus_project_name,
                    self.start_here_panel.profile_fields["project_name"],
                )
            return
        if not state.writable:
            self.set_guidance(
                "Next: Review project status",
                lambda: self._open_guided_page(1),
                self.sidebar,
            )
            return
        if self.library_panel.has_active_intake() or self.library_panel.has_active_thumbnail_loading():
            self.set_guidance("Preparing My Library…", None)
            return
        project_id = state.assessment.manifest["project_id"]
        selected = self.agent_panel.source_combo.currentData()
        if (
            isinstance(selected, SourceArtItem)
            and selected.authority == "active_project"
            and selected.project_id == project_id
        ):
            workflow = self.agent_panel.workflow_combo.currentText()
            self.set_guidance(
                f"Next: Run {workflow}",
                self.run_guided_workflow,
                self.agent_panel.run_button,
            )
            return
        self.set_guidance(
            "Next: Import PNG or JPEG",
            self.open_guided_import,
            self.library_panel.import_button,
        )

    def open_library_source_in_agent_panel(self, item):
        if self.agent_panel.select_source_item(item):
            self._guided_evidence_ready = False
            self.pages.setCurrentIndex(2)
            self.sidebar.setCurrentRow(2)
            self.set_status(f"Opened library source in Agent Workflows: {item.path.name}")
            self.refresh_guided_next_step()

    def open_page(self, index: int):
        self.pages.setCurrentIndex(index)
        if index == 4:
            self.shape_panel.ensure_loaded()

    def closeEvent(self, event):
        if self.library_panel.has_active_intake():
            self.set_status(
                "Project source intake is still active. Wait for its transaction to finish before closing."
            )
            event.ignore()
            return
        if self.agent_panel.has_active_job():
            self.set_status(
                "A local AI workflow is still running. Wait for it to finish before closing."
            )
            event.ignore()
            return

        if (
            self.jobs_panel.has_active_scan()
            or self.library_panel.has_active_thumbnail_loading()
            or self.shape_panel.has_active_scan()
        ):
            self._close_when_background_idle = True
            self.jobs_panel.request_scan_shutdown()
            self.library_panel.request_thumbnail_shutdown()
            self.shape_panel.request_scan_shutdown()
            self.set_status(
                "Stopping background library scans before closing. The interface remains responsive."
            )
            event.ignore()
            return

        self._close_when_background_idle = False
        try:
            self.project_session.close()
        except (OSError, ValueError, RuntimeError) as exc:
            self.set_status(f"Could not safely release the current project lock: {exc}")
            event.ignore()
            return
        self.settings.setValue("main_window/geometry", self.saveGeometry())
        super().closeEvent(event)

    def finish_deferred_close(self):
        if not self._close_when_background_idle:
            return
        if (
            self.jobs_panel.has_active_scan()
            or self.library_panel.has_active_thumbnail_loading()
            or self.shape_panel.has_active_scan()
        ):
            return
        self._close_when_background_idle = False
        QTimer.singleShot(0, self.close)

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
