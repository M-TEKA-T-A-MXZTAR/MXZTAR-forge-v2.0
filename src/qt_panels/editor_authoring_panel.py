#!/usr/bin/env python3
"""Project-aware Editor controls and direct paired shape/object deletion."""

from __future__ import annotations

import copy

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
)

from core.object_scene import save_object_scene
from core.object_scene_membership import reconcile_scene_membership
from core.project_authoring_workflow import create_fresh_project, switch_project
from core.project_session import discover_project_directories
from core.shape_document import write_shape_document_autosave
from core.shape_document_deletion import delete_shape_from_document
from qt_panels.editor_usability_panel import SingleObjectWorkspacePanel


class ProjectAwareEditorPanel(SingleObjectWorkspacePanel):
    """Keep project switching, document switching, and direct deletion inside Editor."""

    project_authority_changed = Signal(object, str)

    def __init__(self, project_session):
        super().__init__(project_session)
        self.header_label.setText(
            "EDITOR; project/document shape-CAD workspace. Switch projects, create a fresh "
            "project document, select one shape/object, then edit or delete it deliberately."
        )
        self._install_project_controls()
        self._install_delete_controls()
        self.refresh_project_choices()
        self._update_delete_controls()

    def _install_project_controls(self) -> None:
        self.project_selector_label = QLabel("Current project:")
        self.project_selector_label.setStyleSheet("font-weight: 600;")
        self.project_selector = QComboBox()
        self.project_selector.setToolTip(
            "Switch the Editor and every connected panel to another canonical Forge project."
        )
        self.refresh_projects_button = QPushButton("Refresh")
        self.refresh_projects_button.clicked.connect(self.refresh_project_choices)
        self.switch_project_button = QPushButton("Switch Project")
        self.switch_project_button.clicked.connect(self.switch_selected_project)
        self.new_project_document_button = QPushButton("New Project + Document")
        self.new_project_document_button.setToolTip(
            "Close the current project safely, create a uniquely named fresh project, "
            "and open a new blank shape document."
        )
        self.new_project_document_button.clicked.connect(
            self.create_fresh_project_and_document
        )

        project_row = QHBoxLayout()
        project_row.setSpacing(7)
        project_row.addWidget(self.project_selector_label)
        project_row.addWidget(self.project_selector, 1)
        project_row.addWidget(self.refresh_projects_button)
        project_row.addWidget(self.switch_project_button)
        project_row.addWidget(self.new_project_document_button)
        self.layout().insertLayout(1, project_row)
        self.project_controls_layout = project_row

    def _install_delete_controls(self) -> None:
        self.delete_selected_action = QAction("Delete Selected Shape/Object…", self)
        self.delete_selected_action.setToolTip(
            "Delete the selected source shape and its paired 3D object. "
            "This is a direct deletion, not Edit → Undo."
        )
        self.delete_selected_action.triggered.connect(
            lambda _checked=False: self.delete_selected_shape_object(confirm=True)
        )
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.delete_selected_action)
        self.object_menu.addSeparator()
        self.object_menu.addAction(self.delete_selected_action)

        self.delete_selected_button = QPushButton("Delete Selected Shape/Object…")
        self.delete_selected_button.setToolTip(self.delete_selected_action.toolTip())
        self.delete_selected_button.clicked.connect(
            lambda _checked=False: self.delete_selected_shape_object(confirm=True)
        )
        inspector_layout = self.inspector.layout()
        inspector_layout.addWidget(self.delete_selected_button, 5, 0, 1, 4)
        inspector_layout.setRowStretch(6, 1)

    def refresh_project_choices(self, *_args) -> None:
        current_path = str(self.project_session.project_dir) if self.project_session.project_dir else None
        selected_path = self.project_selector.currentData()
        signals_were_blocked = self.project_selector.blockSignals(True)
        self.project_selector.clear()
        try:
            projects = discover_project_directories(self.project_session.projects_root)
            for path in projects:
                self.project_selector.addItem(path.name, str(path))
            desired = current_path or selected_path
            if desired:
                index = self.project_selector.findData(desired)
                if index >= 0:
                    self.project_selector.setCurrentIndex(index)
        except Exception as exc:
            self.set_status(f"Could not discover Editor projects: {exc}")
        finally:
            self.project_selector.blockSignals(signals_were_blocked)
        self._update_project_controls()

    def _update_project_controls(self) -> None:
        selected = self.project_selector.currentData()
        current = str(self.project_session.project_dir) if self.project_session.project_dir else None
        self.switch_project_button.setEnabled(bool(selected and selected != current))
        self.new_project_document_button.setEnabled(True)
        self.refresh_projects_button.setEnabled(True)
        self.project_selector.setEnabled(self.project_selector.count() > 0)

    def set_project_state(self, state) -> None:
        super().set_project_state(state)
        if hasattr(self, "project_selector"):
            self.refresh_project_choices()
            self._update_delete_controls()

    def switch_selected_project(self, *_args):
        selected = self.project_selector.currentData()
        if not selected:
            self.set_status("Choose a canonical project before switching the Editor.")
            return None
        try:
            state = switch_project(self.project_session, selected)
            self.set_project_state(state)
            self.project_authority_changed.emit(state, "Switched")
            self.set_status(
                f"Switched Editor authority to project: {state.assessment.project_dir.name}."
            )
            return state
        except Exception as exc:
            self.set_project_state(self.project_session.state)
            self.set_status(f"Could not switch Editor project: {exc}")
            return None

    def create_fresh_project_and_document(self, *_args):
        try:
            state = create_fresh_project(self.project_session)
            self.set_project_state(state)
            self.project_authority_changed.emit(state, "Created")
            self.create_blank_document()
            self.refresh_project_choices()
            self.set_status(
                f"Created fresh project and blank Editor document: "
                f"{state.assessment.project_dir.name}."
            )
            return state
        except Exception as exc:
            self.set_project_state(self.project_session.state)
            self.set_status(f"Could not create a fresh Editor project/document: {exc}")
            return None

    def ensure_ready_document(self) -> bool:
        """Guarantee that entering Editor has project authority and an open document."""
        if self.project_session.state is None:
            return self.create_fresh_project_and_document() is not None
        self.load_project_build()
        if self.document is None:
            self.create_blank_document()
        return self.document is not None

    def _selected_source_shape_id(self) -> str | None:
        selected = self._selected_scene_object()
        if selected is not None:
            source_shape_id = selected.get("source_shape_id")
            if isinstance(source_shape_id, str):
                return source_shape_id
        if isinstance(self.document, dict) and self.document.get("objects"):
            source_shape_id = self.document["objects"][-1].get("object_id")
            return source_shape_id if isinstance(source_shape_id, str) else None
        return None

    def _update_delete_controls(self) -> None:
        if not hasattr(self, "delete_selected_action"):
            return
        enabled = bool(
            self.project_session.is_writable
            and self.document is not None
            and self._selected_source_shape_id() is not None
        )
        self.delete_selected_action.setEnabled(enabled)
        self.delete_selected_button.setEnabled(enabled)

    def update_controls(self) -> None:
        super().update_controls()
        self._update_delete_controls()
        if hasattr(self, "project_selector"):
            self._update_project_controls()

    def select_cad_object(self, object_id) -> None:
        super().select_cad_object(object_id)
        self._update_delete_controls()

    def delete_selected_shape_object(self, *, confirm: bool = True) -> bool:
        if self.document is None or not self.project_session.is_writable:
            self.set_status("Open a writable shape document before deleting a shape/object.")
            return False
        source_shape_id = self._selected_source_shape_id()
        if source_shape_id is None:
            self.set_status("Select one shape/object before deleting it.")
            return False

        shape = next(
            (
                item
                for item in self.document.get("objects", [])
                if item.get("object_id") == source_shape_id
            ),
            None,
        )
        shape_name = shape.get("type", "shape") if isinstance(shape, dict) else "shape"
        if confirm:
            answer = QMessageBox.question(
                self,
                "Delete selected shape/object",
                f"Delete the selected {shape_name} from both the 2D document and 3D scene?\n\n"
                "This direct deletion is separate from Edit → Undo.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel,
            )
            if answer != QMessageBox.StandardButton.Yes:
                self.set_status("Delete cancelled; the selected shape/object was not changed.")
                return False

        original_document = copy.deepcopy(self.document)
        original_scene = copy.deepcopy(self.object_scene)
        original_selection = self.selected_object_id
        shape_written = False
        scene_written = False
        try:
            updated_document = delete_shape_from_document(
                original_document,
                source_shape_id,
            )
            updated_scene = original_scene
            removed = 0
            if original_scene is not None:
                updated_scene, _added, removed = reconcile_scene_membership(
                    original_scene,
                    updated_document,
                )

            write_shape_document_autosave(self.project_session, updated_document)
            shape_written = True
            if updated_scene is not None and updated_scene != original_scene:
                save_object_scene(self.project_session, updated_scene)
                scene_written = True

            selected = None
            if updated_scene is not None and updated_scene.get("objects"):
                selected = updated_scene["objects"][-1]["object_id"]
            self._restore_workspace_state(updated_document, updated_scene, selected)
            self._update_delete_controls()
            self.set_status(
                f"Deleted selected {shape_name} from the 2D document and "
                f"{removed} paired 3D object(s)."
            )
            return True
        except Exception as exc:
            rollback_errors = []
            if scene_written and original_scene is not None:
                try:
                    save_object_scene(self.project_session, original_scene)
                except Exception as rollback_exc:
                    rollback_errors.append(f"3D rollback failed: {rollback_exc}")
            if shape_written:
                try:
                    write_shape_document_autosave(
                        self.project_session,
                        original_document,
                    )
                except Exception as rollback_exc:
                    rollback_errors.append(f"2D rollback failed: {rollback_exc}")
            self._restore_workspace_state(
                original_document,
                original_scene,
                original_selection,
            )
            suffix = f" {'; '.join(rollback_errors)}" if rollback_errors else ""
            self.set_status(f"Could not delete the selected shape/object: {exc}.{suffix}")
            return False
