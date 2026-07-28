#!/usr/bin/env python3
"""Live Qt corrections for visible deletion and unclipped Editor entry.

The underlying document and Project Trash transactions remain authoritative. These
small startup-installed guards correct the live presentation around those durable
operations so a successful deletion is unmistakable and controls remain visible.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QPoint, QTimer
from PySide6.QtWidgets import QHBoxLayout, QLabel

import qt_editor_authoring_app as authoring_app
from qt_panels.editor_authoring_panel import ProjectAwareEditorPanel
from qt_panels.editor_panel import EditorPanel
from qt_panels.editor_wheel_controls import EditorMouseWheelController


_INSTALLED = False


def _short_document_id(document_id: object) -> str:
    value = document_id if isinstance(document_id, str) else "unknown"
    return value[-8:]


def _label_document_choices(panel: EditorPanel) -> None:
    """Make same-title documents distinguishable in the selector."""
    for index in range(panel.document_selector.count()):
        document_id = panel.document_selector.itemData(index)
        label = panel.document_selector.itemText(index)
        suffix = f" [{_short_document_id(document_id)}]"
        if not label.endswith(suffix):
            panel.document_selector.setItemText(index, label + suffix)


def install_live_acceptance_guards() -> None:
    """Install the acceptance-driven UI corrections once before window creation."""
    global _INSTALLED
    if _INSTALLED:
        return
    _INSTALLED = True

    original_refresh_documents = EditorPanel.refresh_documents

    def visible_refresh_documents(self, selected_document_id=None):
        outcome = original_refresh_documents(self, selected_document_id)
        _label_document_choices(self)
        return outcome

    visible_refresh_documents._mxztar_visible_document_labels = True
    EditorPanel.refresh_documents = visible_refresh_documents

    original_delete_open_document = ProjectAwareEditorPanel.delete_open_document

    def visibly_delete_open_document(self, *, confirm: bool = True) -> bool:
        document = self.document
        if not isinstance(document, dict):
            return original_delete_open_document(self, confirm=confirm)
        document_id = document.get("document_id", "unknown")
        document_title = document.get("title", document_id)

        deleted = original_delete_open_document(self, confirm=confirm)
        if not deleted:
            return False

        remaining = self.document_selector.count()
        if self.document is not None:
            self.close_document()
        else:
            blocked = self.document_selector.blockSignals(True)
            try:
                self.document_selector.setCurrentIndex(-1)
            finally:
                self.document_selector.blockSignals(blocked)
            self._restore_workspace_state(None, None, None)

        state = self.project_session.state
        project_name = (
            state.assessment.manifest.get(
                "project_name",
                state.assessment.project_dir.name,
            )
            if state is not None
            else "unknown"
        )
        self.document_label.setText(f"Project: {project_name} | No document is open.")
        noun = "document remains" if remaining == 1 else "documents remain"
        self.set_status(
            f"Deleted {document_title} [{_short_document_id(document_id)}] from project "
            f"authority. {remaining} {noun}; no replacement document was opened. "
            "Choose a remaining document deliberately."
        )
        self._update_document_lifecycle_controls()
        return True

    visibly_delete_open_document._mxztar_visible_deletion = True
    ProjectAwareEditorPanel.delete_open_document = visibly_delete_open_document

    controller_class = authoring_app.StartHereProjectController
    original_controller_init = controller_class.__init__
    original_delete_selected_project = controller_class.delete_selected_project

    def visible_delete_selected_project(self, *_args) -> bool:
        selected = self.panel.project_selector.currentData()
        project_name = Path(str(selected)).name if selected else "selected project"
        deleted = original_delete_selected_project(self, *_args)
        detail = self.panel.status_label.text().strip()
        if deleted:
            self.panel.project_status_label.setText(
                f"Removed from active projects: {project_name}\n"
                "Moved into recoverable Project Trash."
            )
        else:
            self.panel.project_status_label.setText(
                f"Project deletion not completed: {project_name}\n{detail}"
            )
        return deleted

    visible_delete_selected_project._mxztar_near_field_project_feedback = True
    controller_class.delete_selected_project = visible_delete_selected_project

    def visible_controller_init(self, window) -> None:
        original_controller_init(self, window)
        panel = self.panel
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
        panel.project_management_label = management_label
        panel.project_management_layout = management_layout

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
