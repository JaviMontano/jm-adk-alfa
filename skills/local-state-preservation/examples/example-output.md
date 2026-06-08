# Example Output

## Result

Writes are blocked until the preservation packet validates. The draft report inventories tracked edits, untracked files, ignored workspace files, stashes, worktrees, sibling clones, and the private `user-context/jarvis-os` exclusion.

## Artifacts

| Kind | Source | Destination | SHA-256 | Size |
|------|--------|-------------|---------|------|
| patch | `skills/example/SKILL.md` | `workspace/2026-06-08-alfa-repo-sync-cleanup/patches/tracked.patch` | `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` | 128 |
| archive | `workspace/old-session/` | `.local/archive/2026-06-08-alfa-cleanup/old-session.tar.gz` | `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb` | 2048 |

## Validation

- `python3 skills/local-state-preservation/scripts/validate_local_state_preservation.py report.json`: pass
- Stashes: inventory-only
- Private paths: excluded from artifacts
