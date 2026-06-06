# Example Output

## Optimization Target

- Task: implementation [CONFIG]
- Max context tokens: 24000 [CONFIG]
- Target utilization: 85 percent [CONFIG]

## Skill Loading Plan

| Skill | Level | Relevance | Rationale |
|---|---|---:|---|
| context-window-management | L3 | 95 | Active focus for budget plan. |
| session-protocol | L2 | 82 | Needed for session state continuity. |
| tasklog-management | L1 | 55 | Referenced only for task status summary. |
| seo-technical | L1 | 20 | Candidate remains lazy-loaded. |

## Pruning Plan

- `seo-technical` remains `lazy-load` because relevance is low and no current
  task depends on full content. [INFERENCE]

## Session State Plan

- Persist level: `essential` [CONFIG]
- Target path: `project/session-state.json` [CONFIG]
- Fields: active phase, focused skill, loaded levels, unresolved risks [CONFIG]

## Metrics

- Naive tokens: 30000 [CODE]
- Optimized tokens: 18000 [CODE]
- Utilization: 75 percent [CODE]
- Improvement: 40 percent [CODE]

## Guardian Decision

Decision: `pass` [CONFIG]

Rationale: one L3 skill, no risky prune, authorized essential persistence, and
improvement exceeds 20 percent. [CODE]
