---
name: accessibility-testing-deep
type: variation
version: 2.0.0
description: "Accessibility Testing — deep analysis mode with exhaustive evidence coverage."
---

# Accessibility Testing — Deep Mode

## When to Use

Use deep mode when thoroughness matters more than speed: release gates, regulated products, critical user flows, regressions, and audit-ready accessibility evidence.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Load focused knowledge: `knowledge/body-of-knowledge.md` plus only cross-referenced skills needed for the target flow
2. Check guardrails: `references/guardrails/*.json`
3. Lead executes with exhaustive analysis:
   - Cover every declared route, component, dynamic state, and breakpoint
   - Include automation, keyboard, screen reader, contrast, motion, zoom/reflow, and suppression review
   - Document every assumption with `[ASSUMPTION]` or `not verified`
4. Support reviews with expanded scope:
   - User-impact risk, false passes, stale suppressions, missing AT pairings, inaccessible error recovery
   - Adversarial scenarios: what could make the test report misleading?
5. Guardian validates with strict criteria:
   - Evidence tags 100% coverage
   - No blanket conformance claim without target/scope/date/technologies/evidence
   - Confidence score is no higher than the evidence coverage supports

## Output

- Exhaustive accessibility testing report with full evidence trail
- Edge cases documented
- Findings ranked by user impact and retest priority
- Suppression and not-verified register
- Confidence score with evidence-based justification
