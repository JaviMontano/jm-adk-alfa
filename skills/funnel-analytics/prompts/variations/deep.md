---
name: funnel-analytics-deep
type: variation
version: 2.0.0
description: "Funnel Analytics — deep analysis mode. Exhaustive coverage."
---

# Funnel Analytics - Deep Mode

## When to Use

Use deep mode when funnel decisions affect roadmap, revenue, instrumentation, experimentation, compliance, or executive reporting.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Load `knowledge/body-of-knowledge.md`, `assets/deliverable-checklist.md`, and relevant project artifacts
2. Check guardrails: `references/guardrails/*.json` when present
3. Lead executes with exhaustive analysis:
   - Cover event taxonomy, denominators, identity stitching, segment mix, data quality, and privacy
   - Document every assumption as `not verified` or with the requested evidence tag
4. Support reviews with expanded scope:
   - Attribution, causal inference, experiment readiness, and governance
   - Adversarial scenarios: what could make the funnel conclusion false?
5. Guardian validates with strict criteria:
   - Evidence tags cover every claim
   - No invented event, metric, source, or causal explanation
   - Asset checklist fully met

## Output

- Exhaustive deliverable with full evidence trail
- Edge cases and evidence gaps documented
- Risk assessment included
- Recommendations with priority, dependency, and validation method
