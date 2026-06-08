# Runtime Routing

Route agentic work across Claude, Codex, Gemini, Antigravity, VS Code, and local adapters with explicit validation limits.

## Use It For

- Choosing the runtime for a repo task when Codex, Claude, Gemini, Antigravity, VS Code, MCP, hooks, or local adapters have different capabilities.
- Recording which capability claims are verified, pending, or unsupported.
- Selecting the lowest-permission runtime that can complete the task.
- Producing a local-first fallback when runtime support is uncertain.

## Deterministic Contract

The canonical JSON report is defined in `assets/runtime-routing-contract.json`. A valid report includes evidence, capability matrix, recommendation, fallback, validation flags, and Guardian decision.

## Validation

```bash
bash skills/runtime-routing/scripts/check.sh
```

The check executes valid fixtures and rejects invalid mutations for missing evidence, unsupported recommendations, hidden validation limits, missing fallback, and inconsistent Guardian decisions.
