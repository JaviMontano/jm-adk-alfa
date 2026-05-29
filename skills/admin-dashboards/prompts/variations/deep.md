---
name: admin-dashboards-deep
type: variation
version: 2.0.0
description: "Admin Dashboards — deep analysis mode with full data, authorization, state, and test contracts."
---

# Admin Dashboards — Deep Mode

## When to Use

Use deep mode for new admin systems, sensitive data, destructive operations, exports, complex RBAC, unclear APIs, large datasets, realtime requirements, or release gates.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Load focused knowledge: `knowledge/body-of-knowledge.md` plus only related skills needed for security, forms, API, accessibility, audit, or data visualization
2. Check guardrails: `references/guardrails/*.json`
3. Lead executes with exhaustive analysis:
   - Cover entities, data contracts, RBAC, navigation, tables, CRUD, charts, realtime, exports, audit, states, responsive, performance, and tests
   - Document every missing API/schema/policy/metric/channel as `not verified`
   - Decide whether this is Quick Flow or needs BMAD story/readiness gates before implementation
4. Support reviews with expanded scope:
   - IDOR, export leaks, CSV injection, raw HTML, backend authorization gaps, keyboard access, mobile density, large dataset behavior
   - Adversarial scenarios: what could expose data, mislead operators, or fail under operational load?
5. Guardian validates with strict criteria:
   - RBAC, data contract, state matrix, audit, and test plan are present
   - Confidence is capped by missing backend evidence

## Output

- Full admin dashboard specification with evidence trail
- Implementation readiness gaps and story/test recommendations
- Security, accessibility, responsive, performance, audit, and export risks
- Confidence score with evidence-based justification
