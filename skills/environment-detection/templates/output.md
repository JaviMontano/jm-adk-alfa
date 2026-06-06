# Environment Detection Report

## Summary

Environment: `{ide}` | Model tier: `{model_tier}` | Triad mode: `{triad_mode}` | Status: `{status}`

## Signals

| id | kind | source | value | evidence |
|----|------|--------|-------|----------|
| `{signal_id}` | `{kind}` | `{source}` | `{value}` | `{evidence_tag}` |

## Decisions

| decision | evidence ids | status |
|----------|--------------|--------|
| `{decision}` | `{evidence_ids}` | `{status}` |

## Loading Plan

| resource | level | reason |
|----------|-------|--------|
| `{resource}` | `{level}` | `{reason}` |

## Validation

Required checks: `signals_have_evidence`, `mode_matches_capabilities`, `tier_matches_budget`, `loading_plan_bounded`.

## Risks and Limits

List missing signals, conflicts, unknown model budget, or conservative fallbacks.
