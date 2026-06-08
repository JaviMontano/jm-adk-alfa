# Skill Review: google-analytics

## Verdict

- [CODE] Status: `dod-complete`.
- [CODE] Scope: one skill only, `skills/google-analytics`.
- [CONFIG] Ledger update intentionally skipped because this task forbids editing `docs/audits/skill-review-ledger.csv`.
- [CODE] Review date: 2026-06-01.

## Primary Sources

- [DOC] GA4 collection overview: https://developers.google.com/analytics/devguides/collection/ga4
- [DOC] GA4 events guide: https://developers.google.com/analytics/devguides/collection/ga4/events
- [DOC] GA4 recommended events reference: https://developers.google.com/analytics/devguides/collection/ga4/reference/events
- [DOC] GA4 Measurement Protocol: https://developers.google.com/analytics/devguides/collection/protocol/ga4
- [DOC] Google Tag Manager web docs: https://developers.google.com/tag-platform/tag-manager/web
- [DOC] Google Tag Platform docs: https://developers.google.com/tag-platform

## DoD Evidence

- [CODE] `assets/manifest.json` lists every local asset and validates asset consumers.
- [CODE] `assets/ga4-gtm-plan-schema.json` defines the stable structured input contract.
- [CODE] `assets/event-taxonomy-policy.json` defines event classes, naming rules, parameter policy, key-event rules, and Measurement Protocol supplement-only guidance.
- [CODE] `assets/privacy-consent-policy.json` defines consent, data redaction, PII, and legal-owner checks.
- [CODE] `assets/tag-mutation-confirmation-policy.json` blocks tag/container/key-event mutation recommendations without human confirmation.
- [CODE] `assets/debug-checklist-policy.json` defines GTM Preview, Tag Assistant, GA4 DebugView, Realtime, network review, and publish gates.
- [CODE] `scripts/compile-google-analytics.py` compiles structured JSON into Markdown without network, OAuth, Google Analytics, GTM, or MCP calls.
- [CODE] `scripts/check.sh` validates a positive fixture plus missing confirmation, invalid event naming, high-risk PII, and Measurement Protocol-only negative fixtures.
- [CODE] `evals/evals.json` contains concrete GA4/GTM cases with `assets`, `deterministic_scripts`, and `quality_criteria` checks.
- [CODE] `README.md`, `SKILL.md`, prompts, agents, examples, knowledge, and templates now contain GA4/GTM-specific content instead of scaffold placeholders.

## Documentation Alignment

- [DOC] GA4 event documentation distinguishes automatic, enhanced measurement, recommended, and custom events; the skill encodes those classes.
- [DOC] GA4 recommended-event guidance is represented by preferring official events such as `sign_up`, `generate_lead`, and ecommerce events when they fit.
- [DOC] Measurement Protocol guidance says it augments existing tagging; the skill blocks `measurement_protocol_only`.
- [DOC] Google Tag Platform guidance makes consent and privacy implementation responsibilities explicit; the skill requires region, CMP, Consent Mode, data redaction, PII policy, and legal owner checks.
- [DOC] GTM web debugging routes through Preview and Tag Assistant; the skill adds those plus GA4 DebugView, Realtime, and browser network review.

## Validation Commands

```bash
python3 -B scripts/validate-skill-dod.py --skill google-analytics
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-analytics
bash skills/google-analytics/scripts/check.sh
python3 -B -m py_compile skills/google-analytics/scripts/*.py
git diff --check
```

## Residual Limits

- [INFERENCE] This review certifies the `google-analytics` skill only.
- [INFERENCE] The deterministic compiler validates a plan/checklist contract; it does not prove live GA4 property, web data stream, GTM container, Google tag, OAuth grant, or account permission state.
- [INFERENCE] Live mutation remains dependent on human confirmation, container workspace state, site deploy process, consent tooling, browser behavior, and Google account permissions.
