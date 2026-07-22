#!/usr/bin/env python3
"""Purpose-driven project authority and optional profile controls."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from core.onboarding_store import (
    load_profile,
    load_settings_notes,
    save_profile,
    save_settings_notes,
)
from core.project_manifest import project_name_from_purpose
from core.project_session import ProjectSession, discover_project_directories


class StartHerePanel(QWidget):
    status_changed = Signal(str)
    project_changed = Signal(object)
    go_to_project_requested = Signal(object)

    def __init__(self, project_session: ProjectSession | None = None):
        super().__init__()

        self.project_session = project_session or ProjectSession()
        self.profile_fields: dict[str, QLineEdit] = {}
        self._saved_profile_keys: list[str] = []
        self._project_mutation_sources = set()

        title = QLabel("Start Here")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")

        intro = QLabel(
            "State what this project is for, then create or open its local authority. "
            "Creator and workflow profile fields below are optional and do not block editing."
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

        self.open_project_button = QToolButton()
        self.open_project_button.setText("Open Selected")
        self.open_project_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.open_project_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.open_project_button.setToolTip(
            "Choose whether to attach the selected project here or go directly to its Editor build."
        )
        self.open_project_menu = QMenu(self.open_project_button)
        self.open_project_action = QAction("Open Project", self.open_project_menu)
        self.go_to_project_action = QAction("Go to Project", self.open_project_menu)
        self.open_project_action.triggered.connect(self.open_selected_project)
        self.go_to_project_action.triggered.connect(self.go_to_selected_project)
        self.open_project_menu.addActions(
            [self.open_project_action, self.go_to_project_action]
        )
        self.open_project_button.setMenu(self.open_project_menu)

        self.purpose_label = QLabel("PURPOSE:")
        self.purpose_label.setStyleSheet("font-weight: 700;")
        self.purpose_edit = QLineEdit()
        self.purpose_edit.setPlaceholderText(
            "What should this project create, recover, explore, or prepare?"
        )
        self.purpose_edit.setToolTip(
            "The exact wording becomes the first project purpose. Forge derives a safe "
            "display name and directory slug without changing the stored purpose."
        )
        self.purpose_edit.textChanged.connect(lambda _text: self.update_project_controls())

        self.create_project_button = QPushButton("Create Project")
        self.create_project_button.setToolTip(
            "Create and open one canonical local project from the stated Purpose."
        )
        self.create_project_button.clicked.connect(self.create_current_project)
        self.close_project_button = QPushButton("Close Project")
        self.close_project_button.clicked.connect(self.close_project)

        project_row = QHBoxLayout()
        project_row.addWidget(self.project_selector, 1)
        project_row.addWidget(self.refresh_projects_button)
        project_row.addWidget(self.open_project_button)

        self.project_actions_layout = QHBoxLayout()
        self.project_actions_layout.addWidget(self.purpose_label)
        self.project_actions_layout.addWidget(self.purpose_edit, 1)
        self.project_actions_layout.addWidget(self.create_project_button)
        self.project_actions_layout.addWidget(self.close_project_button)

        project_frame = QFrame()
        project_frame.setFrameShape(QFrame.Shape.StyledPanel)
        project_layout = QVBoxLayout()
        project_layout.addWidget(QLabel("Project Authority"))
        project_layout.addWidget(self.project_status_label)
        project_layout.addLayout(project_row)
        project_layout.addLayout(self.project_actions_layout)
        project_frame.setLayout(project_layout)

        optional_title = QLabel("Optional Creator / Workflow Profile")
        optional_title.setStyleSheet("font-size: 16px; font-weight: 600;")

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        field_specs = [
            ("project_role", "Project role"),
            ("creator_name", "Creator name"),
            ("brand_presence", "Brand / presence"),
            ("workflow_focus", "Workflow focus"),
        ]

        for key, label in field_specs:
            edit = QLineEdit()
            edit.setPlaceholderText(f"Enter {label.lower()}...")
            edit.setToolTip(f"Optional profile field saved as {key}.")
            self.profile_fields[key] = edit
            self._saved_profile_keys.append(key)
            form.addRow(label + ":", edit)

        # Compatibility for established guided navigation. Purpose remains project authority
        # and is neither loaded from nor saved into the global onboarding profile.
        self.profile_fields["project_name"] = self.purpose_edit

        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText(
            "Optional profile notes or a pasted working brief. Project-owned artifacts "
            "remain the authority for actual project work."
        )
        self.notes_edit.setMinimumHeight(140)

        self.trust_edit = QTextEdit()
        self.trust_edit.setPlaceholderText(
            "Workflow / trust notes. Use this for rules the app and agents must respect."
        )
        self.trust_edit.setMinimumHeight(160)

        save_fields_button = QPushButton("Save Profile")
        save_fields_button.setToolTip(
            "Save optional creator and workflow fields to the global onboarding profile."
        )
        save_fields_button.clicked.connect(self.save_fields)

        reload_button = QPushButton("Reload Profile")
        reload_button.setToolTip("Reload optional profile and trust notes from disk.")
        reload_button.clicked.connect(self.load_all)

        save_notes_button = QPushButton("Save Profile Notes")
        save_notes_button.setToolTip("Save optional profile notes into the onboarding profile.")
        save_notes_button.clicked.connect(self.save_fields)

        save_trust_button = QPushButton("Save Trust Notes")
        save_trust_button.setToolTip("Save workflow/trust notes to settings_notes.txt.")
        save_trust_button.clicked.connect(self.save_trust_notes)

        top_buttons = QHBoxLayout()
        top_buttons.addWidget(save_fields_button)
        top_buttons.addWidget(reload_button)
        top_buttons.addStretch(1)

        notes_row = QHBoxLayout()
        notes_label = QLabel("Optional Profile Notes")
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
        layout.addWidget(optional_title)
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
        purpose = self.purpose_edit.text()
        try:
            state = self.project_session.create_from_purpose(purpose)
        except (OSError, ValueError, RuntimeError) as exc:
            self.set_status(f"Could not create project: {exc}")
            self.update_project_controls()
            return None
        self.refresh_projects()
        self._show_project_state(state, "Created")
        return state

    def open_selected_project(self, *_args):
        selected = self.project_selector.currentData()
        if not selected:
            self.set_status("No canonical project is selected.")
            return None
        try:
            state = self.project_session.open(selected)
        except (OSError, ValueError, RuntimeError) as exc:
            self.set_status(f"Could not open project: {exc}")
            return None
        self._show_project_state(state, "Opened")
        return state

    def go_to_selected_project(self, *_args):
        state = self.open_selected_project()
        if state is None:
            return None
        self.go_to_project_requested.emit(state)
        self.set_status(
            f"Opened project {state.assessment.project_dir.name}; loading its Editor build."
        )
        return state

    def close_project(self):
        was_writable = self.project_session.is_writable
        try:
            result = self.project_session.close()
        except (OSError, ValueError, RuntimeError) as exc:
            self.set_status(f"Could not safely close project: {exc}")
            return False
        self.project_status_label.setText("No project is open.")
        self.purpose_edit.clear()
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
        self.purpose_edit.setText(assessment.manifest.get("primary_goal", ""))
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

    def _purpose_is_valid(self) -> bool:
        try:
            project_name_from_purpose(self.purpose_edit.text())
        except (TypeError, ValueError):
            return False
        return True

    def update_project_controls(self):
        attached = self.project_session.state is not None
        unlocked = not self._project_mutation_sources
        selection_available = self.project_selector.count() > 0
        open_enabled = not attached and unlocked and selection_available

        self.create_project_button.setEnabled(
            not attached and unlocked and self._purpose_is_valid()
        )
        self.open_project_button.setEnabled(open_enabled)
        self.open_project_action.setEnabled(open_enabled)
        self.go_to_project_action.setEnabled(open_enabled)
        self.project_selector.setEnabled(not attached and unlocked)
        self.refresh_projects_button.setEnabled(not attached and unlocked)
        self.purpose_edit.setEnabled(not attached and unlocked)
        self.close_project_button.setEnabled(attached and unlocked)

    def set_project_mutation_active(self, active: bool, source: str = "source intake"):
        if active:
            self._project_mutation_sources.add(source)
        else:
            self._project_mutation_sources.discard(source)
        self.update_project_controls()
        if active:
            self.set_status(
                f"{source.capitalize()} is active; project switching and close are paused."
            )

    def refresh_attached_project_state(self, state):
        """Refresh displayed authority without announcing a project switch."""
        if state is None:
            self.project_status_label.setText("No project is open.")
            self.purpose_edit.clear()
            self.update_project_controls()
            return
        assessment = state.assessment
        self.purpose_edit.setText(assessment.manifest.get("primary_goal", ""))
        if state.writable:
            detail = "Writable session; this application owns the project lock."
        else:
            diagnostics = " ".join(assessment.diagnostics) or "Writable access is unavailable."
            detail = f"{assessment.status.value}: {diagnostics}"
        self.project_status_label.setText(
            f"Attached: {assessment.project_dir.name}\n{detail}"
        )
        self.update_project_controls()

    def load_all(self):
        profile = load_profile()

        for key in self._saved_profile_keys:
            self.profile_fields[key].setText(profile.get(key, ""))

        self.notes_edit.setPlainText(profile.get("primary_goal", ""))
        self.trust_edit.setPlainText(load_settings_notes())
        self.set_status("Loaded optional profile and trust notes.")

    def save_fields(self):
        profile = load_profile()
        for key in self._saved_profile_keys:
            profile[key] = self.profile_fields[key].text()
        profile["primary_goal"] = self.notes_edit.toPlainText()
        saved = save_profile(profile)

        for key in self._saved_profile_keys:
            self.profile_fields[key].setText(saved.get(key, ""))

        self.set_status("Saved optional onboarding profile.")

    def save_trust_notes(self):
        save_settings_notes(self.trust_edit.toPlainText())
        self.set_status("Saved workflow/trust notes.")

    def set_status(self, message: str):
        self.status_label.setText(message)
        self.status_changed.emit(message)
