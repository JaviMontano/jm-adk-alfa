---
name: admin-dashboards-quick
type: variation
version: 2.0.0
description: "Admin Dashboards quick mode for bounded, low-risk admin changes."
---

# Admin Dashboards — quick Mode

## When to Use

Use quick mode for a small, well-scoped admin change where APIs, permissions, states, and acceptance criteria are already known. Do not use quick mode for new dashboards, destructive actions, exports, sensitive data, or unclear RBAC.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Load skill: `skills/admin-dashboards/knowledge/body-of-knowledge.md`
2. Check guardrails: `references/guardrails/*.json`
3. Execute at quick depth with data source, RBAC impact, UI state impact, and test impact
4. Lead -> Support -> Guardian validation
5. Set confidence from evidence coverage

## Output

- Bounded spec or patch plan
- Explicit assumptions and `not verified` gaps
- Minimal no-regression test checklist
