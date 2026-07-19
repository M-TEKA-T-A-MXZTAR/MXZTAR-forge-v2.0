#!/usr/bin/env python3
"""Transactional, copy-only source intake for an active Forge project."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from core.project_access import SOURCE_TRANSACTION_FILENAME
from core.project_manifest import (
    APPLICATION_VERSION,
    atomic_write_text,
    fsync_directory,
    utc_now_iso,
    validate_manifest,
)
from core.project_session import ProjectSession, ProjectSessionError
from core.source_library import SourceArtItem


MAX_SOURCE_BYTES = 1024 * 1024 * 1024
MAX_PREVIEW_PIXELS = 100_000_000
MAX_HISTORY_BYTES = 16 * 1024 * 1024
MAX_SOURCE_RECORD_BYTES = 1024 * 1024
PREVIEW_MAX_SIZE = (1600, 1600)
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}
FORMAT_BY_EXTENSION = {
    ".png": "PNG",
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".webp": "WEBP",
    ".tif": "TIFF",
    ".tiff": "TIFF",
}
MIME_BY_FORMAT = {
    "PNG": "image/png",
    "JPEG": "image/jpeg",
    "WEBP": "image/webp",
    "TIFF": "image/tiff",
}
SOURCE_RECORD_SCHEMA = "mxztar_forge_source_asset"
SOURCE_RECORD_VERSION = "1.0.0"


class SourceIntakeError(RuntimeError):
    pass


class SourceDiscoveryInterrupted(SourceIntakeError):
    pass


@dataclass(frozen=True)
class SourceIntakeResult:
    record: dict
    duplicate: bool


def scan_project_source_art(
    session: ProjectSession, interrupted: Callable[[], bool] | None = None
) -> list[SourceArtItem]:
    """Read the active project's declared source records without mutating authority."""
    if session.state is None or session.project_dir is None:
        return []
    project_dir = session.project_dir
    manifest = session.state.assessment.manifest
    items: list[SourceArtItem] = []
    seen_ids: set[str] = set()
    for asset_id in manifest["source_asset_ids"]:
        if interrupted is not None and interrupted():
            break
        if not isinstance(asset_id, str) or asset_id in seen_ids:
            raise SourceIntakeError("Project manifest contains an invalid source asset ID.")
        seen_ids.add(asset_id)
        record_path = project_dir / "source" / "originals" / f"{asset_id}.source.json"
        try:
            record = json.loads(
                _read_bounded_regular_text(record_path, MAX_SOURCE_RECORD_BYTES)
            )
        except (OSError, UnicodeError, ValueError, RecursionError) as exc:
            raise SourceIntakeError(f"Could not read source record {asset_id}: {exc}") from exc
        record = _validate_source_record(
            record,
            asset_id,
            record.get("sha256") if isinstance(record, dict) else None,
            manifest["project_id"],
        )
        source_path = _project_artifact_path(project_dir, record["project_relative_path"])
        preview_path = _project_artifact_path(project_dir, record["preview_relative_path"])
        if not source_path.is_file() or not preview_path.is_file():
            raise SourceIntakeError(f"Declared project source artifacts are missing: {asset_id}")
        if _hash_regular_file(source_path, interrupted) != record["sha256"]:
            raise SourceIntakeError(
                f"Project source bytes no longer match their recorded identity: {asset_id}"
            )
        lifecycle = record["lifecycle_status"]
        items.append(
            SourceArtItem(
                label=f"project {project_dir.name} / {record['original_filename']}",
                path=source_path,
                folder_name=f"project source/{lifecycle}",
                suffix=source_path.suffix.casefold(),
                size_bytes=int(record["size_bytes"]),
                preview_path=preview_path,
                asset_id=asset_id,
                project_id=manifest["project_id"],
                authority="active_project",
            )
        )
    return items


