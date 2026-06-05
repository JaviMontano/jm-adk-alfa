---
name: agent-creator-primary
type: execution
version: 2.1.0
description: "Execute the deterministic Agent Creator workflow."
triad:
  lead: "agent-creator-lead"
  support: "agent-creator-support"
  guardian: "agent-creator-guardian"
---

# Agent Creator - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | Agent responsibility and desired output | Yes | User input |
| `{{context}}` | Project scope, existing agents, and constraints | Yes | User or codebase |
| `{{constraints}}` | Tool, model, destination, and approval limits | No | Guardrails JSON |

## Execution Steps

1. Confirm the user needs an agent rather than a skill, hook, CLAUDE.md rule,
   or output style.
2. Read `assets/agent-spec-schema.json`, `assets/tool-policy.json`, and
   `assets/description-trigger-policy.json` for deterministic requirements.
3. Normalize the request into the structured spec; ask only for missing
   required fields.
4. Compile with `scripts/compile-agent.py`.
5. Validate frontmatter, trigger description, least-privilege tools,
   self-sufficient prompt, constraints, output format, and escalation triggers.
