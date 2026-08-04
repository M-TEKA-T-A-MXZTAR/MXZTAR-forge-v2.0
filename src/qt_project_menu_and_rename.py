#!/usr/bin/env python3
"""Unified project menus and editable project display names for Start Here and Editor."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QComboBox, QMenu

import qt_editor_authoring_app as authoring_app
from core.project_manifest import load_project_manifest
from core.project_rename import ProjectRenameError, normalize_project_display_name, rename_project
from core.project_session import ProjectSession
from qt_panels.editor_authoring_panel import ProjectAwareEditorPanel
from qt_panels.editor_authority_guard import GuardedProjectAwareEditorPanel
from qt_panels.start_here_panel import StartHerePanel

RAW_NAME_ROLE = int(Qt.ItemDataRole.UserRole) + 1
PROJECT_ID_ROLE = int(Qt.ItemDataRole.UserRole) + 2


def _resolved_path(value: object) -> Path | None:
    if value is None:
        return None
    try:
        return Path(str(value)).expanduser().resolve()
    except (OSError, RuntimeError, ValueError):
        return None


def _project_metadata(path: Path) -> tuple[str, str]:
    try:
        manifest = load_project_manifest(path)
        return manifest["project_name"], manifest["project_id"]
    except Exception:
        return path.name, f"path_{path.name}"


def _selector_metadata(selector: QComboBox) -> None:
    entries: list[tuple[int, str, str]] = []
    counts: dict[str, int] = {}
    for index in range(selector.count()):
        path = _resolved_path(selector.itemData(index))
        if path is None:
            continue
        name, project_id = _project_metadata(path)
        entries.append((index, name, project_id))
        key = name.casefold()
        counts[key] = counts.get(key, 0) + 1

    for index, name, project_id in entries:
        label = name
        if counts.get(name.casefold(), 0) > 1:
            label = f"{name} [{project_id[-8:]}]"
        selector.setItemText(index, label)
        selector.setItemData(index, name, RAW_NAME_ROLE)
        selector.setItemData(index, project_id, PROJECT_ID_ROLE)

    _show_current_raw_name(selector)


def _show_current_raw_name(selector: QComboBox) -> None:
    if not selector.isEditable() or selector.lineEdit() is None:
        return
    index = selector.currentIndex()
    raw = selector.itemData(index, RAW_NAME_ROLE) if index >= 0 else ""
    line_edit = selector.lineEdit()
    blocked = line_edit.blockSignals(True)
    try:
        line_edit.setText(raw if isinstance(raw, str) else "")
        line_edit.setProperty("mxztar_committed_project_name", raw or "")
    finally:
        line_edit.blockSignals(blocked)


def _item_index_for_path(selector: QComboBox, path: Path) -> int:
    target = str(path)
    for index in range(selector.count()):
        if str(selector.itemData(index)) == target:
            return index
    return -1


def _set_selected_path(selector: QComboBox, path: Path | None) -> None:
    if path is None:
        return
    index = _item_index_for_path(selector, path)
    if index >= 0:
        selector.setCurrentIndex(index)
        _show_current_raw_name(selector)


def _replace_project_prefix(label, project_name: str) -> None:
    text = label.text()
    if text.startswith("Project:") and "|" in text:
        label.setText(f"Project: {project_name} |{text.split('|', 1)[1]}")


def _preview_name(panel, window, text: str) -> None:
    path = _resolved_path(panel.project_selector.currentData())
    if path is None:
        return
    for selector in (
        window.start_here_panel.project_selector,
        window.editor_panel.project_selector,
    ):
        index = _item_index_for_path(selector, path)
        if index >= 0:
            selector.setItemText(index, text)
            if selector is not panel.project_selector and selector.isEditable():
                if selector.currentIndex() == index and selector.lineEdit() is not None:
                    blocked = selector.lineEdit().blockSignals(True)
                    try:
                        selector.lineEdit().setText(text)
                    finally:
                        selector.lineEdit().blockSignals(blocked)

    active = _resolved_path(panel.project_session.project_dir)
    if active != path:
        return
    status_label = window.start_here_panel.project_status_label
    status = status_label.text().splitlines()
    if status:
        prefix = status[0].split(":", 1)[0] if ":" in status[0] else "Attached"
        status[0] = f"{prefix}: {text}"
        status_label.setText("\n".join(status))
    _replace_project_prefix(window.editor_panel.document_label, text)


def _refresh_project_surfaces(window, selected_path: Path | None) -> None:
    window.start_here_panel.refresh_projects()
    window.editor_panel.refresh_project_choices()
    _set_selected_path(window.start_here_panel.project_selector, selected_path)
    _set_selected_path(window.editor_panel.project_selector, selected_path)


def _save_active_project(window, status_panel) -> bool:
    """Route the visible Save Project command to the active Editor authority."""
    editor_panel = getattr(window, "editor_panel", None)
    save_handler = getattr(editor_panel, "save_project", None)
    if not callable(save_handler):
        status_panel.set_status("Save Project is unavailable in the active Editor build.")
        return False
    result = bool(save_handler())
    if status_panel is not editor_panel and hasattr(editor_panel, "status_label"):
        status_panel.set_status(editor_panel.status_label.text())
    return result


def rename_selected_project(panel, window, new_name: str) -> bool:
    """Rename the selected project through its own writable authority boundary."""
    selected_path = _resolved_path(panel.project_selector.currentData())
    if selected_path is None:
        panel.set_status("Choose one canonical project before renaming it.")
        return False
    try:
        name = normalize_project_display_name(new_name)
    except ProjectRenameError as exc:
        panel.set_status(f"Could not rename project: {exc}")
        _refresh_project_surfaces(window, selected_path)
        return False

    active_path = _resolved_path(panel.project_session.project_dir)
    temporary_session: ProjectSession | None = None
    session = panel.project_session
    try:
        if active_path != selected_path:
            temporary_session = ProjectSession(panel.project_session.projects_root)
            state = temporary_session.open(selected_path)
            if not state.writable:
                raise ProjectRenameError(
                    "The selected project is locked or available only for recovery."
                )
            session = temporary_session
        result = rename_project(session, name)
    except Exception as exc:
        panel.set_status(f"Could not rename project: {exc}")
        _refresh_project_surfaces(window, selected_path)
        return False
    finally:
        if temporary_session is not None and temporary_session.state is not None:
            try:
                temporary_session.close()
            except Exception:
                # Preserve the completed rename result; ProjectSession.close already
                # retains recovery diagnostics when lease cleanup cannot be confirmed.
                pass

    _refresh_project_surfaces(window, selected_path)
    current = panel.project_session.state
    if current is not None and _resolved_path(panel.project_session.project_dir) == selected_path:
        window.start_here_panel.refresh_attached_project_state(current)
        window.start_here_panel.project_changed.emit(current)
    panel.set_status(
        f"Renamed project display value from {result.previous_name} to {result.project_name}. "
        f"Directory and project ID were unchanged."
    )
    return True


def _commit_name_edit(panel, window) -> bool:
    if getattr(panel, "_mxztar_committing_project_name", False):
        return False
    line_edit = panel.project_selector.lineEdit()
    if line_edit is None:
        return False
    proposed = line_edit.text()
    committed = line_edit.property("mxztar_committed_project_name") or ""
    if proposed == committed:
        return False
    panel._mxztar_committing_project_name = True
    try:
        return rename_selected_project(panel, window, proposed)
    finally:
        panel._mxztar_committing_project_name = False


def _begin_name_edit(panel) -> None:
    line_edit = panel.project_selector.lineEdit()
    if line_edit is None:
        return
    line_edit.setFocus(Qt.FocusReason.ShortcutFocusReason)
    line_edit.selectAll()


def _prepare_editable_selector(panel, window_provider) -> None:
    selector = panel.project_selector
    selector.setEditable(True)
    selector.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
    selector.setToolTip(
        "Select a project or click its displayed name to edit the project display value. "
        "The canonical directory and immutable project ID do not change."
    )
    line_edit = selector.lineEdit()
    line_edit.setClearButtonEnabled(False)
    line_edit.setPlaceholderText("Select or edit a project name")
    selector.currentIndexChanged.connect(lambda _index: _show_current_raw_name(selector))
    line_edit.textEdited.connect(
        lambda text: _preview_name(panel, window_provider(), text)
    )
    line_edit.editingFinished.connect(
        lambda: _commit_name_edit(panel, window_provider())
    )
    _selector_metadata(selector)


def _install_start_here_menu(controller) -> None:
    panel = controller.panel
    window = controller.window
    _prepare_editable_selector(panel, lambda: window)

    menu = QMenu(panel.open_project_button)
    switch_action = QAction("Switch Project…", menu)
    save_action = QAction("Save Project", menu)
    new_action = QAction("New Project + Document…", menu)
    rename_action = QAction("Rename Selected Project…", menu)
    delete_action = QAction("Delete Selected Project…", menu)
    save_action.setToolTip(
        "Save the currently attached project, including its open document, object scene, "
        "and pending 3D camera state."
    )
    switch_action.triggered.connect(controller.open_selected_project)
    save_action.triggered.connect(
        lambda _checked=False: _save_active_project(window, panel)
    )
    new_action.triggered.connect(controller.create_fresh_project_document)
    rename_action.triggered.connect(lambda _checked=False: _begin_name_edit(panel))
    delete_action.triggered.connect(controller.delete_selected_project)
    menu.addActions([switch_action, save_action, new_action, rename_action])
    menu.addSeparator()
    menu.addAction(delete_action)

    panel.open_project_button.setText("Project")
    panel.open_project_button.setToolTip(
        "Save or switch the active project, create a project, rename a selection, or move "
        "the selected project to Project Trash."
    )
    panel.open_project_button.setMenu(menu)
    controller.delete_project_button.hide()
    controller.new_project_document_button.hide()
    if hasattr(panel, "project_management_label"):
        panel.project_management_label.hide()

    panel.project_menu = menu
    panel.project_switch_action = switch_action
    panel.project_save_action = save_action
    panel.project_new_document_action = new_action
    panel.project_rename_action = rename_action
    panel.project_delete_action = delete_action


def _install_editor_menu(panel) -> None:
    _prepare_editable_selector(panel, panel.window)

    menu = QMenu(panel.switch_project_button)
    switch_action = QAction("Switch Project…", menu)
    save_action = QAction("Save Project", menu)
    new_action = QAction("New Project + Document…", menu)
    rename_action = QAction("Rename Selected Project…", menu)
    delete_action = QAction("Delete Selected Project…", menu)
    save_action.setToolTip(
        "Save the currently attached project, including its open document, object scene, "
        "and pending 3D camera state."
    )
    switch_action.triggered.connect(panel.switch_selected_project)
    save_action.triggered.connect(
        lambda _checked=False: _save_active_project(panel.window(), panel)
    )
    new_action.triggered.connect(panel.create_fresh_project_and_document)
    rename_action.triggered.connect(lambda _checked=False: _begin_name_edit(panel))
    delete_action.triggered.connect(
        lambda _checked=False: panel.delete_selected_project(confirm=True)
    )
    menu.addActions([switch_action, save_action, new_action, rename_action])
    menu.addSeparator()
    menu.addAction(delete_action)

    panel.switch_project_button.setText("Project")
    panel.switch_project_button.setToolTip(
        "Save or switch the active project, create a project, rename a selection, or move "
        "the selected project to Project Trash."
    )
    panel.switch_project_button.setMenu(menu)
    panel.delete_project_button.hide()
    panel.new_project_document_button.hide()

    panel.project_menu = menu
    panel.project_switch_action = switch_action
    panel.project_save_action = save_action
    panel.project_new_document_action = new_action
    panel.project_rename_action = rename_action
    panel.project_delete_action = delete_action


def _sync_start_here_actions(controller) -> None:
    if not hasattr(controller.panel, "project_menu"):
        return
    panel = controller.panel
    unlocked = not panel._project_mutation_sources
    selected = _resolved_path(panel.project_selector.currentData())
    current = _resolved_path(panel.project_session.project_dir)
    writable = bool(panel.project_session.state is not None and panel.project_session.is_writable)
    panel.project_switch_action.setEnabled(bool(unlocked and selected and selected != current))
    panel.project_save_action.setEnabled(bool(unlocked and writable))
    panel.project_new_document_action.setEnabled(unlocked)
    panel.project_rename_action.setEnabled(bool(unlocked and selected))
    panel.project_delete_action.setEnabled(bool(unlocked and selected))
    panel.open_project_button.setEnabled(unlocked)


def _sync_editor_actions(panel) -> None:
    if not hasattr(panel, "project_menu"):
        return
    unlocked = not bool(getattr(panel, "_project_mutation_sources", set()))
    selected = _resolved_path(panel.project_selector.currentData())
    current = _resolved_path(panel.project_session.project_dir)
    writable = bool(panel.project_session.state is not None and panel.project_session.is_writable)
    panel.project_switch_action.setEnabled(bool(unlocked and selected and selected != current))
    panel.project_save_action.setEnabled(bool(unlocked and writable))
    panel.project_new_document_action.setEnabled(unlocked)
    panel.project_rename_action.setEnabled(bool(unlocked and selected))
    panel.project_delete_action.setEnabled(bool(unlocked and selected))
    panel.switch_project_button.setEnabled(unlocked)


def install_project_menu_and_rename() -> None:
    """Install the unified project interaction contract once before window creation."""
    if getattr(install_project_menu_and_rename, "_installed", False):
        return
    install_project_menu_and_rename._installed = True

    original_start_refresh = StartHerePanel.refresh_projects
    original_show_state = StartHerePanel._show_project_state
    original_refresh_attached = StartHerePanel.refresh_attached_project_state

    def display_refresh_projects(self, *_args):
        result = original_start_refresh(self, *_args)
        _selector_metadata(self.project_selector)
        return result

    def display_show_state(self, state, action: str):
        result = original_show_state(self, state, action)
        name = state.assessment.manifest.get("project_name", state.assessment.project_dir.name)
        lines = self.project_status_label.text().splitlines()
        if lines:
            lines[0] = f"{action}: {name}"
            self.project_status_label.setText("\n".join(lines))
        return result

    def display_refresh_attached(self, state):
        result = original_refresh_attached(self, state)
        if state is not None:
            name = state.assessment.manifest.get(
                "project_name", state.assessment.project_dir.name
            )
            lines = self.project_status_label.text().splitlines()
            if lines:
                lines[0] = f"Attached: {name}"
                self.project_status_label.setText("\n".join(lines))
        return result

    StartHerePanel.refresh_projects = display_refresh_projects
    StartHerePanel._show_project_state = display_show_state
    StartHerePanel.refresh_attached_project_state = display_refresh_attached

    original_editor_refresh = ProjectAwareEditorPanel.refresh_project_choices

    def display_refresh_project_choices(self, *_args):
        result = original_editor_refresh(self, *_args)
        _selector_metadata(self.project_selector)
        return result

    ProjectAwareEditorPanel.refresh_project_choices = display_refresh_project_choices

    controller_class = authoring_app.StartHereProjectController
    original_controller_init = controller_class.__init__
    original_controller_update = controller_class.update_controls

    def unified_controller_init(self, window) -> None:
        original_controller_init(self, window)
        _install_start_here_menu(self)
        self.panel.project_menu.aboutToShow.connect(lambda: _sync_start_here_actions(self))
        self.panel.project_selector.currentIndexChanged.connect(
            lambda _index: _sync_start_here_actions(self)
        )
        _sync_start_here_actions(self)

    def unified_controller_update(self) -> None:
        original_controller_update(self)
        _sync_start_here_actions(self)

    controller_class.__init__ = unified_controller_init
    controller_class.update_controls = unified_controller_update

    original_editor_init = ProjectAwareEditorPanel.__init__

    def unified_editor_init(self, project_session) -> None:
        original_editor_init(self, project_session)
        _install_editor_menu(self)
        self.project_menu.aboutToShow.connect(lambda: _sync_editor_actions(self))
        self.project_selector.currentIndexChanged.connect(
            lambda _index: _sync_editor_actions(self)
        )
        _sync_editor_actions(self)

    ProjectAwareEditorPanel.__init__ = unified_editor_init

    for panel_class in (ProjectAwareEditorPanel, GuardedProjectAwareEditorPanel):
        original_update = panel_class._update_project_controls

        def unified_update(self, _original=original_update) -> None:
            _original(self)
            _sync_editor_actions(self)

        panel_class._update_project_controls = unified_update

    unified_controller_init._mxztar_unified_project_menu = True
    unified_controller_init._mxztar_dedicated_project_management_row = getattr(
        original_controller_init, "_mxztar_dedicated_project_management_row", False
    )
    unified_editor_init._mxztar_unified_project_menu = True
    unified_editor_init._mxztar_selection_driven_project_delete = getattr(
        original_editor_init, "_mxztar_selection_driven_project_delete", False
    )
    display_refresh_projects._mxztar_manifest_project_names = True
    display_refresh_project_choices._mxztar_manifest_project_names = True
