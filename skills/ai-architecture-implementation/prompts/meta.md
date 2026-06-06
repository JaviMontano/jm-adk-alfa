---
name: ai-architecture-implementation-meta
type: meta
version: 2.0.0
description: "Meta-prompt for AI Architecture Implementation skill routing."
---

# AI Architecture Implementation — Meta Prompt

Activate this skill when the user request matches:
- Trigger phrases from SKILL.md description
- Direct invocation: `/ai-architecture-implementation`
- Requests to implement, deploy, migrate, remediate, set up, configure, or productionize AI/ML/GenAI architecture.

Do not activate as primary for pure audit, pure design, or cloud-provider-specific implementation.

## Skill Routing
1. Load SKILL.md and confirm implementation intent.
2. If match → activate lead agent: `ai-architecture-implementation-lead`
3. If orchestrated → defer to orchestrating skill
