---
name: agent-creator-meta
type: meta
version: 2.1.0
description: "Meta-prompt for Agent Creator routing and critique."
---

# Agent Creator - Meta Prompt

Activate this skill when the user request asks for a custom agent, subagent, or
agent definition. Reject false positives where a rule, hook, output style, or
skill is the better artifact.

## Critique Checklist

- Trigger description says WHEN to spawn.
- Tools are explicit and least-privilege.
- Prompt is self-sufficient without parent chat context.
- Output format and constraints are concrete.
- Negative triggers and escalation rules prevent over-invocation.
