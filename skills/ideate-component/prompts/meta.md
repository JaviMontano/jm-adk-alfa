---
name: ideate-component-meta
type: meta
version: 2.0.0
description: "Meta-prompt for Ideate Component skill routing."
---

# Ideate Component - Meta Prompt

Activate this skill when the user request matches:
- Trigger phrases from SKILL.md description
- Direct invocation: `/ideate-component`
- Requests to brainstorm one skill, agent, command, or hook for a plugin

## Skill Routing
1. Load SKILL.md and confirm the request is ideation, not implementation.
2. If component type is missing, ask one concise type-selection question.
3. If match is confirmed, activate `ideate-component-lead`.
4. If the user asks for final design or creation, route to the relevant design/build skill after the concept card.
