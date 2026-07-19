#!/usr/bin/env python3
"""Transactional, copy-only source intake for an active Forge project."""

from __future__ import annotations

import hashlib
import json
import mimetypes
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from core.project_manifest import (
    APPLICATION_VERSION,
    atomic_write_text,
    fsync_directory,
    utc_now_iso,
    validate_manifest,
)
from core.project_session import ProjectSession, ProjectSessionError


MAX_SOURCE_BYTES = 1024 * 1024 * 1024
MAX_PREVIEW_PIXELS = 100_000_000
MAX_HISTORY_BYTES = 16 * 1024 * 1024
PREVIEW_MAX_SIZE = (1600, 1600)
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}
SOURCE_RECORD_SCHEMA = "mxztar_forge_source_asset"
SOURCE_RECORD_VERSION = "1.0.0"


class SourceIntakeError(RuntimeError):
    pass


@dataclass(frozen=True)
class SourceIntakeResult:
    record: dict
    duplicate: bool


def _validate_source_record(record: object, asset_id: str, sha256: str) -> dict:
    if not isinstance(record, dict):
        raise SourceIntakeError("Source record root must be a JSON object.")
    if (
        not isinstance(sha256, str)
        or len(sha256) != 64
        or any(character not in "0123456789abcdef" for character in sha256)
        or asset_id != f"source_{sha256[:24]}"
    ):
        raise SourceIntakeError("Source record hash identity is invalid.")
    expected = {
        "schema_name": SOURCE_RECORD_SCHEMA,
        "schema_version": SOURCE_RECORD_VERSION,
        "asset_id": asset_id,
        "sha256": sha256,
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise SourceIntakeError(f"Source record identity mismatch: {key}")
    for key in ("project_relative_path", "preview_relative_path"):
        relative = record.get(key)
        if not isinstance(relative, str) or Path(relative).is_absolute() or ".." in Path(relative).parts:
            raise SourceIntakeError(f"Source record contains an unsafe path: {key}")
    return record


def _safe_name(value: str) -> str:
    stem = re.sub(r"[^\w.-]+", "-", value, flags=re.UNICODE).strip("-._")
    return (stem or "source")[:80]


def _copy_and_hash(source_path: Path, temporary_path: Path) -> tuple[str, int]:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(source_path, flags)
    except OSError as exc:
        raise SourceIntakeError(f"Could not open source art: {exc}") from exc
    digest = hashlib.sha256()
    total = 0
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise SourceIntakeError("Source art must be a regular file.")
        if metadata.st_size > MAX_SOURCE_BYTES:
            raise SourceIntakeError("Source art exceeds the 1 GiB intake limit.")
        with os.fdopen(descriptor, "rb") as source, temporary_path.open("xb") as target:
            descriptor = -1
            while chunk := source.read(1024 * 1024):
                total += len(chunk)
                if total > MAX_SOURCE_BYTES:
                    raise SourceIntakeError("Source art grew beyond the 1 GiB intake limit.")
                digest.update(chunk)
                target.write(chunk)
            target.flush()
            os.fsync(target.fileno())
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    return digest.hexdigest(), total


def _make_preview(copied_path: Path, preview_path: Path) -> tuple[int, int]:
    try:
        with Image.open(copied_path) as image:
            width, height = image.size
            if width <= 0 or height <= 0 or width * height > MAX_PREVIEW_PIXELS:
                raise SourceIntakeError("Source dimensions exceed the safe preview limit.")
            image.thumbnail(PREVIEW_MAX_SIZE)
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGB")
            image.save(preview_path, format="PNG", optimize=True)
    except (OSError, ValueError, UnidentifiedImageError, Image.DecompressionBombError) as exc:
        raise SourceIntakeError(f"Could not create a safe project preview: {exc}") from exc
        with preview_path.open("rb") as preview:
            os.fsync(preview.fileno())
        fsync_directory(preview_path.parent)
    return width, height


def import_source_copy(session: ProjectSession, source_path: Path) -> SourceIntakeResult:
    if not session.is_writable or session.state is None or session.project_dir is None:
        raise ProjectSessionError("A writable project session is required for source intake.")
    unresolved = Path(source_path).expanduser()
    if unresolved.is_symlink():
        raise SourceIntakeError("Source art must not be a symbolic link.")
    extension = unresolved.suffix.casefold()
    if extension not in SUPPORTED_EXTENSIONS:
        raise SourceIntakeError(f"Unsupported source-art extension: {extension or '(none)'}")

    project_dir = session.project_dir
    originals_dir = project_dir / "source" / "originals"
    previews_dir = project_dir / "source" / "previews"
    temporary_copy = originals_dir / ".source-intake.tmp"
    created_paths: list[Path] = []
    history_before: str | None = None
    manifest_before: str | None = None
    history_changed = False
    manifest_changed = False
    try:
        sha256, size_bytes = _copy_and_hash(unresolved, temporary_copy)
        asset_id = f"source_{sha256[:24]}"
        record_path = originals_dir / f"{asset_id}.source.json"
        if asset_id in session.state.assessment.manifest["source_asset_ids"]:
            temporary_copy.unlink()
            try:
                record = json.loads(record_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, ValueError, RecursionError) as exc:
                raise SourceIntakeError(f"Duplicate source record is unavailable: {exc}") from exc
            record = _validate_source_record(record, asset_id, sha256)
            for key in ("project_relative_path", "preview_relative_path"):
                if not (project_dir / record[key]).is_file():
                    raise SourceIntakeError(f"Duplicate source artifact is missing: {record[key]}")
            return SourceIntakeResult(record=record, duplicate=True)

        copied_name = f"{asset_id}-{_safe_name(unresolved.stem)}{extension}"
        copied_path = originals_dir / copied_name
        preview_path = previews_dir / f"{asset_id}.png"
        if copied_path.exists() or record_path.exists() or preview_path.exists():
            raise SourceIntakeError("Source asset paths already exist outside the manifest authority.")
        temporary_copy.rename(copied_path)
        fsync_directory(originals_dir)
        created_paths.append(copied_path)
        created_paths.append(preview_path)
        width, height = _make_preview(copied_path, preview_path)

        now = utc_now_iso()
        record = {
            "schema_name": SOURCE_RECORD_SCHEMA,
            "schema_version": SOURCE_RECORD_VERSION,
            "asset_id": asset_id,
            "project_id": session.state.assessment.manifest["project_id"],
            "project_relative_path": copied_path.relative_to(project_dir).as_posix(),
            "preview_relative_path": preview_path.relative_to(project_dir).as_posix(),
            "original_filename": unresolved.name,
            "mime_type": mimetypes.guess_type(unresolved.name)[0] or "application/octet-stream",
            "size_bytes": size_bytes,
            "width_px": width,
            "height_px": height,
            "sha256": sha256,
            "source_origin": "user_import_copy",
            "lifecycle_status": "ready",
            "imported_at_utc": now,
        }
        created_paths.append(record_path)
        atomic_write_text(record_path, json.dumps(record, indent=2, ensure_ascii=False) + "\n")

        manifest = json.loads(json.dumps(session.state.assessment.manifest))
        manifest["source_asset_ids"].append(asset_id)
        manifest["updated_at_utc"] = now
        manifest["application_version_last_opened"] = APPLICATION_VERSION
        validate_manifest(manifest)
        history_path = project_dir / manifest["history_path"]
        if history_path.stat().st_size > MAX_HISTORY_BYTES:
            raise SourceIntakeError("Project history exceeds the safe intake transaction limit.")
        history_before = history_path.read_text(encoding="utf-8")
        manifest_path = project_dir / "project.json"
        manifest_before = manifest_path.read_text(encoding="utf-8")
        event = {
            "timestamp_utc": now,
            "event": "source_imported",
            "project_id": manifest["project_id"],
            "asset_id": asset_id,
            "project_relative_path": record["project_relative_path"],
            "sha256": sha256,
        }
        atomic_write_text(history_path, history_before + json.dumps(event, ensure_ascii=False) + "\n")
        history_changed = True
        atomic_write_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        manifest_changed = True
        session.update_manifest_snapshot(manifest)
        return SourceIntakeResult(record=record, duplicate=False)
    except Exception as original_error:
        rollback_ok = True
        try:
            if manifest_changed and manifest_before is not None:
                atomic_write_text(project_dir / "project.json", manifest_before)
            if history_changed and history_before is not None:
                atomic_write_text(project_dir / session.state.assessment.manifest["history_path"], history_before)
        except Exception:
            rollback_ok = False
        if rollback_ok:
            for path in reversed(created_paths):
                try:
                    path.unlink()
                    fsync_directory(path.parent)
                except FileNotFoundError:
                    pass
        try:
            temporary_copy.unlink()
        except FileNotFoundError:
            pass
        if not rollback_ok:
            raise SourceIntakeError(
                "Source intake failed and authority rollback could not be confirmed; open read-only recovery."
            ) from original_error
        raise


def mark_source_processed(session: ProjectSession, asset_id: str) -> dict:
    """Move an imported project copy only after an explicit successful-workflow call."""
    if not session.is_writable or session.state is None or session.project_dir is None:
        raise ProjectSessionError("A writable project session is required.")
    if asset_id not in session.state.assessment.manifest["source_asset_ids"]:
        raise SourceIntakeError("Source asset is not declared by the active project manifest.")
    project_dir = session.project_dir
    record_path = project_dir / "source" / "originals" / f"{asset_id}.source.json"
    record_before = record_path.read_text(encoding="utf-8")
    try:
        record = json.loads(record_before)
    except (ValueError, RecursionError) as exc:
        raise SourceIntakeError(f"Could not validate source record: {exc}") from exc
    record = _validate_source_record(record, asset_id, record.get("sha256"))
    if record.get("lifecycle_status") != "ready":
        raise SourceIntakeError("Only a ready source can transition to processed.")
    source_path = project_dir / record["project_relative_path"]
    if not source_path.is_file() or source_path.is_symlink():
        raise SourceIntakeError("Declared source copy is unavailable or unsafe.")
    processed_dir = project_dir / "source" / "processed"
    processed_dir.mkdir(exist_ok=True)
    fsync_directory(processed_dir.parent)
    target_path = processed_dir / source_path.name
    if target_path.exists():
        raise SourceIntakeError("Processed-source target already exists.")

    history_path = project_dir / session.state.assessment.manifest["history_path"]
    if history_path.stat().st_size > MAX_HISTORY_BYTES:
        raise SourceIntakeError("Project history exceeds the safe transaction limit.")
    history_before = history_path.read_text(encoding="utf-8")
    moved = record_changed = history_changed = False
    try:
        source_path.rename(target_path)
        moved = True
        fsync_directory(source_path.parent)
        fsync_directory(target_path.parent)
        now = utc_now_iso()
        record["project_relative_path"] = target_path.relative_to(project_dir).as_posix()
        record["lifecycle_status"] = "processed"
        record["processed_at_utc"] = now
        atomic_write_text(record_path, json.dumps(record, indent=2, ensure_ascii=False) + "\n")
        record_changed = True
        event = {
            "timestamp_utc": now,
            "event": "source_marked_processed",
            "project_id": record["project_id"],
            "asset_id": asset_id,
            "project_relative_path": record["project_relative_path"],
        }
        atomic_write_text(history_path, history_before + json.dumps(event, ensure_ascii=False) + "\n")
        history_changed = True
        return record
    except Exception as original_error:
        rollback_ok = True
        try:
            if history_changed:
                atomic_write_text(history_path, history_before)
            if record_changed:
                atomic_write_text(record_path, record_before)
            if moved and target_path.exists():
                target_path.rename(source_path)
                fsync_directory(source_path.parent)
                fsync_directory(target_path.parent)
        except Exception:
            rollback_ok = False
        if not rollback_ok:
            raise SourceIntakeError(
                "Processed-source transition failed and rollback could not be confirmed."
            ) from original_error
        raise
