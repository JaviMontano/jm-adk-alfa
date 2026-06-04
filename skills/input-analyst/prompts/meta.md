---
name: input-analyst-meta
type: meta
version: 2.0.0
description: "Meta-prompt for Input Analyst skill routing."
---

# Input Analyst — Meta Prompt

Activate this skill when the user request matches:
- Trigger phrases from SKILL.md description
- Direct invocation: `/input-analyst`
- Requests to clarify, normalize, de-risk, route, or reformulate vague input

## Skill Routing
1. Load SKILL.md → read `## When to Activate` section
2. If a reproducible artifact is needed → route through `scripts/compile-input-analysis.py`
3. If match → activate lead agent: `input-analyst-lead`
4. If orchestrated → defer to orchestrating skill after emitting the clarified prompt and routing hints
