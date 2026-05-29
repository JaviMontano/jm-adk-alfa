---
description: "Create or preview local Alfa profile configuration with dry-run-first safety."
user-invocable: true
---

# /jm-adk:setup-workspace

## Purpose

Create `.jm-adk.local.json` only after explicit approval. The file is local-only and must not be committed.

## Dry Run

```bash
python3 scripts/setup-workspace-profile.py --dry-run
```

## Apply

```bash
python3 scripts/setup-workspace-profile.py --apply
```

## Safety

- Do not request or store secrets.
- Do not overwrite an existing profile unless `--force` is explicitly provided after diff review.
- Keep workspace runtime state under `workspace/`.

## Agent And Skill

- Agent: `workspace-diagnostic-agent`
- Skill: `workspace-setup`
