# MXZTAR Forge v2.0 — Adaptive Hardware Policy

## Purpose

MXZTAR Forge must remain usable on modest CPU-only machines while adapting safely when a user's rig has more CPU, memory, or GPU capacity.

The policy is not hard-wired to one reference machine. The T1700-class profile is the safe fallback, not the ceiling.

## Safety rules

- Unknown hardware falls back to a conservative safe mode.
- Modest CPU-only rigs stay at a low thread count.
- Capable CPU-only rigs may receive more CPU threads within a bounded range.
- GPU presence is detected and displayed, but it does not silently enable multiple heavy jobs.
- No model downloads are triggered by hardware detection.
- No AI work may run on the Qt main thread.
- One heavy local job remains the default until job-queue controls explicitly support more.

## Current profile outputs

The policy currently derives:

- profile key;
- profile label;
- Ollama CPU thread count;
- Ollama parallel count;
- maximum heavy local jobs;
- recommended model-size class;
- GPU presence and GPU name when detectable;
- detection notes for UI/debugging.

## Runtime integration

The launcher no longer exports fixed Ollama thread settings. Python detects the hardware profile and applies:

```text
OLLAMA_NUM_THREAD
OLLAMA_NUM_PARALLEL
```

The Ollama request payload uses the selected `num_thread` value.

## Verification

Run:

```bash
PYTHONPATH=src .venv/bin/python tools/verify_hardware_profile_contract.py
PYTHONPATH=src .venv/bin/python -m py_compile \
  src/core/hardware_profile.py \
  src/brain/service.py \
  src/qt_app.py \
  src/qt_panels/agent_panel.py \
  tools/verify_hardware_profile_contract.py
```
