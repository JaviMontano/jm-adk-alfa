---
name: ux-writing-meta
type: meta
version: 2.0.0
description: "Meta-prompt for Ux Writing skill routing."
---

# UX Writing — Meta Prompt

Activate this skill when the user request matches:
- Trigger phrases from SKILL.md description
- Direct invocation: `/ux-writing`

## Skill Routing
1. Load SKILL.md and read `## When to Activate`.
2. If the request asks for readability, microcopy, hierarchy, scannability, or cognitive load, activate lead agent: `ux-writing-lead`.
3. If the request asks for technical correctness, architecture security, visual design, or adoption-risk scoring, route to the adjacent skill instead.
4. If orchestrated, defer to the orchestrating skill.
