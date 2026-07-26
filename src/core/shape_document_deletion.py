#!/usr/bin/env python3
"""Direct deletion for one selected draft shape without misusing Undo."""

from __future__ import annotations

import copy

from core.shape_document import (
    ShapeDocumentError,
    _refresh_derived_state,
    validate_shape_document,
)


def delete_shape_from_document(document: dict, object_id: str) -> dict:
    """Remove one active shape command and compact the draft command history.

    Direct deletion is intentionally distinct from Edit -> Undo. Redo history is
    discarded, matching the existing add-after-undo command contract.
    """
    if not isinstance(object_id, str) or not object_id.startswith("object_"):
        raise ShapeDocumentError("A valid selected shape ID is required for deletion.")

    current = validate_shape_document(document)
    active_commands = copy.deepcopy(current["commands"][: current["history_cursor"]])
    retained = []
    removed = 0
    for command in active_commands:
        payload = command.get("payload") if isinstance(command, dict) else None
        command_object_id = payload.get("object_id") if isinstance(payload, dict) else None
        if command_object_id == object_id:
            removed += 1
            continue
        retained.append(command)

    if removed == 0:
        raise ShapeDocumentError("The selected shape is not present in active document history.")
    if removed != 1:
        raise ShapeDocumentError("Shape history contains duplicate selected-shape commands.")

    current["commands"] = retained
    current["history_cursor"] = len(retained)
    return validate_shape_document(
        _refresh_derived_state(current, revision_increment=True),
        current["project_id"],
    )
