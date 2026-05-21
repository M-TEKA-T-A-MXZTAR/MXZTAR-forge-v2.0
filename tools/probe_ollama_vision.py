#!/usr/bin/env python3
"""
Probe MXZTAR-forge vision workflow service with a small test image.
"""

from pathlib import Path

from brain.service import run_vision_workflow


def main() -> int:
    source_path = Path("workspace/test_inputs/mxztar_test_shapes.png")

    print("MXZTAR-forge Vision Service Probe")
    print(f"Source: {source_path}")
    print("Workflow: source_art_intelligence")
    print()

    result = run_vision_workflow(
        source_path=source_path,
        workflow_key="source_art_intelligence",
        user_notes="This is a small synthetic test image. Keep the response concise.",
        timeout_seconds=300,
    )

    print("OK:", result.ok)
    print("Model:", result.model)
    print("Workflow:", result.workflow_key)

    if result.error:
        print()
        print("ERROR:")
        print(result.error)

    if result.output_text:
        print()
        print("OUTPUT:")
        print(result.output_text[:2000])

    if not result.ok:
        return 1

    print()
    print("PASS: vision workflow service responded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
