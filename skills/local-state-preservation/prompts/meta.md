# Meta Prompt

Evaluate whether `local-state-preservation` prevents local state loss.

## Prompt

Review the skill's instructions, assets, fixtures, and validator. Confirm that dirty trees, untracked files, ignored files, stashes, worktrees, clones, private paths, checksums, source/destination paths, archive manifests, and non-touch decisions are all represented. Propose edits only when they make the preservation packet more deterministic or safer.
