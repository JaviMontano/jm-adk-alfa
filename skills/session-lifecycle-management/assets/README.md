# Session Lifecycle Management Assets

These assets define deterministic resume/fork/fresh decisions for long-running
agent sessions.

- `staleness-policy.json` defines freshness signals for cached tool results.
- `decision-matrix.json` defines resume/fork/fresh transition rules.
- `typed-summary-policy.json` defines summary fields and stale-drop rules.
- `fork-isolation-policy.json` defines fork scratchpad and workspace isolation.
- `lifecycle-decision-contract.json` defines the machine-readable report shape.
