#!/usr/bin/env python3
"""Canonical project skeleton and manifest foundation for MXZTAR Forge v2.0."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path

from core.paths import PROJECTS_DIR


PROJECT_SCHEMA = "mxztar_forge_project"
PROJECT_SCHEMA_VERSION = "1.0.0"
APPLICATION_VERSION = "2.0-development"
MAX_PROJECT_DISPLAY_NAME_CHARS = 80
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
    normalized = unicodedata.normalize("NFC", name.strip()).casefold()
    parts = []
    separator_pending = False
    for character in normalized:
        if character.isalnum():
            if separator_pending and parts:
                parts.append("-")
            parts.append(character)
            separator_pending = False
        else:
            separator_pending = True
    value = "".join(parts)
    if not value:
        raise ProjectManifestError("Project name must contain at least one letter or number.")
    return value[:MAX_PROJECT_DISPLAY_NAME_CHARS]


def project_name_from_purpose(purpose: str) -> str:
    """Derive a bounded display name without changing the stored project purpose."""
    if not isinstance(purpose, str):
        raise ProjectManifestError("Project purpose must be text.")
    exact_purpose = purpose.strip()
    if not exact_purpose:
        raise ProjectManifestError("Project purpose is required.")

    display_name = " ".join(exact_purpose.split())
    project_slug(display_name)
    if len(display_name) <= MAX_PROJECT_DISPLAY_NAME_CHARS:
        return display_name

    shortened = display_name[: MAX_PROJECT_DISPLAY_NAME_CHARS - 1].rstrip(" .,:;_-—")
    if not shortened:
        raise ProjectManifestError("Project purpose must contain at least one letter or number.")
    return shortened + "…"


def new_project_id() -> str:
    return f"project_{uuid.uuid4().hex}"


def fsync_directory(path: Path) -> None:
    """Persist directory entries on the Ubuntu/POSIX target."""
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def atomic_write_text(path: Path, text: str) -> None:
    """Write and fsync a new text value before atomically replacing its target."""
    temporary = path.with_name(f"{path.name}.tmp")
    try:
        with temporary.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        fsync_directory(path.parent)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            if temporary.exists():
                raise


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
        if any(not isinstance(item, str) or not item for item in manifest[key]):
            raise ProjectManifestError(f"Project manifest list contains invalid ID: {key}")
        if len(set(manifest[key])) != len(manifest[key]):
            raise ProjectManifestError(f"Project manifest list contains duplicate ID: {key}")
    if not isinstance(manifest.get("primary_goal"), str):
        raise ProjectManifestError("Project manifest requires string: primary_goal")
    recommendation = manifest.get("last_recommendation_artifact_id", object())
    if recommendation is not None and (
        not isinstance(recommendation, str) or not recommendation
    ):
        raise ProjectManifestError(
            "Project manifest last_recommendation_artifact_id must be null or a non-empty string."
        )
    if manifest["history_path"] != "history/project_history.jsonl":
        raise ProjectManifestError(
            "Project manifest history_path must remain inside the canonical history directory."
        )
    integrity = manifest.get("integrity")
    if not isinstance(integrity, dict):
        raise ProjectManifestError("Project manifest requires integrity object.")
    if "manifest_sha256" not in integrity or "last_validated_at_utc" not in integrity:
        raise ProjectManifestError("Project manifest integrity fields are incomplete.")
    manifest_hash = integrity["manifest_sha256"]
    if manifest_hash is not None and (
        not isinstance(manifest_hash, str)
        or len(manifest_hash) != 64
        or any(character not in "0123456789abcdef" for character in manifest_hash)
    ):
        raise ProjectManifestError("Project manifest integrity hash is invalid.")
    validated_at = integrity["last_validated_at_utc"]
    if validated_at is not None and (not isinstance(validated_at, str) or not validated_at):
        raise ProjectManifestError("Project manifest validation time is invalid.")
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
    fsync_directory(root.parent)
    staging = Path(tempfile.mkdtemp(prefix=f".{slug}.creating-", dir=root))
    fsync_directory(root)
    try:
        for relative in PROJECT_DIRS:
            (staging / relative).mkdir(parents=True, exist_ok=False)

        history_event = {
            "timestamp_utc": now,
            "event": "project_created",
            "project_id": manifest["project_id"],
            "project_name": manifest["project_name"],
            "purpose": manifest["primary_goal"],
        }
        atomic_write_text(
            staging / manifest["history_path"],
            json.dumps(history_event, ensure_ascii=False) + "\n",
        )
        purpose_line = (
            f"\nPurpose: {manifest['primary_goal']}\n" if manifest["primary_goal"] else ""
        )
        atomic_write_text(
            staging / "README.md",
            f"# {manifest['project_name']}\n\nMXZTAR Forge project: {manifest['project_id']}\n"
            f"{purpose_line}",
        )
        atomic_write_text(
            staging / "project.json",
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        )
        if project_dir.exists():
            raise FileExistsError(f"Project already exists: {project_dir}")
        for directory in sorted(
            (path for path in staging.rglob("*") if path.is_dir()),
            key=lambda path: len(path.parts),
            reverse=True,
        ):
            fsync_directory(directory)
        fsync_directory(staging)
        staging.rename(project_dir)
        fsync_directory(root)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
            fsync_directory(root)
    return project_dir, manifest


def load_project_manifest(project_dir: Path) -> dict:
    path = Path(project_dir).expanduser().resolve() / "project.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ProjectManifestError(f"Could not read project manifest {path}: {exc}") from exc
    return validate_manifest(payload)
