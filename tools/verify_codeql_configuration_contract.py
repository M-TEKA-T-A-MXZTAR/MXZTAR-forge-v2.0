#!/usr/bin/env python3
"""Verify that Forge runs genuine CodeQL analysis on every relevant change."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = PROJECT_ROOT / ".github" / "workflows" / "codeql.yml"
CONFIG_PATH = PROJECT_ROOT / ".github" / "codeql" / "codeql-config.yml"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_text(text: str, expected: str, message: str) -> None:
    require(expected in text, message)


def main() -> int:
    require(WORKFLOW_PATH.is_file(), "CodeQL workflow is missing")
    require(CONFIG_PATH.is_file(), "CodeQL configuration is missing")

    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
    config = CONFIG_PATH.read_text(encoding="utf-8")

    require_text(workflow, "name: CodeQL", "CodeQL workflow has no stable identity")
    require_text(workflow, "pull_request:", "CodeQL does not scan pull requests")
    require_text(workflow, "push:", "CodeQL does not scan main-branch pushes")
    require_text(workflow, "security-events: write", "CodeQL cannot upload security results")
    require_text(
        workflow,
        "uses: github/codeql-action/init@v4",
        "CodeQL initialization action is missing",
    )
    require_text(workflow, "languages: python", "CodeQL does not explicitly scan Python")
    require_text(
        workflow,
        "config-file: ./.github/codeql/codeql-config.yml",
        "CodeQL workflow is not connected to the repository configuration",
    )
    require_text(
        workflow,
        "uses: github/codeql-action/analyze@v4",
        "CodeQL analysis action is missing",
    )

    require_text(config, "paths:", "CodeQL configuration has no included source paths")
    require_text(config, "  - src", "CodeQL configuration does not include src")
    require_text(config, "  - tools", "CodeQL configuration does not include tools")
    require_text(config, "uses: security-extended", "Extended security queries are missing")
    require_text(
        config,
        "uses: security-and-quality",
        "Security-and-quality queries are missing",
    )

    print("PASS: CodeQL workflow exists and loads the repository configuration")
    print("PASS: pull requests and main-branch pushes receive genuine Python CodeQL analysis")
    print("PASS: CodeQL configuration includes Forge source and extended query suites")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
