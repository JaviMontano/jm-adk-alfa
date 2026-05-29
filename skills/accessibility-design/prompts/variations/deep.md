---
name: accessibility-design-deep
type: variation
version: 2.0.0
description: "Accessibility Design — deep analysis mode. Exhaustive coverage."
---

# Accessibility Design — Deep Mode

## When to Use

Use deep mode when accessible interaction quality matters more than speed:
design-system components, public release blockers, complex custom widgets,
forms, modals, navigation, or multi-step flows.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Load `SKILL.md`, `knowledge/body-of-knowledge.md`, `templates/output.md`, and relevant component/design-system docs.
2. Enumerate each state and interaction, including empty, loading, error, disabled, hover, focus, active, expanded, selected, and success.
3. Produce a WCAG/POUR mapping, semantic/ARIA decision log, keyboard map, focus plan, content/error guidance, contrast/token requirements, and validation matrix.
4. Include reduced-motion, zoom/reflow, forced-color, and sensory-cue considerations when relevant.
5. Mark contrast ratios, assistive technology behavior, or runtime behavior as not verified when evidence is unavailable.

## Output

- Exhaustive deliverable with full evidence trail
- Edge cases documented
- Risk assessment included
- Recommendations with priority ranking
- Confidence score with justification
