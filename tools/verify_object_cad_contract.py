#!/usr/bin/env python3
"""Verify the project-owned 3D object CAD authority and Editor integration."""

from __future__ import annotations

import copy
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from PySide6.QtWidgets import QApplication  # noqa: E402

import core.object_scene as object_scene_module  # noqa: E402
from core.object_scene import (  # noqa: E402
    create_object_scene,
    load_object_scene,
    redo_scene,
    save_object_scene,
    set_scene_view,
    sync_scene_from_shape_document,
    undo_scene,
    update_scene_object,
)
from core.project_session import ProjectSession  # noqa: E402
from core.shape_document import (  # noqa: E402
    add_circle,
    add_ellipse,
    add_rectangle,
    add_square,
    add_star,
    create_blank_shape_document,
    save_shape_document,
    write_shape_document_autosave,
)
from qt_panels.object_cad_panel import ObjectCadEditorPanel  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def main() -> int:
    app = QApplication.instance() or QApplication([])
    with tempfile.TemporaryDirectory(prefix="mxztar-object-cad-") as temporary:
        projects_root = Path(temporary) / "projects"
        session = ProjectSession(projects_root)
        state = session.create_and_open("Object CAD Contract", "Verify 3D-first object CAD")
        require(state.writable, "object CAD test project opens with writable authority")

        created = create_blank_shape_document(session, title="CAD Shapes")
        document = created.document
        document = add_rectangle(document, x=80, y=90)
        document = add_square(document, x=350, y=90)
        document = add_circle(document, x=580, y=90)
        document = add_ellipse(document, x=180, y=380)
        document = add_star(document, x=500, y=370)
        save_shape_document(session, document)

        scene = create_object_scene(
            session.state.assessment.manifest["project_id"],
            document,
        )
        require(
            [item["primitive_type"] for item in scene["objects"]]
            == ["rectangle", "square", "circle", "ellipse", "star"],
            "all five native shapes become real 3D CAD objects",
        )
        require(
            all(
                item["position"]["z"] > 0
                and item["size"]["z"] > 0
                and set(item["rotation_deg"]) == {"x", "y", "z"}
                for item in scene["objects"]
            ),
            "CAD objects carry 3D position, depth, and three-axis rotation authority",
        )

        scene_path = save_object_scene(session, scene)
        require(scene_path.is_file(), "object scene is written canonically inside the project")
        require(
            scene["scene_id"] in session.state.assessment.manifest["current_artifact_ids"],
            "object scene is registered in project manifest authority",
        )
        loaded = load_object_scene(session, document["document_id"])
        require(loaded == scene, "canonical object scene reloads without state drift")

        first = copy.deepcopy(loaded["objects"][0])
        changed = copy.deepcopy(first)
        changed["position"] = {"x": 420.0, "y": 310.0, "z": 95.0}
        changed["size"] = {"x": 310.0, "y": 205.0, "z": 145.0}
        changed["rotation_deg"] = {"x": 18.0, "y": 27.0, "z": 36.0}
        changed["appearance"] = {"color": "#336699", "opacity": 0.55}
        edited = update_scene_object(loaded, first["object_id"], changed)
        require(
            edited["objects"][0] == changed,
            "move, resize, depth, rotation, color, and opacity are one reversible object command",
        )
        undone = undo_scene(edited)
        require(
            undone["objects"][0] == first,
            "object undo restores the exact pre-edit 3D state",
        )
        redone = redo_scene(undone)
        require(
            redone["objects"][0] == changed,
            "object redo restores the exact edited 3D state",
        )

        viewed = set_scene_view(
            redone,
            yaw_deg=67.0,
            pitch_deg=41.0,
            zoom=1.25,
            perspective=False,
            grid_visible=False,
            edges_visible=False,
        )
        save_object_scene(session, viewed)
        restored_view = load_object_scene(session, document["document_id"])
        require(
            restored_view["view"]
            == {
                "yaw_deg": 67.0,
                "pitch_deg": 41.0,
                "zoom": 1.25,
                "perspective": False,
                "grid_visible": False,
                "edges_visible": False,
            },
            "perspective, camera, grid, lines, and zoom persist in project authority",
        )

        new_shape_document = add_rectangle(document, x=720, y=520, width=120, height=90)
        save_shape_document(session, new_shape_document)
        document = new_shape_document
        synchronized, added = sync_scene_from_shape_document(
            restored_view,
            new_shape_document,
        )
        require(added == 1, "object scene synchronizes one newly visible source shape")
        require(
            len(synchronized["objects"]) == 6,
            "shape-to-object synchronization preserves existing CAD edits",
        )
        save_object_scene(session, synchronized)

        panel = ObjectCadEditorPanel(session)
        panel.set_project_state(session.state)
        app.processEvents()
        require(
            panel.header_label.text().startswith("EDITOR; shape/object CAD workspace"),
            "Editor presents shape/object CAD as the primary workspace",
        )
        require(
            [action.text() for action in panel.object_menu.actions()]
            == [
                "Sync Shapes to 3D",
                "Undo Object Change",
                "Redo Object Change",
                "Reset Selected Object",
                "Change Selected Color…",
            ],
            "Object menu exposes only implemented CAD operations",
        )
        require(
            [action.text() for action in panel.view_menu.actions() if not action.isSeparator()]
            == ["2D Shape View", "3D Object View", "Perspective", "Grid", "Lines"],
            "View menu exposes 2D/3D, perspective, grid, and line controls",
        )
        require(
            panel.object_scene is not None
            and len(panel.object_scene["objects"]) == 6
            and panel.view_stack.currentWidget() is panel.object_viewport,
            "opening a shaped document loads its 3D object scene at the front of Editor",
        )
        panel.object_viewport.resize(800, 560)
        panel.object_viewport.show()
        app.processEvents()
        image = panel.object_viewport.grab()
        require(not image.isNull(), "CPU-safe 3D viewport renders offscreen")
        require(
            bool(panel.object_viewport._projected_faces),
            "3D viewport projects selectable object faces",
        )
        require(
            panel.inspector.isEnabled() and panel.selected_object_id is not None,
            "opening the 3D scene selects an object and enables the numeric inspector",
        )

        selected = panel._selected_scene_object()
        changed_from_panel = copy.deepcopy(selected)
        changed_from_panel["position"]["x"] += 25.0
        changed_from_panel["size"]["z"] += 15.0
        changed_from_panel["rotation_deg"]["y"] += 12.0
        changed_from_panel["appearance"]["opacity"] = 0.4
        panel.commit_viewport_object(selected["object_id"], changed_from_panel)
        require(
            panel._selected_scene_object() == changed_from_panel,
            "Editor commits direct-manipulation object changes through durable scene authority",
        )

        autosave_document = add_rectangle(panel.document, x=20, y=720, width=80, height=60)
        write_shape_document_autosave(session, autosave_document)
        panel.load_project_build()
        require(
            "Recovered a newer autosave" in panel.status_label.text()
            and "Save Document" in panel.status_label.text(),
            "3D scene loading preserves the shape-document autosave recovery warning",
        )

        scene_id = panel.object_scene["scene_id"]
        saved_scene_revision = panel.object_scene["revision"]
        panel.deleteLater()
        app.processEvents()
        session.close()

        reopened = ProjectSession(projects_root)
        reopened_state = reopened.open(projects_root / "object-cad-contract")
        require(reopened_state.writable, "object CAD project reopens with writable authority")
        restored_scene = load_object_scene(reopened, document["document_id"])
        require(
            restored_scene["scene_id"] == scene_id
            and restored_scene["revision"] == saved_scene_revision
            and restored_scene["objects"][0]["appearance"]["opacity"] == 0.4,
            "restart restores the edited 3D object scene and style state",
        )

        manifest_path = reopened.project_dir / "project.json"
        history_path = reopened.project_dir / reopened.state.assessment.manifest["history_path"]
        canonical_path = (
            reopened.project_dir
            / "structures"
            / "object-scenes"
            / f"{document['document_id']}.object-scene.json"
        )
        marker_path = reopened.project_dir / ".mxztar-editor-transaction.json"
        canonical_before = canonical_path.read_bytes()
        manifest_before = manifest_path.read_bytes()
        history_before = history_path.read_bytes()

        failing = set_scene_view(restored_scene, yaw_deg=75.0)
        original_atomic_write = object_scene_module.atomic_write_text
        failure_used = False

        def fail_history_once(path: Path, text: str) -> None:
            nonlocal failure_used
            if Path(path) == history_path and not failure_used:
                failure_used = True
                raise OSError("simulated object-scene history interruption")
            original_atomic_write(path, text)

        object_scene_module.atomic_write_text = fail_history_once
        try:
            try:
                save_object_scene(reopened, failing)
            except OSError as exc:
                require(
                    "simulated object-scene history interruption" in str(exc),
                    "object-scene transaction interruption reaches the caller truthfully",
                )
            else:
                raise AssertionError("simulated object-scene transaction unexpectedly succeeded")
        finally:
            object_scene_module.atomic_write_text = original_atomic_write

        require(
            canonical_path.read_bytes() == canonical_before
            and manifest_path.read_bytes() == manifest_before
            and history_path.read_bytes() == history_before,
            "failed object-scene save rolls back canonical, manifest, and history truth",
        )
        require(
            not marker_path.exists(),
            "confirmed object-scene rollback clears the shared editor transaction marker",
        )
        reopened.close()

    print("PASS: project-owned 3D object CAD contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
