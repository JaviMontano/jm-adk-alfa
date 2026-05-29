---
name: accessibility-testing-quick
type: variation
version: 2.0.0
description: "Accessibility Testing quick mode with explicit evidence limits."
---

# Accessibility Testing — quick Mode

## When to Use

Use quick mode for a fast accessibility smoke test or triage pass. Quick mode must still separate `pass`, `fail`, and `not verified`; speed does not permit unsupported compliance claims.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Load skill: `skills/accessibility-testing/knowledge/body-of-knowledge.md`
2. Check guardrails: `references/guardrails/*.json`
3. Execute at quick depth with a minimum scope table, automated scan plan or result, keyboard smoke script, and not-verified register
4. Lead -> Support -> Guardian validation
5. Set confidence from evidence coverage, not from optimism

## Output

- Concise accessibility testing report calibrated to quick depth
- Evidence-tagged pass/fail/not-verified status
- Next test needed to graduate from smoke coverage to release evidence
