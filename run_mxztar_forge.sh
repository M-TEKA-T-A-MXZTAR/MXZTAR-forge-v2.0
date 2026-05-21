#!/usr/bin/env bash
cd "$HOME/MXZTAR-forge-v2c0" || exit 1

export OLLAMA_NUM_THREAD=2
export OLLAMA_NUM_PARALLEL=1

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

python3 src/mxztar_forge.py
