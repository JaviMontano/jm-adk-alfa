# Subagent Orchestration Assets

These assets define the deterministic contract for hub-and-spoke subagent orchestration plans.

## Inventory

- `manifest.json`: declares every asset and where it is used.
- `orchestration-contract.json`: required JSON report shape.
- `isolation-policy.json`: fresh-session and last-message-only requirements.
- `error-propagation-policy.json`: typed spoke error and valid-empty semantics.
- `aggregation-policy.json`: partial-failure and coverage-gap requirements.
- `anti-pattern-policy.json`: blocked designs.
- `model-tool-policy.json`: deterministic model/tool assignment guidance.

## Offline Rule

Use `scripts/validate_orchestration_plan.py` before treating an orchestration plan as ready.
