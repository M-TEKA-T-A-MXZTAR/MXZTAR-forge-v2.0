#!/usr/bin/env python3
"""Project-owned, CPU-safe 3D object-scene authority for Forge Editor."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import stat
import uuid
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


OBJECT_SCENE_SCHEMA = "mxztar_forge_object_scene"
OBJECT_SCENE_VERSION = "1.0.0"
OBJECT_SCENE_SUFFIX = ".object-scene.json"
OBJECT_SCENE_DIR = Path("structures/object-scenes")
MAX_SCENE_BYTES = 8 * 1024 * 1024
MAX_HISTORY_BYTES = 16 * 1024 * 1024
MAX_COMMANDS = 1000
SUPPORTED_PRIMITIVES = {"rectangle", "square", "circle", "ellipse", "star"}
DEFAULT_DEPTH = 80.0


class ObjectSceneError(RuntimeError):
    pass


def _content_digest(scene: dict) -> str:
    payload = copy.deepcopy(scene)
    payload["integrity"] = {"content_sha256": None}
    serialized = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def _with_integrity(scene: dict) -> dict:
    value = copy.deepcopy(scene)
    value["integrity"] = {"content_sha256": None}
    value["integrity"]["content_sha256"] = _content_digest(value)
    return value


def _serialize_bounded_scene(scene: dict) -> str:
    serialized = json.dumps(scene, indent=2, ensure_ascii=False) + "\n"
    if len(serialized.encode("utf-8")) > MAX_SCENE_BYTES:
        raise ObjectSceneError("Object scene exceeds the safe write limit.")
    return serialized


def _require_string(payload: dict, key: str, label: str | None = None) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ObjectSceneError(f"{label or key} must be a non-empty string.")
    return value


def _require_number(
    value,
    label: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
    positive: bool = False,
) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ObjectSceneError(f"{label} must be a number.")
    number = float(value)
    if not (-1.0e12 < number < 1.0e12):
        raise ObjectSceneError(f"{label} is outside the supported numeric range.")
    if positive and number <= 0:
        raise ObjectSceneError(f"{label} must be positive.")
    if minimum is not None and number < minimum:
        raise ObjectSceneError(f"{label} must be at least {minimum}.")
    if maximum is not None and number > maximum:
        raise ObjectSceneError(f"{label} must be at most {maximum}.")
    return number


def _vector3(value: object, label: str, *, positive: bool = False) -> dict:
    if not isinstance(value, dict):
        raise ObjectSceneError(f"{label} must be an object.")
    return {
        "x": _require_number(value.get("x"), f"{label} x", positive=positive),
        "y": _require_number(value.get("y"), f"{label} y", positive=positive),
        "z": _require_number(value.get("z"), f"{label} z", positive=positive),
    }


def _validate_object(value: object) -> dict:
    if not isinstance(value, dict):
        raise ObjectSceneError("Each CAD object must be an object.")
    item = copy.deepcopy(value)
    object_id = _require_string(item, "object_id", "CAD object ID")
    if not object_id.startswith("cad_"):
        raise ObjectSceneError("CAD object IDs must use the cad_ prefix.")
    source_shape_id = _require_string(item, "source_shape_id", "Source shape ID")
    if not source_shape_id.startswith("object_"):
        raise ObjectSceneError("Source shape IDs must use the object_ prefix.")
    primitive_type = item.get("primitive_type")
    if primitive_type not in SUPPORTED_PRIMITIVES:
        raise ObjectSceneError(f"Unsupported CAD primitive: {primitive_type!r}.")
    position = _vector3(item.get("position"), "Position")
    size = _vector3(item.get("size"), "Size", positive=True)
    rotation = _vector3(item.get("rotation_deg"), "Rotation")
    appearance = item.get("appearance")
    if not isinstance(appearance, dict):
        raise ObjectSceneError("CAD object appearance must be an object.")
    color = appearance.get("color")
    if not isinstance(color, str) or not color.strip():
        raise ObjectSceneError("CAD object color must be a non-empty string.")
    opacity = _require_number(
        appearance.get("opacity"),
        "CAD object opacity",
        minimum=0.0,
        maximum=1.0,
    )
    primitive_parameters = item.get("primitive_parameters", {})
    if not isinstance(primitive_parameters, dict):
        raise ObjectSceneError("CAD primitive parameters must be an object.")
    normalized_parameters: dict[str, float | int] = {}
    if primitive_type == "star":
        points = primitive_parameters.get("points", 5)
        if not isinstance(points, int) or isinstance(points, bool) or not 3 <= points <= 32:
            raise ObjectSceneError("Star point count must be an integer from 3 to 32.")
        inner_ratio = _require_number(
            primitive_parameters.get("inner_ratio", 0.45),
            "Star inner ratio",
            minimum=0.01,
            maximum=0.99,
        )
        normalized_parameters = {"points": points, "inner_ratio": inner_ratio}
    return {
        "object_id": object_id,
        "source_shape_id": source_shape_id,
        "primitive_type": primitive_type,
        "position": position,
        "size": size,
        "rotation_deg": rotation,
        "appearance": {"color": color, "opacity": opacity},
        "primitive_parameters": normalized_parameters,
    }


def _validate_view(value: object) -> dict:
    if not isinstance(value, dict):
        raise ObjectSceneError("Object scene view must be an object.")
    for key in ("perspective", "grid_visible", "edges_visible"):
        if not isinstance(value.get(key), bool):
            raise ObjectSceneError(f"Object scene view {key} must be a boolean.")
    return {
        "yaw_deg": _require_number(value.get("yaw_deg"), "View yaw"),
        "pitch_deg": _require_number(
            value.get("pitch_deg"),
            "View pitch",
            minimum=-89.0,
            maximum=89.0,
        ),
        "zoom": _require_number(
            value.get("zoom"),
            "View zoom",
            minimum=0.05,
            maximum=20.0,
        ),
        "perspective": value["perspective"],
        "grid_visible": value["grid_visible"],
        "edges_visible": value["edges_visible"],
    }


def _shape_to_object(shape: dict) -> dict:
    primitive_type = shape.get("type")
    if primitive_type not in SUPPORTED_PRIMITIVES:
        raise ObjectSceneError(f"Cannot construct a CAD object from {primitive_type!r}.")
    width = _require_number(shape.get("width"), "Source shape width", positive=True)
    height = _require_number(shape.get("height"), "Source shape height", positive=True)
    x = _require_number(shape.get("x"), "Source shape x")
    y = _require_number(shape.get("y"), "Source shape y")
    style = shape.get("style")
    if not isinstance(style, dict):
        raise ObjectSceneError("Source shape style is unavailable.")
    fill = style.get("fill")
    if not isinstance(fill, str) or not fill:
        raise ObjectSceneError("Source shape fill is unavailable.")
    source_shape_id = _require_string(shape, "object_id", "Source shape ID")
    depth = max(24.0, min(180.0, (width + height) / 5.0))
    parameters: dict[str, float | int] = {}
    if primitive_type == "star":
        parameters = {
            "points": int(shape.get("points", 5)),
            "inner_ratio": float(shape.get("inner_ratio", 0.45)),
        }
    return _validate_object(
        {
            "object_id": f"cad_{source_shape_id.removeprefix('object_')}",
            "source_shape_id": source_shape_id,
            "primitive_type": primitive_type,
            "position": {
                "x": x + width / 2.0,
                "y": y + height / 2.0,
                "z": depth / 2.0,
            },
            "size": {"x": width, "y": height, "z": depth},
            "rotation_deg": {"x": 0.0, "y": 0.0, "z": 0.0},
            "appearance": {"color": fill, "opacity": 1.0},
            "primitive_parameters": parameters,
        }
    )


def replay_scene_commands(commands: object, history_cursor: int) -> list[dict]:
    if not isinstance(commands, list):
        raise ObjectSceneError("Object scene commands must be a list.")
    if len(commands) > MAX_COMMANDS:
        raise ObjectSceneError(f"Object scene exceeds the {MAX_COMMANDS}-command limit.")
    if not isinstance(history_cursor, int) or isinstance(history_cursor, bool):
        raise ObjectSceneError("Object scene history cursor must be an integer.")
    if history_cursor < 0 or history_cursor > len(commands):
        raise ObjectSceneError("Object scene history cursor is outside command history.")

    ordered_ids: list[str] = []
    objects: dict[str, dict] = {}
    seen_command_ids: set[str] = set()
    for index, command in enumerate(commands):
        if not isinstance(command, dict):
            raise ObjectSceneError("Each object-scene command must be an object.")
        command_id = _require_string(command, "command_id", "Object-scene command ID")
        if command_id in seen_command_ids:
            raise ObjectSceneError("Object scene contains a duplicate command ID.")
        seen_command_ids.add(command_id)
        _require_string(command, "created_at_utc", "Object-scene command timestamp")
        command_type = command.get("type")
        payload = command.get("payload")
        if not isinstance(payload, dict):
            raise ObjectSceneError("Object-scene command payload must be an object.")
        if command_type == "add_object":
            item = _validate_object(payload.get("object"))
            if index < history_cursor:
                if item["object_id"] in objects:
                    raise ObjectSceneError("Object scene contains a duplicate CAD object ID.")
                ordered_ids.append(item["object_id"])
                objects[item["object_id"]] = item
        elif command_type == "update_object":
            before = _validate_object(payload.get("before"))
            after = _validate_object(payload.get("after"))
            if before["object_id"] != after["object_id"]:
                raise ObjectSceneError("Object update cannot change CAD object identity.")
            if index < history_cursor:
                object_id = before["object_id"]
                if object_id not in objects:
                    raise ObjectSceneError("Object update targets an unavailable CAD object.")
                if objects[object_id] != before:
                    raise ObjectSceneError("Object update before-state does not match replayed state.")
                objects[object_id] = after
        else:
            raise ObjectSceneError(f"Unsupported object-scene command: {command_type!r}.")
    return [objects[object_id] for object_id in ordered_ids if object_id in objects]


def validate_object_scene(scene: object, project_id: str | None = None) -> dict:
    if not isinstance(scene, dict):
        raise ObjectSceneError("Object scene root must be a JSON object.")
    value = copy.deepcopy(scene)
    if value.get("schema_name") != OBJECT_SCENE_SCHEMA:
        raise ObjectSceneError("Unsupported object-scene schema.")
    if value.get("schema_version") != OBJECT_SCENE_VERSION:
        raise ObjectSceneError("Unsupported object-scene schema version.")
    _require_string(value, "application_version", "Application version")
    scene_id = _require_string(value, "scene_id", "Object scene ID")
    if not scene_id.startswith("scene_"):
        raise ObjectSceneError("Object scene IDs must use the scene_ prefix.")
    actual_project_id = _require_string(value, "project_id", "Project ID")
    if project_id is not None and actual_project_id != project_id:
        raise ObjectSceneError("Object scene belongs to a different project.")
    source_document_id = _require_string(
        value,
        "source_document_id",
        "Source shape-document ID",
    )
    if not source_document_id.startswith("shape_"):
        raise ObjectSceneError("Object scenes require a shape_ source document.")
    for key in ("created_at_utc", "updated_at_utc"):
        _require_string(value, key, key)
    revision = value.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise ObjectSceneError("Object scene revision must be a positive integer.")
    view = _validate_view(value.get("view"))
    objects = replay_scene_commands(value.get("commands"), value.get("history_cursor"))
    if value.get("objects") != objects:
        raise ObjectSceneError("Object scene objects do not match replayed command history.")
    source_shape_ids = [item["source_shape_id"] for item in objects]
    if len(source_shape_ids) != len(set(source_shape_ids)):
        raise ObjectSceneError("Object scene contains duplicate source-shape relationships.")
    integrity = value.get("integrity")
    if not isinstance(integrity, dict):
        raise ObjectSceneError("Object scene integrity must be an object.")
    digest = integrity.get("content_sha256")
    if (
        not isinstance(digest, str)
        or len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest)
    ):
        raise ObjectSceneError("Object-scene content hash is invalid.")
    normalized = copy.deepcopy(value)
    normalized["view"] = view
    normalized["objects"] = objects
    if digest != _content_digest(normalized):
        raise ObjectSceneError("Object-scene content hash does not match its contents.")
    return normalized


def _refresh_scene(scene: dict, *, revision_increment: bool = True) -> dict:
    value = copy.deepcopy(scene)
    value["objects"] = replay_scene_commands(value["commands"], value["history_cursor"])
    value["updated_at_utc"] = utc_now_iso()
    if revision_increment:
        value["revision"] += 1
    return _with_integrity(value)


def create_object_scene(project_id: str, shape_document: dict) -> dict:
    if not isinstance(project_id, str) or not project_id:
        raise ObjectSceneError("A project ID is required.")
    if not isinstance(shape_document, dict):
        raise ObjectSceneError("A shape document is required.")
    source_document_id = _require_string(
        shape_document,
        "document_id",
        "Source shape-document ID",
    )
    if not source_document_id.startswith("shape_"):
        raise ObjectSceneError("Object scenes require a shape_ source document.")
    commands = []
    for shape in shape_document.get("objects", []):
        item = _shape_to_object(shape)
        commands.append(
            {
                "command_id": f"command_{uuid.uuid4().hex}",
                "type": "add_object",
                "created_at_utc": utc_now_iso(),
                "payload": {"object": item},
            }
        )
    now = utc_now_iso()
    scene = {
        "schema_name": OBJECT_SCENE_SCHEMA,
        "schema_version": OBJECT_SCENE_VERSION,
        "application_version": APPLICATION_VERSION,
        "scene_id": f"scene_{uuid.uuid4().hex}",
        "project_id": project_id,
        "source_document_id": source_document_id,
        "created_at_utc": now,
        "updated_at_utc": now,
        "revision": 1,
        "view": {
            "yaw_deg": 35.0,
            "pitch_deg": 28.0,
            "zoom": 0.75,
            "perspective": True,
            "grid_visible": True,
            "edges_visible": True,
        },
        "objects": [],
        "commands": commands,
        "history_cursor": len(commands),
        "integrity": {"content_sha256": None},
    }
    return validate_object_scene(_refresh_scene(scene, revision_increment=False), project_id)


def sync_scene_from_shape_document(scene: dict, shape_document: dict) -> tuple[dict, int]:
    current = validate_object_scene(scene)
    if shape_document.get("document_id") != current["source_document_id"]:
        raise ObjectSceneError("Shape document does not match the object scene.")
    existing = {item["source_shape_id"] for item in current["objects"]}
    commands = copy.deepcopy(current["commands"][: current["history_cursor"]])
    added = 0
    for shape in shape_document.get("objects", []):
        source_shape_id = shape.get("object_id")
        if source_shape_id in existing:
            continue
        item = _shape_to_object(shape)
        commands.append(
            {
                "command_id": f"command_{uuid.uuid4().hex}",
                "type": "add_object",
                "created_at_utc": utc_now_iso(),
                "payload": {"object": item},
            }
        )
        existing.add(item["source_shape_id"])
        added += 1
    if not added:
        return current, 0
    if len(commands) > MAX_COMMANDS:
        raise ObjectSceneError(f"Object scene exceeds the {MAX_COMMANDS}-command limit.")
    current["commands"] = commands
    current["history_cursor"] = len(commands)
    return validate_object_scene(_refresh_scene(current), current["project_id"]), added


def update_scene_object(scene: dict, object_id: str, updated_object: dict) -> dict:
    current = validate_object_scene(scene)
    before = next(
        (item for item in current["objects"] if item["object_id"] == object_id),
        None,
    )
    if before is None:
        raise ObjectSceneError("The selected CAD object is unavailable.")
    after = _validate_object(updated_object)
    if after["object_id"] != object_id:
        raise ObjectSceneError("CAD object identity cannot change during an update.")
    if after["source_shape_id"] != before["source_shape_id"]:
        raise ObjectSceneError("CAD object source authority cannot change during an update.")
    if after == before:
        return current
    commands = copy.deepcopy(current["commands"][: current["history_cursor"]])
    commands.append(
        {
            "command_id": f"command_{uuid.uuid4().hex}",
            "type": "update_object",
            "created_at_utc": utc_now_iso(),
            "payload": {"before": before, "after": after},
        }
    )
    if len(commands) > MAX_COMMANDS:
        raise ObjectSceneError(f"Object scene exceeds the {MAX_COMMANDS}-command limit.")
    current["commands"] = commands
    current["history_cursor"] = len(commands)
    return validate_object_scene(_refresh_scene(current), current["project_id"])


def set_scene_view(scene: dict, **changes) -> dict:
    current = validate_object_scene(scene)
    view = copy.deepcopy(current["view"])
    for key in (
        "yaw_deg",
        "pitch_deg",
        "zoom",
        "perspective",
        "grid_visible",
        "edges_visible",
    ):
        if key in changes:
            view[key] = changes[key]
    current["view"] = _validate_view(view)
    return validate_object_scene(_refresh_scene(current), current["project_id"])


def undo_scene(scene: dict) -> dict:
    current = validate_object_scene(scene)
    if current["history_cursor"] == 0:
        raise ObjectSceneError("Nothing is available to undo in the object scene.")
    current["history_cursor"] -= 1
    return validate_object_scene(_refresh_scene(current), current["project_id"])


def redo_scene(scene: dict) -> dict:
    current = validate_object_scene(scene)
    if current["history_cursor"] >= len(current["commands"]):
        raise ObjectSceneError("Nothing is available to redo in the object scene.")
    current["history_cursor"] += 1
    return validate_object_scene(_refresh_scene(current), current["project_id"])


def can_undo_scene(scene: dict | None) -> bool:
    return bool(scene and scene.get("history_cursor", 0) > 0)


def can_redo_scene(scene: dict | None) -> bool:
    return bool(
        scene
        and isinstance(scene.get("commands"), list)
        and scene.get("history_cursor", 0) < len(scene["commands"])
    )


def _require_session(session: ProjectSession, *, writable: bool) -> tuple[Path, str]:
    if session.state is None or session.project_dir is None:
        raise ProjectSessionError("An open project session is required.")
    if writable and not session.is_writable:
        raise ProjectSessionError("A writable project session is required.")
    manifest = session.state.assessment.manifest
    if not isinstance(manifest, dict):
        raise ProjectSessionError("The active project manifest is unavailable.")
    return session.project_dir, manifest["project_id"]


def _scene_store(session: ProjectSession, *, create: bool) -> Path:
    project_dir, _project_id = _require_session(session, writable=create)
    structures = project_dir / "structures"
    if structures.is_symlink() or not structures.is_dir():
        raise ObjectSceneError("Canonical project structures directory is unavailable or unsafe.")
    root = project_dir / OBJECT_SCENE_DIR
    if root.is_symlink():
        raise ObjectSceneError("Object-scene storage must not use symbolic links.")
    if create:
        root.mkdir(exist_ok=True)
        if root.resolve().parent != structures.resolve():
            raise ObjectSceneError("Object-scene storage escapes project structures.")
        fsync_directory(structures)
    elif root.exists() and (not root.is_dir() or root.resolve().parent != structures.resolve()):
        raise ObjectSceneError("Object-scene storage is unavailable or unsafe.")
    return root


def _scene_path(root: Path, source_document_id: str) -> Path:
    if not isinstance(source_document_id, str) or not source_document_id.startswith("shape_"):
        raise ObjectSceneError("Object-scene source document ID is invalid.")
    path = root / f"{source_document_id}{OBJECT_SCENE_SUFFIX}"
    if path.is_symlink() or path.resolve().parent != root.resolve():
        raise ObjectSceneError("Object-scene path is unavailable or unsafe.")
    return path


def _read_bounded_json(path: Path) -> dict:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ObjectSceneError("Object scene must be a regular file.")
        if metadata.st_size > MAX_SCENE_BYTES:
            raise ObjectSceneError("Object scene exceeds the safe read limit.")
        with os.fdopen(descriptor, "rb") as handle:
            descriptor = -1
            payload = handle.read(MAX_SCENE_BYTES + 1)
        if len(payload) > MAX_SCENE_BYTES:
            raise ObjectSceneError("Object scene grew beyond the safe read limit.")
        return json.loads(payload.decode("utf-8"))
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        raise ObjectSceneError(f"Could not read object scene {path}: {exc}") from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def load_object_scene(session: ProjectSession, source_document_id: str) -> dict:
    _project_dir, project_id = _require_session(session, writable=False)
    root = _scene_store(session, create=False)
    if not root.exists():
        raise ObjectSceneError("This project has no object-scene store.")
    path = _scene_path(root, source_document_id)
    if not path.is_file():
        raise ObjectSceneError("Canonical object scene is unavailable.")
    scene = validate_object_scene(_read_bounded_json(path), project_id)
    current_ids = set(session.state.assessment.manifest["current_artifact_ids"])
    if scene["scene_id"] not in current_ids:
        raise ObjectSceneError("Object scene exists outside manifest authority.")
    return scene


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


def save_object_scene(session: ProjectSession, scene: dict) -> Path:
    project_dir, project_id = _require_session(session, writable=True)
    value = validate_object_scene(scene, project_id)
    serialized_value = _serialize_bounded_scene(value)
    with session.mutation_guard():
        if (
            not session.is_writable
            or session.project_dir != project_dir
            or session.state.assessment.manifest["project_id"] != project_id
        ):
            raise ObjectSceneError("Project authority changed before the object-scene save.")

        root = _scene_store(session, create=True)
        canonical_path = _scene_path(root, value["source_document_id"])
        manifest_path = project_dir / "project.json"
        history_path = project_dir / session.state.assessment.manifest["history_path"]
        if history_path.stat().st_size > MAX_HISTORY_BYTES:
            raise ObjectSceneError("Project history exceeds the safe object-scene transaction limit.")
        manifest_before = manifest_path.read_text(encoding="utf-8")
        history_before = history_path.read_text(encoding="utf-8")
        canonical_before = (
            canonical_path.read_text(encoding="utf-8")
            if canonical_path.is_file()
            else None
        )
        marker = _transaction_path(project_dir)
        if marker.exists() or marker.is_symlink():
            raise ObjectSceneError("An earlier editor transaction requires read-only recovery.")

        manifest = json.loads(json.dumps(session.state.assessment.manifest))
        is_new = value["scene_id"] not in manifest["current_artifact_ids"]
        if is_new:
            manifest["current_artifact_ids"].append(value["scene_id"])
        elif canonical_before is None:
            raise ObjectSceneError(
                "Manifest declares an object scene whose canonical file is missing."
            )
        now = utc_now_iso()
        manifest["updated_at_utc"] = now
        manifest["application_version_last_opened"] = APPLICATION_VERSION
        validate_manifest(manifest)
        event = {
            "timestamp_utc": now,
            "event": "object_scene_created" if is_new else "object_scene_saved",
            "project_id": project_id,
            "artifact_id": value["scene_id"],
            "source_document_id": value["source_document_id"],
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
                        "operation": "save_object_scene",
                        "artifact_id": value["scene_id"],
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
            atomic_write_text(
                history_path,
                history_before + json.dumps(event, ensure_ascii=False) + "\n",
            )
            manifest_write_attempted = True
            atomic_write_text(
                manifest_path,
                json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            )
            _clear_transaction_marker(project_dir)
            marker_created = False
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
                    "Object-scene rollback failed; explicit recovery is required."
                )
                raise ObjectSceneError(
                    "Object-scene save failed and rollback could not be confirmed."
                ) from original_error
            raise


def load_or_create_object_scene(
    session: ProjectSession,
    shape_document: dict,
) -> tuple[dict, bool, int]:
    _project_dir, project_id = _require_session(session, writable=False)
    source_document_id = _require_string(
        shape_document,
        "document_id",
        "Source shape-document ID",
    )
    root = _scene_store(session, create=False)
    path = _scene_path(root, source_document_id) if root.exists() else None
    if path is not None and path.is_file():
        scene = load_object_scene(session, source_document_id)
        synchronized, added = sync_scene_from_shape_document(scene, shape_document)
        if added:
            if not session.is_writable:
                raise ObjectSceneError(
                    "New shapes require writable authority before the 3D scene can synchronize."
                )
            save_object_scene(session, synchronized)
            return synchronized, False, added
        return scene, False, 0
    if not session.is_writable:
        raise ObjectSceneError("Writable authority is required to create a 3D object scene.")
    scene = create_object_scene(project_id, shape_document)
    save_object_scene(session, scene)
    return scene, True, len(scene["objects"])
