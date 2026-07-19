#!/usr/bin/env python3
"""
Start Here panel for MXZTAR Forge v2.0.

Purpose:
- store project identity
- store creator/brand notes
- store workflow/trust notes
- give the user a stable restart point after rebuilds
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.onboarding_store import (
    load_profile,
    load_settings_notes,
    save_profile,
    save_settings_notes,
)
from core.project_session import ProjectSession, discover_project_directories


class StartHerePanel(QWidget):
    status_changed = Signal(str)
    project_changed = Signal(object)

    def __init__(self, project_session: ProjectSession | None = None):
        super().__init__()

        self.project_session = project_session or ProjectSession()
        self.profile_fields = {}

        title = QLabel("Start Here")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")

        intro = QLabel(
            "Define the forge identity, project direction, and workflow rules. "
            "These notes are injected later into agent workflows."
        )
        intro.setWordWrap(True)
        intro.setStyleSheet("color: #cfcfcf;")

        self.project_status_label = QLabel("No project is open.")
        self.project_status_label.setWordWrap(True)
        self.project_status_label.setStyleSheet("color: #d6c27a; font-weight: 600;")

        self.project_selector = QComboBox()
        self.project_selector.setToolTip("Canonical projects found in workspace/projects.")
        self.refresh_projects_button = QPushButton("Refresh Projects")
        self.refresh_projects_button.clicked.connect(self.refresh_projects)
        self.open_project_button = QPushButton("Open Selected")
        self.open_project_button.clicked.connect(self.open_selected_project)
        self.create_project_button = QPushButton("Create Project")
        self.create_project_button.clicked.connect(self.create_current_project)
        self.close_project_button = QPushButton("Close Project")
        self.close_project_button.clicked.connect(self.close_project)

        project_row = QHBoxLayout()
        project_row.addWidget(self.project_selector, 1)
        project_row.addWidget(self.refresh_projects_button)
        project_row.addWidget(self.open_project_button)

        project_actions = QHBoxLayout()
        project_actions.addWidget(self.create_project_button)
        project_actions.addWidget(self.close_project_button)
        project_actions.addStretch(1)

        project_frame = QFrame()
        project_frame.setFrameShape(QFrame.Shape.StyledPanel)
        project_layout = QVBoxLayout()
        project_layout.addWidget(QLabel("Project Authority"))
        project_layout.addWidget(self.project_status_label)
        project_layout.addLayout(project_row)
        project_layout.addLayout(project_actions)
        project_frame.setLayout(project_layout)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        field_specs = [
            ("project_name", "Project name"),
            ("project_role", "Project role"),
            ("creator_name", "Creator name"),
            ("brand_presence", "Brand / presence"),
            ("primary_goal", "Primary goal"),
            ("workflow_focus", "Workflow focus"),
        ]

        for key, label in field_specs:
            edit = QLineEdit()
            edit.setPlaceholderText(f"Enter {label.lower()}...")
            edit.setToolTip(f"Saved into onboarding_profile.json as {key}.")
            self.profile_fields[key] = edit
            form.addRow(label + ":", edit)

        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText(
            "Project notes / pasted brief. Use this for the current build direction."
        )
        self.notes_edit.setMinimumHeight(140)

        self.trust_edit = QTextEdit()
        self.trust_edit.setPlaceholderText(
            "Workflow / trust notes. Use this for rules the app and agents must respect."
        )
        self.trust_edit.setMinimumHeight(160)

        save_fields_button = QPushButton("Save Fields")
        save_fields_button.setToolTip("Save profile fields to workspace/data/user_profile/onboarding_profile.json.")
        save_fields_button.clicked.connect(self.save_fields)

        reload_button = QPushButton("Reload")
        reload_button.setToolTip("Reload saved profile and trust notes from disk.")
        reload_button.clicked.connect(self.load_all)

        save_notes_button = QPushButton("Save Notes")
        save_notes_button.setToolTip("Save project notes into the profile primary goal/workflow context.")
        save_notes_button.clicked.connect(self.save_fields)

        save_trust_button = QPushButton("Save Trust Notes")
        save_trust_button.setToolTip("Save workflow/trust notes to settings_notes.txt.")
        save_trust_button.clicked.connect(self.save_trust_notes)

        top_buttons = QHBoxLayout()
        top_buttons.addWidget(save_fields_button)
        top_buttons.addWidget(reload_button)
        top_buttons.addStretch(1)

        notes_row = QHBoxLayout()
        notes_label = QLabel("Project Notes / Pasted Brief")
        notes_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        notes_row.addWidget(notes_label)
        notes_row.addStretch(1)
        notes_row.addWidget(save_notes_button)

        trust_row = QHBoxLayout()
        trust_label = QLabel("Workflow / Trust Notes")
        trust_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        trust_row.addWidget(trust_label)
        trust_row.addStretch(1)
        trust_row.addWidget(save_trust_button)

        self.status_label = QLabel("Ready.")
        self.status_label.setStyleSheet("color: #d6c27a;")

        content = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(intro)
        layout.addWidget(project_frame)
        layout.addSpacing(12)
        layout.addLayout(form)
        layout.addLayout(top_buttons)
        layout.addSpacing(18)
        layout.addLayout(notes_row)
        layout.addWidget(self.notes_edit)
        layout.addSpacing(18)
        layout.addLayout(trust_row)
        layout.addWidget(self.trust_edit)
        layout.addSpacing(12)
        layout.addWidget(self.status_label)
        layout.addStretch(1)
        content.setLayout(layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)

        root = QVBoxLayout()
        root.addWidget(scroll)
        self.setLayout(root)

        self.load_all()
        self.refresh_projects()
        if self.project_session.state is None:
            self.update_project_controls()
        else:
            self._show_project_state(self.project_session.state, "Attached")

    def refresh_projects(self):
        selected_path = self.project_selector.currentData()
        self.project_selector.clear()
        try:
            projects = discover_project_directories(self.project_session.projects_root)
        except (OSError, ValueError, RuntimeError) as exc:
            self.update_project_controls()
            self.set_status(f"Could not discover projects: {exc}")
            return
        for path in projects:
            self.project_selector.addItem(path.name, str(path))
        if selected_path:
            index = self.project_selector.findData(selected_path)
            if index >= 0:
                self.project_selector.setCurrentIndex(index)
        self.update_project_controls()

    def create_current_project(self):
        try:
            state = self.project_session.create_and_open(
                self.profile_fields["project_name"].text(),
                self.profile_fields["primary_goal"].text(),
            )
        except (OSError, ValueError, RuntimeError) as exc:
            self.set_status(f"Could not create project: {exc}")
            return
        self.refresh_projects()
        self._show_project_state(state, "Created")

    def open_selected_project(self):
        selected = self.project_selector.currentData()
        if not selected:
            self.set_status("No canonical project is selected.")
            return
        try:
            state = self.project_session.open(selected)
        except (OSError, ValueError, RuntimeError) as exc:
            self.set_status(f"Could not open project: {exc}")
            return
        self._show_project_state(state, "Opened")

    def close_project(self):
        was_writable = self.project_session.is_writable
        try:
            result = self.project_session.close()
        except (OSError, ValueError, RuntimeError) as exc:
            self.set_status(f"Could not safely close project: {exc}")
            return False
        self.project_status_label.setText("No project is open.")
        self.update_project_controls()
        self.project_changed.emit(None)
        if result.warning:
            message = f"Closed project with a durability warning: {result.warning}"
        elif was_writable and result.released_writer:
            message = "Closed project and released its writer lease."
        else:
            message = "Detached the read-only project; no writer lease was held or released."
        self.set_status(message)
        return True

    def _show_project_state(self, state, action: str):
        assessment = state.assessment
        if state.writable:
            detail = "Writable session; this application owns the project lock."
        else:
            diagnostics = " ".join(assessment.diagnostics) or "Writable access is unavailable."
            detail = f"{assessment.status.value}: {diagnostics}"
        self.project_status_label.setText(
            f"{action}: {assessment.project_dir.name}\n{detail}"
        )
        self.update_project_controls()
        self.project_changed.emit(state)
        self.set_status(f"{action} project {assessment.project_dir.name}: {detail}")

    def update_project_controls(self):
        attached = self.project_session.state is not None
        self.create_project_button.setEnabled(not attached)
        self.open_project_button.setEnabled(not attached and self.project_selector.count() > 0)
        self.project_selector.setEnabled(not attached)
        self.refresh_projects_button.setEnabled(not attached)
        self.close_project_button.setEnabled(attached)

    def load_all(self):
        profile = load_profile()

        for key, edit in self.profile_fields.items():
            edit.setText(profile.get(key, ""))

        self.notes_edit.setPlainText(
            "Current project spine:\n"
            f"{profile.get('workflow_focus', '')}\n\n"
            "Primary goal:\n"
            f"{profile.get('primary_goal', '')}\n"
        )

        self.trust_edit.setPlainText(load_settings_notes())

        self.set_status("Loaded Start Here profile and trust notes.")

    def save_fields(self):
        profile = {key: edit.text() for key, edit in self.profile_fields.items()}

        saved = save_profile(profile)

        self.profile_fields["project_name"].setText(saved.get("project_name", ""))
        self.profile_fields["project_role"].setText(saved.get("project_role", ""))
        self.profile_fields["creator_name"].setText(saved.get("creator_name", ""))
        self.profile_fields["brand_presence"].setText(saved.get("brand_presence", ""))
        self.profile_fields["primary_goal"].setText(saved.get("primary_goal", ""))
        self.profile_fields["workflow_focus"].setText(saved.get("workflow_focus", ""))

        self.set_status("Saved onboarding profile.")

    def save_trust_notes(self):
        save_settings_notes(self.trust_edit.toPlainText())
        self.set_status("Saved workflow/trust notes.")

    def set_status(self, message: str):
        self.status_label.setText(message)
        self.status_changed.emit(message)
