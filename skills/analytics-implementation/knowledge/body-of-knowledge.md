# Analytics Implementation Body of Knowledge

## Canon

Analytics implementation is an engineering handoff for measurement infrastructure. It connects GA4/Firebase setup, custom event contracts, conversions, user properties, BigQuery export, dashboards, consent/privacy handling, and QA.

## GA4 And Firebase

- Define property/app, data streams, platforms, owners, and validation method.
- Validate events in DebugView or an equivalent debug receipt before marking conversions.
- Keep custom event names lower snake_case and under platform limits.
- Use stable ids and safe properties rather than raw personal data.

## BigQuery Export

- Enable export before claiming warehouse readiness.
- Define dataset owner, location, retention, partitioning, and PII handling.
- Validate at least one expected event row after export is enabled.

## Dashboards

- Dashboards require data source, metrics, owner, freshness, and validation.
- Looker Studio readiness is not the same as dashboard visual design.
