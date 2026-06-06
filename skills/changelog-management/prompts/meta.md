---
name: changelog-management-meta
type: meta
version: 2.0.0
description: "Meta-prompt for deterministic Changelog Management routing."
---

# Changelog Management — Meta Prompt

Activate this skill when the request mentions `changelog.md`, changelog update,
log decision, record change, session log, blocker, durable insight, or continuity
entry for this repository.

Do not activate for public release notes, product update summaries, or generic
"what changed" questions that do not require this repo's continuity log.

## Routing

1. Confirm activation through `SKILL.md`.
2. If writing is requested, route through `changelog-management-guardian`.
3. If duplicate risk exists, return skip/revise recommendation before writing.
