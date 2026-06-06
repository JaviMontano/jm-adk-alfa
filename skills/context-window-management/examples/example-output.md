# Example Output

## Token Budget

- Max context tokens: 10000 [CONFIG]
- Reserved response tokens: 1500 [CONFIG]
- Available context tokens: 8500 [CODE]
- Current estimated tokens: 12000 [CODE]
- Post-plan estimated tokens: 7800 [CODE]

## Context Items

| ID | Source | Priority | Tokens | Action | Evidence |
|---|---|---|---:|---|---|
| ctx-001 | active instructions and branch status | P0 | 1800 | keep | [CODE] |
| ctx-002 | current skill files | P1 | 3200 | keep | [CODE] |
| ctx-003 | related review docs | P2 | 4200 | structured-summary | [INFERENCE] |
| ctx-004 | old examples already summarized | P3 | 2800 | evict | [INFERENCE] |

## Compression Plan

- `ctx-003`: structured-summary from 4200 to 2800 tokens, preserving IDs, paths,
  decisions, blockers, validation evidence, and open questions. [CONFIG]

## Eviction Plan

- `ctx-004`: evict P3 historical examples because equivalent summary already
  exists and no active decision depends on the full text. [INFERENCE]

## Guardian Decision

Decision: `pass` [CONFIG]

Rationale: P0 is kept, compression reduces tokens, eviction targets P3 only, and
the final estimate fits the available budget. [CODE]
