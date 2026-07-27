#!/usr/bin/env python3
"""Verify document close/delete authority and non-animated Next guidance."""

from __future__ import annotations

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

import core.shape_document_deletion as deletion_module  # noqa: E402
from core.editor_project_access import EDITOR_TRANSACTION_FILENAME  # noqa: E402
from core.project_session import ProjectSession  # noqa: E402
from qt_app import SETTINGS_APP, SETTINGS_ORG  # noqa: E402
from qt_editor_app import EDITOR_PAGE_INDEX  # noqa: E402
from qt_editor_authoring_app import AuthoringEditorForgeWindow  # noqa: E402


SHAPE_DIR = Path("structures/shape-documents")
SCENE_DIR = Path("structures/object-scenes")


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


def document_path(project_dir: Path, document_id: str) -> Path:
    return project_dir / SHAPE_DIR / f"{document_id}.shape.json"


def scene_path(project_dir: Path, document_id: str) -> Path:
    return project_dir / SCENE_DIR / f"{document_id}.object-scene.json"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mxztar-document-lifecycle-") as temporary:
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
        session.create_and_open(
            "Document Lifecycle Contract",
            "Verify close, delete, rollback, and static guidance",
        )

        window = None
        try:
            window = AuthoringEditorForgeWindow(session)
            window.resize(980, 760)
            window.show()
            window.open_page(EDITOR_PAGE_INDEX)
            process(app)
            panel = window.editor_panel

            require(
                not window.guided_pulse_timer.isActive(),
                "Next Action pulse timer is stopped in the authoring shell",
            )
            static_style = window.next_step_button.styleSheet()
            window.toggle_guided_pulse()
            window.toggle_guided_pulse()
            require(
                static_style
                and window.next_step_button.styleSheet() == static_style,
                "Next Action styling remains static across former pulse callbacks",
            )

            document_actions = [
                action.text()
                for action in panel.document_menu.actions()
                if not action.isSeparator()
            ]
            require(
                "Close Document" in document_actions
                and "Delete Document…" in document_actions,
                "Document dropdown exposes Close Document and Delete Document",
            )

            first_document_id = panel.document["document_id"]
            panel.add_rectangle_command()
            process(app)

            panel.create_blank_document()
            process(app)
            second_document_id = panel.document["document_id"]
            panel.add_circle_command()
            process(app)
            second_scene_id = panel.object_scene["scene_id"]
            second_document_path = document_path(session.project_dir, second_document_id)
            second_scene_path = scene_path(session.project_dir, second_document_id)
            require(
                second_document_path.is_file() and second_scene_path.is_file(),
                "second document and paired 3D scene exist before lifecycle actions",
            )

            require(panel.close_document(), "Close Document succeeds for the open document")
            require(
                panel.document is None
                and panel.object_scene is None
                and panel.document_selector.currentIndex() == -1,
                "Close Document clears only the active workspace selection",
            )
            require(
                second_document_path.is_file() and second_scene_path.is_file(),
                "Close Document leaves canonical project files unchanged",
            )

            second_index = panel.document_selector.findData(second_document_id)
            require(second_index >= 0, "closed document remains available to reopen")
            panel.document_selector.setCurrentIndex(second_index)
            process(app)
            require(
                panel.document is not None
                and panel.document["document_id"] == second_document_id,
                "choosing the closed document reopens it",
            )

            require(
                panel.delete_open_document(confirm=False),
                "Delete Document removes the selected document deliberately",
            )
            require(
                not second_document_path.exists() and not second_scene_path.exists(),
                "Delete Document removes canonical shape and paired object-scene files",
            )
            current_ids = session.state.assessment.manifest["current_artifact_ids"]
            require(
                second_document_id not in current_ids and second_scene_id not in current_ids,
                "Delete Document removes both artifacts from manifest authority",
            )
            require(
                panel.document is not None
                and panel.document["document_id"] == first_document_id,
                "Delete Document continues with the remaining project document",
            )

            panel.create_blank_document()
            process(app)
            rollback_document_id = panel.document["document_id"]
            panel.add_square_command()
            process(app)
            rollback_scene_id = panel.object_scene["scene_id"]
            rollback_document_path = document_path(session.project_dir, rollback_document_id)
            rollback_scene_path = scene_path(session.project_dir, rollback_document_id)
            manifest_path = session.project_dir / "project.json"
            history_path = session.project_dir / session.state.assessment.manifest["history_path"]
            marker_path = session.project_dir / EDITOR_TRANSACTION_FILENAME
            document_before = rollback_document_path.read_bytes()
            scene_before = rollback_scene_path.read_bytes()
            manifest_before = manifest_path.read_bytes()
            history_before = history_path.read_bytes()

            original_atomic_write = deletion_module.atomic_write_text
            failure_used = False

            def fail_history_once(path: Path, text: str) -> None:
                nonlocal failure_used
                if Path(path) == history_path and not failure_used:
                    failure_used = True
                    raise OSError("simulated document deletion history failure")
                original_atomic_write(path, text)

            deletion_module.atomic_write_text = fail_history_once
            try:
                require(
                    not panel.delete_open_document(confirm=False),
                    "failed Delete Document reports failure instead of detaching the workspace",
                )
            finally:
                deletion_module.atomic_write_text = original_atomic_write

            require(failure_used, "rollback test reaches the document deletion history write")
            require(
                rollback_document_path.read_bytes() == document_before
                and rollback_scene_path.read_bytes() == scene_before
                and manifest_path.read_bytes() == manifest_before
                and history_path.read_bytes() == history_before,
                "failed Delete Document restores shape, scene, manifest, and history bytes",
            )
            require(
                rollback_document_id in session.state.assessment.manifest["current_artifact_ids"]
                and rollback_scene_id in session.state.assessment.manifest["current_artifact_ids"]
                and not marker_path.exists()
                and session.is_writable,
                "confirmed deletion rollback preserves authority and clears its marker",
            )
        finally:
            close_safely(window, app)
            if session.state is not None:
                session.close()

    print("PASS: document lifecycle and static Next Action contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
