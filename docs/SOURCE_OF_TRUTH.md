# Source of Truth Policy

This repo is the leading source of truth for MXZTAR-forge v2c0.

## Priority order

1. Git repository history
2. Current local working tree
3. VX12 dated backups
4. Terminal scrollback

Terminal scrollback is not a source of truth. Important outputs must be saved to files.

## Change rule

Every meaningful change should include:

- what changed
- why it changed
- affected files
- verification command
- verification result
- backup status if relevant

## Drift prevention

Before working:

1. Check current branch.
2. Check git status.
3. Pull latest remote if remote is configured.
4. Verify the app still compiles or launches at the expected level.

After working:

1. Compile changed files.
2. Run targeted verifier.
3. Commit known-good state.
4. Backup to VX12 when a stage is stable.
