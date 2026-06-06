# Context Optimization

`context-optimization` designs deterministic loading, pruning, compression, lazy
loading, and session-state strategies for token-efficient agent work.

## Triggers

- `context-optimization`
- `optimize context`
- `reduce token usage`
- `prune context window`
- `configure progressive loading`
- `manage session state`

## Allowed Tools

- Read
- Write
- Edit
- Glob
- Grep
- Bash

## Deterministic Assets

| Asset | Purpose |
|---|---|
| `assets/loading-level-policy.json` | L1/L2/L3 definitions and one-L3 limit. |
| `assets/relevance-policy.json` | Relevance score thresholds and promotion rules. |
| `assets/pruning-policy.json` | Safe prune/compress/lazy-load decisions. |
| `assets/session-state-policy.json` | Persistence levels and authorization. |
| `assets/optimization-report-contract.json` | Machine-checkable report schema. |

## Output Format

Return Markdown with optimization target, skill loading plan, pruning plan,
session-state plan, metrics, and Guardian decision.

```bash
bash skills/context-optimization/scripts/check.sh
```

## Safety Rules

- Do not load more than one skill at L3.
- Do not prune sources with risk flags.
- Do not persist session state without authorization.
- Do not claim success unless utilization is within target and improvement is at
  least 20 percent versus naive loading.
