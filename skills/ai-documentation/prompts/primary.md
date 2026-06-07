---
name: ai-documentation-primary
type: execution
version: 2.1.0
description: "Execute source-backed AI documentation generation with deterministic packet validation."
triad:
  lead: "ai-documentation-lead"
  support: "ai-documentation-support"
  guardian: "ai-documentation-guardian"
---

# AI Documentation - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | Requested documentation work | Yes | User input |
| `{{sources}}` | Code, docs, configs, specs, tests, or snippets | Yes | User or repo scan |
| `{{doc_targets}}` | README / API_REFERENCE / RUNBOOK / ARCHITECTURE_NOTE / QUICKSTART / CHANGELOG_DRAFT | No | User or inferred |
| `{{audience}}` | developer / operator / end_user / maintainer / api_consumer | No | User or inferred |
| `{{output_format}}` | packet / markdown / html / docx | No | Auto |

## Execution

1. Read `knowledge/body-of-knowledge.md` and `assets/*.json`.
2. Build a source inventory with evidence ids.
3. Generate only sections supported by evidence.
4. Record gaps for missing, stale, or conflicting sources.
5. Validate the packet contract before delivery.

## Output

Return the documentation packet plus the user-facing documentation draft when requested.
