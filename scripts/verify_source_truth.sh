#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

echo "=== MXZTAR-FORGE SOURCE TRUTH VERIFY ==="

echo
echo "=== REQUIRED DOCS ==="
for f in \
  README.md \
  docs/SOURCE_OF_TRUTH.md \
  docs/NZ_COMPLIANCE_AND_SUBSCRIPTION_NOTES.md \
  docs/CODING_PRACTICE_PRINCIPLES.md \
  docs/product/FIRST_RENTABLE_RELEASE.md \
  docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md \
  docs/product/OUTPUT_ARTIFACT_CONTRACTS.md \
  docs/product/MASTER_BUILD_PLAN.md \
  docs/product/FUTURE_CONSTRUCT_AND_WORLD_VISION.md \
  docs/product/LEVEL_FOUR_PLATFORM_PRIORITIES.md \
  docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md \
  docs/PROGRESS_LEDGER.md
do
  if [ -f "$f" ]; then
    echo "PASS FILE: $f"
  else
    echo "FAIL FILE: $f (missing)" >&2
    exit 1
  fi
done

echo
echo "=== PYTHON COMPILE CHECK ==="
if [ -x ".venv/bin/python" ]; then
  PYTHON_EXECUTABLE=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_EXECUTABLE="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYTHON_EXECUTABLE="$(command -v python)"
else
  echo "FAIL: Python 3 is required; create .venv or install python3." >&2
  exit 1
fi

PYTHONPATH=src "$PYTHON_EXECUTABLE" -m py_compile \
  src/brain/prompts.py \
  src/brain/service.py \
  src/core/agent_runner.py \
  src/core/editor_project_access.py \
  src/core/job_records.py \
  src/core/project_access.py \
  src/core/project_manifest.py \
  src/core/project_session.py \
  src/core/project_source_intake.py \
  src/core/project_workflow_run.py \
  src/core/shape_document.py \
  src/core/source_library.py \
  src/mxztar_forge.py \
  src/qt_app.py \
  src/qt_editor_app.py \
  src/qt_panels/__init__.py \
  src/qt_panels/agent_panel.py \
  src/qt_panels/agent_worker.py \
  src/qt_panels/editor_panel.py \
  src/qt_panels/jobs_panel.py \
  src/qt_panels/my_library_panel.py \
  src/qt_panels/shape_library_panel.py \
  src/qt_panels/start_here_panel.py \
  tools/verify_agent_panel_execution_contract.py \
  tools/verify_jobs_panel_contract.py \
  tools/verify_launcher_import_contract.py \
  tools/verify_project_source_intake_ui_contract.py \
  tools/verify_project_workflow_run_contract.py \
  tools/verify_shape_document_editor_contract.py

echo "PASS: listed Python files compile"

echo
echo "=== LAUNCHER IMPORT CONTRACT ==="
PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_launcher_import_contract.py

echo
echo "=== PROMPT CONTRACT CHECK ==="
PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_prompts.py

echo
echo "=== SOURCE TRUTH VERIFY COMPLETE ==="
