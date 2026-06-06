---
name: ai-architecture-audit-meta
type: meta
version: 2.0.0
description: "Meta-prompt for AI Architecture Audit skill routing."
---

# AI Architecture Audit — Meta Prompt

Activate this skill when the user request matches:
- Trigger phrases from SKILL.md description
- Direct invocation: `/ai-architecture-audit`
- Existing AI/ML/GenAI system audit, review, technical debt, quality, security, compliance, drift, or governance assessment.

Do not activate as primary when the user asks to design a new architecture, implement remediation, write tests, or perform a cloud-provider-specific audit.

## Skill Routing
1. Load SKILL.md and confirm audit-not-design intent.
2. If match → activate lead agent: `ai-architecture-audit-lead`
3. If orchestrated → defer to orchestrating skill
