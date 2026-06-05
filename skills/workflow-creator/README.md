# Workflow Creator

Creates deterministic 17-field workflow definitions for agentic ecosystems.

## Activation

Use this skill when the user asks to create a workflow, define workflow steps,
build workflow YAML, add RACI/KPIs/DoD, or convert an agentic procedure into a
repeatable workflow. Decline generic checklists, one-off plans, and conceptual
questions that do not need the full workflow contract.

## Deterministic Resources

- `assets/workflow-definition-contract.json`: machine-readable contract.
- `assets/activation-policy.json`: activation, decline, and clarification
  rules.
- `assets/quality-gates.json`: blocking quality gates.
- `assets/workflow-output-template.md`: stable output layout.
- `scripts/validate_workflow_spec.py`: offline JSON workflow validator.
- `scripts/check.sh`: positive and negative fixture smoke test.

## Local Checks

```bash
bash skills/workflow-creator/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill workflow-creator
python3 -B scripts/validate-skill-dod.py --skill workflow-creator
```
