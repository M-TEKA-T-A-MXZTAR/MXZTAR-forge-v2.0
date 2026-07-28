#!/usr/bin/env python3
"""Live Qt corrections for visible deletion and unclipped Editor entry.

The underlying document and Project Trash transactions remain authoritative. These
small startup-installed guards correct the live presentation around those durable
operations so a successful deletion is unmistakable and controls remain visible.
"""

from __future__ import annotations

from pathlib import Path
from types import MethodType

from PySide6.QtCore import QPoint, QTimer
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMessageBox

import qt_editor_authoring_app as authoring_app
from core.shape_document import list_shape_documents
from qt_panels.editor_authoring_panel import ProjectAwareEditorPanel
from qt_panels.editor_panel import EditorPanel
from qt_panels.editor_wheel_controls import EditorMouseWheelController


def _short_document_id(document_id: object) -> str:
    value = document_id if isinstance(document_id, str) else "unknown"
    return value[-8:]


def _project_name(panel: EditorPanel) -> str:
    state = panel.project_session.state
    if state is None:
        return "unknown"
    return state.assessment.manifest.get(
        "project_name",
        state.assessment.project_dir.name,
    )


def _label_document_choices(panel: EditorPanel) -> None:
    """Make same-title documents distinguishable in the selector."""
    for index in range(panel.document_selector.count()):
        document_id = panel.document_selector.itemData(index)
        label = panel.document_selector.itemText(index)
        suffix = f" [{_short_document_id(document_id)}]"
        if not label.endswith(suffix):
            panel.document_selector.setItemText(index, label + suffix)


def _refresh_document_choices_without_open(panel: EditorPanel) -> str:
    """Rebuild the selector without loading or mutating any remaining document."""
    panel._refreshing_documents = True
    signals_were_blocked = panel.document_selector.blockSignals(True)
    panel.document_selector.clear()
    try:
        state = panel.project_session.state
        if state is None:
            panel.document = None
            panel._restore_workspace_state(None, None, None)
            panel.document_label.setText("No project build is loaded.")
            panel.set_status("Open a project before using the Editor.")
            panel._mxztar_last_document_refresh_error = None
            return "detached"

        documents = list_shape_documents(panel.project_session)
        for document in documents:
            panel.document_selector.addItem(
                f"{document['title']} — r{document['revision']}",
                document["document_id"],
            )
        _label_document_choices(panel)
        panel.document_selector.setCurrentIndex(-1)
        panel._restore_workspace_state(None, None, None)
        panel._mxztar_last_document_refresh_error = None

        project_name = _project_name(panel)
        if documents:
            panel.document_label.setText(
                f"Project: {project_name} | No document is open."
            )
            return "loaded"

        panel.document_label.setText(
            f"Project: {project_name} | No native shape document exists yet."
        )
        panel.set_status(
            "This project has no native shape documents. "
            "Use Document → New Blank Document."
        )
        return "empty"
    except Exception as exc:
        panel.document = None
        panel._restore_workspace_state(None, None, None)
        panel.document_label.setText("Project build could not be loaded.")
        panel._mxztar_last_document_refresh_error = str(exc)
        panel.set_status(f"Editor document discovery failed: {exc}")
        return "error"
    finally:
        panel.document_selector.blockSignals(signals_were_blocked)
        panel._refreshing_documents = False
        panel.update_controls()
        if hasattr(panel, "_update_document_lifecycle_controls"):
            panel._update_document_lifecycle_controls()


def _refresh_guided_navigation(panel: EditorPanel) -> None:
    shell = panel.window()
    refresh = getattr(shell, "refresh_guided_next_step", None)
    if callable(refresh):
        refresh()


def _confirm_project_trash(parent, project_name: str) -> bool:
    answer = QMessageBox.question(
        parent,
        "Move project to Project Trash",
        f"Move the selected project into recoverable Project Trash?\n\n{project_name}\n\n"
        "It will disappear from the active project list but remain recoverable.",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
        QMessageBox.StandardButton.Cancel,
    )
    return answer == QMessageBox.StandardButton.Yes


