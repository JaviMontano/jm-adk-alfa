# Context Window Management Report

## Token Budget

- Max context tokens: `{max_context_tokens}` `{evidence_tag}`
- Reserved response tokens: `{reserved_response_tokens}` `{evidence_tag}`
- Available context tokens: `{available_context_tokens}` `{evidence_tag}`
- Current estimated tokens: `{current_estimated_tokens}` `{evidence_tag}`
- Post-plan estimated tokens: `{post_plan_estimated_tokens}` `{evidence_tag}`

## Context Items

| ID | Source | Priority | Tokens | Action | Evidence |
|---|---|---|---:|---|---|
| `{id}` | `{source}` | `{priority}` | `{estimated_tokens}` | `{retention_action}` | `{evidence_tag}` |

## Compression Plan

| Source ID | Method | Before | After | Preserves | Evidence |
|---|---|---:|---:|---|---|
| `{source_id}` | `{method}` | `{estimated_tokens_before}` | `{estimated_tokens_after}` | `{preserves}` | `{evidence_tag}` |

## Eviction Plan

| Source ID | Priority | Reason | Evidence |
|---|---|---|---|
| `{source_id}` | `{priority}` | `{reason}` | `{evidence_tag}` |

## Guardian Decision

Decision: `{decision}` `{evidence_tag}`

Rationale: `{rationale}` `{evidence_tag}`
