---
name: google-analytics-primary
type: execution
version: 2.1.0
description: "Execute the offline GA4/GTM measurement-planning workflow with triad review."
triad:
  lead: "google-analytics-lead"
  support: "google-analytics-support"
  guardian: "google-analytics-guardian"
---

# Google Analytics — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|---|---|---|---|
| `{{task}}` | GA4/GTM measurement request | Yes | User input |
| `{{context}}` | Site, funnel, product, codebase, or analytics context | Yes | User or codebase |
| `{{constraints}}` | Privacy, region, tooling, ownership, and mutation constraints | No | User or guardrails |
| `{{depth}}` | quick / standard / deep | No | Auto |
| `{{output_format}}` | md / html / docx | No | Auto |

## Execution

1. Read `SKILL.md`, `knowledge/body-of-knowledge.md`, and `assets/source-map.md`.
2. If structured JSON is available, run `scripts/compile-google-analytics.py`.
3. If structured JSON is not available, produce the same sections as `templates/output.md` and identify missing fields.
4. Lead designs the GA4/GTM plan:
   - Property and data-stream readiness.
   - Measurement strategy.
   - Event taxonomy.
   - Parameter contract.
   - Key-event plan.
   - Tag/container plan.
5. Support reviews:
   - Privacy/consent state.
   - PII parameter risk.
   - Measurement Protocol supplement-only constraint.
   - GTM Preview, Tag Assistant, DebugView, Realtime, and network debug checks.
6. Guardian validates:
   - Human confirmation before mutation-ready recommendations.
   - Evidence tags.
   - Offline determinism.
   - Residual risks.

## Output

- Use `templates/output.md` for Markdown.
- Use `templates/output.html` only for standalone HTML reports.
- Include evidence, validation commands when scripts are changed, and limits.
- Do not call Google Analytics, GTM, OAuth, MCP, or network from the deterministic script.
