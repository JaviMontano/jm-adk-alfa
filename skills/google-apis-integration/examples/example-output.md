# Example Output

## Summary

- [CODE] Project: `Customer Operations Dashboard`.
- [CODE] Services planned: Sheets, Docs, Calendar, Maps JavaScript, YouTube.
- [CODE] Mutating operations: 3.
- [CODE] Consent gate: `confirmed`.
- [CODE] Output mode: deterministic offline plan.

## Service Operation Checklist

- [DOC] Sheets uses `spreadsheets.values.batchUpdate` with `drive.file` scope for app-opened file mutation.
- [DOC] Docs uses `documents.batchUpdate` with `drive.file` scope after document inspection.
- [DOC] Calendar uses `events.insert` with `calendar.events` scope and invitation review.
- [DOC] Maps JavaScript uses a browser API key restricted to approved referrers and APIs.
- [DOC] YouTube uses public read API-key access for `search.list`.

## Validation

- [CODE] The compiler rendered the plan from local assets and fixtures only.
- [CODE] The plan includes consent, secrets, retry/idempotency, quota, operation, and test-matrix checks.
- [INFERENCE] Live API execution must still verify enabled APIs, account access, quotas, and project policy.
