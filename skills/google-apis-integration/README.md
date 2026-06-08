# Google APIs Integration

Offline planner for integrations that combine Google Sheets API v4, Docs API
v1, Calendar API v3, Maps JavaScript API, and YouTube Data API v3. [DOC]

## Triggers

- google-apis-integration
- google api integration
- multi google api
- sheets docs calendar maps youtube
- oauth scopes

## What It Produces

- A deterministic Markdown or JSON integration plan. [CODE]
- Service-by-service auth and scope checklist. [CODE]
- Quota, error, retry, and idempotency checklist. [CODE]
- Secrets and consent gates before mutating operations. [CODE]
- API-specific operation notes and test matrix. [CODE]

## Offline Compiler

```bash
python3 skills/google-apis-integration/scripts/compile-google-apis-integration.py \
  --input skills/google-apis-integration/scripts/fixtures/google-apis-integration-input.json
```

```bash
python3 skills/google-apis-integration/scripts/compile-google-apis-integration.py \
  --format json \
  --input skills/google-apis-integration/scripts/fixtures/google-apis-integration-input.json
```

The compiler reads local `assets/` and fixture JSON only. It does not call
Google APIs, OAuth endpoints, HTTP, network, or MCP tools. [CODE]

## Validation

```bash
bash skills/google-apis-integration/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill google-apis-integration
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-apis-integration
```

## Output Format

Use `templates/output.md` for Markdown reports and `templates/output.html` for
offline HTML rendering. [CODE]
