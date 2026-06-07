---
name: analytics-events-deep
type: variation
version: 2.0.0
description: "Analytics Events — deep analysis mode. Exhaustive coverage."
---

# Analytics Events — Deep Mode

## When to Use

Use deep mode when instrumentation quality, privacy, migration, or multi-platform consistency matters more than speed.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Load `knowledge/body-of-knowledge.md` and all `assets/` policy files.
2. Inventory existing events, destinations, platforms, identities, duplicates, PII risks, and QA evidence.
3. Design taxonomy, canonical event names, legacy aliases, property schema, identity merge policy, tracking plan, governance, rollout, and validation.
4. Test the plan against false positives, blocked PII, duplicate event names, unknown properties, and missing owners.
5. Guardian blocks if any event lacks trigger, owner, properties, evidence, or QA method.

## Output

- Exhaustive deliverable with full evidence trail
- Edge cases documented
- Risk assessment included
- Recommendations with priority ranking
- Confidence score with justification
