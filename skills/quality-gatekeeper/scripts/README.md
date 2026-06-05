# Quality Gatekeeper Scripts

Deterministic report checks for `quality-gatekeeper`.

- `validate_gate_report.py`: validates a JSON gate report against local G0-G3
  criteria, report contract, evidence policy, and score-history schema.
- `check.sh`: parses assets and fixtures, then verifies positive and negative
  validation paths.

The scripts are offline and read only explicit JSON paths supplied to them.
