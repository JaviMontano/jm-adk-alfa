---
description: "Diagnose Alfa repo, local profile, workspace registry, and first-use readiness without modifying files."
user-invocable: true
---

# /jm-adk:diagnose-workspace

## Purpose

Report first-use readiness and workspace status safely.

## Command

```bash
python3 scripts/diagnose-first-use.py --dry-run
```

## Outputs

- `ready`
- `needs_setup`
- `needs_task`
- `fresh_clone`
- `empty_workspace`
- `requires_confirmation`

## Agent

Use `workspace-diagnostic-agent`.
