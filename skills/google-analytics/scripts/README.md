# Google Analytics Scripts

## `compile-google-analytics.py`

Compiles a structured JSON request into a deterministic offline GA4/GTM measurement plan.

```bash
python3 skills/google-analytics/scripts/compile-google-analytics.py \
  --input skills/google-analytics/scripts/fixtures/google-analytics-input.json
```

## `check.sh`

Runs the positive fixture, verifies expected output fragments, and checks negative fixtures for blocked mutation confirmation, invalid naming, high-risk PII, and Measurement Protocol-only usage.

```bash
bash skills/google-analytics/scripts/check.sh
```

## Offline Contract

- No Google Analytics calls.
- No Google Tag Manager calls.
- No OAuth, MCP, or network calls.
- Local `assets/` and `scripts/fixtures/` are the only inputs.
