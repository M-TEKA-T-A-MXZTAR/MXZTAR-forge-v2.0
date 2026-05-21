#!/usr/bin/env python3
"""
Verify MXZTAR-forge prompt contracts.
"""

from brain.prompts import WORKFLOW_PROMPTS, build_prompt


REQUIRED_WORKFLOWS = [
    "source_art_intelligence",
    "modular_set_perspective",
    "prototype_imagination",
    "shape_structure_harvest",
    "concept_brief",
    "render_prompt_pack",
    "recommend_next_step",
]


def main() -> int:
    print("MXZTAR-forge Prompt Contract Verification")
    print()

    missing = [key for key in REQUIRED_WORKFLOWS if key not in WORKFLOW_PROMPTS]

    if missing:
        print("FAIL: missing workflows")
        for key in missing:
            print(f"- {key}")
        return 1

    print(f"PASS: workflow count = {len(WORKFLOW_PROMPTS)}")

    for key in REQUIRED_WORKFLOWS:
        prompt = build_prompt(key, "/tmp/test.png")
        if key not in prompt:
            print(f"FAIL: workflow key not found in built prompt: {key}")
            return 1
        print(f"PASS: {key}")

    print()
    print("PASS: all required prompt contracts build successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
