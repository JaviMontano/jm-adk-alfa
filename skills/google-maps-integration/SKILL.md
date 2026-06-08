---
name: google-maps-integration
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Produces deterministic offline Google Maps Platform integration plans for
  Maps JavaScript API, Advanced Markers, marker clustering, Geocoding API,
  Places API, and Directions API (Legacy).
  Trigger: "Google Maps", "maps API", "geocoding", "Places API", "Directions API", "markers"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Google Maps Integration

## TL;DR

[DOC] Produces an offline plan/checklist for location-aware web applications that need interactive maps, custom markers, marker clustering, location search, geocoding, route directions, privacy controls, and API key restrictions.
[CONFIG] The primary script is `scripts/compile-google-maps-plan.py`; it reads local assets/fixtures only and never calls Google APIs.

## Procedure

### Step 1: Discover

- [CODE] Identify requested features: `interactive_map`, `location_search`, `address_geocoding`, `reverse_geocoding`, `route_directions`, `dense_markers`, `advanced_markers`, and `place_details`.
- [CODE] Check `assets/maps-platform-plan-schema.json` before drafting or compiling a plan.
- [DOC] Use Maps JavaScript API for client-side interactive web maps, markers, custom data layers, and JavaScript map services.
- [DOC] Use Advanced Markers when marker customization, DOM click, keyboard interaction, or HTML/CSS marker content is required.
- [DOC] Use MarkerClusterer when dense marker sets need grouping and zoom-dependent simplification.

### Step 2: Analyze

- [DOC] Select APIs using `assets/api-selection-policy.json`.
- [DOC] Treat Places API (New) as the default Places web-service path and minimize returned fields.
- [DOC] Treat Geocoding API as the address/coordinate/place ID conversion path and cache normalized results where allowed.
- [DOC] Treat Directions API as `Legacy`; require explicit legacy acknowledgement and evaluate newer routing services before production.
- [DOC] Apply `assets/api-key-restriction-policy.json`: separate browser/server keys, one application restriction per key, and API restrictions only for selected services.
- [CONFIG] Do not include monetary prices, currency amounts, or per-request amounts in the plan.

### Step 3: Execute

- [CODE] Fill a JSON input matching `assets/maps-platform-plan-schema.json`.
- [CODE] Run `python3 skills/google-maps-integration/scripts/compile-google-maps-plan.py --input <fixture-or-input.json> --output <plan.md>`.
- [CODE] Include API selection, key restrictions, billing/quota risk checklist, Places/Geocoding/Directions data flow, marker clustering, accessibility, privacy, and human-confirmation gate.
- [CONFIG] Keep `operations.offline_plan_only=true` and `operations.external_api_calls=false`.
- [CONFIG] Require `human_confirmation.status=confirmed` before treating the plan as ready.

### Step 4: Validate

- [CODE] Run `bash skills/google-maps-integration/scripts/check.sh`.
- [CODE] Run `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-maps-integration`.
- [CODE] Run `python3 -B scripts/validate-skill-dod.py --skill google-maps-integration`.
- [CODE] Confirm all generated output claims keep evidence tags.

## Quality Criteria

- [ ] [CODE] `assets/manifest.json` lists every local asset and its consumer files.
- [ ] [CODE] The compiler is deterministic, offline, and validated by positive and negative fixtures.
- [ ] [DOC] API selection covers Maps JavaScript API, Advanced Markers, MarkerClusterer, Places API, Geocoding API, and Directions API (Legacy) when triggered.
- [ ] [DOC] API keys are separated by browser/server runtime with application and API restrictions.
- [ ] [CONFIG] Billing/quota risk is checked without monetary prices.
- [ ] [CODE] Accessibility includes keyboard paths, marker titles/accessibility names, map summary, and non-map location list.
- [ ] [CONFIG] Privacy includes consent, retention, redaction, and human confirmation.

## Anti-Patterns

- [DOC] Unrestricted API key exposed to browser traffic.
- [DOC] Browser and server web-service traffic sharing one key.
- [CODE] Geocoding the same address on every page load instead of using a cache policy.
- [CODE] Requesting broad Places fields when the feature needs only ID, display name, formatted address, or location.
- [CONFIG] Producing live API calls from this skill.
- [CONFIG] Including monetary prices in the plan.

## Related Skills

- [INFERENCE] `google-apis-integration` covers broader backend Google API patterns.
- [INFERENCE] `vanilla-javascript` can implement Maps JavaScript API without framework wrappers.
- [INFERENCE] `responsive-design` can support responsive map containers and mobile interaction.
- [INFERENCE] `performance-architecture` can support lazy loading and marker density decisions.

## Usage

Example invocations: [EXPLICIT]

- "/google-maps-integration" — Run the full google maps integration workflow
- "google maps integration on this project" — Apply to current context


## Assumptions & Limits

- [SUPUESTO] Assumes the user can supply requirements as structured JSON or enough context to produce that JSON.
- [CONFIG] Does not call Google APIs, validate real credentials, enable services, or inspect Cloud Console.
- [INFERENCE] Real implementation still needs browser testing, Cloud Console verification, accessibility testing, and privacy/legal review.

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | [CODE] Produce a gap list against `assets/maps-platform-plan-schema.json`. |
| Directions requested | [DOC] Require `directions_legacy_acknowledged=true` and flag Legacy status. |
| Dense marker set | [DOC] Require MarkerClusterer and an alternate list/table. |
| Precise user location | [CONFIG] Require consent, retention, redaction, and human confirmation. |
| API call requested | [CONFIG] Refuse live call and produce offline plan only. |
