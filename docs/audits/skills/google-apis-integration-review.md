# Google APIs Integration Skill Review

## Status

- [CODE] DoD hardening completed for `skills/google-apis-integration`.
- [CODE] Scope of edits is limited to `skills/google-apis-integration/**` and this review file.
- [CODE] The skill now includes deterministic `assets/`, `scripts/`, fixtures, templates, examples, evals, prompts, agents, and knowledge files.

## Source Basis

- [DOC] OAuth 2.0 overview: https://developers.google.com/identity/protocols/oauth2
- [DOC] Workspace error guide requested by task returned 404 during verification: https://developers.google.com/workspace/guides/handle-errors
- [DOC] Error policy fallback source, Drive API error guide: https://developers.google.com/workspace/drive/api/guides/handle-errors
- [DOC] Error policy fallback source, Calendar API error guide: https://developers.google.com/workspace/calendar/api/guides/errors
- [DOC] Sheets REST reference: https://developers.google.com/workspace/sheets/api/reference/rest
- [DOC] Docs REST reference: https://developers.google.com/workspace/docs/api/reference/rest
- [DOC] Calendar API v3 reference: https://developers.google.com/calendar/api/v3/reference
- [DOC] Maps JavaScript API overview: https://developers.google.com/maps/documentation/javascript/overview
- [DOC] Maps JavaScript API key guide: https://developers.google.com/maps/documentation/javascript/get-api-key
- [DOC] YouTube Data API v3 reference: https://developers.google.com/youtube/v3/docs
- [DOC] YouTube authorization guide: https://developers.google.com/youtube/v3/guides/authentication

## Review Notes

- [CODE] `scripts/compile-google-apis-integration.py` reads local assets and fixtures only.
- [CODE] The compiler emits Markdown by default and stable JSON when `--format json` is passed.
- [CODE] Positive fixture covers Sheets write, Docs write, Calendar event insert, Maps JavaScript browser load, and YouTube public read.
- [CODE] Negative fixtures cover missing consent, broad scope for a read operation, and missing idempotency for mutation.
- [CODE] `templates/output.html` is offline-safe and does not import external fonts or scripts.

## Residual Limits

- [INFERENCE] The compiler cannot prove enabled APIs, live OAuth consent screen state, account ACLs, quota allocation, billing, or production resource existence.
- [INFERENCE] Live implementation still needs sandbox integration tests and read-back verification outside this offline skill.
