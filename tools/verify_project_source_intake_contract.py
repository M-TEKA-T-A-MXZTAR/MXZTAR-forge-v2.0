#!/usr/bin/env python3
"""Verify copy-only project source intake and processed transition."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from core import project_source_intake as intake_module
from core.project_session import ProjectSession, ProjectSessionError
from core.project_source_intake import (
    SourceIntakeError,
    import_source_copy,
    mark_source_processed,
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
        print("PASS: source intake copies bytes, hashes identity, and creates a bounded preview")

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

    print("PASS: project source intake contract verified")


if __name__ == "__main__":
    main()
