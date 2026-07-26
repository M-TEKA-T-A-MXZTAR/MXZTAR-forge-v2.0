#!/usr/bin/env python3
"""Reconcile object-scene membership with its authoritative shape document."""

from __future__ import annotations

import copy
import hashlib
import json
import uuid

from core.object_scene import (
    ObjectSceneError,
    create_object_scene,
    validate_object_scene,
)
from core.project_manifest import utc_now_iso


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


def reconcile_scene_membership(
    scene: dict,
    shape_document: dict,
) -> tuple[dict, int, int]:
    """Match 3D membership to 2D authority while preserving surviving CAD edits.

    Shape history and object history are separate authorities. When shape Undo or
    Redo changes membership, compact the active object commands into one canonical
    add command per currently visible source shape. The scene identity, camera/view,
    and edited state of every surviving object remain unchanged.
    """

    current = validate_object_scene(scene)
    if shape_document.get("document_id") != current["source_document_id"]:
        raise ObjectSceneError("Shape document does not match the object scene.")

    shapes = shape_document.get("objects", [])
    if not isinstance(shapes, list):
        raise ObjectSceneError("Shape document objects must be a list.")

    desired_ids = [shape.get("object_id") for shape in shapes]
    if any(not isinstance(source_id, str) for source_id in desired_ids):
        raise ObjectSceneError("Shape document contains an invalid source-shape ID.")
    if len(desired_ids) != len(set(desired_ids)):
        raise ObjectSceneError("Shape document contains duplicate source-shape IDs.")

    current_by_source = {
        item["source_shape_id"]: copy.deepcopy(item)
        for item in current["objects"]
    }
    current_ids = set(current_by_source)
    desired_set = set(desired_ids)
    added = len(desired_set - current_ids)
    removed = len(current_ids - desired_set)

    if not added and not removed:
        return current, 0, 0

    defaults = create_object_scene(current["project_id"], shape_document)
    default_by_source = {
        item["source_shape_id"]: item
        for item in defaults["objects"]
    }
    reconciled_objects = [
        copy.deepcopy(current_by_source.get(source_id, default_by_source[source_id]))
        for source_id in desired_ids
    ]

    now = utc_now_iso()
    commands = [
        {
            "command_id": f"command_{uuid.uuid4().hex}",
            "type": "add_object",
            "created_at_utc": now,
            "payload": {"object": copy.deepcopy(item)},
        }
        for item in reconciled_objects
    ]

    reconciled = copy.deepcopy(current)
    reconciled["commands"] = commands
    reconciled["history_cursor"] = len(commands)
    reconciled["objects"] = reconciled_objects
    reconciled["revision"] += 1
    reconciled["updated_at_utc"] = now
    reconciled = _with_integrity(reconciled)
    return validate_object_scene(reconciled, current["project_id"]), added, removed
