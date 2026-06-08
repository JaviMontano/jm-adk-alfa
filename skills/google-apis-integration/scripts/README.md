# Google APIs Integration Scripts

These scripts are offline and deterministic. They read local assets and JSON
fixtures only; they never call Google APIs, OAuth endpoints, HTTP, network, or
MCP tools. [CODE]

## Compiler

```bash
python3 skills/google-apis-integration/scripts/compile-google-apis-integration.py \
  --input skills/google-apis-integration/scripts/fixtures/google-apis-integration-input.json \
  --output /tmp/google-apis-integration-plan.md
```

```bash
python3 skills/google-apis-integration/scripts/compile-google-apis-integration.py \
  --format json \
  --input skills/google-apis-integration/scripts/fixtures/google-apis-integration-input.json
```

## Check

```bash
bash skills/google-apis-integration/scripts/check.sh
```

The check validates the positive fixture, JSON output schema, expected report
fragments, and negative fixtures for missing consent, broad scope, and missing
idempotency. [CODE]
