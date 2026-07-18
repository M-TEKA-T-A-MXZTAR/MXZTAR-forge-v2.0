#!/usr/bin/env python3
"""
MXZTAR Forge v2.0 agent runner.

Purpose:
Run one safe local vision workflow and save the result as a JSON record.

This module is UI-safe only when called from a worker thread.
Do not call long AI jobs directly from the Qt main thread.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple

from brain.service import DEFAULT_MODEL, AgentResult, run_vision_workflow
from core.paths import (
    CONCEPT_BRIEFS_DIR,
    RENDER_PROMPT_PACKS_DIR,
    SOURCE_ART_INTELLIGENCE_DIR,
    ensure_project_dirs,
)


WORKFLOW_OUTPUT_DIRS = {
    "source_art_intelligence": SOURCE_ART_INTELLIGENCE_DIR,
    "modular_set_perspective": SOURCE_ART_INTELLIGENCE_DIR,
    "prototype_imagination": SOURCE_ART_INTELLIGENCE_DIR,
    "shape_structure_harvest": SOURCE_ART_INTELLIGENCE_DIR,
    "concept_brief": CONCEPT_BRIEFS_DIR,
    "render_prompt_pack": RENDER_PROMPT_PACKS_DIR,
    "recommend_next_step": SOURCE_ART_INTELLIGENCE_DIR,
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def safe_slug(text: str) -> str:
    cleaned = []

    for char in text.lower():
        if char.isalnum():
            cleaned.append(char)
        elif char in {" ", "-", "_", "."}:
            cleaned.append("_")

    slug = "".join(cleaned).strip("_")

    while "__" in slug:
        slug = slug.replace("__", "_")

    return slug[:80] or "source"


def output_path_for(workflow_key: str, source_path: Path) -> Path:
    ensure_project_dirs()

    out_dir = WORKFLOW_OUTPUT_DIRS.get(
        workflow_key,
        SOURCE_ART_INTELLIGENCE_DIR,
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    source_slug = safe_slug(source_path.stem)
    return out_dir / f"{workflow_key}-{utc_stamp()}-{source_slug}.json"


def run_agent_job(
    source_path: Path,
    workflow_key: str,
    user_notes: str = "",
    model: str = DEFAULT_MODEL,
) -> Tuple[AgentResult, Path]:
    source_path = Path(source_path).expanduser().resolve()

    result = run_vision_workflow(
        source_path=source_path,
        workflow_key=workflow_key,
        user_notes=user_notes,
        model=model,
    )

    out_path = output_path_for(workflow_key, source_path)

    record = {
        "created_utc": utc_now_iso(),
        "model": model,
        "workflow_key": workflow_key,
        "source_path": str(source_path),
        "ok": result.ok,
        "error": result.error,
        "output_text": result.output_text,
    }

    out_path.write_text(
        json.dumps(record, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return result, out_path
