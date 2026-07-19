# AGENTS.md

Repository role: MXZTAR Forge v2.0 is a local Ubuntu creative-concept engineering forge. It turns complex source art into structured production material, prompt packs, modular design intelligence, and future workflow-ready assets.

Use this file as the compact coding source of truth for AI agents working in this repo.

## Core rules

- Preserve working behaviour before changing layout, workflow contracts, prompt contracts, agent runners, model calls, file paths, or verification scripts.
- Do not add visible UI, menu items, buttons, feature flags, or settings unless the full workflow exists: handler, engine/helper path, input path, output path, error handling, user feedback, logging where useful, and verification.
- Every name is a promise. Remove unused imports, variables, functions, stale comments, and misleading names.
- Programming is controlled change. Before editing, identify state before, allowed change, state after, and what happens on failure.
- Good functions have one clear responsibility. Split mixed validation, persistence, UI, logging, and side-effect work where useful.
- Data shape is destiny. Avoid duplicate authority fields, vague status strings, and schemas that allow impossible states.
- Abstractions should remove difficulty, not hide reality. Avoid vague helpers such as `processData`, `handleThing`, or `doAction`.
- Prefer small, reversible changes. Do not perform sweeping refactors unless the task explicitly requires them.

## MXZTAR Forge guardrails

- Git repository history is the leading source of truth. VX12 backups are dated safety copies. Terminal scrollback is not a source of truth.
- Preserve the source-image to visual-intelligence to modular-candidates to prompt-pack/output path.
- Maintain prompt-contract discipline. Do not change prompt keys, output shapes, or stored JSON contracts without updating verifiers.
- This project is built for a modest CPU-only rig. Default local AI policy: low thread count, one job at a time, no silent long jobs, and no AI work on the Qt main thread.
- No dead UI and no frozen UI. Long-running agent/model work must be queued/asynchronous with visible status.
- Do not overstate what vision or AI analysis can infer. Separate observed facts, model guesses, and user decisions.
- Access/support text must stay truthful: official use is free of charge, founder
  support is voluntary, and no recognised open-source licence may be invented before
  founder selection. Do not advertise '+ GST' unless GST registration and
  checkout/accounting handling are ready.

## Compliance and conduct

- Follow New Zealand legal/compliance assumptions unless repo docs say otherwise.
- Do not add content or behaviour involving occult, obscene, hateful, grooming, criminal, exploitative, or unsafe material.
- Do not claim AI certainty where the system only has an estimate, score, or heuristic.
- Do not expose secrets, private keys, buyer data, credentials, or unnecessary tracking.

## Workflow for agents

1. Inspect relevant files before editing.
2. Identify the existing workflow contract before adding behaviour.
3. Make the smallest complete change that satisfies the task.
4. Run the narrowest useful verification first.
5. Report changed files, verification performed, and remaining risk.

## Verification ladder

- Documentation-only change: check Markdown clarity and links if relevant.
- Syntax-only Python change: run `python -m py_compile` on changed Python files.
- Prompt-contract change: run `PYTHONPATH=src python tools/verify_prompts.py`.
- Source-truth or meaningful workflow change: run `./scripts/verify_source_truth.sh`.
- Qt/UI or agent-runner change: compile changed files and verify the UI cannot freeze on long work.

Never leave dead UI, frozen UI, unverified workflow claims, broken prompt contracts, broken checks, or hidden drift behind.
