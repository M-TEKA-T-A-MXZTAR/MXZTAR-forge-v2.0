#!/usr/bin/env python3
"""Verify validated project opening and the single-writer boundary."""

from __future__ import annotations

import json
import os
import socket
import tempfile
from pathlib import Path

from core import project_access as access_module

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
    identity = access_module.process_identity(process_id)
    boot_id, process_start_id = identity if identity is not None else (None, None)
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
                "acquisition_id": "lock_test",
                "boot_id": boot_id,
                "process_start_id": process_start_id,
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

        foreign = ProjectLockLease(
            project_dir, "writer_foreign", os.getpid(), socket.gethostname(), "lock_foreign"
        )
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

        first = acquire_project_lock(project_dir, "writer_reused")
        release_project_lock(first)
        second = acquire_project_lock(project_dir, "writer_reused")
        try:
            release_project_lock(first)
        except ProjectAccessError:
            pass
        else:
            raise AssertionError("old lease released a new lock incarnation")
        require((project_dir / LOCK_FILENAME).exists(), "old lease removed the current lock")
        release_project_lock(second)
        print("PASS: lock incarnation tokens reject delayed stale leases")

        original_fsync = access_module.fsync_directory
        access_module.fsync_directory = lambda _path: (_ for _ in ()).throw(OSError("fsync test"))
        try:
            try:
                acquire_project_lock(project_dir, "writer_failed")
            except OSError:
                pass
            else:
                raise AssertionError("injected acquisition failure was ignored")
        finally:
            access_module.fsync_directory = original_fsync
        require(not (project_dir / LOCK_FILENAME).exists(), "failed acquisition leaked its lock")
        print("PASS: failed acquisition removes only its owned lock file")

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

        oversized_integer = project_dir / LOCK_FILENAME
        oversized_integer.write_text('{"process_id":' + "9" * 5000 + "}", encoding="utf-8")
        require(
            assess_project_open(project_dir).status is ProjectAccessStatus.READ_ONLY_RECOVERY,
            "oversized integer escaped malformed-lock containment",
        )
        oversized_integer.unlink()
        print("PASS: oversized-integer JSON is contained as read-only recovery")

        fifo = project_dir / LOCK_FILENAME
        os.mkfifo(fifo)
        require(
            assess_project_open(project_dir).status is ProjectAccessStatus.READ_ONLY_RECOVERY,
            "non-regular lock was accepted",
        )
        fifo.unlink()
        print("PASS: non-regular lock objects cannot block project opening")

        foreign_path = write_lock(project_dir, process_id=os.getpid(), host="another-host")
        require(assess_project_open(project_dir).status is ProjectAccessStatus.LOCKED, "foreign host lock ignored")
        foreign_path.unlink()
        print("PASS: an unverifiable foreign-host writer remains locked")

        recycled_path = write_lock(project_dir, process_id=os.getpid())
        recycled_payload = json.loads(recycled_path.read_text(encoding="utf-8"))
        recycled_payload["process_start_id"] = "recycled-process-start"
        recycled_path.write_text(json.dumps(recycled_payload), encoding="utf-8")
        require(
            assess_project_open(project_dir).status is ProjectAccessStatus.READ_ONLY_RECOVERY,
            "recycled PID was classified as an active writer",
        )
        recycled_path.unlink()
        print("PASS: boot and process-start identity detect recycled PIDs")

        try:
            acquire_project_lock(project_dir, "x" * 257)
        except ProjectAccessError:
            pass
        else:
            raise AssertionError("oversized writer ID was accepted")
        require(not (project_dir / LOCK_FILENAME).exists(), "oversized writer created a lock")
        print("PASS: writer IDs cannot create unreadable oversized locks")

        parent_lease = acquire_project_lock(project_dir, "writer_parent")
        original_getpid = access_module.os.getpid
        access_module.os.getpid = lambda: parent_lease.process_id + 1
        try:
            try:
                release_project_lock(parent_lease)
            except ProjectAccessError:
                pass
            else:
                raise AssertionError("non-owning process released the lock")
        finally:
            access_module.os.getpid = original_getpid
        require((project_dir / LOCK_FILENAME).exists(), "non-owning process removed the lock")
        release_project_lock(parent_lease)
        print("PASS: a forked child cannot release its parent's lock")

        symlink_dir, _ = create_project("Symlink Structure", projects_root=root)
        source_dir = symlink_dir / "source"
        source_real = symlink_dir / "source-real"
        source_dir.rename(source_real)
        source_dir.symlink_to(source_real, target_is_directory=True)
        require(
            assess_project_open(symlink_dir).status is ProjectAccessStatus.READ_ONLY_RECOVERY,
            "intermediate canonical symlink was writable",
        )
        print("PASS: every canonical path component rejects symbolic links")

        manifest_link_dir, _ = create_project("Symlink Manifest", projects_root=root)
        manifest_path = manifest_link_dir / "project.json"
        manifest_real = manifest_link_dir / "project-real.json"
        manifest_path.rename(manifest_real)
        manifest_path.symlink_to(manifest_real)
        require(
            assess_project_open(manifest_link_dir).status is ProjectAccessStatus.READ_ONLY_RECOVERY,
            "symlinked manifest was followed",
        )
        print("PASS: project manifests are never loaded through symbolic links")

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
