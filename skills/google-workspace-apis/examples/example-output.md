# Example Output

## Summary

[CODE] The workflow uses Sheets read, Docs create/update, Drive upload, Gmail
draft, and Calendar event creation in a read-only-first sequence.

## Evidence

- [CODE] Spreadsheet, Drive folder, Calendar ID, and recipient domain are named
  as resource identifiers.
- [DOC] Service methods map to official Google Workspace REST resources.
- [CONFIG] Mutations require `human_consent.status=confirmed`.

## Result

The plan starts with Sheets and Drive read checks, then compiles document and
draft payloads offline. Docs, Drive, Gmail, and Calendar writes are gated by
confirmation and stable idempotency keys.

## Validation

- Static schema validation passes.
- Positive fixture renders the expected service matrix.
- Negative fixtures reject broad scopes, missing consent, and writes without
  read-before-write.
- Live validation is limited to read-only probes until the owner confirms.

## Risks and Limits

[INFERENCE] OAuth grants, API enablement, quota, billing, and live resource
permissions still require provider-side checks outside the offline compiler.
