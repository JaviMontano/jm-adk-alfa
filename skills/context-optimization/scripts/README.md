# Context Optimization Scripts

Validates JSON Context Optimization reports offline.

```bash
bash skills/context-optimization/scripts/check.sh
```

The check accepts valid standard and lazy-load reports, then rejects two-L3,
low-relevance-L3, risky-prune, no-improvement, and unauthorized-persist reports.
