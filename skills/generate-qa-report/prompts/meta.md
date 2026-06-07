---
name: generate-qa-report-meta
type: meta
version: 2.0.0
description: "Meta-prompt for Generate Qa Report skill routing."
---

# Generate QA Report - Meta Prompt

Activate this skill when the user request matches:
- Trigger phrases from SKILL.md description
- Direct invocation: `/generate-qa-report`
- Requests to summarize completed validation/audit outputs

## Skill Routing
1. Load SKILL.md and confirm QA report generation applies.
2. If validation sources are absent, report the missing inputs or offer to run validations in a separate workflow.
3. If match, activate `generate-qa-report-lead`.
4. If orchestrated, defer to the orchestrator after stating source requirements.
