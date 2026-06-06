---
name: tasklog-management-meta
type: meta
version: 2.0.0
description: "Meta-prompt for deterministic Tasklog Management routing."
---

# Tasklog Management — Meta Prompt

Activate this skill when the user request mentions `tasklog.md`, open tasks,
pending items, stale tasks, task status, task closure, task archive, or
`workspace/tasks/` bridges.

Do not activate for unrelated operating-system task apps, calendar reminders, or
general productivity advice that does not require repository tasklog state.

## Routing

1. Confirm activation through `SKILL.md`.
2. If the request includes writes, route through `tasklog-management-guardian`.
3. If the request only needs review, return recommendations and keep writes
   disabled.
