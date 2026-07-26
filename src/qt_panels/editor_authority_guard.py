#!/usr/bin/env python3
"""Mutation guard for project switching and deletion inside Editor."""

from __future__ import annotations

from qt_panels.editor_authoring_panel import ProjectAwareEditorPanel
from qt_panels.positioning_guides import install_positioning_guides


class GuardedProjectAwareEditorPanel(ProjectAwareEditorPanel):
    """Block authority changes while intake or local AI work is active."""

    def __init__(self, project_session):
        self._project_mutation_sources: set[str] = set()
        super().__init__(project_session)
        install_positioning_guides(self)
        self.header_label.setText(
            "EDITOR; project/document shape-CAD workspace. Move one selected object with "
            "transient guides and measurements, optionally snap it, or drag empty space "
            "to orbit the perspective."
        )
        self.project_selector.currentIndexChanged.connect(
            lambda _index: self._update_project_controls()
        )
        self._update_project_controls()

    def _authority_unlocked(self) -> bool:
        return not self._project_mutation_sources

    def _update_project_controls(self) -> None:
        if not hasattr(self, "project_selector"):
            return
        unlocked = self._authority_unlocked()
        selected = self.project_selector.currentData()
        current = str(self.project_session.project_dir) if self.project_session.project_dir else None
        self.switch_project_button.setEnabled(
            bool(unlocked and selected and selected != current)
        )
        self.delete_project_button.setEnabled(bool(unlocked and selected))
        self.new_project_document_button.setEnabled(unlocked)
        self.refresh_projects_button.setEnabled(unlocked)
        self.project_selector.setEnabled(unlocked and self.project_selector.count() > 0)

    def _update_delete_controls(self) -> None:
        if not hasattr(self, "delete_selected_action"):
            return
        enabled = bool(
            self._authority_unlocked()
            and self.project_session.is_writable
            and self.document is not None
            and self._selected_source_shape_id() is not None
        )
        self.delete_selected_action.setEnabled(enabled)
        self.delete_selected_button.setEnabled(enabled)

    def set_project_mutation_active(self, active: bool, source: str) -> None:
        if active:
            self._project_mutation_sources.add(source)
        else:
            self._project_mutation_sources.discard(source)
        self._update_project_controls()
        self._update_delete_controls()
        if active:
            self.set_status(
                f"{source.capitalize()} is active; project switching and deletion are paused."
            )

    def switch_selected_project(self, *_args):
        if not self._authority_unlocked():
            self.set_status("Finish active project work before switching projects.")
            return None
        return super().switch_selected_project(*_args)

    def delete_selected_project(self, *, confirm: bool = True) -> bool:
        if not self._authority_unlocked():
            self.set_status("Finish active project work before deleting a project.")
            return False
        return super().delete_selected_project(confirm=confirm)

    def create_fresh_project_and_document(self, *_args):
        if not self._authority_unlocked():
            self.set_status("Finish active project work before creating a fresh project.")
            return None
        return super().create_fresh_project_and_document(*_args)

    def delete_selected_shape_object(self, *, confirm: bool = True) -> bool:
        if not self._authority_unlocked():
            self.set_status("Finish active project work before deleting a shape/object.")
            return False
        return super().delete_selected_shape_object(confirm=confirm)
