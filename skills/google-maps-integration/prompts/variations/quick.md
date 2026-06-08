---
name: google-maps-integration-quick
type: variation
version: 2.0.0
description: "Google Maps Integration in quick mode."
---

# Google Maps Integration — quick Mode

## When to Use

Use quick mode when you need adjusted depth for the Google Maps Integration workflow.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Load skill: `skills/google-maps-integration/knowledge/body-of-knowledge.md`
2. [CODE] Read `assets/maps-platform-plan-schema.json` and `assets/api-selection-policy.json`.
3. [CODE] Produce a concise offline plan with API selection, key restrictions, data flow, marker clustering, accessibility, privacy, and human confirmation.
4. [CONFIG] Do not call Google APIs.
5. [CONFIG] Do not include monetary prices.
6. [CODE] Lead -> Support -> Guardian validation.
7. [CODE] Confidence >= 0.95.

## Output

- [CODE] Deliverable calibrated to quick depth.
- [CODE] Evidence-tagged and Constitution-compliant.
- [CODE] Residual risks and missing-input gaps only.
