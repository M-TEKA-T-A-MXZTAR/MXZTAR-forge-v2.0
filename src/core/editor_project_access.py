#!/usr/bin/env python3
"""Project-open guard for interrupted native editor transactions."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from core.project_access import (
    ProjectAccessStatus,
    ProjectOpenAssessment,
    assess_project_open as assess_base_project_open,
)


EDITOR_TRANSACTION_FILENAME = ".mxztar-editor-transaction.json"


def assess_project_open(project_dir: Path) -> ProjectOpenAssessment:
    """Preserve editor interruption evidence without hiding an active writer lock."""
    assessment = assess_base_project_open(project_dir)
    marker = assessment.project_dir / EDITOR_TRANSACTION_FILENAME
    if not marker.exists() and not marker.is_symlink():
        return assessment
    diagnostic = "An interrupted editor transaction requires explicit read-only recovery."
    status = (
        ProjectAccessStatus.READ_ONLY_RECOVERY
        if assessment.status is ProjectAccessStatus.WRITABLE
        else assessment.status
    )
    return replace(
        assessment,
        status=status,
        diagnostics=assessment.diagnostics + (diagnostic,),
    )
