---
name: accessibility-writing-quick
type: variation
version: 2.0.0
description: "Accessibility Writing quick mode for concise, bounded rewrites."
---

# Accessibility Writing — quick Mode

## When to Use

Use quick mode for a fast rewrite or triage pass on a small amount of content. Quick mode still must mark missing context and avoid invented visual details or exact reading-level claims.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Load skill: `skills/accessibility-writing/knowledge/body-of-knowledge.md`
2. Check guardrails: `references/guardrails/*.json`
3. Execute at quick depth with source item, rewrite, rationale, and not-verified notes
4. Lead -> Support -> Guardian validation
5. Set confidence from source completeness, not from tone

## Output

- Concise reader-facing rewrite
- Small validation table: issue, rewrite, reason, assumption
- Next input needed to move from quick pass to publish-ready review
