---
name: prompt-forge-meta
type: meta
version: 2.0.0
description: "Meta-prompt for Prompt Forge skill routing."
---

# Prompt Forge - Meta Prompt

Activate this skill when the user asks to create, review, evolve, repair, or port a system prompt, or explicitly names Prompt Forge / Playbook format.

Do not activate when:

- The user asks to be reminded or prompted later.
- The user asks only for a plain-language concept explanation.
- The user asks for a durable prompt file without analysis; route to `prompt-creator`.

## Routing

1. Load `SKILL.md` and confirm `## When to Activate`.
2. If active, select one mode.
3. If another skill owns the output, return a routing note and the minimum handoff context.
