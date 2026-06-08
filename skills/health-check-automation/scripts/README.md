# Health Check Automation Scripts

## `validate_health_check.py`

Validates a structured JSON health-check report against the local assets
contract.

## `check.sh`

Runs deterministic fixtures:

- `valid-*.json` must pass.
- `invalid-*.json` must fail.

The check is offline and uses only files inside this skill.
