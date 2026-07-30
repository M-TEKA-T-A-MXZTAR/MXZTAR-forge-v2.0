#!/usr/bin/env python3
"""Transactional project display-name changes without directory or identity changes."""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path

from core.project_manifest import (
    APPLICATION_VERSION,
    MAX_PROJECT_DISPLAY_NAME_CHARS,
    atomic_write_text,
    fsync_directory,
    project_slug,
    utc_now_iso,
    validate_manifest,
)
from core.project_session import ProjectSession

MAX_PROJECT_HISTORY_BYTES = 8 * 1024 * 1024
TRANSACTION_MARKER = ".mxztar-project-rename-transaction.json"


class ProjectRenameError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProjectRenameResult:
    project_id: str
    project_dir: Path
    previous_name: str
    project_name: str


def normalize_project_display_name(value: str) -> str:
    if not isinstance(value, str):
        raise ProjectRenameError("Project name must be text.")
    name = " ".join(value.split())
    if not name:
        raise ProjectRenameError("Project name is required.")
    if len(name) > MAX_PROJECT_DISPLAY_NAME_CHARS:
        raise ProjectRenameError(
            f"Project name must be {MAX_PROJECT_DISPLAY_NAME_CHARS} characters or fewer."
        )
    try:
        project_slug(name)
    except ValueError as exc:
        raise ProjectRenameError(str(exc)) from exc
    return name


def _renamed_readme(readme_before: str, project_name: str) -> str:
    lines = readme_before.splitlines(keepends=True)
    heading = f"# {project_name}\n"
    if not lines:
        return heading
    if lines[0].startswith("# "):
        lines[0] = heading
        return "".join(lines)
    return heading + "\n" + readme_before


def rename_project(session: ProjectSession, new_name: str) -> ProjectRenameResult:
    """Change only the project display name inside one guarded rollback boundary."""
    name = normalize_project_display_name(new_name)
    state = session.state
    if state is None or not state.writable or session.project_dir is None:
        raise ProjectRenameError("Writable project authority is required to rename a project.")

    project_dir = session.project_dir
    project_id = state.assessment.manifest["project_id"]

    with session.mutation_guard():
        current = session.state
        if (
            current is None
            or not current.writable
            or session.project_dir != project_dir
            or current.assessment.manifest["project_id"] != project_id
        ):
            raise ProjectRenameError("Project authority changed before the rename.")

        manifest_path = project_dir / "project.json"
        history_path = project_dir / current.assessment.manifest["history_path"]
        readme_path = project_dir / "README.md"
        marker_path = project_dir / TRANSACTION_MARKER
        if marker_path.exists() or marker_path.is_symlink():
            raise ProjectRenameError(
                "An earlier project rename transaction requires explicit recovery."
            )
        if history_path.stat().st_size > MAX_PROJECT_HISTORY_BYTES:
            raise ProjectRenameError("Project history exceeds the safe rename transaction limit.")

        manifest_before = manifest_path.read_text(encoding="utf-8")
        history_before = history_path.read_text(encoding="utf-8")
        readme_existed = readme_path.is_file()
        readme_before = readme_path.read_text(encoding="utf-8") if readme_existed else ""

        manifest = copy.deepcopy(current.assessment.manifest)
        previous_name = manifest["project_name"]
        if name == previous_name:
            return ProjectRenameResult(project_id, project_dir, previous_name, name)

        now = utc_now_iso()
        manifest["project_name"] = name
        manifest["updated_at_utc"] = now
        manifest["application_version_last_opened"] = APPLICATION_VERSION
        manifest = validate_manifest(manifest)
        event = {
            "timestamp_utc": now,
            "event": "project_renamed",
            "project_id": project_id,
            "previous_project_name": previous_name,
            "project_name": name,
            "project_directory": project_dir.name,
        }
        readme_after = _renamed_readme(readme_before, name)

        marker_created = False
        history_write_attempted = False
        readme_write_attempted = False
        manifest_write_attempted = False
        try:
            atomic_write_text(
                marker_path,
                json.dumps(
                    {
                        "schema_name": "mxztar_forge_project_rename_transaction",
                        "schema_version": "1.0.0",
                        "operation": "rename_project_display_name",
                        "project_id": project_id,
                        "project_directory": project_dir.name,
                        "manifest_before": manifest_before,
                        "history_before": history_before,
                        "readme_before": readme_before,
                    },
                    ensure_ascii=False,
                )
                + "\n",
            )
            marker_created = True

            history_write_attempted = True
            atomic_write_text(
                history_path,
                history_before + json.dumps(event, ensure_ascii=False) + "\n",
            )
            readme_write_attempted = True
            atomic_write_text(readme_path, readme_after)
            manifest_write_attempted = True
            atomic_write_text(
                manifest_path,
                json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            )
            marker_path.unlink()
            fsync_directory(project_dir)
            marker_created = False
            session.update_manifest_snapshot(manifest)
            return ProjectRenameResult(project_id, project_dir, previous_name, name)
        except Exception as original_error:
            rollback_ok = True
            try:
                if manifest_write_attempted:
                    atomic_write_text(manifest_path, manifest_before)
                if readme_write_attempted:
                    if readme_existed:
                        atomic_write_text(readme_path, readme_before)
                    else:
                        readme_path.unlink(missing_ok=True)
                        fsync_directory(project_dir)
                if history_write_attempted:
                    atomic_write_text(history_path, history_before)
            except Exception:
                rollback_ok = False
            if marker_created and rollback_ok:
                try:
                    marker_path.unlink(missing_ok=True)
                    fsync_directory(project_dir)
                except OSError:
                    rollback_ok = False
            if not rollback_ok:
                session.revoke_writable_authority(
                    "Project rename rollback failed; explicit recovery is required."
                )
                raise ProjectRenameError(
                    "Project rename failed and rollback could not be confirmed."
                ) from original_error
            raise ProjectRenameError(f"Could not rename project: {original_error}") from original_error
