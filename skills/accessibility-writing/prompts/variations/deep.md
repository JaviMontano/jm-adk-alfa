---
name: accessibility-writing-deep
type: variation
version: 2.0.0
description: "Accessibility Writing — deep analysis mode with full content inventory and evidence boundaries."
---

# Accessibility Writing — Deep Mode

## When to Use

Use deep mode when thoroughness matters more than speed: public pages, onboarding flows, support docs, legal-adjacent disclosures, multi-locale content, or content with images, charts, forms, and error states.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Load focused knowledge: `knowledge/body-of-knowledge.md` plus only cross-referenced skills needed for routing decisions
2. Check guardrails: `references/guardrails/*.json`
3. Lead executes with exhaustive analysis:
   - Inventory every content item, image, chart, link, error, instruction, heading, and locale-sensitive phrase
   - Preserve meaning, warnings, legal constraints, brand terms, and code/API names
   - Document every missing source, unmeasured reading claim, and unverifiable visual detail as `not verified`
4. Support reviews with expanded scope:
   - Cognitive load, inclusive language, localization, source fidelity, user recovery, and publishability
   - Adversarial scenarios: what could mislead, exclude, over-simplify, or overclaim?
5. Guardian validates with strict criteria:
   - No evidence tags inside final reader-facing copy unless requested
   - No invented image/chart details or exact reading-level claims without measurement
   - Confidence score is capped by missing source context

## Output

- Full content inventory and accessible rewrite
- Alt text and long-description decisions
- Plain-language, inclusive-language, link, instruction, and error-copy tables
- Not-verified register and publication risks
- Confidence score with source-completeness justification