def _read_bounded_regular_text(path: Path, max_bytes: int) -> str:
    """Read a small regular UTF-8 file without following links or trusting a stale stat."""
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise SourceIntakeError("Source record must be a regular file.")
        if metadata.st_size > max_bytes:
            raise SourceIntakeError("Source record exceeds the safe read limit.")
        with os.fdopen(descriptor, "rb") as handle:
            descriptor = -1
            payload = handle.read(max_bytes + 1)
        if len(payload) > max_bytes:
            raise SourceIntakeError("Source record grew beyond the safe read limit.")
        return payload.decode("utf-8")
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _validate_source_record(
    record: object, asset_id: str, sha256: str, project_id: str
) -> dict:
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
    if record.get("project_id") != project_id:
        raise SourceIntakeError("Source record belongs to a different project.")
    lifecycle = record.get("lifecycle_status")
    if lifecycle not in ("ready", "processed"):
        raise SourceIntakeError("Source record lifecycle status is invalid.")
    source_relative = Path(str(record.get("project_relative_path", "")))
    expected_parent = Path("source/originals" if lifecycle == "ready" else "source/processed")
    if (
        source_relative.parent != expected_parent
        or not source_relative.name.startswith(f"{asset_id}-")
        or source_relative.suffix.casefold() not in SUPPORTED_EXTENSIONS
    ):
        raise SourceIntakeError("Source record does not reference its canonical asset path.")
    if record.get("preview_relative_path") != f"source/previews/{asset_id}.png":
        raise SourceIntakeError("Source record does not reference its canonical preview path.")
    return record


def _transaction_path(project_dir: Path) -> Path:
    return project_dir / SOURCE_TRANSACTION_FILENAME


def _write_transaction_marker(project_dir: Path, payload: dict) -> Path:
    path = _transaction_path(project_dir)
    if path.exists() or path.is_symlink():
        raise SourceIntakeError("An earlier source transaction requires read-only recovery.")
    atomic_write_text(path, json.dumps(payload, ensure_ascii=False) + "\n")
    return path


def _clear_transaction_marker(project_dir: Path, missing_ok: bool = False) -> None:
    try:
        _transaction_path(project_dir).unlink()
    except FileNotFoundError:
        if not missing_ok:
            raise
        return
    fsync_directory(project_dir)


def _hash_regular_file(
    path: Path, interrupted: Callable[[], bool] | None = None
) -> str:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise SourceIntakeError(f"Could not inspect stored source copy: {exc}") from exc
    if not stat.S_ISREG(metadata.st_mode):
        raise SourceIntakeError("Stored source copy must be a regular non-symlink file.")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            if interrupted is not None and interrupted():
                raise SourceDiscoveryInterrupted("Project source discovery was interrupted.")
            digest.update(chunk)
    return digest.hexdigest()


def _project_artifact_path(project_dir: Path, relative: str) -> Path:
    path = project_dir / relative
    parent = project_dir / Path(relative).parent
    if (
        parent.is_symlink()
        or path.is_symlink()
        or parent.resolve().parent not in (project_dir, project_dir / "source")
        or path.resolve().parent != parent.resolve()
    ):
        raise SourceIntakeError("Source artifact path escapes its canonical project directory.")
    return path


def _safe_name(value: str) -> str:
    stem = re.sub(r"[^\w.-]+", "-", value, flags=re.UNICODE).strip("-._")
    return (stem or "source")[:80]


def _copy_and_hash(source_path: Path, temporary_path: Path) -> tuple[str, int]:
    try:
        unresolved_metadata = source_path.lstat()
    except OSError as exc:
        raise SourceIntakeError(f"Could not inspect source art: {exc}") from exc
    if not stat.S_ISREG(unresolved_metadata.st_mode):
        raise SourceIntakeError("Source art must be a regular file.")
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
        source = os.fdopen(descriptor, "rb")
        descriptor = -1
        with source, temporary_path.open("xb") as target:
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


