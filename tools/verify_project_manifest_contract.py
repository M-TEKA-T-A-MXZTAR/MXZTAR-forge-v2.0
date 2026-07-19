#!/usr/bin/env python3
"""Verify the core-only project skeleton and manifest foundation."""

from __future__ import annotations

import json
import copy
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from core import project_manifest as project_module  # noqa: E402
from core.project_manifest import (  # noqa: E402
    PROJECT_DIRS,
    PROJECT_SCHEMA,
    ProjectManifestError,
    create_project,
    load_project_manifest,
    project_slug,
    validate_manifest,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="mxztar-project-") as temp_dir:
        projects_root = Path(temp_dir) / "projects"
        fsynced_directories = []
        original_fsync_directory = project_module.fsync_directory

        def tracked_fsync_directory(path):
            fsynced_directories.append(Path(path))
            original_fsync_directory(path)

        project_module.fsync_directory = tracked_fsync_directory
        try:
            project_dir, created = create_project(
                "Lunar Forest #1",
                primary_goal="Build a modular settlement.",
                projects_root=projects_root,
                application_version="test",
            )
        finally:
            project_module.fsync_directory = original_fsync_directory

        require(project_dir == projects_root / "lunar-forest-1", "project slug/path is unstable")
        require(created["schema_name"] == PROJECT_SCHEMA, "project schema is wrong")
        require(created["project_id"].startswith("project_"), "project ID is missing")
        require(created["primary_goal"] == "Build a modular settlement.", "goal was lost")
        require((project_dir / "project.json").is_file(), "manifest was not written")
        require((project_dir / "README.md").is_file(), "project README was not written")
        for relative in PROJECT_DIRS:
            require((project_dir / relative).is_dir(), f"project directory missing: {relative}")

        loaded = load_project_manifest(project_dir)
        require(loaded == created, "saved manifest differs from validated creation result")
        history = (project_dir / loaded["history_path"]).read_text(encoding="utf-8").splitlines()
        require(len(history) == 1, "project creation history is not singular")
        event = json.loads(history[0])
        require(event["event"] == "project_created", "project creation event is missing")
        require(event["project_id"] == created["project_id"], "history project ID drifted")
        require(not list(project_dir.rglob("*.tmp")), "atomic write left temporary files")
        require(not list(projects_root.glob(".*.creating-*")), "staging directory leaked")
        require(projects_root in fsynced_directories, "projects directory entry was not fsynced")

        try:
            create_project("Lunar Forest #1", projects_root=projects_root)
            raise RuntimeError("existing project was overwritten")
        except FileExistsError:
            pass

        for invalid_name in ("", "---", "../../../"):
            try:
                project_slug(invalid_name)
                raise RuntimeError(f"unsafe project name accepted: {invalid_name!r}")
            except ProjectManifestError:
                pass

        require(project_slug("Māori Whenua") == "māori-whenua", "Māori slug was distorted")
        require(project_slug("中文 项目") == "中文-项目", "international slug was rejected")

        for missing_key in ("primary_goal", "last_recommendation_artifact_id"):
            damaged = copy.deepcopy(created)
            damaged.pop(missing_key)
            try:
                validate_manifest(damaged)
                raise RuntimeError(f"manifest missing {missing_key} was accepted")
            except ProjectManifestError:
                pass

        for unsafe_history in ("/tmp/history.jsonl", "../../outside.jsonl"):
            damaged = copy.deepcopy(created)
            damaged["history_path"] = unsafe_history
            try:
                validate_manifest(damaged)
                raise RuntimeError(f"unsafe history path accepted: {unsafe_history}")
            except ProjectManifestError:
                pass

        gitignore = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8")
        require("workspace/projects/" in gitignore, "runtime projects are not Git-ignored")

        malformed = projects_root / "malformed"
        malformed.mkdir()
        (malformed / "project.json").write_text("{bad", encoding="utf-8")
        try:
            load_project_manifest(malformed)
            raise RuntimeError("malformed project manifest was accepted")
        except ProjectManifestError:
            pass

        print("PASS: canonical project directory tree is created")
        print("PASS: stable project identity and intent are durable")
        print("PASS: project manifest and initial history validate after reload")
        print("PASS: atomic writes leave no temporary files")
        print("PASS: existing projects cannot be overwritten")
        print("PASS: unsafe names and malformed manifests are rejected")
        print("PASS: Māori and international project names retain Unicode letters")
        print("PASS: contracted state fields and project-contained history are enforced")
        print("PASS: project and file directory entries are fsynced")
        print("PASS: private runtime projects are Git-ignored")
        print("PASS: core project manifest foundation verified")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
