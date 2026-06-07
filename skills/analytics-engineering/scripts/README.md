# Analytics Engineering Scripts

`validate_analytics_engineering.py` validates structured analytics engineering JSON handoffs against the static policies in `../assets/`.

## Commands

```bash
bash skills/analytics-engineering/scripts/check.sh
python3 -B skills/analytics-engineering/scripts/validate_analytics_engineering.py skills/analytics-engineering/scripts/fixtures/valid-revenue-mart.json
```

The check script is deterministic. It accepts every `valid-*.json` fixture and requires every `invalid-*.json` fixture to fail.