def _make_preview(copied_path: Path, preview_path: Path, extension: str) -> tuple[int, int, str]:
    try:
        with Image.open(copied_path) as image:
            decoded_format = image.format
            if decoded_format != FORMAT_BY_EXTENSION[extension]:
                raise SourceIntakeError(
                    f"Source bytes decode as {decoded_format or 'unknown'}, not {extension}."
                )
            width, height = image.size
            if width <= 0 or height <= 0 or width * height > MAX_PREVIEW_PIXELS:
                raise SourceIntakeError("Source dimensions exceed the safe preview limit.")
            image.thumbnail(PREVIEW_MAX_SIZE)
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGB")
            image.save(preview_path, format="PNG", optimize=True)
        with preview_path.open("rb") as preview:
            os.fsync(preview.fileno())
        fsync_directory(preview_path.parent)
    except (OSError, ValueError, UnidentifiedImageError, Image.DecompressionBombError) as exc:
        raise SourceIntakeError(f"Could not create a safe project preview: {exc}") from exc
    return width, height, decoded_format


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
    history_path = project_dir / session.state.assessment.manifest["history_path"]
    manifest_path = project_dir / "project.json"
    if history_path.stat().st_size > MAX_HISTORY_BYTES:
        raise SourceIntakeError("Project history exceeds the safe intake transaction limit.")
    history_before = history_path.read_text(encoding="utf-8")
    manifest_before = manifest_path.read_text(encoding="utf-8")
    history_write_attempted = False
    manifest_write_attempted = False
    marker_created = False
    if _transaction_path(project_dir).exists() or _transaction_path(project_dir).is_symlink():
        raise SourceIntakeError("An earlier source transaction requires read-only recovery.")
    try:
        marker_created = True
        _write_transaction_marker(
            project_dir,
            {
                "schema_name": "mxztar_forge_source_transaction",
                "schema_version": "1.0.0",
                "operation": "import_source_copy",
                "temporary_path": temporary_copy.relative_to(project_dir).as_posix(),
                "manifest_before": manifest_before,
                "history_before": history_before,
            },
        )
        sha256, size_bytes = _copy_and_hash(unresolved, temporary_copy)
        asset_id = f"source_{sha256[:24]}"
        record_path = originals_dir / f"{asset_id}.source.json"
        if asset_id in session.state.assessment.manifest["source_asset_ids"]:
            temporary_copy.unlink()
            try:
                record = json.loads(record_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, ValueError, RecursionError) as exc:
                raise SourceIntakeError(f"Duplicate source record is unavailable: {exc}") from exc
            record = _validate_source_record(
                record,
                asset_id,
                sha256,
                session.state.assessment.manifest["project_id"],
            )
            for key in ("project_relative_path", "preview_relative_path"):
                artifact_path = _project_artifact_path(project_dir, record[key])
                if not artifact_path.is_file():
                    raise SourceIntakeError(f"Duplicate source artifact is missing: {record[key]}")
            if _hash_regular_file(
                _project_artifact_path(project_dir, record["project_relative_path"])
            ) != sha256:
                raise SourceIntakeError("Stored source copy no longer matches its recorded SHA-256.")
            _clear_transaction_marker(project_dir)
            marker_created = False
            return SourceIntakeResult(record=record, duplicate=True)

        copied_name = f"{asset_id}-{_safe_name(unresolved.stem)}{extension}"
        copied_path = originals_dir / copied_name
        preview_path = previews_dir / f"{asset_id}.png"
        if copied_path.exists() or record_path.exists() or preview_path.exists():
            raise SourceIntakeError("Source asset paths already exist outside the manifest authority.")
        temporary_copy.rename(copied_path)
        created_paths.append(copied_path)
        fsync_directory(originals_dir)
        created_paths.append(preview_path)
        width, height, decoded_format = _make_preview(copied_path, preview_path, extension)

        now = utc_now_iso()
        record = {
            "schema_name": SOURCE_RECORD_SCHEMA,
            "schema_version": SOURCE_RECORD_VERSION,
            "asset_id": asset_id,
            "project_id": session.state.assessment.manifest["project_id"],
            "project_relative_path": copied_path.relative_to(project_dir).as_posix(),
            "preview_relative_path": preview_path.relative_to(project_dir).as_posix(),
            "original_filename": unresolved.name,
            "mime_type": MIME_BY_FORMAT[decoded_format],
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
        event = {
            "timestamp_utc": now,
            "event": "source_imported",
            "project_id": manifest["project_id"],
            "asset_id": asset_id,
            "project_relative_path": record["project_relative_path"],
            "sha256": sha256,
        }
        history_write_attempted = True
        atomic_write_text(history_path, history_before + json.dumps(event, ensure_ascii=False) + "\n")
        manifest_write_attempted = True
        atomic_write_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        _clear_transaction_marker(project_dir)
        marker_created = False
        session.update_manifest_snapshot(manifest)
        return SourceIntakeResult(record=record, duplicate=False)
    except Exception as original_error:
        rollback_ok = True
        try:
            if manifest_write_attempted and manifest_before is not None:
                atomic_write_text(project_dir / "project.json", manifest_before)
            if history_write_attempted and history_before is not None:
                atomic_write_text(project_dir / session.state.assessment.manifest["history_path"], history_before)
        except Exception:
            rollback_ok = False
        if rollback_ok:
            for path in reversed(created_paths):
                try:
                    path.unlink()
                    fsync_directory(path.parent)
                except FileNotFoundError:
                    # A failed stage may not have created every registered path.
                    pass
            if marker_created:
                try:
                    _clear_transaction_marker(project_dir, missing_ok=True)
                except OSError:
                    rollback_ok = False
        try:
            temporary_copy.unlink()
        except FileNotFoundError:
            # Successful rename or earlier cleanup means no temporary copy remains.
            pass
        if not rollback_ok:
            session.revoke_writable_authority(
                "Source intake rollback failed; explicit recovery is required."
            )
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
    if record_path.is_symlink() or not record_path.is_file():
        raise SourceIntakeError("Canonical source record is unavailable or unsafe.")
    record_before = record_path.read_text(encoding="utf-8")
    try:
        record = json.loads(record_before)
    except (ValueError, RecursionError) as exc:
        raise SourceIntakeError(f"Could not validate source record: {exc}") from exc
    record = _validate_source_record(
        record,
        asset_id,
        record.get("sha256"),
        session.state.assessment.manifest["project_id"],
    )
    if record.get("lifecycle_status") != "ready":
        raise SourceIntakeError("Only a ready source can transition to processed.")
    source_path = project_dir / record["project_relative_path"]
    originals_dir = project_dir / "source" / "originals"
    if (
        originals_dir.is_symlink()
        or source_path.parent != originals_dir
        or not source_path.is_file()
        or source_path.is_symlink()
        or source_path.resolve().parent != originals_dir.resolve()
    ):
        raise SourceIntakeError("Declared source copy is unavailable or unsafe.")
    processed_dir = project_dir / "source" / "processed"
    if processed_dir.is_symlink():
        raise SourceIntakeError("Processed-source directory must not be a symbolic link.")
    if processed_dir.exists() and not processed_dir.is_dir():
        raise SourceIntakeError("Processed-source path must be a directory.")
    processed_dir.mkdir(exist_ok=True)
    if processed_dir.resolve().parent != (project_dir / "source").resolve():
        raise SourceIntakeError("Processed-source directory escapes the project boundary.")
    fsync_directory(processed_dir.parent)
    target_path = processed_dir / source_path.name
    if target_path.exists():
        raise SourceIntakeError("Processed-source target already exists.")

    history_path = project_dir / session.state.assessment.manifest["history_path"]
    if history_path.stat().st_size > MAX_HISTORY_BYTES:
        raise SourceIntakeError("Project history exceeds the safe transaction limit.")
    history_before = history_path.read_text(encoding="utf-8")
    if _transaction_path(project_dir).exists() or _transaction_path(project_dir).is_symlink():
        raise SourceIntakeError("An earlier source transaction requires read-only recovery.")
    moved = record_write_attempted = history_write_attempted = False
    marker_created = False
    try:
        marker_created = True
        _write_transaction_marker(
            project_dir,
            {
                "schema_name": "mxztar_forge_source_transaction",
                "schema_version": "1.0.0",
                "operation": "mark_source_processed",
                "asset_id": asset_id,
                "record_before": record_before,
                "history_before": history_before,
                "source_path": source_path.relative_to(project_dir).as_posix(),
                "target_path": target_path.relative_to(project_dir).as_posix(),
            },
        )
        source_path.rename(target_path)
        moved = True
        fsync_directory(source_path.parent)
        fsync_directory(target_path.parent)
        now = utc_now_iso()
        record["project_relative_path"] = target_path.relative_to(project_dir).as_posix()
        record["lifecycle_status"] = "processed"
        record["processed_at_utc"] = now
        record_write_attempted = True
        atomic_write_text(record_path, json.dumps(record, indent=2, ensure_ascii=False) + "\n")
        event = {
            "timestamp_utc": now,
            "event": "source_marked_processed",
            "project_id": record["project_id"],
            "asset_id": asset_id,
            "project_relative_path": record["project_relative_path"],
        }
        history_write_attempted = True
        atomic_write_text(history_path, history_before + json.dumps(event, ensure_ascii=False) + "\n")
        _clear_transaction_marker(project_dir)
        return record
    except Exception as original_error:
        rollback_ok = True
        try:
            if history_write_attempted:
                atomic_write_text(history_path, history_before)
            if record_write_attempted:
                atomic_write_text(record_path, record_before)
            if moved and target_path.exists():
                target_path.rename(source_path)
                fsync_directory(source_path.parent)
                fsync_directory(target_path.parent)
            if marker_created:
                _clear_transaction_marker(project_dir, missing_ok=True)
        except Exception:
            rollback_ok = False
        if not rollback_ok:
            session.revoke_writable_authority(
                "Processed-source rollback failed; explicit recovery is required."
            )
            raise SourceIntakeError(
                "Processed-source transition failed and rollback could not be confirmed."
            ) from original_error
        raise
