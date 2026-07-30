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
  docs/product/ASSET_GENERATION_AND_CONSTRUCT_ARCHITECTURE.md \
  docs/product/CURRENT_CAPABILITY_BOUNDARY.md \
  docs/product/EDITOR_DOCUMENT_LIFECYCLE_CORRECTION.md \
  docs/product/VISIBLE_DELETION_AND_EDITOR_ENTRY_CORRECTION.md \
  docs/product/UNIFIED_PROJECT_MENU_AND_RENAME.md \
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
  src/core/object_scene.py \
  src/core/object_scene_membership.py \
  src/core/positioning_guides.py \
  src/core/project_access.py \
  src/core/project_authoring_workflow.py \
  src/core/project_manifest.py \
  src/core/project_rename.py \
  src/core/project_session.py \
  src/core/project_source_intake.py \
  src/core/project_trash.py \
  src/core/project_workflow_run.py \
  src/core/shape_document.py \
  src/core/shape_document_deletion.py \
  src/core/source_library.py \
  src/mxztar_forge.py \
  src/qt_app.py \
  src/qt_editor_app.py \
  src/qt_editor_authoring_app.py \
  src/qt_editor_usability_app.py \
  src/qt_live_acceptance_guards.py \
  src/qt_project_menu_and_rename.py \
  src/qt_project_menu_review_fixes.py \
  src/qt_panels/__init__.py \
  src/qt_panels/agent_panel.py \
  src/qt_panels/agent_worker.py \
  src/qt_panels/editor_authoring_panel.py \
  src/qt_panels/editor_authority_guard.py \
  src/qt_panels/editor_panel.py \
  src/qt_panels/editor_usability_panel.py \
  src/qt_panels/editor_wheel_controls.py \
  src/qt_panels/jobs_panel.py \
  src/qt_panels/my_library_panel.py \
  src/qt_panels/object_cad_panel.py \
  src/qt_panels/positioning_guides.py \
  src/qt_panels/shape_library_panel.py \
  src/qt_panels/start_here_panel.py \
  tools/verify_agent_panel_execution_contract.py \
  tools/verify_codeql_configuration_contract.py \
  tools/verify_document_lifecycle_and_static_guidance_contract.py \
  tools/verify_documentation_runtime_state_contract.py \
  tools/verify_sticky_editor_options_documentation_contract.py \
  tools/verify_editor_mouse_wheel_contract.py \
  tools/verify_editor_project_authoring_contract.py \
  tools/verify_editor_single_object_workspace_contract.py \
  tools/verify_jobs_panel_contract.py \
  tools/verify_launcher_import_contract.py \
  tools/verify_object_cad_contract.py \
  tools/verify_persistent_options_and_project_trash_contract.py \
  tools/verify_positioning_guides_contract.py \
  tools/verify_project_birth_contract.py \
  tools/verify_project_session_contract.py \
  tools/verify_project_source_intake_ui_contract.py \
  tools/verify_project_workflow_run_contract.py \
  tools/verify_select_project_restoration_contract.py \
  tools/verify_shape_document_editor_contract.py \
  tools/verify_unified_project_menu_and_rename_contract.py \
  tools/verify_unified_project_menu_and_rename_current_contract.py \
  tools/verify_visible_deletion_and_editor_entry_contract.py

echo "PASS: listed Python files compile"

echo
echo "=== DOCUMENTATION RUNTIME-STATE CONTRACT ==="
PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_documentation_runtime_state_contract.py

echo
echo "=== STICKY EDITOR OPTIONS DOCUMENTATION CONTRACT ==="
PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_sticky_editor_options_documentation_contract.py

echo
echo "=== CODEQL CONFIGURATION CONTRACT ==="
PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_codeql_configuration_contract.py

echo
echo "=== LAUNCHER IMPORT CONTRACT ==="
PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_launcher_import_contract.py

echo
echo "=== PROJECT BIRTH AND ROUTING CONTRACT ==="
QT_QPA_PLATFORM=offscreen PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_project_birth_contract.py

echo
echo "=== EDITOR MENU AND PRIMITIVE CONTRACT ==="
QT_QPA_PLATFORM=offscreen PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_shape_document_editor_contract.py

echo
echo "=== 3D OBJECT CAD CONTRACT ==="
QT_QPA_PLATFORM=offscreen PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_object_cad_contract.py

echo
echo "=== SINGLE-OBJECT EDITOR USABILITY CONTRACT ==="
QT_QPA_PLATFORM=offscreen PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_editor_single_object_workspace_contract.py

echo
echo "=== POSITIONING GUIDES AND VIEWPORT NAVIGATION CONTRACT ==="
QT_QPA_PLATFORM=offscreen PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_positioning_guides_contract.py

echo
echo "=== EDITOR MOUSE-WHEEL AND STICKY OPTIONS CONTRACT ==="
QT_QPA_PLATFORM=offscreen PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_editor_mouse_wheel_contract.py

echo
echo "=== PERSISTENT OPTIONS AND PROJECT TRASH CONTRACT ==="
QT_QPA_PLATFORM=offscreen PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_persistent_options_and_project_trash_contract.py

echo
echo "=== EDITOR PROJECT AUTHORING CONTRACT ==="
QT_QPA_PLATFORM=offscreen PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_editor_project_authoring_contract.py

echo
echo "=== DOCUMENT LIFECYCLE AND STATIC GUIDANCE CONTRACT ==="
QT_QPA_PLATFORM=offscreen PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_document_lifecycle_and_static_guidance_contract.py

echo
echo "=== VISIBLE DELETION AND EDITOR ENTRY CONTRACT ==="
QT_QPA_PLATFORM=offscreen PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_visible_deletion_and_editor_entry_contract.py

echo
echo "=== UNIFIED PROJECT MENU AND RENAME CONTRACT ==="
QT_QPA_PLATFORM=offscreen PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_unified_project_menu_and_rename_current_contract.py

echo
echo "=== SELECT PROJECT RESTORATION CONTRACT ==="
QT_QPA_PLATFORM=offscreen PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_select_project_restoration_contract.py

echo
echo "=== PROMPT CONTRACT CHECK ==="
PYTHONPATH=src "$PYTHON_EXECUTABLE" tools/verify_prompts.py

echo
echo "=== SOURCE TRUTH VERIFY COMPLETE ==="
