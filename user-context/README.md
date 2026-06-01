# JM-ADK User Context

This directory is the in-kit context repo for durable user context.

It is identified by `.jm-adk-context.json`, not by whatever files the user adds
later. Keep the marker file intact so Alfa can recognize this directory as the
context repo even when the private contents change.

## What Belongs Here

- `context/`: durable background about the user, work style, domain, projects,
  and long-lived facts the user explicitly wants Alfa to consider.
- `preferences/`: stable preferences for language, output shape, tools,
  autonomy, privacy, and recurring workflows.
- `memory/`: user-approved long-lived notes that should outlive a task
  workspace.
- `sources/`: private source files or source indexes referenced by context
  notes.
- `resources/`: curated persistent resources such as CVs, identification,
  relevant URLs, reference documents, and user-provided consultation material.
- `personal-skills/`: canonical private source for user-authored skills that
  should survive SDK updates and sync to runtime skill roots by copy mirror.
- `schemas/`: public schemas for local context manifests, cards, resources, and
  personal skill markers.

## Privacy Boundary

Personal content is ignored by git by default. Only this scaffold, the marker,
schemas, and documentation are tracked.

Agents should read `_INDICE.md` first, then only the specific context files
needed for the current task. Agents should not bulk-load `sources/` or
`resources/`. Agents should write here only after an explicit context-update
instruction from the user.

Personal skills are created with `scripts/scaffold-skill.py --personal` and
synced with `scripts/sync-personal-skills.py`. Do not store user-authored skills
in root `skills/`.

## Safe Starter Files

Use these optional local files when the user asks to add durable context:

- `preferences/output-style.md`: stable preferences for language, density, and
  evidence level.
- `context/current-focus.md`: durable background that should survive across
  workspaces.
- `memory/decisions.md`: user-approved long-lived decisions.
- `resources/resource-cards.md`: index cards for private resources.

Do not add credentials, tokens, API keys, private keys, or passwords. Put task
outputs in `workspace/{active}/artifacts/`, not here.
