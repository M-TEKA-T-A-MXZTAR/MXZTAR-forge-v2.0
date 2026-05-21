#!/usr/bin/env bash
set -euo pipefail

cd "$HOME/MXZTAR-forge-v2c0"

echo "=== MXZTAR-FORGE SOURCE TRUTH VERIFY ==="

echo
echo "=== REQUIRED DOCS ==="
for f in \
  README.md \
  docs/SOURCE_OF_TRUTH.md \
  docs/NZ_COMPLIANCE_AND_SUBSCRIPTION_NOTES.md \
  docs/CODING_PRACTICE_PRINCIPLES.md
do
  test -f "$f"
  echo "PASS FILE: $f"
done

echo
echo "=== PYTHON COMPILE CHECK ==="
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

PYTHONPATH=src python -m py_compile \
  src/brain/prompts.py \
  src/brain/service.py \
  src/core/agent_runner.py

echo "PASS: core Python files compile"

echo
echo "=== PROMPT CONTRACT CHECK ==="
PYTHONPATH=src python tools/verify_prompts.py

echo
echo "=== SOURCE TRUTH VERIFY COMPLETE ==="
