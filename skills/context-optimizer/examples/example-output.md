# Context Optimizer Report

## Summary

Active task remains full fidelity at L3. [CONFIG]
Completed PR notes are compressed to L2 with decisions and evidence retained. [CONFIG]
Old brainstorming transcript is deferred because relevance is below eviction threshold and no active dependency exists. [INFERENCIA]
Open blocker decision is kept because it is risk-flagged. [CONFIG]

## Loading Plan

| source | level | relevance | rationale |
|--------|-------|-----------|-----------|
| `skills/workspace-governance/SKILL.md` | L3 | 96 | Active skill contract. [CÓDIGO] |
| `skills/workspace-governance/references/policy.md` | L2 | 88 | Needed as summarized policy until exact clause is requested. [CÓDIGO] |
| Prior merged PR notes | L2 | 42 | Completed context compressed into handoff summary. [INFERENCIA] |
| Old brainstorming transcript | L1 | 15 | Index only; not active. [INFERENCIA] |
| Open blocker decision | L2 | 83 | Risk-flagged unresolved decision retained. [CONFIG] |

## Metrics

- naive_tokens: 104000 [CÓDIGO]
- optimized_tokens: 69000 [INFERENCIA]
- reduction_percent: 34 [INFERENCIA]
- utilization_percent: 54 [INFERENCIA]

## Validation

- At most one L3 source. [CONFIG]
- No risk-flagged source evicted. [CONFIG]
- Compression includes retention summaries. [CONFIG]
- Metrics are computed from explicit counts. [CONFIG]
