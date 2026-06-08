# Example Output

## Summary

- [CODE] The compiled plan uses `hybrid` GA4/GTM implementation mode.
- [CODE] The event taxonomy includes `sign_up`, `generate_lead`, and `demo_video_progress`.
- [CODE] `generate_lead` is the only key-event candidate in the fixture.
- [CODE] The plan requires human confirmation before live tag/container/key-event mutation recommendations.

## Evidence

- [DOC] GA4 collection overview: https://developers.google.com/analytics/devguides/collection/ga4
- [DOC] GA4 events guide: https://developers.google.com/analytics/devguides/collection/ga4/events
- [DOC] GA4 recommended events reference: https://developers.google.com/analytics/devguides/collection/ga4/reference/events
- [DOC] GA4 Measurement Protocol: https://developers.google.com/analytics/devguides/collection/protocol/ga4
- [DOC] Google Tag Platform docs: https://developers.google.com/tag-platform
- [DOC] Google Tag Manager web docs: https://developers.google.com/tag-platform/tag-manager/web

## Event Taxonomy

| Event | Type | Surface | Goal |
|---|---|---|---|
| `sign_up` | recommended | GTM GA4 event tag | Measure account creation |
| `generate_lead` | recommended | GTM GA4 event tag | Measure qualified lead form submissions |
| `demo_video_progress` | custom | gtag | Measure high-intent product engagement |

## Key-Event Plan

| Event | Reason | Owner |
|---|---|---|
| `generate_lead` | Lead submission is the primary business action | growth-analytics |

## Human Confirmation Gate

- [CODE] Required phrase prefix: `CONFIRM GA4/GTM MUTATION:`.
- [CODE] Mutation recommendations remain blocked until confirmation is retained with the plan.

## Validation

- [CODE] `bash skills/google-analytics/scripts/check.sh` validates the positive fixture and negative fixtures for missing confirmation, invalid naming, high-risk PII, and Measurement Protocol-only usage.
- [CODE] The compiler performs no network, OAuth, Google Analytics, GTM, or MCP calls.

## Risks And Limits

- [INFERENCE] The offline plan does not prove that a GA4 property, GTM container, or web tag exists.
- [INFERENCE] Live execution still depends on account access, site access, consent tooling, workspace state, and human confirmation.
