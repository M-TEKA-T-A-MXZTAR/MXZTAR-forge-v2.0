#!/usr/bin/env python3
"""Canonical project skeleton and manifest foundation for MXZTAR Forge v2.0."""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

from core.paths import PROJECTS_DIR


PROJECT_SCHEMA = "mxztar_forge_project"
PROJECT_SCHEMA_VERSION = "1.0.0"
APPLICATION_VERSION = "2.0-development"
PROJECT_DIRS = (
    "source/originals",
    "source/previews",
    "findings/raw",
    "findings/approved",
    "findings/rejected",
    "findings/superseded",
    "structures/raw",
    "structures/approved",
    "structures/superseded",
    "briefs/draft",
    "briefs/approved",
    "briefs/superseded",
    "prompts/draft",
    "prompts/approved",
    "prompts/superseded",
    "recommendations",
    "exports",
    "diagnostics",
    "logs",
    "history",
)


class ProjectManifestError(ValueError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def project_slug(name: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    if not value:
        raise ProjectManifestError("Project name must contain at least one letter or number.")
    return value[:80]


def new_project_id() -> str:
    return f"project_{uuid.uuid4().hex}"


def atomic_write_text(path: Path, text: str) -> None:
    """Write and fsync a new text value before atomically replacing its target."""
    temporary = path.with_name(f"{path.name}.tmp")
    try:
        with temporary.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def validate_manifest(manifest: object) -> dict:
    if not isinstance(manifest, dict):
        raise ProjectManifestError("Project manifest root must be a JSON object.")
    required_strings = (
        "schema_name",
        "schema_version",
        "project_id",
        "project_name",
        "created_at_utc",
        "updated_at_utc",
        "application_version_created",
        "application_version_last_opened",
        "project_status",
        "history_path",
    )
    for key in required_strings:
        if not isinstance(manifest.get(key), str) or not manifest[key]:
            raise ProjectManifestError(f"Project manifest requires non-empty string: {key}")
    if manifest["schema_name"] != PROJECT_SCHEMA:
        raise ProjectManifestError(f"Unsupported project schema: {manifest['schema_name']}")
    if manifest["schema_version"] != PROJECT_SCHEMA_VERSION:
        raise ProjectManifestError(f"Unsupported project schema version: {manifest['schema_version']}")
    for key in (
        "source_asset_ids",
        "current_artifact_ids",
        "approved_artifact_ids",
        "superseded_artifact_ids",
    ):
        if not isinstance(manifest.get(key), list):
            raise ProjectManifestError(f"Project manifest requires list: {key}")
    if not isinstance(manifest.get("integrity"), dict):
        raise ProjectManifestError("Project manifest requires integrity object.")
    return manifest


def create_project(
    project_name: str,
    primary_goal: str = "",
    projects_root: Path = PROJECTS_DIR,
    application_version: str = APPLICATION_VERSION,
) -> tuple[Path, dict]:
    """Create one self-contained project without overwriting existing state."""
    slug = project_slug(project_name)
    root = Path(projects_root).expanduser().resolve()
    project_dir = root / slug
    if project_dir.exists():
        raise FileExistsError(f"Project already exists: {project_dir}")

    now = utc_now_iso()
    manifest = validate_manifest(
        {
            "schema_name": PROJECT_SCHEMA,
            "schema_version": PROJECT_SCHEMA_VERSION,
            "project_id": new_project_id(),
            "project_name": project_name.strip(),
            "created_at_utc": now,
            "updated_at_utc": now,
            "application_version_created": application_version,
            "application_version_last_opened": application_version,
            "project_status": "active",
            "primary_goal": primary_goal.strip(),
            "source_asset_ids": [],
            "current_artifact_ids": [],
            "approved_artifact_ids": [],
            "superseded_artifact_ids": [],
            "last_recommendation_artifact_id": None,
            "history_path": "history/project_history.jsonl",
            "integrity": {
                "manifest_sha256": None,
                "last_validated_at_utc": None,
            },
        }
    )

    root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{slug}.creating-", dir=root))
    try:
        for relative in PROJECT_DIRS:
            (staging / relative).mkdir(parents=True, exist_ok=False)

        history_event = {
            "timestamp_utc": now,
            "event": "project_created",
            "project_id": manifest["project_id"],
            "project_name": manifest["project_name"],
        }
        atomic_write_text(
            staging / manifest["history_path"],
            json.dumps(history_event, ensure_ascii=False) + "\n",
        )
        atomic_write_text(
            staging / "README.md",
            f"# {manifest['project_name']}\n\nMXZTAR Forge project: {manifest['project_id']}\n",
        )
        atomic_write_text(
            staging / "project.json",
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        )
        if project_dir.exists():
            raise FileExistsError(f"Project already exists: {project_dir}")
        staging.rename(project_dir)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return project_dir, manifest


def load_project_manifest(project_dir: Path) -> dict:
    path = Path(project_dir).expanduser().resolve() / "project.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ProjectManifestError(f"Could not read project manifest {path}: {exc}") from exc
    return validate_manifest(payload)
