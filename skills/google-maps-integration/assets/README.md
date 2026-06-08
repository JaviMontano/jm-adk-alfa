# Google Maps Integration Assets

[DOC] These assets encode the offline planning contract for Google Maps Platform web integrations.

## Contents

- [CODE] `maps-platform-plan-schema.json` defines the stable input contract consumed by `scripts/compile-google-maps-plan.py`.
- [CODE] `api-selection-policy.json` maps requirements to Maps JavaScript API, Places API, Geocoding API, Directions API (Legacy), Advanced Markers, and MarkerClusterer decisions.
- [CODE] `api-key-restriction-policy.json` encodes client/server key separation, application restrictions, API restrictions, and monitoring checks.
- [CODE] `data-flow-policy.json` defines Places, Geocoding, and Directions data-flow safeguards.
- [CODE] `marker-accessibility-policy.json` defines marker clustering, advanced marker, map ID, keyboard, and alternate-list expectations.
- [CODE] `billing-quota-risk-checklist.md` captures billing and quota risk checks without monetary amounts.
- [CODE] `human-confirmation-policy.json` blocks external API calls and requires a human confirmation gate for the generated plan.
- [CODE] `maps-platform-plan-template.md` is the deterministic Markdown report template.

## Offline Contract

[CODE] The compiler reads only local JSON, Markdown templates, and fixtures.
[CODE] The compiler does not call Google APIs, Cloud Console, OAuth endpoints, package registries, or any network resource.
