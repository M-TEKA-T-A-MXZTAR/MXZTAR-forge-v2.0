#!/usr/bin/env python3
"""
Probe MXZTAR-forge agent runner.

Purpose:
- run one safe vision workflow
- save a JSON output record
- verify output path exists
"""

from pathlib import Path

from core.agent_runner import run_agent_job


def main() -> int:
    source_path = Path("workspace/test_inputs/mxztar_test_shapes.png")

    print("MXZTAR-forge Agent Runner Probe")
    print(f"Source: {source_path}")
    print("Workflow: source_art_intelligence")
    print()

    result, out_path = run_agent_job(
        source_path=source_path,
        workflow_key="source_art_intelligence",
        user_notes="Small synthetic test image. Keep output concise.",
    )

    print("OK:", result.ok)
    print("Model:", result.model)
    print("Output path:", out_path)

    if result.error:
        print()
        print("ERROR:")
        print(result.error)

    if result.output_text:
        print()
        print("OUTPUT PREVIEW:")
        print(result.output_text[:1200])

    if not out_path.exists():
        print()
        print("FAIL: output JSON was not created.")
        return 1

    print()
    print("PASS: output JSON exists.")

    if not result.ok:
        print("FAIL: agent result was not OK.")
        return 1

    print("PASS: agent runner completed and saved output.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
