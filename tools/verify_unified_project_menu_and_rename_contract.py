#!/usr/bin/env python3
"""Verify one Project menu and transactional editable project display names."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PySide6.QtCore import QSettings  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

import core.editor_project_access as editor_project_access  # noqa: E402
import core.project_access as project_access  # noqa: E402
import core.project_rename as project_rename  # noqa: E402
import qt_editor_authoring_app as authoring_app  # noqa: E402
import qt_live_acceptance_guards as live_guards  # noqa: E402
import qt_project_menu_and_rename as project_ui  # noqa: E402
import qt_project_menu_review_fixes as review_fixes  # noqa: E402
from core.project_manifest import load_project_manifest  # noqa: E402
from core.project_session import ProjectSession  # noqa: E402
from qt_app import SETTINGS_APP, SETTINGS_ORG  # noqa: E402


EXPECTED_ACTIONS = [
    "Switch Project…",
    "Save Project",
    "New Project + Document…",
    "Rename Selected Project…",
    "Delete Selected Project…",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def process(app: QApplication) -> None:
    app.processEvents()
    app.processEvents()


def close_safely(window, app: QApplication) -> None:
    if window is None:
        return
    window.close()
    deadline = time.monotonic() + 10.0
    while window.isVisible() and time.monotonic() < deadline:
        process(app)
        time.sleep(0.01)
    if window.isVisible():
        window.jobs_panel.request_scan_shutdown()
        window.library_panel.request_thumbnail_shutdown()
        window.shape_panel.request_scan_shutdown()
        deadline = time.monotonic() + 10.0
        while (
            window.jobs_panel.has_active_scan()
            or window.library_panel.has_active_thumbnail_loading()
            or window.shape_panel.has_active_scan()
        ) and time.monotonic() < deadline:
            process(app)
            time.sleep(0.01)
        window.close()
        process(app)
    window.deleteLater()
    process(app)


def action_labels(menu) -> list[str]:
    return [action.text() for action in menu.actions() if not action.isSeparator()]


def selector_labels(selector) -> list[str]:
    return [selector.itemText(index) for index in range(selector.count())]


def main() -> int:
    live_guards.install_live_acceptance_guards()
    project_ui.install_project_menu_and_rename()
    review_fixes.install_project_menu_review_fixes()

    with tempfile.TemporaryDirectory(prefix="mxztar-project-menu-rename-") as temporary:
        root = Path(temporary)
        settings_root = root / "settings"
        settings_root.mkdir()
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        QSettings.setPath(
            QSettings.Format.IniFormat,
            QSettings.Scope.UserScope,
            str(settings_root),
        )

        app = QApplication.instance() or QApplication([])
        app.setOrganizationName(SETTINGS_ORG)
        app.setApplicationName(SETTINGS_APP)
        settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
        settings.clear()
        settings.sync()

        projects_root = root / "projects"
        session = ProjectSession(projects_root)
        alpha_state = session.create_and_open("Alpha Project", "Verify active rename")
        alpha_path = alpha_state.assessment.project_dir
        alpha_id = alpha_state.assessment.manifest["project_id"]
        (alpha_path / "README.md").write_text(
            "Project preamble retained during rename.\n\n# Alpha Project\n\nOriginal details.\n",
            encoding="utf-8",
        )

        beta_session = ProjectSession(projects_root)
        beta_state = beta_session.create_and_open("Beta Project", "Verify inactive rename")
        beta_path = beta_state.assessment.project_dir
        beta_id = beta_state.assessment.manifest["project_id"]
        beta_session.close()

        window = None
        try:
            window = authoring_app.AuthoringEditorForgeWindow(session)
            window.resize(980, 760)
            window.show()
            process(app)

            start_panel = window.start_here_panel
            editor_panel = window.editor_panel
            controller = window.start_here_project_controller

            require(
                start_panel.project_selector.isEditable()
                and editor_panel.project_selector.isEditable(),
                "Start Here and Editor project names are directly editable",
            )
            require(
                start_panel.open_project_button.text() == "Project"
                and editor_panel.switch_project_button.text() == "Project",
                "Start Here and Editor expose one Project dropdown control",
            )
            require(
                action_labels(start_panel.project_menu) == EXPECTED_ACTIONS
                and action_labels(editor_panel.project_menu) == EXPECTED_ACTIONS,
                "both Project dropdowns expose switch, save, create, rename, and delete",
            )
            require(
                controller.delete_project_button.isHidden()
                and controller.new_project_document_button.isHidden()
                and editor_panel.delete_project_button.isHidden()
                and editor_panel.new_project_document_button.isHidden(),
                "scattered project delete and create buttons are removed from view",
            )

            save_calls: list[str] = []
            original_save_project = editor_panel.save_project

            def counted_save_project(*_args) -> bool:
                save_calls.append("save")
                editor_panel.set_status("Saved active project verification.")
                return True

            editor_panel.save_project = counted_save_project
            try:
                require(
                    start_panel.project_save_action.isEnabled()
                    and editor_panel.project_save_action.isEnabled(),
                    "Save Project is visibly enabled for the attached writable project",
                )
                start_panel.project_save_action.trigger()
                process(app)
                editor_panel.project_save_action.trigger()
                process(app)
            finally:
                editor_panel.save_project = original_save_project
            require(
                save_calls == ["save", "save"],
                "both visible Save Project actions route through the active Editor save authority",
            )

            alpha_index = start_panel.project_selector.findData(str(alpha_path))
            start_panel.project_selector.setCurrentIndex(alpha_index)
            process(app)
            require(
                project_ui.rename_selected_project(
                    start_panel,
                    window,
                    "Alpha Display Renamed",
                ),
                "the attached project can be renamed through writable authority",
            )
            process(app)

            alpha_manifest = load_project_manifest(alpha_path)
            require(
                alpha_path.exists()
                and alpha_path.name == "alpha-project"
                and alpha_manifest["project_id"] == alpha_id
                and alpha_manifest["project_name"] == "Alpha Display Renamed",
                "rename changes display value without changing directory or immutable project ID",
            )
            history_lines = (
                alpha_path / alpha_manifest["history_path"]
            ).read_text(encoding="utf-8").splitlines()
            rename_event = json.loads(history_lines[-1])
            require(
                rename_event["event"] == "project_renamed"
                and rename_event["previous_project_name"] == "Alpha Project"
                and rename_event["project_name"] == "Alpha Display Renamed",
                "project rename records one durable old-name/new-name history event",
            )
            readme_text = (alpha_path / "README.md").read_text(encoding="utf-8")
            readme_headings = [line for line in readme_text.splitlines() if line.startswith("# ")]
            require(
                readme_text.startswith("Project preamble retained during rename.")
                and readme_headings == ["# Alpha Display Renamed"],
                "rename replaces the first README heading without duplicating a preambled heading",
            )
            require(
                session.project_dir == alpha_path
                and session.state.assessment.manifest["project_name"]
                == "Alpha Display Renamed",
                "attached writer authority remains on the same project after rename",
            )

            start_panel.project_selector.setCurrentIndex(
                start_panel.project_selector.findData(str(alpha_path))
            )
            line_edit = start_panel.project_selector.lineEdit()
            start_panel._project_mutation_sources.add("verification-active-work")
            try:
                line_edit.setText("Blocked During Active Work")
                require(
                    not project_ui._commit_name_edit(start_panel, window)
                    and load_project_manifest(alpha_path)["project_name"]
                    == "Alpha Display Renamed"
                    and line_edit.text() == "Alpha Display Renamed",
                    "active project work blocks an editing-finished rename and restores the committed label",
                )
            finally:
                start_panel._project_mutation_sources.discard("verification-active-work")

            beta_index = editor_panel.project_selector.findData(str(beta_path))
            editor_panel.project_selector.setCurrentIndex(beta_index)
            process(app)
            require(
                project_ui.rename_selected_project(
                    editor_panel,
                    window,
                    "Alpha Display Renamed",
                ),
                "an inactive selected project can be renamed through a temporary lock",
            )
            process(app)
            beta_manifest = load_project_manifest(beta_path)
            require(
                beta_path.exists()
                and beta_path.name == "beta-project"
                and beta_manifest["project_id"] == beta_id
                and beta_manifest["project_name"] == "Alpha Display Renamed"
                and session.project_dir == alpha_path,
                "inactive rename preserves its directory and the currently attached project",
            )

            start_panel.refresh_projects()
            editor_panel.refresh_project_choices()
            process(app)
            start_alpha = start_panel.project_selector.itemText(
                start_panel.project_selector.findData(str(alpha_path))
            )
            start_beta = start_panel.project_selector.itemText(
                start_panel.project_selector.findData(str(beta_path))
            )
            require(
                alpha_id[-8:] in start_alpha
                and beta_id[-8:] in start_beta
                and start_alpha != start_beta,
                "duplicate display names remain distinguishable by short immutable IDs",
            )

            gamma_session = ProjectSession(projects_root)
            gamma_state = gamma_session.create_and_open("Gamma Project", "Verify label collision")
            gamma_path = gamma_state.assessment.project_dir
            gamma_id = gamma_state.assessment.manifest["project_id"]
            gamma_session.close()
            editor_panel.refresh_project_choices()
            gamma_index = editor_panel.project_selector.findData(str(gamma_path))
            editor_panel.project_selector.setCurrentIndex(gamma_index)
            literal_collision = f"Alpha Display Renamed [{alpha_id[-8:]}]"
            require(
                project_ui.rename_selected_project(
                    editor_panel,
                    window,
                    literal_collision,
                ),
                "a literal suffix-like display name can be committed",
            )
            start_panel.refresh_projects()
            editor_panel.refresh_project_choices()
            process(app)
            labels = selector_labels(start_panel.project_selector)
            require(
                len(labels) == len({label.casefold() for label in labels})
                and gamma_id in " ".join(labels),
                "final rendered selector labels remain unique after a literal suffix collision",
            )

            recovery_session = ProjectSession(projects_root)
            recovery_state = recovery_session.create_and_open(
                "Recovery Marker Project",
                "Verify interrupted rename recovery",
            )
            recovery_path = recovery_state.assessment.project_dir
            recovery_session.close()
            (recovery_path / project_rename.TRANSACTION_MARKER).write_text(
                "{}\n",
                encoding="utf-8",
            )
            base_assessment = project_access.assess_project_open(recovery_path)
            editor_assessment = editor_project_access.assess_project_open(recovery_path)
            require(
                base_assessment.status is project_access.ProjectAccessStatus.READ_ONLY_RECOVERY
                and editor_assessment.status
                is project_access.ProjectAccessStatus.READ_ONLY_RECOVERY
                and any("rename transaction" in item for item in base_assessment.diagnostics)
                and any("rename transaction" in item for item in editor_assessment.diagnostics),
                "interrupted rename markers block both base and Editor writable project opening",
            )
            (recovery_path / project_rename.TRANSACTION_MARKER).unlink()

            cleanup_session = ProjectSession(projects_root)
            cleanup_state = cleanup_session.create_and_open(
                "Cleanup Failure Project",
                "Verify temporary lease cleanup reporting",
            )
            cleanup_path = cleanup_state.assessment.project_dir
            cleanup_session.close()
            editor_panel.refresh_project_choices()
            editor_panel.project_selector.setCurrentIndex(
                editor_panel.project_selector.findData(str(cleanup_path))
            )
            original_close = ProjectSession.close

            def injected_close_failure(self):
                if self.project_dir == cleanup_path:
                    raise RuntimeError("injected temporary lease release failure")
                return original_close(self)

            ProjectSession.close = injected_close_failure
            try:
                cleanup_result = project_ui.rename_selected_project(
                    editor_panel,
                    window,
                    "Cleanup Rename Committed",
                )
            finally:
                ProjectSession.close = original_close
            lock_path = cleanup_path / project_access.LOCK_FILENAME
            require(
                not cleanup_result
                and load_project_manifest(cleanup_path)["project_name"]
                == "Cleanup Rename Committed"
                and lock_path.exists()
                and "could not be released" in editor_panel.status_label.text().lower()
                and "explicit recovery" in editor_panel.status_label.text().lower(),
                "temporary lease cleanup failure is reported as a partial failure with recovery guidance",
            )
            lock_path.unlink()

            start_panel.project_selector.setCurrentIndex(
                start_panel.project_selector.findData(str(alpha_path))
            )
            project_ui._preview_name(start_panel, window, "Live Name Preview")
            process(app)
            editor_alpha = editor_panel.project_selector.itemText(
                editor_panel.project_selector.findData(str(alpha_path))
            )
            require(
                editor_alpha == "Live Name Preview"
                and "Live Name Preview" in start_panel.project_status_label.text(),
                "typing a project name updates matching visible project values immediately",
            )
            start_panel.refresh_projects()
            editor_panel.refresh_project_choices()
        finally:
            close_safely(window, app)
            if session.state is not None:
                session.close()

    print("PASS: unified Project menu and editable project-name contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
