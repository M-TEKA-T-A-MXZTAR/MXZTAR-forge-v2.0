#!/usr/bin/env python3
"""Project-owned native shape documents with bounded durable command history."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import stat
import uuid
from dataclasses import dataclass
from pathlib import Path

from core.editor_project_access import EDITOR_TRANSACTION_FILENAME
from core.project_manifest import (
    APPLICATION_VERSION,
    atomic_write_text,
    fsync_directory,
    utc_now_iso,
    validate_manifest,
)
from core.project_session import ProjectSession, ProjectSessionError


SHAPE_DOCUMENT_SCHEMA = "mxztar_forge_shape_document"
SHAPE_DOCUMENT_VERSION = "1.0.0"
SHAPE_DOCUMENT_SUFFIX = ".shape.json"
SHAPE_DOCUMENT_DIR = Path("structures/shape-documents")
AUTOSAVE_DIR = SHAPE_DOCUMENT_DIR / ".autosave"
MAX_DOCUMENT_BYTES = 4 * 1024 * 1024
MAX_HISTORY_BYTES = 16 * 1024 * 1024
MAX_COMMANDS = 500
DEFAULT_CANVAS_WIDTH = 1024.0
DEFAULT_CANVAS_HEIGHT = 1024.0
SUPPORTED_UNITS = {"px", "mm", "cm", "in"}


class ShapeDocumentError(RuntimeError):
    pass


@dataclass(frozen=True)
class ShapeDocumentLoadResult:
    document: dict
    canonical_path: Path
    recovered_from_autosave: bool


def _content_digest(document: dict) -> str:
    payload = copy.deepcopy(document)
    payload["integrity"] = {"content_sha256": None}
    serialized = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def _with_integrity(document: dict) -> dict:
    value = copy.deepcopy(document)
    value["integrity"] = {"content_sha256": None}
    value["integrity"]["content_sha256"] = _content_digest(value)
    return value


def _serialize_bounded_document(document: dict) -> str:
    serialized = json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    if len(serialized.encode("utf-8")) > MAX_DOCUMENT_BYTES:
        raise ShapeDocumentError("Shape document exceeds the safe write limit.")
    return serialized


def _require_non_empty_string(payload: dict, key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ShapeDocumentError(f"Shape document requires non-empty string: {key}")
    return value


def _require_number(value, label: str, *, positive: bool = False) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ShapeDocumentError(f"{label} must be a number.")
    number = float(value)
    if not (-1.0e12 < number < 1.0e12):
        raise ShapeDocumentError(f"{label} is outside the supported numeric range.")
    if positive and number <= 0:
        raise ShapeDocumentError(f"{label} must be positive.")
    return number


def _validate_style(style: object) -> dict:
    if not isinstance(style, dict):
        raise ShapeDocumentError("Shape style must be an object.")
    fill = style.get("fill")
    stroke = style.get("stroke")
    stroke_width = _require_number(style.get("stroke_width"), "Stroke width")
    if not isinstance(fill, str) or not fill:
        raise ShapeDocumentError("Shape fill must be a non-empty string.")
    if not isinstance(stroke, str) or not stroke:
        raise ShapeDocumentError("Shape stroke must be a non-empty string.")
    if stroke_width < 0:
        raise ShapeDocumentError("Stroke width cannot be negative.")
    return {"fill": fill, "stroke": stroke, "stroke_width": stroke_width}


def _rectangle_from_command(command: dict) -> dict:
    payload = command["payload"]
    return {
        "object_id": _require_non_empty_string(payload, "object_id"),
        "type": "rectangle",
        "layer_id": _require_non_empty_string(payload, "layer_id"),
        "x": _require_number(payload.get("x"), "Rectangle x"),
        "y": _require_number(payload.get("y"), "Rectangle y"),
        "width": _require_number(payload.get("width"), "Rectangle width", positive=True),
        "height": _require_number(payload.get("height"), "Rectangle height", positive=True),
        "style": _validate_style(payload.get("style")),
        "origin": "user_created",
    }


def replay_commands(commands: object, history_cursor: int) -> list[dict]:
    if not isinstance(commands, list):
        raise ShapeDocumentError("Shape document commands must be a list.")
    if len(commands) > MAX_COMMANDS:
        raise ShapeDocumentError(f"Shape document exceeds the {MAX_COMMANDS}-command limit.")
    if not isinstance(history_cursor, int) or isinstance(history_cursor, bool):
        raise ShapeDocumentError("Shape document history cursor must be an integer.")
    if history_cursor < 0 or history_cursor > len(commands):
        raise ShapeDocumentError("Shape document history cursor is outside command history.")

    objects: list[dict] = []
    seen_command_ids: set[str] = set()
    seen_object_ids: set[str] = set()
    for index, command in enumerate(commands):
        if not isinstance(command, dict):
            raise ShapeDocumentError("Each editor command must be an object.")
        command_id = _require_non_empty_string(command, "command_id")
        if command_id in seen_command_ids:
            raise ShapeDocumentError("Shape document contains a duplicate command ID.")
        seen_command_ids.add(command_id)
        _require_non_empty_string(command, "created_at_utc")
        if command.get("type") != "add_rectangle":
            raise ShapeDocumentError(f"Unsupported editor command: {command.get('type')!r}")
        if not isinstance(command.get("payload"), dict):
            raise ShapeDocumentError("Editor command payload must be an object.")
        rectangle = _rectangle_from_command(command)
        if rectangle["object_id"] in seen_object_ids:
            raise ShapeDocumentError("Shape document contains a duplicate object ID.")
        seen_object_ids.add(rectangle["object_id"])
        if index < history_cursor:
            objects.append(rectangle)
    return objects


def validate_shape_document(document: object, project_id: str | None = None) -> dict:
    if not isinstance(document, dict):
        raise ShapeDocumentError("Shape document root must be a JSON object.")
    value = copy.deepcopy(document)
    if value.get("schema_name") != SHAPE_DOCUMENT_SCHEMA:
        raise ShapeDocumentError("Unsupported shape document schema.")
    if value.get("schema_version") != SHAPE_DOCUMENT_VERSION:
        raise ShapeDocumentError("Unsupported shape document schema version.")
    _require_non_empty_string(value, "application_version")
    document_id = _require_non_empty_string(value, "document_id")
    if not document_id.startswith("shape_"):
        raise ShapeDocumentError("Shape document ID must use the shape_ prefix.")
    actual_project_id = _require_non_empty_string(value, "project_id")
    if project_id is not None and actual_project_id != project_id:
        raise ShapeDocumentError("Shape document belongs to a different project.")
    for key in ("title", "created_at_utc", "updated_at_utc", "creator"):
        _require_non_empty_string(value, key)
    if value.get("creator") != "user":
        raise ShapeDocumentError("Native shape document creator must be user.")
    revision = value.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise ShapeDocumentError("Shape document revision must be a positive integer.")
    if value.get("approval_state") != "draft":
        raise ShapeDocumentError("This editor milestone supports draft shape documents only.")
    if value.get("lifecycle_status") != "editable":
        raise ShapeDocumentError("This editor milestone supports editable documents only.")
    supersedes = value.get("supersedes_document_id")
    if supersedes is not None and (not isinstance(supersedes, str) or not supersedes):
        raise ShapeDocumentError("Supersedes document ID must be null or a non-empty string.")

    coordinate = value.get("coordinate_space")
    if not isinstance(coordinate, dict):
        raise ShapeDocumentError("Shape document coordinate_space must be an object.")
    if coordinate.get("kind") != "cartesian_2d":
        raise ShapeDocumentError("Shape document coordinate kind is unsupported.")
    if coordinate.get("origin") != "top_left" or coordinate.get("y_axis") != "down":
        raise ShapeDocumentError("Shape document version 1 requires top-left, downward-y coordinates.")
    if coordinate.get("units") not in SUPPORTED_UNITS:
        raise ShapeDocumentError("Shape document units are unsupported.")
    canvas = coordinate.get("canvas")
    if not isinstance(canvas, dict):
        raise ShapeDocumentError("Shape document canvas must be an object.")
    _require_number(canvas.get("width"), "Canvas width", positive=True)
    _require_number(canvas.get("height"), "Canvas height", positive=True)

    for key in ("source_relationships", "groups", "anchors"):
        if not isinstance(value.get(key), list):
            raise ShapeDocumentError(f"Shape document {key} must be a list.")
    if value["groups"] or value["anchors"]:
        raise ShapeDocumentError("Groups and anchors are reserved for a later editor milestone.")
    for relationship in value["source_relationships"]:
        if not isinstance(relationship, dict):
            raise ShapeDocumentError("Source relationship must be an object.")
        _require_non_empty_string(relationship, "source_asset_id")
        digest = _require_non_empty_string(relationship, "source_sha256")
        if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
            raise ShapeDocumentError("Source relationship SHA-256 is invalid.")

    replayed = replay_commands(value.get("commands"), value.get("history_cursor"))
    replayed_ids = [item["object_id"] for item in replayed]
    layers = value.get("layers")
    if not isinstance(layers, list) or len(layers) != 1 or not isinstance(layers[0], dict):
        raise ShapeDocumentError("Shape document version 1 requires exactly one layer.")
    layer = layers[0]
    _require_non_empty_string(layer, "layer_id")
    _require_non_empty_string(layer, "name")
    if not isinstance(layer.get("visible"), bool) or not isinstance(layer.get("locked"), bool):
        raise ShapeDocumentError("Shape layer visibility and lock state must be booleans.")
    if layer.get("object_ids") != replayed_ids:
        raise ShapeDocumentError("Shape layer object IDs do not match replayed command state.")
    if value.get("objects") != replayed:
        raise ShapeDocumentError("Shape document objects do not match replayed command history.")

    integrity = value.get("integrity")
    if not isinstance(integrity, dict):
        raise ShapeDocumentError("Shape document integrity must be an object.")
    digest = integrity.get("content_sha256")
    if (
        not isinstance(digest, str)
        or len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest)
    ):
        raise ShapeDocumentError("Shape document content hash is invalid.")
    if digest != _content_digest(value):
        raise ShapeDocumentError("Shape document content hash does not match its contents.")
    return value


def _refresh_derived_state(document: dict, *, revision_increment: bool) -> dict:
    value = copy.deepcopy(document)
    value["objects"] = replay_commands(value["commands"], value["history_cursor"])
    value["layers"][0]["object_ids"] = [item["object_id"] for item in value["objects"]]
    value["updated_at_utc"] = utc_now_iso()
    if revision_increment:
        value["revision"] += 1
    return _with_integrity(value)


def blank_shape_document(
    project_id: str,
    title: str = "Untitled Shape",
    width: float = DEFAULT_CANVAS_WIDTH,
    height: float = DEFAULT_CANVAS_HEIGHT,
    units: str = "px",
) -> dict:
    if not isinstance(project_id, str) or not project_id:
        raise ShapeDocumentError("A project ID is required.")
    title_value = title.strip() if isinstance(title, str) else ""
    if not title_value:
        raise ShapeDocumentError("Shape document title is required.")
    if units not in SUPPORTED_UNITS:
        raise ShapeDocumentError("Shape document units are unsupported.")
    now = utc_now_iso()
    document = {
        "schema_name": SHAPE_DOCUMENT_SCHEMA,
        "schema_version": SHAPE_DOCUMENT_VERSION,
        "application_version": APPLICATION_VERSION,
        "document_id": f"shape_{uuid.uuid4().hex}",
        "project_id": project_id,
        "title": title_value,
        "creator": "user",
        "created_at_utc": now,
        "updated_at_utc": now,
        "revision": 1,
        "approval_state": "draft",
        "lifecycle_status": "editable",
        "supersedes_document_id": None,
        "coordinate_space": {
            "kind": "cartesian_2d",
            "origin": "top_left",
            "y_axis": "down",
            "units": units,
            "canvas": {
                "width": _require_number(width, "Canvas width", positive=True),
                "height": _require_number(height, "Canvas height", positive=True),
            },
        },
        "source_relationships": [],
        "layers": [
            {
                "layer_id": f"layer_{uuid.uuid4().hex}",
                "name": "Layer 1",
                "visible": True,
                "locked": False,
                "object_ids": [],
            }
        ],
        "groups": [],
        "anchors": [],
        "objects": [],
        "commands": [],
        "history_cursor": 0,
        "integrity": {"content_sha256": None},
    }
    return validate_shape_document(_with_integrity(document), project_id)


def add_rectangle(
    document: dict,
    *,
    x: float = 120.0,
    y: float = 120.0,
    width: float = 240.0,
    height: float = 160.0,
) -> dict:
    current = validate_shape_document(document)
    commands = copy.deepcopy(current["commands"][: current["history_cursor"]])
    commands.append(
        {
            "command_id": f"command_{uuid.uuid4().hex}",
            "type": "add_rectangle",
            "created_at_utc": utc_now_iso(),
            "payload": {
                "object_id": f"object_{uuid.uuid4().hex}",
                "layer_id": current["layers"][0]["layer_id"],
                "x": _require_number(x, "Rectangle x"),
                "y": _require_number(y, "Rectangle y"),
                "width": _require_number(width, "Rectangle width", positive=True),
                "height": _require_number(height, "Rectangle height", positive=True),
                "style": {"fill": "#d6c27a", "stroke": "#2a2415", "stroke_width": 2.0},
            },
        }
    )
    if len(commands) > MAX_COMMANDS:
        raise ShapeDocumentError(f"Shape document exceeds the {MAX_COMMANDS}-command limit.")
    current["commands"] = commands
    current["history_cursor"] = len(commands)
    return validate_shape_document(_refresh_derived_state(current, revision_increment=True))


def undo(document: dict) -> dict:
    current = validate_shape_document(document)
    if current["history_cursor"] == 0:
        raise ShapeDocumentError("Nothing is available to undo.")
    current["history_cursor"] -= 1
    return validate_shape_document(_refresh_derived_state(current, revision_increment=True))


def redo(document: dict) -> dict:
    current = validate_shape_document(document)
    if current["history_cursor"] >= len(current["commands"]):
        raise ShapeDocumentError("Nothing is available to redo.")
    current["history_cursor"] += 1
    return validate_shape_document(_refresh_derived_state(current, revision_increment=True))


def can_undo(document: dict | None) -> bool:
    return bool(document and document.get("history_cursor", 0) > 0)


def can_redo(document: dict | None) -> bool:
    return bool(
        document
        and isinstance(document.get("commands"), list)
        and document.get("history_cursor", 0) < len(document["commands"])
    )


def _read_bounded_json(path: Path) -> dict:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ShapeDocumentError("Shape document must be a regular file.")
        if metadata.st_size > MAX_DOCUMENT_BYTES:
            raise ShapeDocumentError("Shape document exceeds the safe read limit.")
        with os.fdopen(descriptor, "rb") as handle:
            descriptor = -1
            payload = handle.read(MAX_DOCUMENT_BYTES + 1)
        if len(payload) > MAX_DOCUMENT_BYTES:
            raise ShapeDocumentError("Shape document grew beyond the safe read limit.")
        return json.loads(payload.decode("utf-8"))
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        raise ShapeDocumentError(f"Could not read shape document {path}: {exc}") from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _require_session(session: ProjectSession, *, writable: bool) -> tuple[Path, str]:
    if session.state is None or session.project_dir is None:
        raise ProjectSessionError("An open project session is required.")
    if writable and not session.is_writable:
        raise ProjectSessionError("A writable project session is required.")
    manifest = session.state.assessment.manifest
    if not isinstance(manifest, dict):
        raise ProjectSessionError("The active project manifest is unavailable.")
    return session.project_dir, manifest["project_id"]


def _shape_store(session: ProjectSession, *, create: bool) -> tuple[Path, Path]:
    project_dir, _project_id = _require_session(session, writable=create)
    structures = project_dir / "structures"
    if structures.is_symlink() or not structures.is_dir():
        raise ShapeDocumentError("Canonical project structures directory is unavailable or unsafe.")
    root = project_dir / SHAPE_DOCUMENT_DIR
    autosave = project_dir / AUTOSAVE_DIR
    for candidate in (root, autosave):
        if candidate.is_symlink():
            raise ShapeDocumentError("Shape document storage must not use symbolic links.")
    if create:
        root.mkdir(exist_ok=True)
        if root.resolve().parent != structures.resolve():
            raise ShapeDocumentError("Shape document storage escapes project structures.")
        fsync_directory(structures)
        autosave.mkdir(exist_ok=True)
        if autosave.resolve().parent != root.resolve():
            raise ShapeDocumentError("Shape autosave storage escapes the shape document directory.")
        fsync_directory(root)
    elif root.exists() and (not root.is_dir() or root.resolve().parent != structures.resolve()):
        raise ShapeDocumentError("Shape document storage is unavailable or unsafe.")
    return root, autosave


def _document_path(root: Path, document_id: str) -> Path:
    if not isinstance(document_id, str) or not document_id.startswith("shape_"):
        raise ShapeDocumentError("Shape document ID is invalid.")
    path = root / f"{document_id}{SHAPE_DOCUMENT_SUFFIX}"
    if path.is_symlink() or path.resolve().parent != root.resolve():
        raise ShapeDocumentError("Shape document path is unavailable or unsafe.")
    return path


def _autosave_path(autosave_root: Path, document_id: str) -> Path:
    path = autosave_root / f"{document_id}.autosave.json"
    if path.is_symlink() or path.resolve().parent != autosave_root.resolve():
        raise ShapeDocumentError("Shape autosave path is unavailable or unsafe.")
    return path


def list_shape_documents(session: ProjectSession) -> tuple[dict, ...]:
    project_dir, project_id = _require_session(session, writable=False)
    root, _autosave = _shape_store(session, create=False)
    if not root.exists():
        return ()
    current_ids = set(session.state.assessment.manifest["current_artifact_ids"])
    documents = []
    for path in sorted(root.glob(f"shape_*{SHAPE_DOCUMENT_SUFFIX}"))[:200]:
        document = validate_shape_document(_read_bounded_json(path), project_id)
        if document["document_id"] not in current_ids:
            raise ShapeDocumentError(
                f"Shape document exists outside manifest authority: {path.relative_to(project_dir)}"
            )
        documents.append(document)
    return tuple(documents)


def load_shape_document(session: ProjectSession, document_id: str) -> ShapeDocumentLoadResult:
    _project_dir, project_id = _require_session(session, writable=False)
    root, autosave_root = _shape_store(session, create=False)
    if not root.exists():
        raise ShapeDocumentError("This project has no shape document store.")
    canonical_path = _document_path(root, document_id)
    if not canonical_path.is_file():
        raise ShapeDocumentError("Canonical shape document is unavailable.")
    canonical = validate_shape_document(_read_bounded_json(canonical_path), project_id)
    autosave_path = _autosave_path(autosave_root, document_id)
    if autosave_path.is_file():
        autosave = validate_shape_document(_read_bounded_json(autosave_path), project_id)
        if autosave["document_id"] != canonical["document_id"]:
            raise ShapeDocumentError("Shape autosave identity does not match its canonical document.")
        if autosave["revision"] > canonical["revision"]:
            return ShapeDocumentLoadResult(autosave, canonical_path, True)
    return ShapeDocumentLoadResult(canonical, canonical_path, False)


def write_shape_document_autosave(session: ProjectSession, document: dict) -> Path:
    _project_dir, project_id = _require_session(session, writable=True)
    value = validate_shape_document(document, project_id)
    serialized_value = _serialize_bounded_document(value)
    root, autosave_root = _shape_store(session, create=True)
    canonical_path = _document_path(root, value["document_id"])
    if not canonical_path.is_file():
        raise ShapeDocumentError("Save the blank shape document before creating autosave changes.")
    path = _autosave_path(autosave_root, value["document_id"])
    atomic_write_text(path, serialized_value)
    return path


def _transaction_path(project_dir: Path) -> Path:
    return project_dir / EDITOR_TRANSACTION_FILENAME


def _clear_transaction_marker(project_dir: Path, *, missing_ok: bool = False) -> None:
    try:
        _transaction_path(project_dir).unlink()
    except FileNotFoundError:
        if not missing_ok:
            raise
        return
    fsync_directory(project_dir)


def save_shape_document(session: ProjectSession, document: dict) -> Path:
    project_dir, project_id = _require_session(session, writable=True)
    value = validate_shape_document(document, project_id)
    serialized_value = _serialize_bounded_document(value)
    with session.mutation_guard():
        if (
            not session.is_writable
            or session.project_dir != project_dir
            or session.state.assessment.manifest["project_id"] != project_id
        ):
            raise ShapeDocumentError("Project authority changed before the shape document save.")

        root, autosave_root = _shape_store(session, create=True)
        canonical_path = _document_path(root, value["document_id"])
        autosave_path = _autosave_path(autosave_root, value["document_id"])
        manifest_path = project_dir / "project.json"
        history_path = project_dir / session.state.assessment.manifest["history_path"]
        if history_path.stat().st_size > MAX_HISTORY_BYTES:
            raise ShapeDocumentError("Project history exceeds the safe editor transaction limit.")
        manifest_before = manifest_path.read_text(encoding="utf-8")
        history_before = history_path.read_text(encoding="utf-8")
        canonical_before = canonical_path.read_text(encoding="utf-8") if canonical_path.is_file() else None
        marker = _transaction_path(project_dir)
        if marker.exists() or marker.is_symlink():
            raise ShapeDocumentError("An earlier editor transaction requires read-only recovery.")

        manifest = json.loads(json.dumps(session.state.assessment.manifest))
        is_new = value["document_id"] not in manifest["current_artifact_ids"]
        if is_new:
            manifest["current_artifact_ids"].append(value["document_id"])
        elif canonical_before is None:
            raise ShapeDocumentError("Manifest declares a shape document whose canonical file is missing.")
        now = utc_now_iso()
        manifest["updated_at_utc"] = now
        manifest["application_version_last_opened"] = APPLICATION_VERSION
        validate_manifest(manifest)
        event = {
            "timestamp_utc": now,
            "event": "shape_document_created" if is_new else "shape_document_saved",
            "project_id": project_id,
            "artifact_id": value["document_id"],
            "project_relative_path": canonical_path.relative_to(project_dir).as_posix(),
            "revision": value["revision"],
            "content_sha256": value["integrity"]["content_sha256"],
        }

        marker_created = canonical_write_attempted = False
        history_write_attempted = manifest_write_attempted = False
        try:
            atomic_write_text(
                marker,
                json.dumps(
                    {
                        "schema_name": "mxztar_forge_editor_transaction",
                        "schema_version": "1.0.0",
                        "operation": "save_shape_document",
                        "artifact_id": value["document_id"],
                        "canonical_before": canonical_before,
                        "manifest_before": manifest_before,
                        "history_before": history_before,
                    },
                    ensure_ascii=False,
                )
                + "\n",
            )
            marker_created = True
            canonical_write_attempted = True
            atomic_write_text(canonical_path, serialized_value)
            history_write_attempted = True
            atomic_write_text(history_path, history_before + json.dumps(event, ensure_ascii=False) + "\n")
            manifest_write_attempted = True
            atomic_write_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
            _clear_transaction_marker(project_dir)
            marker_created = False
            if autosave_path.exists():
                autosave_path.unlink()
                fsync_directory(autosave_root)
            session.update_manifest_snapshot(manifest)
            return canonical_path
        except Exception as original_error:
            rollback_ok = True
            try:
                if manifest_write_attempted:
                    atomic_write_text(manifest_path, manifest_before)
                if history_write_attempted:
                    atomic_write_text(history_path, history_before)
                if canonical_write_attempted:
                    if canonical_before is None:
                        try:
                            canonical_path.unlink()
                            fsync_directory(canonical_path.parent)
                        except FileNotFoundError:
                            # The failed save may not have created the canonical file before rollback.
                            pass
                    else:
                        atomic_write_text(canonical_path, canonical_before)
            except Exception:
                rollback_ok = False
            if marker_created and rollback_ok:
                try:
                    _clear_transaction_marker(project_dir, missing_ok=True)
                except OSError:
                    rollback_ok = False
            if not rollback_ok:
                session.revoke_writable_authority(
                    "Shape document rollback failed; explicit recovery is required."
                )
                raise ShapeDocumentError(
                    "Shape document save failed and rollback could not be confirmed."
                ) from original_error
            raise


def create_blank_shape_document(
    session: ProjectSession,
    title: str = "Untitled Shape",
    width: float = DEFAULT_CANVAS_WIDTH,
    height: float = DEFAULT_CANVAS_HEIGHT,
    units: str = "px",
) -> ShapeDocumentLoadResult:
    _project_dir, project_id = _require_session(session, writable=True)
    document = blank_shape_document(project_id, title, width, height, units)
    path = save_shape_document(session, document)
    return ShapeDocumentLoadResult(document, path, False)
