# Google Analytics Assets

Deterministic offline resources for the `google-analytics` skill.

## Contents

- `manifest.json` lists every asset and its consumers.
- `ga4-gtm-plan-schema.json` defines the stable structured input contract.
- `event-taxonomy-policy.json` defines event naming, event classes, parameter rules, and key-event planning rules.
- `privacy-consent-policy.json` defines GA4 privacy, consent, data redaction, and PII checks.
- `tag-mutation-confirmation-policy.json` defines the human-confirmation gate before tag/container mutation recommendations.
- `debug-checklist-policy.json` defines GTM Preview, Tag Assistant, GA4 DebugView, and Realtime checks.
- `ga4-gtm-plan-template.md` renders the Markdown report compiled by the offline script.
- `source-map.md` records official source references used to update this skill.

## Contract

- Scripts may read these files and local fixtures only.
- Scripts must not call Google Analytics, Google Tag Manager, Google APIs, OAuth, MCP, or the network.
- Mutating tag/container recommendations must remain blocked until human confirmation is explicit.
