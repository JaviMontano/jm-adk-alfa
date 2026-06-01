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
- `schemas/`: public schemas for local context manifests and cards.

## Privacy Boundary

Personal content is ignored by git by default. Only this scaffold, the marker,
schemas, and documentation are tracked.

Agents should read `_INDICE.md` first, then only the specific context files
needed for the current task. Agents should write here only after an explicit
context-update instruction from the user.

## Safe Starter Files

Use these optional local files when the user asks to add durable context:

- `preferences/output-style.md`: stable preferences for language, density, and
  evidence level.
- `context/current-focus.md`: durable background that should survive across
  workspaces.
- `memory/decisions.md`: user-approved long-lived decisions.

Do not add credentials, tokens, API keys, private keys, or passwords. Put task
outputs in `workspace/{active}/artifacts/`, not here.
