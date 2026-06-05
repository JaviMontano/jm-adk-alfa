---
name: quality-gatekeeper-meta
type: meta
version: 2.0.0
description: "Meta-prompt for Quality Gatekeeper skill routing."
---

# Quality Gatekeeper Meta Prompt

Activate this skill when the user request matches:

- JM-ADK gate readiness, G0-G3, phase transition, `/jm:advance`, PR/release
  gate decision, or score-history validation.

Do not activate for generic writing quality, generic CI explanation, or
Lighthouse-only requests unless the user asks for a JM-ADK gate decision.

## Routing

1. Load `assets/activation-policy.json`.
2. If in scope, activate `quality-gatekeeper-lead`.
3. If out of scope, route to the adjacent skill and do not produce a gate
   report.
