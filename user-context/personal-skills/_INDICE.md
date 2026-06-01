# _INDICE.md · Personal Skills

This index lists private user-authored skills that live outside Alfa core.

| Area | Purpose |
|---|---|
| `skills/` | Canonical private personal skill source |
| `.jm-adk-personal-skills.json` | Marker and sync contract |

## Loading Rule

Load a personal skill only when the user's request or runtime matching requires it. Do not scan or bulk-load every personal skill.

## Sync Rule

Use `scripts/sync-personal-skills.py --dry-run` before any copy mirror apply.
