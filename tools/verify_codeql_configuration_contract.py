#!/usr/bin/env python3
"""Verify the proven CodeQL Advanced workflow remains active and complete."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = PROJECT_ROOT / ".github" / "workflows" / "codeql.yml"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_text(text: str, expected: str, message: str) -> None:
    require(expected in text, message)


def main() -> int:
    require(WORKFLOW_PATH.is_file(), "CodeQL Advanced workflow is missing")
    workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

    require_text(
        workflow,
        'name: "CodeQL Advanced"',
        "CodeQL Advanced workflow has no stable identity",
    )
    require_text(workflow, "pull_request:", "CodeQL does not scan pull requests")
    require_text(workflow, "push:", "CodeQL does not scan main-branch pushes")
    require_text(
        workflow,
        "security-events: write",
        "CodeQL cannot upload security results",
    )
    require_text(workflow, "packages: read", "CodeQL cannot read required query packs")
    require_text(workflow, "actions: read", "CodeQL cannot inspect Actions workflows")
    require_text(workflow, "contents: read", "CodeQL cannot read repository contents")
    require_text(
        workflow,
        "- language: actions",
        "CodeQL does not scan GitHub Actions workflows",
    )
    require_text(
        workflow,
        "- language: python",
        "CodeQL does not scan Python",
    )
    require_text(workflow, "build-mode: none", "CodeQL no-build analysis is missing")
    require_text(
        workflow,
        "uses: github/codeql-action/init@v4",
        "CodeQL initialization action is missing",
    )
    require_text(
        workflow,
        "languages: ${{ matrix.language }}",
        "CodeQL language matrix is not connected to initialization",
    )
    require_text(
        workflow,
        "uses: github/codeql-action/analyze@v4",
        "CodeQL analysis action is missing",
    )
    require_text(
        workflow,
        'category: "/language:${{matrix.language}}"',
        "CodeQL result categories are not separated by language",
    )

    print("PASS: CodeQL Advanced scans pull requests and main-branch pushes")
    print("PASS: CodeQL Advanced analyzes both Actions workflows and Python")
    print("PASS: CodeQL initialization, analysis, permissions, and categories are intact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
