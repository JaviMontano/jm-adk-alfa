---
name: agent-constitution-creator-primary
type: execution
version: 2.1.0
description: "Execute the deterministic Agent Constitution Creator workflow."
triad:
  lead: "agent-constitution-creator-lead"
  support: "agent-constitution-creator-support"
  guardian: "agent-constitution-creator-guardian"
---

# Agent Constitution Creator — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | Requested agent id and role | Yes | User input |
| `{{context}}` | Existing agents, tool registry, security policy, memory policy | Yes | User or repo |
| `{{constraints}}` | Approval boundaries and forbidden actions | No | Guardrails JSON |

## Execution Steps

1. Read `SKILL.md ## When to Activate` and confirm this is constitution-grade work.
2. Read `assets/authority-policy.json` before assigning authority or tools.
3. If required inputs are missing, ask interview questions and stop before generation.
4. Generate with `assets/agent-constitution-template.md` without changing the 22 headings.
5. Validate with `scripts/validate_agent_constitution.py`.
6. Deliver Markdown plus validation result and unresolved `[OPEN]` items.
