---
name: accessibility-audit-meta
type: meta
version: 2.0.0
description: "Meta-prompt for Accessibility Audit skill routing."
---

# Accessibility Audit — Meta Prompt

Activate this skill when the user request matches:
- Trigger phrases from SKILL.md description
- Direct invocation: `/accessibility-audit`

## Skill Routing
1. Load `SKILL.md` and read `## Purpose`, `## Protocol`, and `## Quality Gates`.
2. Activate only for digital accessibility, WCAG, axe-core, keyboard, screen reader, contrast, form/error, focus, or UI audit requests.
3. If the request is about physical accessibility, financial access, or generic availability, ask for clarification instead of activating.
4. If match is confirmed, activate lead agent: `accessibility-audit-lead`.
5. If orchestrated, defer to the orchestrating skill.
