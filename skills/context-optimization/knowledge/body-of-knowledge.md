# Context Optimization — Body of Knowledge

## Canon

Context Optimization selects what to load, what to summarize, what to keep in
session state, and what to leave lazy-loaded. It is broader than context-window
budgeting: it governs progressive MOAT loading, skill routing, pruning, and
persistence.

## Loading Levels

| Level | Contents | Use |
|---|---|---|
| L1 | metadata, triggers, summary | routing and exploration |
| L2 | SKILL.md and quality gate | standard operation |
| L3 | references, examples, fixtures | one active focus skill |

## Quality Metrics

| Metric | Target | How to Measure |
|---|---:|---|
| L3 discipline | 100% | At most one L3 skill per plan. |
| Relevance safety | 100% | L3 relevance score is at least 80. |
| Prune safety | 100% | Risk-flagged sources are not pruned. |
| Improvement | >=20% | Optimized tokens versus naive loading. |
| Utilization | <=85% | Optimized tokens divided by max context tokens. |
| Offline validation | 100% | `bash skills/context-optimization/scripts/check.sh` passes. |
