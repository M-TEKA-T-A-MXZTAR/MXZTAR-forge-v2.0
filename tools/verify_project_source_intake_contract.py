#!/usr/bin/env python3
"""Verify copy-only project source intake and processed transition."""

from __future__ import annotations

import hashlib
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from core import project_source_intake as intake_module
from core.project_access import SOURCE_TRANSACTION_FILENAME, ProjectAccessStatus
from core.project_session import ProjectSession, ProjectSessionError
from core.project_source_intake import (
    SourceIntakeError,
    import_source_copy,
    mark_source_processed,
    scan_project_source_art,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        external = root / "external"
        projects = root / "projects"
        external.mkdir()
        source = external / "Source Art.png"
        Image.new("RGB", (2400, 1200), (20, 40, 80)).save(source)
        source_before = source.read_bytes()

        session = ProjectSession(projects)
        session.create_and_open("Source Intake Contract")
        result = import_source_copy(session, source)
        record = result.record
        project_dir = session.project_dir
        require(not result.duplicate, "first intake was classified duplicate")
        require(source.read_bytes() == source_before, "external source bytes changed")
        require(record["sha256"] == hashlib.sha256(source_before).hexdigest(), "hash drifted")
        require((project_dir / record["project_relative_path"]).read_bytes() == source_before, "copy drifted")
        require((project_dir / record["preview_relative_path"]).is_file(), "preview missing")
        with Image.open(project_dir / record["preview_relative_path"]) as preview:
            require(preview.width <= 1600 and preview.height <= 1600, "preview is unbounded")
        manifest = json.loads((project_dir / "project.json").read_text(encoding="utf-8"))
        require(manifest["source_asset_ids"] == [record["asset_id"]], "manifest source ID missing")
        history = (project_dir / manifest["history_path"]).read_text(encoding="utf-8")
        require('"event": "source_imported"' in history, "intake history event missing")
        discovered = scan_project_source_art(session)
        require(len(discovered) == 1, "project discovery omitted imported source")
        require(discovered[0].path == project_dir / record["project_relative_path"], "discovery path drifted")
        require(discovered[0].preview_path == project_dir / record["preview_relative_path"], "preview path drifted")
        require(discovered[0].authority == "active_project", "project authority was not explicit")
        print("PASS: source intake copies bytes, hashes identity, and creates a bounded preview")
        print("PASS: active-project discovery resolves canonical source and preview authority")

        history_before = history
        duplicate = import_source_copy(session, source)
        require(duplicate.duplicate, "identical bytes were imported twice")
        require(
            (project_dir / manifest["history_path"]).read_text(encoding="utf-8") == history_before,
            "duplicate intake appended history",
        )
        print("PASS: content-addressed duplicate intake is idempotent")

        processed = mark_source_processed(session, record["asset_id"])
        require(processed["lifecycle_status"] == "processed", "processed status missing")
        require(processed["project_relative_path"].startswith("source/processed/"), "source not moved")
        require((project_dir / processed["project_relative_path"]).read_bytes() == source_before, "move changed bytes")
        require(source.read_bytes() == source_before, "processed transition moved external source")
        processed_discovery = scan_project_source_art(session)
        require(
            processed_discovery[0].path == project_dir / processed["project_relative_path"],
            "processed project source was not rediscovered",
        )
        print("PASS: explicit processed transition moves only the project-owned copy")

        symlink = external / "link.png"
        symlink.symlink_to(source)
        try:
            import_source_copy(session, symlink)
        except SourceIntakeError:
            pass
        else:
            raise AssertionError("symlink source was accepted")
        try:
            import_source_copy(session, external / "unsupported.svg")
        except SourceIntakeError:
            pass
        else:
            raise AssertionError("unsupported source extension was accepted")
        print("PASS: unsafe and unsupported source paths are rejected")

        invalid = external / "invalid.png"
        invalid.write_bytes(b"not an image")
        manifest_before = (project_dir / "project.json").read_bytes()
        history_before_bytes = (project_dir / manifest["history_path"]).read_bytes()
        try:
            import_source_copy(session, invalid)
        except SourceIntakeError:
            pass
        else:
            raise AssertionError("invalid image was imported")
        require((project_dir / "project.json").read_bytes() == manifest_before, "failed intake changed manifest")
        require(
            (project_dir / manifest["history_path"]).read_bytes() == history_before_bytes,
            "failed intake changed history",
        )
        require(not list((project_dir / "source").rglob(".source-intake.tmp")), "temporary copy leaked")
        print("PASS: failed preview validation rolls back without authority drift")

        other_source = external / "other.png"
        Image.new("RGB", (32, 32), (90, 30, 10)).save(other_source)
        real_atomic_write = intake_module.atomic_write_text
        manifest_failures_remaining = 1

        def fail_manifest(path, text):
            nonlocal manifest_failures_remaining
            if Path(path).name == "project.json" and manifest_failures_remaining:
                manifest_failures_remaining -= 1
                raise OSError("manifest write test")
            return real_atomic_write(path, text)

        with patch.object(intake_module, "atomic_write_text", side_effect=fail_manifest):
            try:
                import_source_copy(session, other_source)
            except OSError:
                pass
            else:
                raise AssertionError("manifest failure was ignored")
        require((project_dir / "project.json").read_bytes() == manifest_before, "manifest failure drifted manifest")
        require(
            (project_dir / manifest["history_path"]).read_bytes() == history_before_bytes,
            "manifest failure drifted history",
        )
        print("PASS: manifest-write failure restores history and removes staged artifacts")

        session.close()
        detached = ProjectSession(projects)
        try:
            import_source_copy(detached, source)
        except ProjectSessionError:
            pass
        else:
            raise AssertionError("detached intake was accepted")
        print("PASS: source mutation requires a writable project session")

        format_session = ProjectSession(projects)
        format_session.create_and_open("Format Contract")
        disguised = external / "disguised.png"
        Image.new("RGB", (20, 20), (1, 2, 3)).save(disguised, format="GIF")
        try:
            import_source_copy(format_session, disguised)
        except SourceIntakeError:
            pass
        else:
            raise AssertionError("decoded format mismatch was accepted")
        print("PASS: decoded image format must match its supported extension")

        canonical_source = external / "canonical.png"
        Image.new("RGB", (40, 40), (4, 5, 6)).save(canonical_source)
        canonical_result = import_source_copy(format_session, canonical_source)
        canonical_record_path = (
            format_session.project_dir
            / "source"
            / "originals"
            / f"{canonical_result.record['asset_id']}.source.json"
        )
        damaged_record = json.loads(canonical_record_path.read_text(encoding="utf-8"))
        damaged_record["project_relative_path"] = "project.json"
        canonical_record_path.write_text(json.dumps(damaged_record), encoding="utf-8")
        try:
            mark_source_processed(format_session, canonical_result.record["asset_id"])
        except SourceIntakeError:
            pass
        else:
            raise AssertionError("noncanonical source record path was trusted")
        require((format_session.project_dir / "project.json").is_file(), "manifest was moved")
        canonical_record_path.write_text(
            json.dumps(canonical_result.record, indent=2) + "\n", encoding="utf-8"
        )
        print("PASS: source records are constrained to canonical asset paths")

        stored_path = format_session.project_dir / canonical_result.record["project_relative_path"]
        stored_path.write_bytes(b"corrupted project copy")
        try:
            import_source_copy(format_session, canonical_source)
        except SourceIntakeError:
            pass
        else:
            raise AssertionError("corrupt stored copy was accepted as duplicate")
        print("PASS: duplicate intake rehashes the stored project copy")
        format_session.close()

        symlink_session = ProjectSession(projects)
        symlink_session.create_and_open("Processed Symlink")
        symlink_result = import_source_copy(symlink_session, source)
        processed_link = symlink_session.project_dir / "source" / "processed"
        processed_link.symlink_to(external, target_is_directory=True)
        try:
            mark_source_processed(symlink_session, symlink_result.record["asset_id"])
        except SourceIntakeError:
            pass
        else:
            raise AssertionError("symlinked processed directory was accepted")
        require(source.read_bytes() == source_before, "symlink transition changed external bytes")
        print("PASS: processed-source destination cannot escape through a symlink")
        symlink_session.close()

        fifo_session = ProjectSession(projects)
        fifo_session.create_and_open("FIFO Contract")
        fifo = external / "pipe.png"
        os.mkfifo(fifo)
        try:
            import_source_copy(fifo_session, fifo)
        except SourceIntakeError:
            pass
        else:
            raise AssertionError("FIFO source was accepted")
        fifo.unlink()
        print("PASS: FIFO sources are rejected before a blocking open")

        fsync_source = external / "fsync.png"
        Image.new("RGB", (24, 24), (7, 8, 9)).save(fsync_source)
        real_fsync_directory = intake_module.fsync_directory

        def fail_originals_fsync(path):
            if Path(path) == fifo_session.project_dir / "source" / "originals":
                raise OSError("originals fsync test")
            return real_fsync_directory(path)

        with patch.object(intake_module, "fsync_directory", side_effect=fail_originals_fsync):
            try:
                import_source_copy(fifo_session, fsync_source)
            except OSError:
                pass
            else:
                raise AssertionError("renamed-copy fsync failure was ignored")
        require(
            not list((fifo_session.project_dir / "source" / "originals").glob("source_*-fsync.png")),
            "renamed copy escaped rollback tracking",
        )
        print("PASS: renamed copies enter rollback tracking before directory fsync")

        existing_temp = fifo_session.project_dir / "source" / "originals" / ".source-intake.tmp"
        existing_temp.write_bytes(b"occupied")
        try:
            intake_module._copy_and_hash(fsync_source, existing_temp)
        except FileExistsError:
            pass
        except OSError as exc:
            raise AssertionError(f"temporary-file error was masked: {exc}") from exc
        else:
            raise AssertionError("occupied temporary path was overwritten")
        existing_temp.unlink()
        print("PASS: temporary-target failure does not double-close the source descriptor")
        fifo_session.close()

        marker_session = ProjectSession(projects)
        marker_session.create_and_open("Crash Marker")
        marker_path = marker_session.project_dir / SOURCE_TRANSACTION_FILENAME
        marker_path.write_text('{"operation":"interrupted"}\n', encoding="utf-8")
        marker_project = marker_session.project_dir
        marker_session.close()
        recovery_session = ProjectSession(projects)
        recovery_state = recovery_session.open(marker_project)
        require(
            recovery_state.assessment.status is ProjectAccessStatus.READ_ONLY_RECOVERY,
            "interrupted transaction marker reopened writable",
        )
        recovery_session.close()
        print("PASS: interrupted transaction markers force read-only recovery on reopen")

        rollback_session = ProjectSession(projects)
        rollback_session.create_and_open("Rollback Poison")
        rollback_source = external / "rollback.png"
        Image.new("RGB", (28, 28), (10, 11, 12)).save(rollback_source)

        def persistent_manifest_failure(path, text):
            if Path(path).name == "project.json":
                raise OSError("persistent manifest failure")
            return real_atomic_write(path, text)

        with patch.object(
            intake_module, "atomic_write_text", side_effect=persistent_manifest_failure
        ):
            try:
                import_source_copy(rollback_session, rollback_source)
            except SourceIntakeError:
                pass
            else:
                raise AssertionError("unrecoverable rollback was ignored")
        require(not rollback_session.is_writable, "rollback failure retained writable authority")
        require(
            (rollback_session.project_dir / SOURCE_TRANSACTION_FILENAME).is_file(),
            "rollback failure removed its recovery marker",
        )
        rollback_session.close()
        print("PASS: rollback failure revokes writes and preserves recovery evidence")

    print("PASS: project source intake contract verified")


if __name__ == "__main__":
    main()
