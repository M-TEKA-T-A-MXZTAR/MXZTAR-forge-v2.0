from __future__ import annotations

from PySide6.QtCore import QObject, Signal, Slot

from core.agent_runner import run_agent_job
from core.project_workflow_run import run_project_agent_job


class AgentWorker(QObject):
    """
    Runs one MXZTAR-forge agent workflow outside the Qt main thread.

    This worker exists to protect the UI from freezing while a local Ollama
    vision workflow is running. It performs exactly one job, emits progress,
    then reports the saved output/diagnostic path and the true AgentResult
    success state.
    """

    progress = Signal(str)
    finished = Signal(bool, str, str)

    def __init__(
        self,
        workflow_key: str,
        source_path: str,
        user_notes: str = "",
        project_session=None,
        source_item=None,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self.workflow_key = workflow_key
        self.source_path = source_path
        self.user_notes = user_notes
        self.project_session = project_session
        self.source_item = source_item

    @Slot()
    def run(self) -> None:
        self.progress.emit("Starting agent workflow.")
        self.progress.emit(f"Workflow: {self.workflow_key}")
        self.progress.emit(f"Source: {self.source_path}")

        try:
            self.progress.emit("Calling local agent runner.")
            if self.project_session is not None and self.source_item is not None:
                project_run = run_project_agent_job(
                    session=self.project_session,
                    source=self.source_item,
                    workflow_key=self.workflow_key,
                    user_notes=self.user_notes,
                )
                result = project_run.agent_result
                output_path = project_run.evidence_path
                self.progress.emit(
                    "Saved project-owned model-run evidence; structured findings remain unvalidated."
                )
            else:
                result, output_path = run_agent_job(
                    workflow_key=self.workflow_key,
                    source_path=self.source_path,
                    user_notes=self.user_notes,
                )

            self.progress.emit(f"Saved output record: {output_path}")

            if result.ok:
                self.progress.emit("Agent workflow completed successfully.")
                self.finished.emit(True, str(output_path), "")
                return

            message = result.error or "Agent workflow returned an unsuccessful result."
            self.progress.emit(f"Agent workflow returned failure: {message}")
            self.finished.emit(False, str(output_path), message)

        except Exception as exc:
            message = f"{type(exc).__name__}: {exc}"
            self.progress.emit(f"Agent workflow failed before saving a result: {message}")
            self.finished.emit(False, "", message)
