---
name: session-manager-meta
type: meta
version: 2.0.0
description: "Meta-prompt for deterministic Session Manager routing."
---

# Session Manager — Meta Prompt

Activate this skill when the request asks to recover project session state,
compute pipeline stage, run `/jm:status`, or persist an authorized update to
`.specify/context.json`.

Do not activate for unrelated browser sessions, login sessions, chat summaries,
or cleanup tasks that do not require project state.

## Skill Routing

1. Load `SKILL.md` and confirm `## When to Activate`.
2. If matched, activate `session-manager-lead`.
3. If persistence is requested, route final output through
   `session-manager-guardian` before writing.
4. If orchestrated by another skill, return the status report and let the
   orchestrator decide the next workflow step.
