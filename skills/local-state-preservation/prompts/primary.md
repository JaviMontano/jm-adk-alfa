# Primary Prompt

Use `local-state-preservation` to create a preservation packet before repository mutation.

## Prompt

Inspect the repository state without mutating it. Produce a JSON preservation report that inventories tracked changes, untracked files, ignored files, stashes, worktrees, clones, private path exclusions, preservation artifacts, non-touch decisions, and validation commands. Validate the report with `skills/local-state-preservation/scripts/validate_local_state_preservation.py` before recommending any cleanup, import, sync, or branch switch.
