# Constitution Compliance Scripts

Deterministic report checks for `constitution-compliance`.

- `validate_constitution_report.py`: validates a JSON compliance report against
  the local Constitution v6.0.0 principle map, report contract, and severity
  policy.
- `check.sh`: parses assets and fixtures, then verifies positive and negative
  validation paths.

The scripts are offline and read only explicit JSON paths supplied to them.
