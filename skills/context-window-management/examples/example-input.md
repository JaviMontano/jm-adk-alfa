# Example Input

Run `context-window-management` for a `10000` token context window with `1500`
tokens reserved for the response.

Context items:

| ID | Source | Priority | Estimated Tokens |
|---|---|---|---:|
| ctx-001 | active user instructions and branch status | P0 | 1800 |
| ctx-002 | current skill files | P1 | 3200 |
| ctx-003 | related review docs | P2 | 4200 |
| ctx-004 | old examples already summarized | P3 | 2800 |

Return a keep/compress/evict plan that fits the available budget and preserves
IDs, paths, decisions, blockers, validation evidence, and open questions.
