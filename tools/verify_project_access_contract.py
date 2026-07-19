#!/usr/bin/env python3
"""Verify validated project opening and the single-writer boundary."""

from __future__ import annotations

import json
import os
import socket
import tempfile
from pathlib import Path

from core.project_access import (
    LOCK_FILENAME,
    LOCK_SCHEMA,
    LOCK_SCHEMA_VERSION,
    ProjectAccessError,
    ProjectAccessStatus,
    ProjectLockLease,
    ProjectLockedError,
    acquire_project_lock,
    assess_project_open,
    release_project_lock,
)
from core.project_manifest import create_project


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def write_lock(project_dir: Path, *, process_id: int, host: str | None = None) -> Path:
    path = project_dir / LOCK_FILENAME
    path.write_text(
        json.dumps(
            {
                "lock_schema": LOCK_SCHEMA,
                "lock_schema_version": LOCK_SCHEMA_VERSION,
                "writer_id": "writer_test",
                "process_id": process_id,
                "created_at_utc": "2026-07-20T00:00:00+00:00",
                "host": host or socket.gethostname(),
            }
        ),
        encoding="utf-8",
    )
    return path


def main() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        project_dir, _ = create_project("Access Contract", projects_root=root)

        assessment = assess_project_open(project_dir)
        require(assessment.status is ProjectAccessStatus.WRITABLE, "valid project should be writable")
        lease = acquire_project_lock(project_dir, "writer_contract")
        locked = assess_project_open(project_dir)
        require(locked.status is ProjectAccessStatus.LOCKED, "active writer should classify locked")
        try:
            acquire_project_lock(project_dir, "writer_second")
        except ProjectLockedError:
            pass
        else:
            raise AssertionError("second writer was accepted")
        print("PASS: one active writer is enforced by an exclusive project lock")

        foreign = ProjectLockLease(project_dir, "writer_foreign", os.getpid(), socket.gethostname())
        try:
            release_project_lock(foreign)
        except ProjectAccessError:
            pass
        else:
            raise AssertionError("foreign writer released the lock")
        require((project_dir / LOCK_FILENAME).exists(), "foreign release removed the lock")
        release_project_lock(lease)
        require(assess_project_open(project_dir).status is ProjectAccessStatus.WRITABLE, "release failed")
        print("PASS: only the owning lease can release a project lock")

        stale_path = write_lock(project_dir, process_id=999_999_999)
        stale = assess_project_open(project_dir)
        require(stale.status is ProjectAccessStatus.READ_ONLY_RECOVERY, "stale lock not recovered read-only")
        require(stale_path.exists(), "stale lock was silently removed")
        stale_path.unlink()
        print("PASS: stale locks are preserved and classified read-only recovery")

        malformed = project_dir / LOCK_FILENAME
        malformed.write_text("{not-json", encoding="utf-8")
        uncertain = assess_project_open(project_dir)
        require(uncertain.status is ProjectAccessStatus.READ_ONLY_RECOVERY, "malformed lock not contained")
        require(malformed.read_text(encoding="utf-8") == "{not-json", "malformed lock changed")
        malformed.unlink()
        print("PASS: malformed locks are preserved without silent repair")

        foreign_path = write_lock(project_dir, process_id=os.getpid(), host="another-host")
        require(assess_project_open(project_dir).status is ProjectAccessStatus.LOCKED, "foreign host lock ignored")
        foreign_path.unlink()
        print("PASS: an unverifiable foreign-host writer remains locked")

        missing_dir, _ = create_project("Missing Structure", projects_root=root)
        (missing_dir / "source" / "originals").rmdir()
        require(
            assess_project_open(missing_dir).status is ProjectAccessStatus.READ_ONLY_RECOVERY,
            "missing canonical directory was writable",
        )
        print("PASS: incomplete project structure opens read-only recovery")

        corrupt_dir, _ = create_project("Corrupt Manifest", projects_root=root)
        manifest_path = corrupt_dir / "project.json"
        original = manifest_path.read_text(encoding="utf-8")
        manifest_path.write_text("[]", encoding="utf-8")
        require(
            assess_project_open(corrupt_dir).status is ProjectAccessStatus.READ_ONLY_RECOVERY,
            "corrupt manifest was writable",
        )
        require(manifest_path.read_text(encoding="utf-8") == "[]", "corrupt manifest changed")
        require(original != "[]", "test fixture was invalid")
        print("PASS: invalid manifests are reported without mutation")

    print("PASS: project access and locking contract verified")


if __name__ == "__main__":
    main()
