---
name: google-maps-integration-deep
type: variation
version: 2.0.0
description: "Google Maps Integration — deep analysis mode. Exhaustive coverage."
---

# Google Maps Integration — Deep Mode

## When to Use

Use deep mode when thoroughness matters more than speed: architecture decisions, security audits, compliance reviews, critical deliverables.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. [CODE] Load all local skill knowledge and every file in `assets/`.
2. [DOC] Re-check official Google Maps Platform docs if the user asks for current guidance.
3. [CODE] Lead executes exhaustive offline analysis:
   - [CODE] Cover schema gaps, selected APIs, key restrictions, data flow, markers, accessibility, privacy, billing/quota, and confirmation.
   - [DOC] Flag Directions API Legacy status when route directions are requested.
   - [SUPUESTO] Document every missing user input as an assumption or open item.
4. [CODE] Support reviews with expanded scope:
   - [CODE] Security, accessibility, privacy, performance, quota exposure, and offline determinism.
   - [INFERENCE] Adversarial scenarios: unrestricted key, missing consent, unbounded autocomplete, repeated geocoding, inaccessible marker-only results.
5. [CODE] Guardian validates with strict criteria:
   - [CODE] Evidence tags 100% coverage.
   - [CODE] No monetary prices.
   - [CODE] No external API calls.
   - [CODE] Confidence >= 0.95 with evidence support.

## Output

- [CODE] Exhaustive deliverable with full evidence trail.
- [CODE] Edge cases documented.
- [CODE] Risk assessment included.
- [CODE] Recommendations with priority ranking.
- [CODE] Confidence score with justification.
