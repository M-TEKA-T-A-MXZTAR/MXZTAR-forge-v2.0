#!/usr/bin/env bash
cd "$HOME/MXZTAR-forge-v2.0" || exit 1

if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

python3 src/mxztar_forge.py
