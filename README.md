# MXZTAR Forge v2.0

MXZTAR Forge v2.0 is a local-first, human-governed creative concept-engineering forge.

It helps creators, concept artists, 3D/blockout artists, game/film/animation planners, and design-system builders turn complex source art into structured, inspectable, reusable production intelligence.

It is not merely an image captioner, an automatic art generator, or a one-click 2D-to-3D converter. Its purpose is to recover and organise the design grammar needed for controlled 2D derivatives, 2.5D constructions, modular blockouts, Blender/CAD handoffs, and later production-oriented 3D workflows.

Core value path:

```text
source art
→ source suitability and rights context
→ visual and schematic intelligence
→ line, shape, layer, depth, perspective, and module evidence
→ observed versus inferred structure
→ approved reusable design grammar
→ concept brief / extraction map / module plan / prompt pack
→ 2D derivative, 2.5D stack, blockout, Blender/CAD, or later 3D handoff
```

## Planning source of truth

- [First rentable release](docs/product/FIRST_RENTABLE_RELEASE.md)
- [Workflow compatibility matrix](docs/product/WORKFLOW_COMPATIBILITY_MATRIX.md)
- [Output artifact contracts](docs/product/OUTPUT_ARTIFACT_CONTRACTS.md)
- [Project state and data authority](docs/architecture/PROJECT_STATE_AND_DATA_AUTHORITY.md)
- [Master build plan](docs/product/MASTER_BUILD_PLAN.md)
- [Progress ledger](docs/PROGRESS_LEDGER.md)

## Source-of-truth policy

This repository is the leading source of truth.

VX12 backups are dated safety copies. GitHub is the repo history. Local project files are the working copy. Terminal scrollback is not project truth.

## Adaptive machine policy

This project must remain safe on a modest CPU-only rig while adapting upward when a user's machine has more capacity.

Default fallback policy:

- `OLLAMA_NUM_THREAD=2` when hardware is unknown or modest;
- `OLLAMA_NUM_PARALLEL=1` by default;
- no silent long jobs;
- no AI work on the Qt main thread;
- no dead UI;
- no frozen UI;
- no silent model downloads;
- one heavy local job at a time by default.

Adaptive detection may recommend more CPU threads on capable rigs and may record GPU presence, but GPU detection must not silently enable multiple heavy local jobs or trigger model downloads.

## Desktop launchers

Install or safely refresh both the Linux application-menu launcher and the
Desktop launcher:

```bash
bash tools/install_desktop_launchers.sh
```

Both launchers use the repository-owned star icon and target the checkout's
relocatable `run_mxztar_forge.sh`. Existing launcher files are backed up before
replacement. The installer also creates a Desktop folder-link named
`MXZTAR-Forge-Input` that points directly to the authoritative
`workspace/input` intake directory.
