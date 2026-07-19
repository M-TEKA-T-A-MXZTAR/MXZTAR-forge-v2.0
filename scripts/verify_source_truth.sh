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
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

PYTHONPATH=src python -m py_compile \
  src/brain/prompts.py \
  src/brain/service.py \
  src/core/agent_runner.py \
  src/core/project_access.py \
  src/core/project_manifest.py

echo "PASS: core Python files compile"

echo
echo "=== PROMPT CONTRACT CHECK ==="
PYTHONPATH=src python tools/verify_prompts.py

echo
echo "=== SOURCE TRUTH VERIFY COMPLETE ==="
