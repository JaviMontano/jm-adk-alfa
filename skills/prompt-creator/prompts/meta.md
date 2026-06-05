---
name: prompt-creator-meta
type: meta
version: 2.0.0
description: "Meta-prompt for Prompt Creator skill routing."
---

# Prompt Creator - Meta Prompt

Activate this skill when the user request matches:
- Trigger phrases from SKILL.md description
- Direct invocation: `/prompt-creator`

## Skill Routing
1. Load SKILL.md and read `## When to Activate`.
2. If request asks for a prompt artifact, activate `prompt-creator-lead`.
3. If request asks for a full agent constitution, redirect to `agent-constitution-creator`.
4. If request asks for workflow step prompt, redirect to `workflow-creator`.
5. If source agent or prompt type is missing, ask for the missing field.

## Determinism Check

- Preserve evidence tags even in short outputs.
- Never invent agent files, prompt paths, tools, dates, or validation gates.
- Keep generated prompt artifact separate from downstream execution.
