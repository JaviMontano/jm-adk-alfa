# Workflow Creator Assets

Deterministic assets for creating and validating 17-field workflow definitions.

- `workflow-definition-contract.json`: required top-level fields, step fields,
  RACI/KPI rules, cadence values, and placeholder blockers.
- `activation-policy.json`: activation, decline, clarification, and network
  rules.
- `quality-gates.json`: fail-closed gates for workflow quality.
- `workflow-output-template.md`: canonical Markdown and YAML output order.

Use these assets before finalizing a workflow spec, then run
`scripts/validate_workflow_spec.py` when a JSON representation is available.
