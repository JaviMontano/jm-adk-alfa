# Workflow Creator Scripts

Deterministic checks for workflow definition specs.

- `validate_workflow_spec.py`: validates a JSON workflow spec against
  `assets/workflow-definition-contract.json`.
- `check.sh`: parses assets and fixtures, then verifies positive and negative
  validation paths.

The scripts are offline and deterministic: they do not use network, system time,
randomness, model calls, or workspace files outside the explicit asset and
fixture paths passed to them.
