---
name: pre-compact-context-meta
type: self-improvement
version: 2.1.0
description: "Evaluate and improve deterministic context preservation before compaction."
---

# Pre Compact Context - Self-Improvement

## Evaluate

1. Do recent packets preserve hard rules, blockers, and next action as P0?
2. Are DROP decisions safe and explained?
3. Do fixtures reject dropped P0 items and missing rehydration prompts?
4. Are secrets redacted instead of copied verbatim?
5. Are source gaps marked `[OPEN]` rather than invented?

## Improve

1. Add deterministic fixtures for every repeated context-loss failure.
2. Tighten `assets/retention-policy.json` before adding new prose rules.
3. Update the rehydration checklist when resume failures recur.
4. Keep scripts offline and free of wall-clock, network, or random inputs.

## Trigger

Run this meta-prompt when a compacted thread resumes poorly, loses hard rules,
or cannot identify the next action.
