#!/usr/bin/env python3
"""Verify visible shape placement, isolated object edits, and current-page Editor sizing."""

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

from PySide6.QtCore import QSize  # noqa: E402
from PySide6.QtWidgets import QApplication, QWidget  # noqa: E402

from core.project_session import ProjectSession  # noqa: E402
from qt_editor_usability_app import CurrentPageStack  # noqa: E402
from qt_panels.editor_usability_panel import SingleObjectWorkspacePanel  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def overlaps(first: dict, second: dict) -> bool:
    return not (
        first["x"] + first["width"] <= second["x"]
        or second["x"] + second["width"] <= first["x"]
        or first["y"] + first["height"] <= second["y"]
        or second["y"] + second["height"] <= first["y"]
    )


class HintWidget(QWidget):
    def __init__(self, size: QSize):
        super().__init__()
        self._hint = size

    def sizeHint(self) -> QSize:
        return self._hint

    def minimumSizeHint(self) -> QSize:
        return self._hint


def main() -> int:
    app = QApplication.instance() or QApplication([])
    with tempfile.TemporaryDirectory(prefix="mxztar-single-object-") as temporary:
        session = ProjectSession(Path(temporary) / "projects")
        state = session.create_and_open(
            "Single Object Workspace",
            "Verify one-object editing and visible Editor layout",
        )
        require(state.writable, "single-object test project opens with writable authority")

        panel = SingleObjectWorkspacePanel(session)
        panel.set_project_state(session.state)
        panel.create_blank_document()
        panel.add_rectangle_command()
        panel.add_square_command()
        panel.add_circle_command()
        panel.add_ellipse_command()
        panel.add_star_command()
        app.processEvents()

        shapes = panel.document["objects"]
        require(len(shapes) == 5, "all five requested shapes exist in the native document")
        require(
            not any(
                overlaps(shapes[first], shapes[second])
                for first in range(len(shapes))
                for second in range(first + 1, len(shapes))
            ),
            "new shapes use non-overlapping visible grid positions",
        )
        require(
            panel.object_scene is not None
            and len(panel.object_scene["objects"]) == 5
            and len(panel.object_viewport._preview_objects) == 5,
            "each new shape appears in the 3D Editor immediately without manual resynchronization",
        )
        newest_shape = shapes[-1]
        expected_selected = f"cad_{newest_shape['object_id'].removeprefix('object_')}"
        require(
            panel.selected_object_id == expected_selected,
            "the newest created object becomes the single active selection",
        )

        require(
            panel.layout().indexOf(panel.workspace_splitter) == 3
            and panel.workspace_splitter.widget(0) is panel.view_stack
            and panel.workspace_splitter.widget(1) is panel.inspector,
            "visual output and Object Inspector share one side-by-side Editor workspace",
        )

        target_before = panel.object_viewport._scene_target()
        objects_before = {
            item["object_id"]: copy.deepcopy(item)
            for item in panel.object_scene["objects"]
        }
        selected = panel._selected_scene_object()
        updated = copy.deepcopy(selected)
        updated["position"]["x"] += 85.0
        updated["position"]["y"] += 45.0
        panel.commit_viewport_object(selected["object_id"], updated)
        app.processEvents()

        require(
            panel.object_viewport._scene_target() == target_before,
            "moving one object does not recenter the camera or make every object slide",
        )
        require(
            all(
                item["object_id"] == selected["object_id"]
                or item == objects_before[item["object_id"]]
                for item in panel.object_scene["objects"]
            ),
            "moving the selected object leaves every nonselected object unchanged",
        )

        pages = CurrentPageStack()
        tall_hidden_page = HintWidget(QSize(900, 1400))
        compact_editor_page = HintWidget(QSize(900, 430))
        pages.addWidget(tall_hidden_page)
        pages.addWidget(compact_editor_page)
        pages.setCurrentWidget(compact_editor_page)
        require(
            pages.minimumSizeHint().height() == 430
            and pages.sizeHint().height() == 430,
            "page sizing follows the visible Editor instead of a taller hidden page",
        )

        panel.deleteLater()
        pages.deleteLater()
        app.processEvents()
        session.close()

    print("PASS: single-object Editor workspace contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
