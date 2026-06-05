---
name: prompt-engineering-deep
type: variation
version: 2.0.0
description: "Prompt Engineering — deep analysis mode. Exhaustive coverage."
---

# Prompt Engineering - Deep Mode

## When to Use

Use deep mode when thoroughness matters more than speed: architecture decisions, security audits, compliance reviews, critical deliverables.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | Yes | User + codebase scan |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Load relevant knowledge: `knowledge/body-of-knowledge.md`, assets matrix, and only task-relevant related skill docs.
2. Check guardrails from `assets/prompt-engineering-checklist.md`.
3. Lead executes with exhaustive analysis:
   - Cover ALL edge cases, not just common path
   - Research only when the user asks or sources are provided; cite source and retrieval date for freshness
   - Document every assumption with `[ASSUMPTION]` tag
4. Support reviews with expanded scope:
   - Security, accessibility, performance, business viability
   - Adversarial scenarios: what could go wrong?
5. Guardian validates with strict criteria:
   - Evidence tags 100% coverage (no untagged claims)
   - Quality gate fully met
   - Deterministic packet validator passes when a JSON packet is produced

## Output

- Exhaustive deliverable with full evidence trail
- Edge cases documented
- Risk assessment included
- Recommendations with priority ranking
- Confidence band with evidence and unresolved gaps
