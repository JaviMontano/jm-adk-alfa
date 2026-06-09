# katas-adaptive-investigation Assets

These assets define the deterministic contract for Kata 19 reports.

- `adaptive-investigation-report-contract.json` defines required report fields.
- `exploration-budget-policy.json` defines hard budget accounting.
- `replan-gate-policy.json` defines when a re-plan is allowed.
- `evidence-policy.json` defines evidence tags and source requirements.
- `scratchpad-policy.json` defines persisted state requirements.

The offline validator in `scripts/validate_adaptive_investigation_report.py`
uses these assets as the local acceptance contract.
