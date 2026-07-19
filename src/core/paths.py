#!/usr/bin/env python3
"""
MXZTAR Forge v2.0 path registry.

Centralizes project paths so panels and engines do not hard-code folders.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"
ASSETS_ROOT = PROJECT_ROOT / "assets"

INPUT_DIR = WORKSPACE_ROOT / "input"
IMPORTS_DIR = WORKSPACE_ROOT / "imports"
TEST_INPUTS_DIR = WORKSPACE_ROOT / "test_inputs"

OUTPUT_DIR = WORKSPACE_ROOT / "output"
CONCEPT_FOLDERS_DIR = OUTPUT_DIR / "concept_folders"

DATA_DIR = WORKSPACE_ROOT / "data"
USER_PROFILE_DIR = DATA_DIR / "user_profile"
BRAIN_DATA_DIR = DATA_DIR / "brain"

SOURCE_ART_INTELLIGENCE_DIR = BRAIN_DATA_DIR / "source_art_intelligence"
CONCEPT_BRIEFS_DIR = BRAIN_DATA_DIR / "concept_briefs"
RENDER_PROMPT_PACKS_DIR = BRAIN_DATA_DIR / "render_prompt_packs"

MY_PROMPTS_DIR = DATA_DIR / "my_prompts"
WEB_COPY_DRAFTS_DIR = DATA_DIR / "web_copy_drafts"
DESIGN_ENGINE_STAGING_DIR = DATA_DIR / "design_engine_staging"
MIGRATION_DIR = DATA_DIR / "migration"

LOGS_DIR = WORKSPACE_ROOT / "logs"
CACHE_DIR = WORKSPACE_ROOT / "cache"
SOURCE_PREVIEW_CACHE_DIR = CACHE_DIR / "source_previews"

ONBOARDING_PROFILE_PATH = USER_PROFILE_DIR / "onboarding_profile.json"
SETTINGS_NOTES_PATH = USER_PROFILE_DIR / "settings_notes.txt"


def ensure_project_dirs() -> None:
    """Create the standard MXZTAR Forge folders if missing."""
    for path in [
        INPUT_DIR,
        IMPORTS_DIR,
        TEST_INPUTS_DIR,
        CONCEPT_FOLDERS_DIR,
        USER_PROFILE_DIR,
        SOURCE_ART_INTELLIGENCE_DIR,
        CONCEPT_BRIEFS_DIR,
        RENDER_PROMPT_PACKS_DIR,
        MY_PROMPTS_DIR,
        WEB_COPY_DRAFTS_DIR,
        DESIGN_ENGINE_STAGING_DIR,
        MIGRATION_DIR,
        LOGS_DIR,
        SOURCE_PREVIEW_CACHE_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)
