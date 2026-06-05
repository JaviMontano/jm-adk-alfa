# Assets

These assets make `assembly-skill` deterministic.

## Files

- `mode-policy.json`: exact mode selection ranges, phase set, side-effect rules, and fallback behavior.
- `assembly-report-contract.json`: machine-readable Assembly Report requirements.
- `assembly-report-template.md`: canonical Markdown report skeleton.
- `phase-gate-checklist.md`: human-readable Gate A/B/C closure checklist.

Use these assets before reporting a pipeline result, then validate the report with `scripts/validate_assembly_contract.py`.
