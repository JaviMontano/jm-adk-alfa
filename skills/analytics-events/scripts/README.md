# Analytics Events Scripts

`validate_analytics_events.py` validates structured analytics event taxonomy and tracking plan JSON handoffs against the static policies in `../assets/`.

## Commands

```bash
bash skills/analytics-events/scripts/check.sh
python3 -B skills/analytics-events/scripts/validate_analytics_events.py skills/analytics-events/scripts/fixtures/valid-product-activation.json
```

The check script accepts every `valid-*.json` fixture and requires every `invalid-*.json` fixture to fail.
