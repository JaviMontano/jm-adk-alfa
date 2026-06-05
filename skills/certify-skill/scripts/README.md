# Certify Skill Scripts

Deterministic report checks for `certify-skill`.

- `validate_certification_report.py`: validates a JSON certification report
  against local phase/check inventory, report contract, evidence policy, and
  certification level formulas.
- `check.sh`: parses assets and fixtures, then verifies positive and negative
  validation paths.

The scripts are offline and read only explicit JSON paths supplied to them.
