# AI Assisted Testing Assets

These assets define the deterministic operating contract for AI Assisted Testing.

Use them to keep generated tests reviewable, bounded, and evidence-backed:

- `test-taxonomy-policy.json` defines allowed test types and required fields.
- `evidence-policy.json` defines evidence tags and reference rules.
- `fuzzing-policy.json` defines bounded fuzzing limits and safety gates.
- `mutation-policy.json` defines baseline and mutation-survivor requirements.
- `coverage-policy.json` defines measurable coverage target requirements.
- `assisted-testing-plan-contract.json` defines the machine-readable plan shape.

The runtime validator in `scripts/validate_ai_assisted_testing_plan.py` enforces
the same contract against deterministic JSON fixtures.
