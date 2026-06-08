# Error Recovery Automation Scripts

## `validate_error_recovery.py`

Validates a structured JSON recovery plan against the local assets contract.

## `check.sh`

Runs the validator against deterministic fixtures:

- `valid-*.json` must pass.
- `invalid-*.json` must fail.

The check is offline, uses only repository files, and does not mutate tracked
state.
