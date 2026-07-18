#!/usr/bin/env python3
"""
Agent Workflows panel for MXZTAR Forge v2.0.

Stage 3B:
- define the actual MXZTAR Forge workflows
- show end-user value and market/audience problem solved
- restore source-art discovery UI
- show local model policy
- avoid dead AI execution until QThread worker is restored
"""

import os
import subprocess
from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.source_library import SourceArtItem, format_size, known_source_dirs, scan_source_art


WORKFLOWS = {
    "source_art_intelligence": {
        "title": "Source-art intelligence",
        "purpose": (
            "Inspect the design as production material, not just as a picture. Identify visible "
            "forms, layers, visual systems, motifs, reusable surfaces, structural hints, and "
            "possible concept-engineering value."
        ),
        "end_user": (
            "For creators who have strong source art but need help converting it into usable "
            "concept, design, prompt, or asset-planning material."
        ),
        "outputs": (
            "Output forms: visual intelligence report, structure notes, reusable motif list, "
            "possible component groups, risk/quality notes, next recommended workflow."
        ),
        "next_contract": "QThread vision-agent runner using qwen2.5vl:3b with live elapsed timer.",
    },
    "modular_set_perspective": {
        "title": "Modular set perspective",
        "purpose": (
            "Imagine the source art as a kit of building-block modules. Identify candidate "
            "blocks, panels, joints, surfaces, towers, ribs, plates, connectors, shells, "
            "mechanical forms, abstract components, and repeatable construction grammar."
        ),
        "end_user": (
            "For 3D/blockout/game/film/animation creators who want a kitbash-style module set "
            "derived from their own source imagery."
        ),
        "outputs": (
            "Output forms: module candidate list, parent/child structure map, naming suggestions, "
            "blockout hints, extraction priorities, possible future OBJ/GLB/SVG planning data."
        ),
        "next_contract": "Vision report must separate real visible forms from imagined design extensions.",
    },
    "prototype_imagination": {
        "title": "Tech prototype imagination",
        "purpose": (
            "Use the source image as inspiration for possible products, machines, environments, "
            "interfaces, vehicles, tools, industrial systems, or speculative tech prototypes."
        ),
        "end_user": (
            "For concept designers and product/world builders who need idea expansion from a "
            "single visual seed."
        ),
        "outputs": (
            "Output forms: prototype concepts, user/audience gap solved, functional features, "
            "visual references, production risks, promptable variations."
        ),
        "next_contract": "Must label ideas as inferred/speculative, not factual image contents.",
    },
    "shape_structure_harvest": {
        "title": "Shape / structure harvest",
        "purpose": (
            "Identify shapes, silhouettes, curves, layers, structural stacks, repeated forms, "
            "perspective cues, and candidate extraction zones."
        ),
        "end_user": (
            "For users who want to manually understand, trace, classify, or reuse structures "
            "from detailed source art."
        ),
        "outputs": (
            "Output forms: extraction target list, visual layer notes, candidate SVG/PNG cutout "
            "ideas, manual build guidance, future shape-library entries."
        ),
        "next_contract": "Later connects to image processing and manual extraction tools.",
    },
    "concept_brief": {
        "title": "Concept brief",
        "purpose": (
            "Turn the source-art intelligence into a clear production brief with visual direction, "
            "intended outputs, audience/use case, and practical next steps."
        ),
        "end_user": (
            "For creators who need a reusable brief before prompting, modeling, rendering, or "
            "packaging a concept folder."
        ),
        "outputs": (
            "Output forms: README-ready brief, production intent, use cases, constraints, "
            "prompt direction, design-engine staging notes."
        ),
        "next_contract": "Depends on source-art intelligence report or direct user brief.",
    },
    "render_prompt_pack": {
        "title": "Render prompt pack",
        "purpose": (
            "Create prompt-ready render variations from the source art and concept brief. Prompts "
            "must be structured, reusable, and saved into My Prompts."
        ),
        "end_user": (
            "For AI-assisted creators who want faster production of coherent visual variations "
            "without losing the original design intent."
        ),
        "outputs": (
            "Output forms: prompt pack, prompt variants, negative constraints, style/material "
            "directions, My Prompts export."
        ),
        "next_contract": "Restore smart prompt extraction and My Prompts save action.",
    },
    "recommend_next_step": {
        "title": "Recommend next step",
        "purpose": (
            "Look at the selected source and current project state, then tell the user what to do "
            "next. This prevents being stuck in a wall of buttons."
        ),
        "end_user": (
            "For solo builders who need the system to behave like a cockpit, not a control maze."
        ),
        "outputs": (
            "Output forms: one recommended action, reason, expected output, and what button/workflow "
            "to run next."
        ),
        "next_contract": "Later becomes the dashboard's cockpit recommendation engine.",
    },
}


