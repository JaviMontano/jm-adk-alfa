---
name: analytics-implementation-meta
type: meta
version: 2.0.0
description: "Meta-prompt for Analytics Implementation skill routing."
---

# Analytics Implementation — Meta Prompt

Activate this skill when the user request matches:
- Trigger phrases from SKILL.md description
- Direct invocation: `/analytics-implementation`
- GA4/Firebase setup, custom events, conversions, user properties, BigQuery export, Looker Studio readiness, DebugView QA, or consent/privacy analytics implementation

## Skill Routing
1. Load SKILL.md and confirm the task is analytics implementation, not Firestore database design or dashboard visual design.
2. If matched, activate `analytics-implementation-lead`.
3. If orchestrated, defer to the orchestrator while preserving the `assets/` and `scripts/` contract.
