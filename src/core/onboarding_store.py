#!/usr/bin/env python3
"""
Persistent onboarding/profile storage for MXZTAR Forge v2.0.
"""

import json
from datetime import datetime, timezone
from typing import Dict

from core.paths import (
    ONBOARDING_PROFILE_PATH,
    SETTINGS_NOTES_PATH,
    ensure_project_dirs,
)


DEFAULT_PROFILE = {
    "project_name": "MXZTAR Forge v2.0",
    "project_role": "Local creative-concept engineering forge",
    "creator_name": "",
    "brand_presence": "",
    "primary_goal": "Turn source art into structured concept-engineering outputs.",
    "workflow_focus": "source art → intelligence → concept brief → prompt pack → concept folder",
    "updated_utc": "",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_profile() -> Dict[str, str]:
    ensure_project_dirs()

    if not ONBOARDING_PROFILE_PATH.exists():
        return dict(DEFAULT_PROFILE)

    try:
        data = json.loads(ONBOARDING_PROFILE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return dict(DEFAULT_PROFILE)

    profile = dict(DEFAULT_PROFILE)
    for key, value in data.items():
        if key in profile:
            profile[key] = str(value)
    return profile


def save_profile(profile: Dict[str, str]) -> Dict[str, str]:
    ensure_project_dirs()

    clean = dict(DEFAULT_PROFILE)
    for key in clean:
        if key == "updated_utc":
            continue
        clean[key] = str(profile.get(key, clean[key])).strip()

    clean["updated_utc"] = utc_now()

    ONBOARDING_PROFILE_PATH.write_text(
        json.dumps(clean, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return clean


def load_settings_notes() -> str:
    ensure_project_dirs()

    if not SETTINGS_NOTES_PATH.exists():
        return (
            "Trust/workflow notes:\n"
            "- preserve working features before changes\n"
            "- no dead UI\n"
            "- long AI jobs must show elapsed time and activity\n"
            "- default local AI jobs use 2 CPU threads\n"
        )

    return SETTINGS_NOTES_PATH.read_text(encoding="utf-8")


def save_settings_notes(text: str) -> None:
    ensure_project_dirs()
    SETTINGS_NOTES_PATH.write_text(text.strip() + "\n", encoding="utf-8")
