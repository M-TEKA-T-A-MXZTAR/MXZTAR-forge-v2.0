#!/usr/bin/env python3
"""Verify the native shape-document and minimum Editor foundation."""

from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PySide6.QtWidgets import QApplication, QPushButton

import core.shape_document as shape_document_module
import qt_panels.editor_panel as editor_panel_module
from core.editor_project_access import EDITOR_TRANSACTION_FILENAME
from core.project_session import ProjectSession
from core.shape_document import (
    add_rectangle,
    create_blank_shape_document,
    list_shape_documents,
    load_shape_document,
    save_shape_document,
)
from qt_panels.editor_panel import EditorPanel


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def main() -> int:
    app = QApplication.instance() or QApplication([])
    with tempfile.TemporaryDirectory(prefix="mxztar-shape-editor-") as temporary:
        projects_root = Path(temporary) / "projects"
        session = ProjectSession(projects_root)
        state = session.create_and_open("Native Shape Contract", "Verify editor foundation")
        require(state.writable, "test project opens with writable authority")
        require(list_shape_documents(session) == (), "legacy project opens before editor storage exists")

        created = create_blank_shape_document(session)
        document_id = created.document["document_id"]
        canonical_path = created.canonical_path
        second = create_blank_shape_document(session, title="Second Shape")
        second_document_id = second.document["document_id"]
        autosave_path = (
            session.project_dir
            / "structures"
            / "shape-documents"
            / ".autosave"
            / f"{document_id}.autosave.json"
        )
        require(canonical_path.is_file(), "blank shape document is written canonically")
        require(
            document_id in session.state.assessment.manifest["current_artifact_ids"],
            "blank shape document is registered in manifest authority",
        )
        require(
            created.document["objects"] == [] and created.document["history_cursor"] == 0,
            "blank document starts with empty replayable editor state",
        )

        panel = EditorPanel(session)
        panel.set_project_state(session.state)
        require(panel.document_selector.count() == 2, "Editor discovers both project-owned documents")
        require(panel.document is not None, "Editor opens a discovered native document")

        current_document_id = panel.document_selector.currentData()
        selection_target = (
            second_document_id if current_document_id != second_document_id else document_id
        )
        require(
            panel.document_selector.findData(selection_target)
            != panel.document_selector.currentIndex(),
            "Editor refresh verifier targets a non-current document",
        )
        original_panel_load = editor_panel_module.load_shape_document
        panel_load_count = 0

        def count_panel_load(project_session: ProjectSession, selected_id: str):
            nonlocal panel_load_count
            panel_load_count += 1
            return original_panel_load(project_session, selected_id)

        editor_panel_module.load_shape_document = count_panel_load
        try:
            panel.refresh_documents(selection_target)
        finally:
            editor_panel_module.load_shape_document = original_panel_load
        require(
            panel_load_count == 1
            and panel.document_selector.currentData() == selection_target,
            "Editor refresh selects, loads, and renders a non-first document exactly once",
        )
        panel.refresh_documents(document_id)
        require(
            panel.document is not None and panel.document["document_id"] == document_id,
            "Editor returns to the primary document for command verification",
        )
        require(
            not any(
                word in button.text().casefold()
                for button in panel.findChildren(QPushButton)
                for word in ("extract", "boolean", "3d", "export", "approve")
            ),
            "Editor exposes no unsupported extraction, boolean, 3D, export, or approval controls",
        )

        panel.add_rectangle_button.click()
        app.processEvents()
        require(len(panel.document["objects"]) == 1, "Add Rectangle creates one visible object")
        require(len(panel.scene.items()) == 1, "Editor canvas renders the rectangle")
        require(autosave_path.is_file(), "reversible edit is autosaved separately from canonical truth")
        recovered = load_shape_document(session, document_id)
        require(recovered.recovered_from_autosave, "newer autosave is recovered on reopen")
        require(recovered.document["revision"] == 2, "autosave recovery preserves edited revision")

        panel.undo_button.click()
        app.processEvents()
        require(len(panel.document["objects"]) == 0, "Undo removes the replayed rectangle")
        require(panel.redo_button.isEnabled(), "Redo becomes available after undo")
        panel.redo_button.click()
        app.processEvents()
        require(len(panel.document["objects"]) == 1, "Redo restores the replayed rectangle")

        panel.save_button.click()
        app.processEvents()
        require(not autosave_path.exists(), "explicit save clears the superseded autosave")
        saved_revision = panel.document["revision"]
        require(
            load_shape_document(session, document_id).document["revision"] == saved_revision,
            "explicit save makes the current editor revision canonical",
        )

        session.close()
        reopened = ProjectSession(projects_root)
        reopened_state = reopened.open(projects_root / "native-shape-contract")
        require(reopened_state.writable, "saved editor project reopens with writable authority")
        restored = load_shape_document(reopened, document_id)
        require(
            restored.document["revision"] == saved_revision
            and len(restored.document["objects"]) == 1,
            "restart restores the editable document and command state",
        )

        manifest_path = reopened.project_dir / "project.json"
        history_path = reopened.project_dir / reopened.state.assessment.manifest["history_path"]
        marker_path = reopened.project_dir / EDITOR_TRANSACTION_FILENAME
        canonical_before = canonical_path.read_bytes()
        manifest_before = manifest_path.read_bytes()
        history_before = history_path.read_bytes()
        oversized = copy.deepcopy(restored.document)
        oversized["title"] = "x" * shape_document_module.MAX_DOCUMENT_BYTES
        oversized = shape_document_module._with_integrity(oversized)

        for writer, label in (
            (
                lambda: shape_document_module.write_shape_document_autosave(reopened, oversized),
                "oversized autosave",
            ),
            (lambda: save_shape_document(reopened, oversized), "oversized canonical save"),
        ):
            try:
                writer()
            except shape_document_module.ShapeDocumentError as exc:
                require(
                    "safe write limit" in str(exc),
                    f"{label} is rejected before unreadable bytes are written",
                )
            else:
                raise AssertionError(f"{label} unexpectedly succeeded")

        require(not autosave_path.exists(), "oversized autosave rejection creates no recovery file")
        require(
            canonical_path.read_bytes() == canonical_before
            and manifest_path.read_bytes() == manifest_before
            and history_path.read_bytes() == history_before,
            "oversized write rejection leaves canonical project truth unchanged",
        )
        require(not marker_path.exists(), "oversized canonical rejection creates no transaction marker")

        stale_temporary = canonical_path.with_name(f"{canonical_path.name}.tmp")
        stale_temporary.write_text("{interrupted", encoding="utf-8")
        require(
            load_shape_document(reopened, document_id).document["revision"] == saved_revision,
            "stale interrupted temporary bytes cannot replace the last valid canonical document",
        )
        stale_temporary.unlink()

        changed = add_rectangle(restored.document, x=420, y=420)
        original_atomic_write = shape_document_module.atomic_write_text
        failure_used = False

        def fail_history_once(path: Path, text: str) -> None:
            nonlocal failure_used
            if Path(path) == history_path and not failure_used:
                failure_used = True
                raise OSError("simulated history write interruption")
            original_atomic_write(path, text)

        shape_document_module.atomic_write_text = fail_history_once
        try:
            try:
                save_shape_document(reopened, changed)
            except OSError as exc:
                require(
                    "simulated history write interruption" in str(exc),
                    "simulated transaction failure reaches the caller truthfully",
                )
            else:
                raise AssertionError("simulated editor transaction failure was not raised")
        finally:
            shape_document_module.atomic_write_text = original_atomic_write

        require(
            load_shape_document(reopened, document_id).document["revision"] == saved_revision,
            "failed multi-file save rolls canonical shape truth back",
        )
        require(
            not (reopened.project_dir / EDITOR_TRANSACTION_FILENAME).exists(),
            "confirmed rollback clears the editor transaction marker",
        )
        require(reopened.is_writable, "confirmed rollback preserves writable project authority")

        reopened.close()
        marker = projects_root / "native-shape-contract" / EDITOR_TRANSACTION_FILENAME
        marker.write_text(
            json.dumps(
                {
                    "schema_name": "mxztar_forge_editor_transaction",
                    "schema_version": "1.0.0",
                    "operation": "save_shape_document",
                }
            )
            + "\n",
            encoding="utf-8",
        )
        interrupted = ProjectSession(projects_root)
        interrupted_state = interrupted.open(projects_root / "native-shape-contract")
        require(
            not interrupted_state.writable
            and any("editor transaction" in item for item in interrupted_state.assessment.diagnostics),
            "interrupted editor transaction reopens as explicit read-only recovery",
        )
        interrupted.close()
        marker.unlink()

        panel.deleteLater()
        app.processEvents()

    print("PASS: native shape-document and minimum Editor contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
