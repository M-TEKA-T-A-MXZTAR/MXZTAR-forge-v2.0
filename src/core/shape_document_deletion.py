#!/usr/bin/env python3
"""Direct shape deletion and guarded removal of one complete shape document."""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path

from core.object_scene import (
    _read_bounded_json as _read_scene_json,
    _scene_path,
    _scene_store,
    validate_object_scene,
)
from core.project_manifest import (
    APPLICATION_VERSION,
    atomic_write_text,
    fsync_directory,
    utc_now_iso,
    validate_manifest,
)
from core.project_session import ProjectSession
from core.shape_document import (
    MAX_HISTORY_BYTES,
    ShapeDocumentError,
    _autosave_path,
    _clear_transaction_marker,
    _document_path,
    _read_bounded_json,
    _refresh_derived_state,
    _require_session,
    _shape_store,
    _transaction_path,
    validate_shape_document,
)


@dataclass(frozen=True)
class ShapeDocumentDeletionResult:
    document_id: str
    canonical_path: Path
    object_scene_path: Path | None
    autosave_removed: bool


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


def delete_shape_document(
    session: ProjectSession,
    document_id: str,
) -> ShapeDocumentDeletionResult:
    """Remove one canonical document and its paired 3D scene transactionally.

    The manifest, project history, canonical shape file, optional autosave, and
    optional object-scene file move through one rollback boundary. A failed
    operation restores every changed artifact or revokes writable authority.
    """
    project_dir, project_id = _require_session(session, writable=True)

    with session.mutation_guard():
        if (
            not session.is_writable
            or session.project_dir != project_dir
            or session.state.assessment.manifest["project_id"] != project_id
        ):
            raise ShapeDocumentError(
                "Project authority changed before the shape document deletion."
            )

        root, autosave_root = _shape_store(session, create=False)
        if not root.exists():
            raise ShapeDocumentError("This project has no shape document store.")
        canonical_path = _document_path(root, document_id)
        if not canonical_path.is_file():
            raise ShapeDocumentError("Canonical shape document is unavailable.")
        canonical_document = validate_shape_document(
            _read_bounded_json(canonical_path),
            project_id,
        )
        if canonical_document["document_id"] != document_id:
            raise ShapeDocumentError("Shape document identity does not match its path.")

        autosave_path = _autosave_path(autosave_root, document_id)
        if autosave_path.exists() and not autosave_path.is_file():
            raise ShapeDocumentError("Shape document autosave is unavailable or unsafe.")

        scene_path: Path | None = None
        scene_id: str | None = None
        scene_before: str | None = None
        scene_root = _scene_store(session, create=False)
        if scene_root.exists():
            candidate = _scene_path(scene_root, document_id)
            if candidate.exists() and not candidate.is_file():
                raise ShapeDocumentError("Paired object scene is unavailable or unsafe.")
            if candidate.is_file():
                scene = validate_object_scene(_read_scene_json(candidate), project_id)
                if scene["source_document_id"] != document_id:
                    raise ShapeDocumentError(
                        "Paired object scene does not belong to the selected document."
                    )
                scene_path = candidate
                scene_id = scene["scene_id"]
                scene_before = candidate.read_text(encoding="utf-8")

        manifest_path = project_dir / "project.json"
        history_path = project_dir / session.state.assessment.manifest["history_path"]
        if history_path.stat().st_size > MAX_HISTORY_BYTES:
            raise ShapeDocumentError(
                "Project history exceeds the safe document-deletion transaction limit."
            )
        manifest_before = manifest_path.read_text(encoding="utf-8")
        history_before = history_path.read_text(encoding="utf-8")
        canonical_before = canonical_path.read_text(encoding="utf-8")
        autosave_before = (
            autosave_path.read_text(encoding="utf-8")
            if autosave_path.is_file()
            else None
        )
        marker = _transaction_path(project_dir)
        if marker.exists() or marker.is_symlink():
            raise ShapeDocumentError(
                "An earlier editor transaction requires read-only recovery."
            )

        manifest = json.loads(json.dumps(session.state.assessment.manifest))
        current_ids = manifest["current_artifact_ids"]
        if document_id not in current_ids:
            raise ShapeDocumentError(
                "Manifest authority does not include the selected shape document."
            )
        current_ids.remove(document_id)
        if scene_id is not None:
            if scene_id not in current_ids:
                raise ShapeDocumentError(
                    "Manifest authority does not include the paired object scene."
                )
            current_ids.remove(scene_id)

        now = utc_now_iso()
        manifest["updated_at_utc"] = now
        manifest["application_version_last_opened"] = APPLICATION_VERSION
        validate_manifest(manifest)
        event = {
            "timestamp_utc": now,
            "event": "shape_document_deleted",
            "project_id": project_id,
            "artifact_id": document_id,
            "project_relative_path": canonical_path.relative_to(project_dir).as_posix(),
            "revision": canonical_document["revision"],
            "content_sha256": canonical_document["integrity"]["content_sha256"],
            "paired_object_scene_id": scene_id,
        }

        marker_created = False
        canonical_removed = False
        autosave_removed = False
        scene_removed = False
        history_write_attempted = False
        manifest_write_attempted = False
        try:
            atomic_write_text(
                marker,
                json.dumps(
                    {
                        "schema_name": "mxztar_forge_editor_transaction",
                        "schema_version": "1.0.0",
                        "operation": "delete_shape_document",
                        "artifact_id": document_id,
                        "canonical_before": canonical_before,
                        "autosave_before": autosave_before,
                        "object_scene_before": scene_before,
                        "manifest_before": manifest_before,
                        "history_before": history_before,
                    },
                    ensure_ascii=False,
                )
                + "\n",
            )
            marker_created = True

            canonical_path.unlink()
            canonical_removed = True
            fsync_directory(root)

            if autosave_path.is_file():
                autosave_path.unlink()
                autosave_removed = True
                fsync_directory(autosave_root)

            if scene_path is not None:
                scene_path.unlink()
                scene_removed = True
                fsync_directory(scene_root)

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
            return ShapeDocumentDeletionResult(
                document_id=document_id,
                canonical_path=canonical_path,
                object_scene_path=scene_path,
                autosave_removed=autosave_removed,
            )
        except Exception as original_error:
            rollback_ok = True
            try:
                if manifest_write_attempted:
                    atomic_write_text(manifest_path, manifest_before)
                if history_write_attempted:
                    atomic_write_text(history_path, history_before)
                if scene_removed and scene_path is not None and scene_before is not None:
                    atomic_write_text(scene_path, scene_before)
                if autosave_removed and autosave_before is not None:
                    atomic_write_text(autosave_path, autosave_before)
                if canonical_removed:
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
                    "Shape document deletion rollback failed; explicit recovery is required."
                )
                raise ShapeDocumentError(
                    "Shape document deletion failed and rollback could not be confirmed."
                ) from original_error
            raise