class AgentPanel(QWidget):
    status_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.source_items = []

        title = QLabel("Agent Workflows")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")

        intro = QLabel(
            "This panel defines how MXZTAR Forge turns source art into production intelligence. "
            "AI execution is deliberately held back until the safe threaded worker is restored."
        )
        intro.setWordWrap(True)
        intro.setStyleSheet("color: #cfcfcf;")

        self.model_label = QLabel(self.model_policy_text())
        self.model_label.setWordWrap(True)
        self.model_label.setStyleSheet("color: #d6c27a;")

        self.source_combo = QComboBox()
        self.source_combo.setToolTip(
            "Known source art from workspace/input, workspace/imports, and workspace/test_inputs."
        )
        self.source_combo.currentIndexChanged.connect(self.update_source_details)

        refresh_button = QPushButton("Refresh Sources")
        refresh_button.setToolTip("Rescan known source folders for supported image files.")
        refresh_button.clicked.connect(self.refresh_sources)

        open_folder_button = QPushButton("Open Source Folders")
        open_folder_button.setToolTip("Open the workspace folder in the file manager.")
        open_folder_button.clicked.connect(self.open_source_root)

        source_row = QHBoxLayout()
        source_row.addWidget(QLabel("Known source:"))
        source_row.addWidget(self.source_combo, 1)
        source_row.addWidget(refresh_button)
        source_row.addWidget(open_folder_button)

        self.workflow_combo = QComboBox()
        self.workflow_combo.addItems(WORKFLOWS.keys())
        self.workflow_combo.setToolTip("Choose the workflow definition to inspect.")
        self.workflow_combo.currentTextChanged.connect(self.update_workflow_details)

        workflow_row = QHBoxLayout()
        workflow_row.addWidget(QLabel("Workflow:"))
        workflow_row.addWidget(self.workflow_combo, 1)

        self.workflow_details = QTextEdit()
        self.workflow_details.setReadOnly(True)
        self.workflow_details.setMinimumHeight(260)

        self.source_details = QTextEdit()
        self.source_details.setReadOnly(True)
        self.source_details.setMinimumHeight(180)

        self.status_label = QLabel("Ready.")
        self.status_label.setStyleSheet("color: #d6c27a;")

        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet(
            "QFrame {"
            "background-color: #252525;"
            "border: 1px solid #3a3a3a;"
            "border-radius: 10px;"
            "padding: 12px;"
            "}"
        )

        card_layout = QVBoxLayout()
        card_layout.addWidget(self.model_label)
        card_layout.addSpacing(8)
        card_layout.addLayout(source_row)
        card_layout.addSpacing(8)
        card_layout.addLayout(workflow_row)
        card_layout.addSpacing(8)
        card_layout.addWidget(QLabel("Workflow definition / value contract:"))
        card_layout.addWidget(self.workflow_details)
        card_layout.addWidget(QLabel("Selected source details:"))
        card_layout.addWidget(self.source_details)
        card_layout.addWidget(self.status_label)
        card.setLayout(card_layout)

        next_title = QLabel("Next restoration target")
        next_title.setStyleSheet("font-size: 18px; font-weight: 700;")

        next_body = QLabel(
            "Next we rebuild the safe AI worker: Ollama call, qwen2.5vl:3b default model, "
            "2-thread policy, QThread execution, elapsed timer, progress messages, and clear "
            "output saved to workspace/data/brain. No silent freeze, no mystery waiting."
        )
        next_body.setWordWrap(True)
        next_body.setStyleSheet("color: #cfcfcf;")

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.addWidget(title)
        layout.addWidget(intro)
        layout.addSpacing(8)
        layout.addWidget(card)
        layout.addSpacing(12)
        layout.addWidget(next_title)
        layout.addWidget(next_body)
        layout.addStretch(1)
        self.setLayout(layout)

        self.refresh_sources()
        self.update_workflow_details(self.workflow_combo.currentText())

    def model_policy_text(self) -> str:
        threads = os.environ.get("OLLAMA_NUM_THREAD", "not set")
        parallel = os.environ.get("OLLAMA_NUM_PARALLEL", "not set")
        return (
            "Local core agent target: qwen2.5vl:3b. "
            f"Hardware-kind policy: {threads} CPU threads, {parallel} parallel AI job."
        )

    def refresh_sources(self):
        self.source_combo.blockSignals(True)
        self.source_combo.clear()

        self.source_items = scan_source_art()

        if not self.source_items:
            self.source_combo.addItem("No supported source art found", None)
            self.source_combo.blockSignals(False)
            self.source_details.setPlainText(self.empty_source_message())
            self.set_status("No source art found. Add PNG/JPG/WEBP files to a known source folder.")
            return

        for item in self.source_items:
            self.source_combo.addItem(item.label, item)

        self.source_combo.blockSignals(False)
        self.source_combo.setCurrentIndex(0)
        self.update_source_details()
        self.set_status(f"Found {len(self.source_items)} supported source file(s).")

    def update_source_details(self):
        item = self.source_combo.currentData()

        if not isinstance(item, SourceArtItem):
            self.source_details.setPlainText(self.empty_source_message())
            return

        self.source_details.setPlainText(
            "Selected source art\n"
            "-------------------\n"
            f"Label: {item.label}\n"
            f"Path: {item.path}\n"
            f"Folder: {item.folder_name}\n"
            f"Type: {item.suffix}\n"
            f"Size: {format_size(item.size_bytes)}\n\n"
            "Current state:\n"
            "- Source selection works.\n"
            "- Workflow definitions are visible.\n"
            "- AI execution comes next after safe worker restoration."
        )

    def update_workflow_details(self, workflow_name: str):
        workflow = WORKFLOWS.get(workflow_name)

        if not workflow:
            self.workflow_details.setPlainText("No workflow definition found.")
            return

        self.workflow_details.setPlainText(
            f"{workflow['title']}\n"
            f"{'-' * len(workflow['title'])}\n\n"
            f"Purpose:\n{workflow['purpose']}\n\n"
            f"End-user workflow value:\n{workflow['end_user']}\n\n"
            f"Output/value forms:\n{workflow['outputs']}\n\n"
            f"Next technical contract:\n{workflow['next_contract']}\n"
        )

    def empty_source_message(self) -> str:
        folders = "\n".join(f"- {path}" for path in known_source_dirs())
        return (
            "No supported source art found.\n\n"
            "Add one or more files with these extensions:\n"
            ".png, .jpg, .jpeg, .webp, .bmp, .tif, .tiff\n\n"
            "Known source folders:\n"
            f"{folders}"
        )

    def open_source_root(self):
        root = Path(__file__).resolve().parents[2] / "workspace"

        try:
            subprocess.Popen(["xdg-open", str(root)])
            self.set_status(f"Opened workspace folder: {root}")
        except Exception as exc:
            self.set_status(f"Could not open workspace folder: {exc}")

    def set_status(self, message: str):
        self.status_label.setText(message)
        self.status_changed.emit(message)
