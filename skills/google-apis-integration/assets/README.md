# Google APIs Integration Assets

Local deterministic policy assets for `google-apis-integration`. [CODE]

## Files

- `google-apis-integration-schema.json`: stable input contract and validation fields. [CODE]
- `service-catalog.json`: supported service operations mapped to official Google API surfaces. [DOC]
- `auth-scope-policy.json`: OAuth scope and restricted API-key profiles. [DOC]
- `error-retry-policy.json`: retry, quota, status handling, and idempotency policy. [DOC]
- `consent-secrets-policy.json`: human consent and secret-handling gates. [CODE]
- `test-matrix-policy.json`: required test layers. [CODE]
- `source-map.md`: official references reviewed for this skill. [DOC]
- `google-apis-integration-template.md`: Markdown report template used by the compiler. [CODE]

These assets are read by `scripts/compile-google-apis-integration.py` and are
safe for offline validation. [CODE]
