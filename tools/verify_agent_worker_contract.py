#!/usr/bin/env python3
"""
Verify AgentWorker success/failure signalling.

This verifier does not call Ollama. It monkeypatches the imported
`run_agent_job` function inside `qt_panels.agent_worker` so the worker contract
can be tested deterministically.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from qt_panels import agent_worker as agent_worker_module  # noqa: E402
from qt_panels.agent_worker import AgentWorker  # noqa: E402


@dataclass
class FakeAgentResult:
    ok: bool
    model: str = "fake-model"
    workflow_key: str = "source_art_intelligence"
    source_path: str = "fake-source.png"
    output_text: str = ""
    error: str = ""


FinishedSignal = Tuple[bool, str, str]


def run_worker_with(fake_runner: Callable[..., Tuple[FakeAgentResult, Path]]) -> Tuple[List[str], List[FinishedSignal]]:
    original_runner = agent_worker_module.run_agent_job
    progress_messages: List[str] = []
    finished_signals: List[FinishedSignal] = []

    agent_worker_module.run_agent_job = fake_runner

    try:
        worker = AgentWorker(
            workflow_key="source_art_intelligence",
            source_path="workspace/test_inputs/fake.png",
            user_notes="contract verifier",
        )
        worker.progress.connect(progress_messages.append)
        worker.finished.connect(lambda ok, path, error: finished_signals.append((ok, path, error)))
        worker.run()
    finally:
        agent_worker_module.run_agent_job = original_runner

    return progress_messages, finished_signals


def assert_single_finished(finished_signals: List[FinishedSignal]) -> FinishedSignal:
    if len(finished_signals) != 1:
        raise AssertionError(f"Expected exactly one finished signal, got {len(finished_signals)}")
    return finished_signals[0]


def verify_success_path() -> None:
    def fake_runner(**_: object) -> Tuple[FakeAgentResult, Path]:
        return FakeAgentResult(ok=True), Path("workspace/data/brain/source_art_intelligence/success.json")

    progress, finished = run_worker_with(fake_runner)
    ok, path, error = assert_single_finished(finished)

    assert ok is True
    assert path.endswith("success.json")
    assert error == ""
    assert any("completed successfully" in message for message in progress)

    print("PASS: success result emits success with saved path")


def verify_saved_failure_path() -> None:
    def fake_runner(**_: object) -> Tuple[FakeAgentResult, Path]:
        return (
            FakeAgentResult(
                ok=False,
                error="Could not reach Ollama HTTP API: 400 Client Error",
            ),
            Path("workspace/data/brain/source_art_intelligence/failure.json"),
        )

    progress, finished = run_worker_with(fake_runner)
    ok, path, error = assert_single_finished(finished)

    assert ok is False
    assert path.endswith("failure.json")
    assert "400 Client Error" in error
    assert any("returned failure" in message for message in progress)

    print("PASS: saved failure result emits failure with diagnostic path")


def verify_exception_path() -> None:
    def fake_runner(**_: object) -> Tuple[FakeAgentResult, Path]:
        raise RuntimeError("simulated runner explosion")

    progress, finished = run_worker_with(fake_runner)
    ok, path, error = assert_single_finished(finished)

    assert ok is False
    assert path == ""
    assert "RuntimeError" in error
    assert "simulated runner explosion" in error
    assert any("failed before saving" in message for message in progress)

    print("PASS: exception before saved result emits failure without path")


def main() -> int:
    print("MXZTAR-forge AgentWorker Contract Verification")
    verify_success_path()
    verify_saved_failure_path()
    verify_exception_path()
    print("PASS: AgentWorker contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
