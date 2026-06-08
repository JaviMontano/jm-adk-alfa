# Google Analytics

## Purpose

`google-analytics` produces offline GA4/GTM measurement plans with event taxonomy, key-event planning, consent/privacy checks, tag/container checklists, debug gates, and human confirmation before mutation.

## Triggers

- google analytics
- GA4
- GTM
- Google Tag Manager
- event tracking
- key events
- conversion tracking
- Measurement Protocol
- DebugView
- Tag Assistant

## Deterministic Resources

- `assets/ga4-gtm-plan-schema.json` defines the structured input contract.
- `assets/event-taxonomy-policy.json` defines taxonomy, naming, parameter, Measurement Protocol, and key-event rules.
- `assets/privacy-consent-policy.json` defines privacy and consent checks.
- `assets/tag-mutation-confirmation-policy.json` defines the human-confirmation gate.
- `assets/debug-checklist-policy.json` defines debug and publish checks.
- `scripts/compile-google-analytics.py` compiles Markdown plans offline.
- `scripts/check.sh` runs deterministic fixture checks.

## Quick Use

```bash
python3 skills/google-analytics/scripts/compile-google-analytics.py \
  --input skills/google-analytics/scripts/fixtures/google-analytics-input.json
```

## Output Format

Markdown or HTML with summary, evidence, property checklist, measurement strategy, event taxonomy, parameter contract, key-event plan, tag/container plan, privacy/consent checks, debug checklist, confirmation gate, validation, and residual risks.
