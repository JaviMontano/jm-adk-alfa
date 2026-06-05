---
name: agent-constitution-creator-meta
type: meta
version: 2.1.0
description: "Route constitution-grade agent identity requests."
---

# Agent Constitution Creator — Meta Prompt

Activate this skill when the request asks for persistent agent identity, governance, `agent.md`, authority boundaries, allowed tools, forbidden tools, memory policy, escalation, or a 22-field constitution.

Do not activate for lightweight subagent metadata. Route those requests to `agent-creator`.

## Skill Routing

1. Load `SKILL.md` and read `## When to Activate`.
2. If the request lacks role, peer-agent context, or tool registry, activate interview mode.
3. If the request is constitution-grade, activate `agent-constitution-creator-lead`.
4. If an orchestrator already owns the workflow, return the deterministic contract and validation gate.
