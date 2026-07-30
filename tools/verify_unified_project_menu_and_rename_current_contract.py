#!/usr/bin/env python3
"""Run the PR #71 verifier with the restored Select Project action included."""

from __future__ import annotations

import verify_unified_project_menu_and_rename_contract as base_contract


base_contract.EXPECTED_ACTIONS = [
    "Select Project…",
    "Switch Project…",
    "New Project + Document…",
    "Rename Selected Project…",
    "Delete Selected Project…",
]


if __name__ == "__main__":
    raise SystemExit(base_contract.main())
