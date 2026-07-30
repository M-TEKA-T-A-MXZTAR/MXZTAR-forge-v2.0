#!/usr/bin/env python3
"""Codex-review corrections for project menus and editable project names."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from PySide6.QtWidgets import QComboBox

import qt_project_menu_and_rename as project_ui
import core.editor_project_access as editor_project_access
import core.project_access as project_access
import core.project_rename as project_rename
import core.project_session as project_session_module
from core.project_rename import ProjectRenameError, normalize_project_display_name, rename_project
from core.project_session import ProjectSession


_BASE_ASSESS_PROJECT_OPEN = project_access.assess_project_open
_BASE_SYNC_START_HERE_ACTIONS = project_ui._sync_start_here_actions
_BASE_SYNC_EDITOR_ACTIONS = project_ui._sync_editor_actions


def _assess_project_open_with_rename_recovery(project_dir: Path):
    """Make an interrupted rename marker a first-class recovery blocker."""
    assessment = _BASE_ASSESS_PROJECT_OPEN(project_dir)
    marker = assessment.project_dir / project_rename.TRANSACTION_MARKER
    if not marker.exists() and not marker.is_symlink():
        return assessment
    diagnostic = "An interrupted project rename transaction requires explicit read-only recovery."
    status = (
        project_access.ProjectAccessStatus.READ_ONLY_RECOVERY
        if assessment.status is project_access.ProjectAccessStatus.WRITABLE
        else assessment.status
    )
    return replace(
        assessment,
        status=status,
        diagnostics=assessment.diagnostics + (diagnostic,),
    )


def _renamed_readme_first_heading(readme_before: str, project_name: str) -> str:
    """Replace the first Markdown H1 wherever it appears, preserving any preamble."""
    lines = readme_before.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if not line.startswith("# "):
            continue
        ending = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
        lines[index] = f"# {project_name}{ending or chr(10)}"
        return "".join(lines)
    heading = f"# {project_name}\n"
    return heading if not readme_before else heading + "\n" + readme_before


def _collision_safe_selector_metadata(selector: QComboBox) -> None:
    """Render unique labels while keeping the selected editor text as the raw name."""
    entries: list[tuple[int, str, str]] = []
    counts: dict[str, int] = {}
    for index in range(selector.count()):
        path = project_ui._resolved_path(selector.itemData(index))
        if path is None:
            continue
        name, project_id = project_ui._project_metadata(path)
        entries.append((index, name, project_id))
        key = name.casefold()
        counts[key] = counts.get(key, 0) + 1

    labels = [
        f"{name} [{project_id[-8:]}]" if counts.get(name.casefold(), 0) > 1 else name
        for _index, name, project_id in entries
    ]
    if len({label.casefold() for label in labels}) != len(labels):
        # A literal display name can imitate a short-ID suffix. Full immutable IDs
        # make every dropdown label unambiguous without altering the editable name.
        labels = [f"{name} [{project_id}]" for _index, name, project_id in entries]

    for (index, name, project_id), label in zip(entries, labels, strict=True):
        selector.setItemText(index, label)
        selector.setItemData(index, name, project_ui.RAW_NAME_ROLE)
        selector.setItemData(index, project_id, project_ui.PROJECT_ID_ROLE)

    project_ui._show_current_raw_name(selector)


def _project_work_active(panel) -> bool:
    return bool(getattr(panel, "_project_mutation_sources", set()))


def _fixed_rename_selected_project(panel, window, new_name: str) -> bool:
    """Rename through writable authority and report any temporary-lease failure."""
    selected_path = project_ui._resolved_path(panel.project_selector.currentData())
    if selected_path is None:
        panel.set_status("Choose one canonical project before renaming it.")
        return False
    if _project_work_active(panel):
        panel.set_status("Finish active project work before renaming a project.")
        project_ui._refresh_project_surfaces(window, selected_path)
        return False

    try:
        name = normalize_project_display_name(new_name)
    except ProjectRenameError as exc:
        panel.set_status(f"Could not rename project: {exc}")
        project_ui._refresh_project_surfaces(window, selected_path)
        return False

    active_path = project_ui._resolved_path(panel.project_session.project_dir)
    temporary_session: ProjectSession | None = None
    session = panel.project_session
    result = None
    operation_error: Exception | None = None
    cleanup_error: Exception | None = None

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
        operation_error = exc
    finally:
        if temporary_session is not None and temporary_session.state is not None:
            try:
                temporary_session.close()
            except Exception as exc:
                cleanup_error = exc
                failures = getattr(window, "_mxztar_project_rename_cleanup_failures", [])
                failures.append((selected_path, str(exc)))
                window._mxztar_project_rename_cleanup_failures = failures

    project_ui._refresh_project_surfaces(window, selected_path)

    if operation_error is not None:
        detail = f"Could not rename project: {operation_error}"
        if cleanup_error is not None:
            detail += (
                f" Temporary writer-lock release also failed: {cleanup_error}. "
                "The selected project remains locked and requires explicit recovery."
            )
        panel.set_status(detail)
        return False

    current = panel.project_session.state
    if current is not None and project_ui._resolved_path(panel.project_session.project_dir) == selected_path:
        window.start_here_panel.refresh_attached_project_state(current)
        window.start_here_panel.project_changed.emit(current)

    if result is None:
        panel.set_status("Could not rename project: no rename result was produced.")
        return False

    if cleanup_error is not None:
        panel.set_status(
            f"Renamed project display value from {result.previous_name} to {result.project_name}, "
            f"but the temporary writer lock could not be released: {cleanup_error}. "
            "The project remains locked and requires explicit recovery."
        )
        return False

    panel.set_status(
        f"Renamed project display value from {result.previous_name} to {result.project_name}. "
        "Directory and project ID were unchanged."
    )
    return True


def _fixed_commit_name_edit(panel, window) -> bool:
    if getattr(panel, "_mxztar_committing_project_name", False):
        return False
    line_edit = panel.project_selector.lineEdit()
    if line_edit is None:
        return False
    proposed = line_edit.text()
    committed = line_edit.property("mxztar_committed_project_name") or ""
    if proposed == committed:
        return False

    selected_path = project_ui._resolved_path(panel.project_selector.currentData())
    if _project_work_active(panel):
        panel.set_status("Finish active project work before renaming a project.")
        project_ui._refresh_project_surfaces(window, selected_path)
        return False

    panel._mxztar_committing_project_name = True
    try:
        return _fixed_rename_selected_project(panel, window, proposed)
    finally:
        panel._mxztar_committing_project_name = False


def _sync_start_here_actions_with_selector(controller) -> None:
    """Keep the established project selector usable while authority is attached."""
    _BASE_SYNC_START_HERE_ACTIONS(controller)
    panel = controller.panel
    unlocked = not panel._project_mutation_sources
    panel.project_selector.setEnabled(bool(unlocked and panel.project_selector.count() > 0))


def _sync_editor_actions_with_selector(panel) -> None:
    """Keep the Editor project selector usable whenever project mutation is unlocked."""
    _BASE_SYNC_EDITOR_ACTIONS(panel)
    unlocked = not bool(getattr(panel, "_project_mutation_sources", set()))
    panel.project_selector.setEnabled(bool(unlocked and panel.project_selector.count() > 0))


def install_project_menu_review_fixes() -> None:
    """Install the review corrections once after the base project-menu contract."""
    if getattr(install_project_menu_review_fixes, "_installed", False):
        return
    install_project_menu_review_fixes._installed = True

    project_access.assess_project_open = _assess_project_open_with_rename_recovery
    editor_project_access.assess_base_project_open = _assess_project_open_with_rename_recovery
    project_session_module.assess_project_open = editor_project_access.assess_project_open
    project_rename._renamed_readme = _renamed_readme_first_heading

    project_ui._selector_metadata = _collision_safe_selector_metadata
    project_ui.rename_selected_project = _fixed_rename_selected_project
    project_ui._commit_name_edit = _fixed_commit_name_edit
    project_ui._sync_start_here_actions = _sync_start_here_actions_with_selector
    project_ui._sync_editor_actions = _sync_editor_actions_with_selector


install_project_menu_review_fixes._mxztar_codex_review_corrections = True
