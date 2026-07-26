#!/usr/bin/env python3
"""Forge shell with project authoring, persistent options, and Project Trash."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QInputDialog, QPushButton

from qt_app import SETTINGS_APP, SETTINGS_ORG
from qt_editor_app import EDITOR_PAGE_INDEX, START_HERE_PAGE_INDEX
from qt_editor_usability_app import UsableEditorForgeWindow
from qt_panels.editor_authority_guard import GuardedProjectAwareEditorPanel
from qt_panels.editor_wheel_controls import EditorMouseWheelController
from core.project_authoring_workflow import switch_project
from core.project_trash import move_project_to_trash


class StartHereProjectController:
    """Keep Start Here useful while one project is already attached."""

    def __init__(self, window: "AuthoringEditorForgeWindow"):
        self.window = window
        self.panel = window.start_here_panel

        self.new_project_document_button = QPushButton("New Project + Document")
        self.new_project_document_button.setToolTip(
            "Close the current project safely, create a fresh project, and open a blank "
            "Editor document."
        )
        self.delete_project_button = QPushButton("Delete Selected Project…")
        self.delete_project_button.setToolTip(
            "Move the exactly selected project into recoverable Project Trash after typing "
            "its directory name. Active work and locked projects are protected."
        )
        insert_at = max(0, self.panel.project_actions_layout.count() - 1)
        self.panel.project_actions_layout.insertWidget(
            insert_at,
            self.delete_project_button,
        )
        self.panel.project_actions_layout.insertWidget(
            insert_at + 1,
            self.new_project_document_button,
        )
        self.new_project_document_button.clicked.connect(self.create_fresh_project_document)
        self.delete_project_button.clicked.connect(self.delete_selected_project)
        self.panel.new_project_document_button = self.new_project_document_button
        self.panel.delete_project_button = self.delete_project_button
        self.panel.open_project_button.setText("Open / Switch Selected")

        self._disconnect(self.panel.open_project_action.triggered, self.panel.open_selected_project)
        self._disconnect(self.panel.go_to_project_action.triggered, self.panel.go_to_selected_project)
        self.panel.open_selected_project = self.open_selected_project
        self.panel.go_to_selected_project = self.go_to_selected_project
        self.panel.update_project_controls = self.update_controls
        self.panel.open_project_action.triggered.connect(self.open_selected_project)
        self.panel.go_to_project_action.triggered.connect(self.go_to_selected_project)
        self.panel.project_selector.currentIndexChanged.connect(
            lambda _index: self.update_controls()
        )
        self.update_controls()

    @staticmethod
    def _disconnect(signal, slot) -> None:
        try:
            signal.disconnect(slot)
        except (RuntimeError, TypeError):
            # The original Qt connection may already be absent during shell replacement.
            pass

    def update_controls(self) -> None:
        panel = self.panel
        attached = panel.project_session.state is not None
        unlocked = not panel._project_mutation_sources
        selected = panel.project_selector.currentData()
        current = str(panel.project_session.project_dir) if panel.project_session.project_dir else None
        selection_available = bool(selected)
        switch_available = bool(unlocked and selection_available and selected != current)

        panel.create_project_button.setEnabled(
            not attached and unlocked and panel._purpose_is_valid()
        )
        panel.open_project_button.setEnabled(switch_available)
        panel.open_project_action.setEnabled(switch_available)
        panel.go_to_project_action.setEnabled(switch_available)
        self.delete_project_button.setEnabled(bool(unlocked and selection_available))
        panel.project_selector.setEnabled(unlocked and panel.project_selector.count() > 0)
        panel.refresh_projects_button.setEnabled(unlocked)
        panel.purpose_edit.setEnabled(not attached and unlocked)
        panel.close_project_button.setEnabled(attached and unlocked)
        self.new_project_document_button.setEnabled(unlocked)

    def open_selected_project(self, *_args):
        selected = self.panel.project_selector.currentData()
        if not selected:
            self.panel.set_status("No canonical project is selected.")
            return None
        try:
            state = switch_project(self.panel.project_session, selected)
        except Exception as exc:
            if self.panel.project_session.state is None:
                self.panel.project_changed.emit(None)
                self.panel.project_status_label.setText("No project is open.")
            self.panel.refresh_projects()
            self.update_controls()
            self.panel.set_status(f"Could not switch project: {exc}")
            return None

        self.panel.refresh_projects()
        self.panel._show_project_state(state, "Switched")
        self.update_controls()
        return state

    def go_to_selected_project(self, *_args):
        state = self.open_selected_project()
        if state is None:
            return None
        self.panel.go_to_project_requested.emit(state)
        self.panel.set_status(
            f"Switched to project {state.assessment.project_dir.name}; loading its Editor build."
        )
        return state

    def delete_selected_project(self, *_args) -> bool:
        panel = self.panel
        if panel._project_mutation_sources:
            panel.set_status("Finish active project work before deleting a project.")
            return False
        selected = panel.project_selector.currentData()
        if not selected:
            panel.set_status("Choose one canonical project before using Delete Project.")
            return False
        selected_path = Path(str(selected)).expanduser().resolve()
        project_name = selected_path.name
        typed, accepted = QInputDialog.getText(
            panel,
            "Move project to Project Trash",
            f"Type the exact project directory name to continue:\n\n{project_name}",
        )
        if not accepted:
            panel.set_status("Project deletion cancelled; no project was moved.")
            return False
        if typed.strip() != project_name:
            panel.set_status(
                "Project deletion cancelled; the typed project name did not match."
            )
            return False

        try:
            result = move_project_to_trash(panel.project_session, selected_path)
        except Exception as exc:
            panel.set_status(f"Could not move selected project to Project Trash: {exc}")
            panel.refresh_projects()
            self.update_controls()
            return False

        panel.refresh_projects()
        self.window.editor_panel.refresh_project_choices()
        if result.was_active:
            panel.refresh_attached_project_state(None)
            panel.project_changed.emit(None)
        self.update_controls()
        panel.set_status(
            f"Moved project {project_name} to recoverable Project Trash: "
            f"{result.trashed_project_dir.name}."
        )
        self.window.refresh_guided_next_step()
        return True

    def create_fresh_project_document(self, *_args):
        state = self.window.editor_panel.create_fresh_project_and_document()
        if state is None:
            return None
        self.window._open_guided_page(EDITOR_PAGE_INDEX)
        self.panel.set_status(
            f"Created fresh project/document and opened Editor: "
            f"{state.assessment.project_dir.name}."
        )
        return state


class AuthoringEditorForgeWindow(UsableEditorForgeWindow):
    """Expose complete project/document authoring and visible interaction controls."""

    def __init__(self, project_session=None):
        super().__init__(project_session)
        self._replace_authoring_editor_panel()
        self.start_here_project_controller = StartHereProjectController(self)
        self.editor_mouse_wheel_controller = EditorMouseWheelController(
            self,
            self.editor_panel,
        )
        self.pages.setCurrentIndex(START_HERE_PAGE_INDEX)
        self.sidebar.setCurrentRow(START_HERE_PAGE_INDEX)
        self.refresh_guided_next_step()

    def _replace_authoring_editor_panel(self) -> None:
        old_editor = self.editor_panel
        editor_index = self.pages.indexOf(old_editor)
        try:
            self.start_here_panel.project_changed.disconnect(old_editor.set_project_state)
        except (RuntimeError, TypeError):
            # Safe during replacement when Qt has already removed the old connection.
            pass

        self.pages.removeWidget(old_editor)
        editor = GuardedProjectAwareEditorPanel(self.project_session)
        editor.status_changed.connect(self.set_status)
        editor.project_authority_changed.connect(self.accept_editor_project_authority)
        self.pages.insertWidget(editor_index, editor)
        self.editor_panel = editor
        self.start_here_panel.project_changed.connect(editor.set_project_state)
        self.agent_panel.job_active_changed.connect(
            lambda active: editor.set_project_mutation_active(active, "local AI workflow")
        )
        self.library_panel.intake_active_changed.connect(
            lambda active: editor.set_project_mutation_active(active, "source intake")
        )
        editor.set_project_state(self.project_session.state)
        old_editor.deleteLater()

    def accept_editor_project_authority(self, state, action: str) -> None:
        self.start_here_panel.refresh_projects()
        if state is None:
            self.start_here_panel.refresh_attached_project_state(None)
            self.start_here_panel.project_changed.emit(None)
        else:
            self.start_here_panel._show_project_state(state, action)
        if hasattr(self, "start_here_project_controller"):
            self.start_here_project_controller.update_controls()
        self.refresh_guided_next_step()

    def refresh_guided_next_step(self) -> None:
        """Keep Project Birth pointed at one blank document before source workflows."""
        if not hasattr(self, "editor_panel"):
            super().refresh_guided_next_step()
            return
        if self.agent_panel.has_active_job() or self._guided_evidence_ready:
            super().refresh_guided_next_step()
            return

        state = self.project_session.state
        if (
            state is not None
            and state.writable
            and not self.library_panel.has_active_intake()
            and not self.editor_panel.has_open_document()
        ):
            self.set_guidance(
                "Next: New blank document",
                self.open_guided_blank_document,
                self.editor_panel.document_button,
            )
            return

        super().refresh_guided_next_step()

    def _ensure_editor_ready(self) -> bool:
        return self.editor_panel.ensure_ready_document()

    def _open_guided_page(self, page_index: int) -> None:
        if page_index == EDITOR_PAGE_INDEX and hasattr(self, "editor_panel"):
            if not self._ensure_editor_ready():
                return
        super()._open_guided_page(page_index)

    def open_page(self, index: int):
        if index == EDITOR_PAGE_INDEX and hasattr(self, "editor_panel"):
            if not self._ensure_editor_ready():
                return
        super().open_page(index)

    def open_current_project_in_editor(self, state=None) -> None:
        if not self._ensure_editor_ready():
            self.set_status("Could not prepare a fresh Editor project/document.")
            return
        self._open_guided_page(EDITOR_PAGE_INDEX)
        active = self.project_session.state
        project_name = (
            active.assessment.manifest.get(
                "project_name",
                active.assessment.project_dir.name,
            )
            if active is not None
            else "unknown"
        )
        self.set_status(f"Opened the current project/document in Editor: {project_name}.")
        self.refresh_guided_next_step()

    def open_guided_blank_document(self) -> None:
        if self.project_session.state is None:
            if self.editor_panel.create_fresh_project_and_document() is None:
                return
        else:
            self.editor_panel.load_project_build()
            if not self.editor_panel.has_open_document():
                self.editor_panel.create_blank_document()
        self._open_guided_page(EDITOR_PAGE_INDEX)
        self.refresh_guided_next_step()


def main() -> int:
    app = QApplication(sys.argv)
    app.setOrganizationName(SETTINGS_ORG)
    app.setApplicationName(SETTINGS_APP)
    window = AuthoringEditorForgeWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
