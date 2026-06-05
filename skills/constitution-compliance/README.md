# Constitution Compliance

Validates artifacts against JM-ADK Constitution v6.0.0 using all 18 principles,
G0-G3 gate impact, evidence tags, severity, remediation, and missing-evidence
handling.

## Activation

Use this skill for constitutional audit, Pristino governance validation,
pre-delivery compliance, and gate checks. Route Constitution viewing or
amendment to `/jm-adk:constitution`.

## Deterministic Resources

- `assets/constitution-v6-principles.json`: 18 principles and G0-G3 gates.
- `assets/compliance-report-contract.json`: required report shape.
- `assets/severity-policy.json`: P0-P3 severity and block policy.
- `assets/activation-policy.json`: activation, false-positive, and version-drift
  rules.
- `scripts/validate_constitution_report.py`: offline report validator.
- `scripts/check.sh`: deterministic fixture checks.

## Local Checks

```bash
bash skills/constitution-compliance/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill constitution-compliance
python3 -B scripts/validate-skill-dod.py --skill constitution-compliance
```
