# Context Window Management

`context-window-management` creates deterministic keep/compress/evict plans for
large context sets. It protects active instructions and validation evidence while
reducing lower-priority material into verifiable summaries or references.

## Triggers

- `context-window-management`
- `context window management`
- `token budget`
- `context budget`
- `trim context`
- `compress context`
- `preserve before compact`

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Deterministic Assets

| Asset | Purpose |
|---|---|
| `assets/budget-policy.json` | Budget fields and response reserve rules. |
| `assets/priority-policy.json` | P0/P1/P2/P3 retention tiers. |
| `assets/compression-policy.json` | Allowed compression methods and preservation requirements. |
| `assets/eviction-policy.json` | Eviction order and P0 protection. |
| `assets/report-contract.json` | Machine-checkable report schema. |

## Output Format

Return Markdown with:

- token budget
- context items
- compression plan
- eviction plan
- final token estimate
- Guardian decision

Machine-readable reports should pass:

```bash
bash skills/context-window-management/scripts/check.sh
```

## Safety Rules

- Do not evict P0 context.
- Do not compress in a way that loses IDs, paths, decisions, blockers, validation
  evidence, or open questions.
- Do not claim the plan fits if final tokens exceed available budget.
- Do not activate for browser or OS window-management requests.
