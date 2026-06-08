# Skill Review: google-maps-integration

## Verdict

- [CODE] Status: `dod-complete`.
- [CODE] Scope: one skill only, `skills/google-maps-integration`.
- [CODE] Review date: 2026-06-01.

## Primary Sources

- [DOC] Maps JavaScript API overview: https://developers.google.com/maps/documentation/javascript/overview.
- [DOC] Advanced Markers overview: https://developers.google.com/maps/documentation/javascript/advanced-markers/overview.
- [DOC] Marker clustering: https://developers.google.com/maps/documentation/javascript/marker-clustering.
- [DOC] Geocoding API overview: https://developers.google.com/maps/documentation/geocoding/overview.
- [DOC] Places API overview: https://developers.google.com/maps/documentation/places/web-service/overview.
- [DOC] Directions API overview: https://developers.google.com/maps/documentation/directions/overview.
- [DOC] API security best practices: https://developers.google.com/maps/api-security-best-practices.

## DoD Evidence

- [CODE] `assets/manifest.json` lists every local asset and validates asset consumers.
- [CODE] `assets/maps-platform-plan-schema.json` defines the stable offline input contract.
- [CODE] `assets/api-selection-policy.json` maps requirements to Maps JavaScript API, Places API (New), Geocoding API, Directions API (Legacy), Advanced Markers, and MarkerClusterer.
- [CODE] `assets/api-key-restriction-policy.json` encodes browser/server key separation, application restrictions, API restrictions, and monitoring checks.
- [CODE] `assets/data-flow-policy.json` defines Places, Geocoding, and Directions data-flow controls.
- [CODE] `assets/marker-accessibility-policy.json` defines map ID, marker clustering, keyboard, marker title, and alternate-list checks.
- [CODE] `assets/billing-quota-risk-checklist.md` covers billing/quota exposure without monetary prices.
- [CODE] `assets/human-confirmation-policy.json` enforces offline/no-network and human-confirmation gates.
- [CODE] `scripts/compile-google-maps-plan.py` compiles a deterministic Markdown plan from local JSON and local assets only.
- [CODE] `scripts/check.sh` validates a positive fixture and negative fixtures for missing confirmation, missing browser referrers, and monetary-amount language.
- [CODE] `evals/evals.json` includes nine concrete cases and the required `assets`, `deterministic_scripts`, and `quality_criteria` checks.
- [CODE] `README.md`, `SKILL.md`, agents, prompts, knowledge, examples, and templates contain Google Maps Platform-specific content instead of scaffold placeholders.

## Documentation Alignment

- [DOC] Maps JavaScript API supports interactive web maps, markers, custom data layers, Places library usage, and JavaScript map services; the skill selects it for web map and marker requirements.
- [DOC] Advanced Markers require a map ID and support click and keyboard interaction; the skill gates advanced markers behind `map_id_required=true` and accessibility checks.
- [DOC] Marker clustering uses `@googlemaps/markerclusterer` with Maps JavaScript API to group nearby markers; the skill requires it for dense marker plans.
- [DOC] Geocoding API converts addresses, coordinates, and place IDs; the skill requires input normalization, caching policy, and redaction.
- [DOC] Places API (New) supports search, autocomplete, details, place IDs, and selected fields; the skill requires session tokens and field minimization.
- [DOC] Directions API is in Legacy status; the skill requires explicit legacy acknowledgement and flags newer routing evaluation as a residual risk.
- [DOC] API security guidance recommends API key restrictions, separate keys per app, checking key usage, and matching application restrictions to platform type; the skill encodes browser referrer and server IP restriction checks.

## Validation Commands

```bash
python3 -B scripts/validate-skill-dod.py --skill google-maps-integration
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-maps-integration
bash skills/google-maps-integration/scripts/check.sh
python3 -B -m py_compile skills/google-maps-integration/scripts/*.py
git diff --check
```

## Residual Limits

- [INFERENCE] This review certifies `google-maps-integration` only.
- [INFERENCE] The deterministic compiler renders safe plans; real implementations still require Cloud Console verification, browser testing, accessibility testing, and privacy/legal review.
- [INFERENCE] Directions API remains Legacy, so new production route features should evaluate newer routing services before implementation.
- [CONFIG] No commit and no push were performed.
