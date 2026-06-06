# Context Optimizer Report

## Summary

Active task: `{active_task}`
Status: `{validation_status}`

## Context Snapshot

| max tokens | current tokens | target utilization |
|------------|----------------|--------------------|
| `{max_tokens}` | `{current_tokens}` | `{target_utilization_percent}` |

## Loading Plan

| source | level | relevance | rationale |
|--------|-------|-----------|-----------|
| `{source_id}` | `{level}` | `{relevance_score}` | `{rationale}` |

## Compression Plan

| artifact | action | before | after | retention summary |
|----------|--------|--------|-------|-------------------|
| `{artifact_id}` | `{action}` | `{current_tokens}` | `{optimized_tokens}` | `{retention_summary}` |

## Eviction Safety

List sources deferred or evicted, with risk flags and evidence tags.

## Metrics

Report token reduction and utilization from explicit counts.
