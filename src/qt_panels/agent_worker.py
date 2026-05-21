from __future__ import annotations

from PySide6.QtCore import QObject, Signal, Slot

from core.agent_runner import run_agent_job


class AgentWorker(QObject):
    """
    Runs one MXZTAR-forge agent workflow outside the Qt main thread.

    This worker exists to protect the UI from freezing while a local Ollama
    vision workflow is running. It performs exactly one job, emits progress,
    then reports either the saved output path or an error message.
    """

    progress = Signal(str)
    finished = Signal(bool, str, str)

    def __init__(
        self,
        workflow_key: str,
        source_path: str,
        user_notes: str = "",
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self.workflow_key = workflow_key
        self.source_path = source_path
        self.user_notes = user_notes

    @Slot()
    def run(self) -> None:
        self.progress.emit("Starting agent workflow.")
        self.progress.emit(f"Workflow: {self.workflow_key}")
        self.progress.emit(f"Source: {self.source_path}")

        try:
            self.progress.emit("Calling local agent runner.")
            output_path = run_agent_job(
                workflow_key=self.workflow_key,
                source_path=self.source_path,
                user_notes=self.user_notes,
            )

            self.progress.emit("Agent workflow completed.")
            self.progress.emit(f"Saved output: {output_path}")
            self.finished.emit(True, str(output_path), "")

        except Exception as exc:
            message = f"{type(exc).__name__}: {exc}"
            self.progress.emit(f"Agent workflow failed: {message}")
            self.finished.emit(False, "", message)