def install_live_acceptance_guards() -> None:
    """Install the acceptance-driven UI corrections once before window creation."""
    if getattr(install_live_acceptance_guards, "_installed", False):
        return
    install_live_acceptance_guards._installed = True

    original_refresh_documents = EditorPanel.refresh_documents
    original_load_project_build = EditorPanel.load_project_build
    original_open_selected_document = EditorPanel.open_selected_document

    def visible_refresh_documents(self, selected_document_id=None):
        outcome = original_refresh_documents(self, selected_document_id)
        _label_document_choices(self)
        self._mxztar_last_document_refresh_outcome = outcome
        if outcome != "error":
            self._mxztar_last_document_refresh_error = None
        return outcome

    def visible_load_project_build(self, *_args) -> None:
        if (
            getattr(self, "_mxztar_deliberate_no_document", False)
            and self.project_session.state is not None
        ):
            outcome = _refresh_document_choices_without_open(self)
            self._mxztar_last_document_refresh_outcome = outcome
            return
        original_load_project_build(self, *_args)

    def visible_open_selected_document(self, *_args) -> None:
        if (
            not self._refreshing_documents
            and isinstance(self.document_selector.currentData(), str)
        ):
            self._mxztar_deliberate_no_document = False
        original_open_selected_document(self, *_args)

    visible_refresh_documents._mxztar_visible_document_labels = True
    visible_load_project_build._mxztar_preserves_deliberate_empty_state = True
    visible_open_selected_document._mxztar_deliberate_reopening = True
    EditorPanel.refresh_documents = visible_refresh_documents
    EditorPanel.load_project_build = visible_load_project_build
    EditorPanel.open_selected_document = visible_open_selected_document

    original_project_panel_init = ProjectAwareEditorPanel.__init__
    original_close_document = ProjectAwareEditorPanel.close_document
    original_delete_open_document = ProjectAwareEditorPanel.delete_open_document
    original_delete_editor_project = ProjectAwareEditorPanel.delete_selected_project
    original_ensure_ready_document = ProjectAwareEditorPanel.ensure_ready_document

    def visible_project_panel_init(self, *args, **kwargs) -> None:
        original_project_panel_init(self, *args, **kwargs)
        self.delete_project_button.setToolTip(
            "Move the selected project into recoverable Project Trash after a simple "
            "Yes/Cancel confirmation. Active work and locked projects are protected."
        )

    def visible_close_document(self, *_args) -> bool:
        closed = original_close_document(self, *_args)
        if closed:
            self._mxztar_deliberate_no_document = True
            _refresh_guided_navigation(self)
        return closed

    def visible_delete_editor_project(self, *, confirm: bool = True) -> bool:
        selected = self.project_selector.currentData()
        if not selected:
            return original_delete_editor_project(self, confirm=False)
        project_name = Path(str(selected)).expanduser().resolve().name
        if confirm and not _confirm_project_trash(self, project_name):
            self.set_status("Project deletion cancelled; no project was moved.")
            return False
        return original_delete_editor_project(self, confirm=False)

    def visible_ensure_ready_document(self) -> bool:
        if (
            getattr(self, "_mxztar_deliberate_no_document", False)
            and self.project_session.state is not None
        ):
            outcome = _refresh_document_choices_without_open(self)
            self._mxztar_last_document_refresh_outcome = outcome
            return outcome != "error"
        if self.project_session.state is None:
            self._mxztar_deliberate_no_document = False
        return original_ensure_ready_document(self)

    def visibly_delete_open_document(self, *, confirm: bool = True) -> bool:
        document = self.document
        if not isinstance(document, dict):
            return original_delete_open_document(self, confirm=confirm)
        document_id = document.get("document_id", "unknown")
        document_title = document.get("title", document_id)

        refresh_outcomes: list[str] = []

        def refresh_without_open(instance, _selected_document_id=None):
            outcome = _refresh_document_choices_without_open(instance)
            instance._mxztar_last_document_refresh_outcome = outcome
            refresh_outcomes.append(outcome)
            return outcome

        had_instance_refresh = "refresh_documents" in self.__dict__
        previous_instance_refresh = self.__dict__.get("refresh_documents")
        self.refresh_documents = MethodType(refresh_without_open, self)
        try:
            deleted = original_delete_open_document(self, confirm=confirm)
        finally:
            if had_instance_refresh:
                self.refresh_documents = previous_instance_refresh
            else:
                del self.refresh_documents

        if not deleted:
            return False

        self._mxztar_deliberate_no_document = True
        outcome = (
            refresh_outcomes[-1]
            if refresh_outcomes
            else getattr(self, "_mxztar_last_document_refresh_outcome", "error")
        )

        if outcome == "error":
            discovery_error = getattr(
                self,
                "_mxztar_last_document_refresh_error",
                "unknown discovery failure",
            )
            self.set_status(
                f"Deleted {document_title} [{_short_document_id(document_id)}] from "
                "project authority, but remaining document discovery failed: "
                f"{discovery_error}. No remaining-document count is claimed."
            )
        else:
            remaining = self.document_selector.count()
            noun = "document remains" if remaining == 1 else "documents remain"
            self.document_label.setText(
                f"Project: {_project_name(self)} | No document is open."
            )
            self.set_status(
                f"Deleted {document_title} [{_short_document_id(document_id)}] from "
                f"project authority. {remaining} {noun}; no replacement document was "
                "opened. Choose a remaining document deliberately."
            )

        self._update_document_lifecycle_controls()
        if outcome != "error":
            _refresh_guided_navigation(self)
        return True

    visible_project_panel_init._mxztar_selection_driven_project_delete = True
    visible_close_document._mxztar_persistent_closed_document = True
    visible_delete_editor_project._mxztar_selection_confirmation = True
    visible_ensure_ready_document._mxztar_preserves_deliberate_empty_state = True
    visibly_delete_open_document._mxztar_visible_deletion = True
    ProjectAwareEditorPanel.__init__ = visible_project_panel_init
    ProjectAwareEditorPanel.close_document = visible_close_document
    ProjectAwareEditorPanel.delete_selected_project = visible_delete_editor_project
    ProjectAwareEditorPanel.ensure_ready_document = visible_ensure_ready_document
    ProjectAwareEditorPanel.delete_open_document = visibly_delete_open_document

    original_open_guided_blank_document = (
        authoring_app.AuthoringEditorForgeWindow.open_guided_blank_document
    )

    def visible_open_guided_blank_document(self) -> None:
        panel = self.editor_panel
        if (
            self.project_session.state is not None
            and getattr(panel, "_mxztar_deliberate_no_document", False)
        ):
            panel.create_blank_document()
            self._open_guided_page(authoring_app.EDITOR_PAGE_INDEX)
            self.refresh_guided_next_step()
            return
        original_open_guided_blank_document(self)

    visible_open_guided_blank_document._mxztar_creates_after_deliberate_close = True
    authoring_app.AuthoringEditorForgeWindow.open_guided_blank_document = (
        visible_open_guided_blank_document
    )

    controller_class = authoring_app.StartHereProjectController
    original_controller_init = controller_class.__init__

    def visible_delete_selected_project(self, *_args) -> bool:
        panel = self.panel
        feedback = panel.project_trash_feedback_label
        if panel._project_mutation_sources:
            detail = "Finish active project work before deleting a project."
            panel.set_status(detail)
            feedback.setText(f"Project Trash: deletion not completed. {detail}")
            return False

        selected = panel.project_selector.currentData()
        if not selected:
            detail = "Choose one canonical project before using Delete Project."
            panel.set_status(detail)
            feedback.setText(f"Project Trash: deletion not completed. {detail}")
            return False

        selected_path = Path(str(selected)).expanduser().resolve()
        project_name = selected_path.name
        if not _confirm_project_trash(panel, project_name):
            detail = "Project deletion cancelled; no project was moved."
            panel.set_status(detail)
            feedback.setText(
                f"Project Trash: deletion cancelled for {project_name}; no project was moved."
            )
            return False

        try:
            result = authoring_app.move_project_to_trash(
                panel.project_session,
                selected_path,
            )
        except Exception as exc:
            detail = f"Could not move selected project to Project Trash: {exc}"
            panel.set_status(detail)
            panel.refresh_projects()
            self.update_controls()
            feedback.setText(
                f"Project Trash: deletion not completed for {project_name}. {detail}"
            )
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
        feedback.setText(
            f"Project Trash: removed {project_name} from active projects and moved "
            "it into recoverable Project Trash."
        )
        return True

    visible_delete_selected_project._mxztar_near_field_project_feedback = True
    visible_delete_selected_project._mxztar_selection_confirmation = True
    controller_class.delete_selected_project = visible_delete_selected_project

    def visible_controller_init(self, window) -> None:
        original_controller_init(self, window)
        panel = self.panel
        self.delete_project_button.setToolTip(
            "Move the selected project into recoverable Project Trash after a simple "
            "Yes/Cancel confirmation. Active work and locked projects are protected."
        )
        panel.project_actions_layout.removeWidget(self.delete_project_button)
        panel.project_actions_layout.removeWidget(self.new_project_document_button)

        management_label = QLabel("Project management:")
        management_label.setStyleSheet("font-weight: 700;")
        management_layout = QHBoxLayout()
        management_layout.setSpacing(8)
        management_layout.addWidget(management_label)
        management_layout.addWidget(self.delete_project_button)
        management_layout.addWidget(self.new_project_document_button)
        management_layout.addStretch(1)

        project_frame = panel.close_project_button.parentWidget()
        project_layout = project_frame.layout() if project_frame is not None else None
        if project_layout is None:
            raise RuntimeError("Start Here project authority layout is unavailable.")
        project_layout.addLayout(management_layout)

        project_trash_feedback_label = QLabel("Project Trash: no recent action.")
        project_trash_feedback_label.setWordWrap(True)
        project_trash_feedback_label.setStyleSheet("color: #cfcfcf;")
        project_layout.addWidget(project_trash_feedback_label)

        panel.project_management_label = management_label
        panel.project_management_layout = management_layout
        panel.project_trash_feedback_label = project_trash_feedback_label

    visible_controller_init._mxztar_dedicated_project_management_row = True
    controller_class.__init__ = visible_controller_init

    def visible_update(self, *_args) -> None:
        editor_active = self.window.pages.currentWidget() is self.panel
        self.bar.setVisible(editor_active)
        if editor_active:
            QTimer.singleShot(
                0,
                lambda: self.page_scroll.verticalScrollBar().setValue(
                    self.page_scroll.verticalScrollBar().minimum()
                ),
            )

    def reveal_without_clipped_copy(self) -> None:
        if self.window.pages.currentWidget() is not self.panel:
            return
        target = self.panel.view_stack.currentWidget()
        content = self.page_scroll.widget()
        if target is None or content is None:
            return
        target_top = target.mapTo(content, QPoint(0, 0)).y()
        scrollbar = self.page_scroll.verticalScrollBar()
        scrollbar.setValue(
            max(scrollbar.minimum(), min(scrollbar.maximum(), target_top))
        )

    visible_update._mxztar_unclipped_editor_entry = True
    reveal_without_clipped_copy._mxztar_unclipped_output_reveal = True
    EditorMouseWheelController._update_visibility = visible_update
    EditorMouseWheelController._reveal_active_output = reveal_without_clipped_copy
