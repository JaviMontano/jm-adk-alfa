---
name: context-optimizer-meta
type: meta
version: 2.0.0
description: "Meta-prompt for Context Optimizer skill routing."
---

# Context Optimizer — Meta Prompt

Activate this skill when the user request matches:
- Trigger phrases from SKILL.md description
- Direct invocation: `/context-optimizer`
- Requests to optimize token budget, context window, lazy loading, progressive disclosure, or session compression

## Skill Routing
1. Load only `SKILL.md` and this prompt first.
2. If the request is about context optimization, activate `context-optimizer-lead`.
3. Keep unrelated skill references deferred until the active skill requires them.
4. If the request is about creating a compact handoff, route to `pre-compact-context`.
