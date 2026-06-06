# Context Optimizer Assets

These assets define deterministic context-budget decisions for active sessions.

- `loading-level-policy.json` defines L1/L2/L3 promotion rules.
- `token-budget-policy.json` defines token-count and utilization math.
- `compression-policy.json` defines retention-summary requirements.
- `eviction-policy.json` defines sources that must never be evicted.
- `optimizer-report-contract.json` defines the machine-readable report shape.

`scripts/check.sh` validates the same contract offline against deterministic fixtures.
