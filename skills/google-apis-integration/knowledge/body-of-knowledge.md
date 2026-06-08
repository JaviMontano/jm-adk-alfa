# Google APIs Integration - Body of Knowledge

## Canon

This skill plans integrations across Google Sheets API v4, Docs API v1,
Calendar API v3, Maps JavaScript API, and YouTube Data API v3 using official
Google API references and deterministic local assets. [DOC]

## Auth Model

- Google APIs that access private user data use OAuth 2.0 with explicit scopes. [DOC]
- Sheets, Docs, Calendar, and YouTube user-data operations are modeled as OAuth
  profiles in `assets/auth-scope-policy.json`. [CODE]
- Maps JavaScript browser loading is modeled as a restricted API-key profile,
  not an OAuth scope. [DOC]
- Public YouTube reads can use an API key profile; YouTube uploads and
  authenticated mutations require OAuth scopes. [DOC]

## Service Operation Model

| Service | Read Operations | Mutating Operations | Credential Family |
|---|---|---|---|
| Sheets | `spreadsheets.get`, `spreadsheets.values.get` | `spreadsheets.batchUpdate`, `spreadsheets.values.batchUpdate` | OAuth 2.0 |
| Docs | `documents.get` | `documents.create`, `documents.batchUpdate` | OAuth 2.0 |
| Calendar | `events.list`, `freebusy.query` | `events.insert`, `events.patch`, `events.delete` | OAuth 2.0 |
| Maps JavaScript | `maps.load_js_api`, libraries and browser render operations | none in this skill contract | restricted API key |
| YouTube | `search.list`, `videos.list` | `playlists.insert`, `playlistItems.insert`, `videos.insert` | API key or OAuth 2.0 |

## Safety Gates

- Mutations require consent, read-before-write evidence, retry policy, and
  idempotency key. [CODE]
- Broad scopes require an explicit escalation reason and are blocked for
  read-only operations by the compiler. [CODE]
- Secrets must not be committed, embedded in static HTML, or sent to clients
  except for restricted browser API keys where the official API model requires
  client-side key loading. [CODE]

## Error And Quota Handling

- `400` errors are modeled as user or request fixes, not blind retries. [DOC]
- `401` errors trigger token refresh and then re-authentication if refresh fails. [DOC]
- `403` and `429` errors require quota/rate-limit handling and exponential
  backoff when the reason is recoverable. [DOC]
- `5xx` errors use bounded exponential backoff with jitter. [DOC]
- Mutating retries must be tied to idempotency keys or resource-level
  deduplication evidence. [CODE]

## Quality Metrics

| Metric | Target | How to Measure |
|---|---:|---|
| Asset coverage | 100% | `assets/manifest.json` references existing files |
| Script determinism | 100% | `bash scripts/check.sh` uses local fixtures only |
| Scope fit | 100% | compiler rejects broad scope for read-only operations |
| Consent gate | 100% | compiler rejects unconfirmed mutating plans |
| Test matrix coverage | 7 layers | `assets/test-matrix-policy.json` required layers |

## References

Primary source map lives in `assets/source-map.md`. [CODE]
