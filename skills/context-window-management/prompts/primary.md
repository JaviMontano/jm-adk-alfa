---
name: context-window-management-primary
type: execution
version: 2.0.0
description: "Execute deterministic Context Window Management workflow."
triad:
  lead: "context-window-management-lead"
  support: "context-window-management-support"
  guardian: "context-window-management-guardian"
---

# Context Window Management — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|---|---|---:|---|
| `{{task}}` | Context budgeting request | Yes | User input |
| `{{context_items}}` | Source IDs and token estimates | Yes | User or codebase |
| `{{max_context_tokens}}` | Maximum context window | Yes | Runtime or user |
| `{{reserved_response_tokens}}` | Response-token reserve | Yes | Runtime or user |

## Execution

1. Confirm activation through `SKILL.md ## When to Activate`.
2. Load budget, priority, compression, and eviction policies from `assets/`.
3. Inventory context items with stable IDs and token estimates.
4. Classify priority and assign keep/compress/evict actions.
5. Validate budget arithmetic and final fit.
6. Block P0 eviction, expanding compression, missing estimates, and over-budget plans.
7. Return the Markdown report using `templates/output.md`.
8. When a JSON report is produced, validate it with
   `scripts/validate_context_window_report.py`.
