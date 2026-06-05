---
name: user-representative-meta
type: meta
version: 2.0.0
description: "Meta-prompt for User Representative skill routing."
---

# User Representative — Meta Prompt

Activate this skill when the user request matches:
- Trigger phrases from SKILL.md description
- Direct invocation: `/user-representative`

## Skill Routing
1. Load SKILL.md and read `## When to Activate`.
2. If the request asks for review from the user or stakeholder perspective, activate lead agent: `user-representative-lead`.
3. If the request asks to write requirements, UX copy, UI design, or technical validation, route to the adjacent skill instead.
4. If orchestrated, defer to the orchestrating skill.
