# Google Maps Integration

[DOC] Deterministic offline planning skill for Google Maps Platform web integrations.

## Triggers

- [CONFIG] `google-maps-integration`
- [CONFIG] `Google Maps`
- [CONFIG] `maps API`
- [CONFIG] `geocoding`
- [CONFIG] `Places API`
- [CONFIG] `Directions API`
- [CONFIG] `markers`

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Quick Use

[CODE] Use this skill when a project needs a Maps Platform plan/checklist before implementation.
[CODE] The main offline compiler is:

```bash
python3 skills/google-maps-integration/scripts/compile-google-maps-plan.py \
  --input skills/google-maps-integration/scripts/fixtures/google-maps-plan-input.json \
  --output /tmp/google-maps-platform-plan.md
```

[CONFIG] The compiler reads local assets and fixtures only.
[CONFIG] The compiler does not call Google APIs, Cloud Console, OAuth, package registries, or external URLs.

## Local Assets

- [CODE] `assets/maps-platform-plan-schema.json` defines the stable input schema.
- [CODE] `assets/api-selection-policy.json` maps requirements to Maps JavaScript API, Places API, Geocoding API, Directions API (Legacy), Advanced Markers, and MarkerClusterer.
- [CODE] `assets/api-key-restriction-policy.json` defines browser/server key separation and restrictions.
- [CODE] `assets/data-flow-policy.json` defines Places, Geocoding, and Directions data-flow controls.
- [CODE] `assets/marker-accessibility-policy.json` defines map UI and accessibility checks.
- [CODE] `assets/billing-quota-risk-checklist.md` defines billing/quota risk checks without monetary prices.
- [CODE] `assets/human-confirmation-policy.json` defines the offline/human-confirmation gate.

## Validation

```bash
python3 -B scripts/validate-skill-dod.py --skill google-maps-integration
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-maps-integration
bash skills/google-maps-integration/scripts/check.sh
python3 -B -m py_compile skills/google-maps-integration/scripts/*.py
```

## Output Format

[CODE] Markdown and HTML templates include summary, evidence, API selection, key restrictions, data flow, marker clustering, accessibility, privacy, billing/quota risk checklist, human confirmation, and residual risks.
