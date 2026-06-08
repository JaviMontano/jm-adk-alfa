# Google Maps Integration — Body of Knowledge

## Canon

- [DOC] Maps JavaScript API is the client-side web API for interactive maps, map styling, markers, custom data layers, and Maps JavaScript services.
- [DOC] Advanced Markers support customizable marker UI, DOM click events, keyboard interaction, custom HTML/CSS, and require a map ID.
- [DOC] Marker clustering uses `@googlemaps/markerclusterer` with Maps JavaScript API to group nearby markers for dense map views.
- [DOC] Geocoding API converts addresses, coordinates, or place IDs into coordinates, place IDs, or human-readable addresses.
- [DOC] Places API (New) supports place search, autocomplete, place details, place IDs, and selected fields.
- [DOC] Directions API is marked Legacy and returns route information between locations with origins, destinations, waypoints, travel mode, legs, and steps.
- [DOC] Google Maps Platform API security guidance recommends restricting API keys with one application restriction and one or more API restrictions.
- [DOC] Google Maps Platform API security guidance recommends separate keys per app and split client-side/server-side usage when platform types differ.

## Offline Planning Contract

- [CODE] `assets/maps-platform-plan-schema.json` is the stable input contract.
- [CODE] `scripts/compile-google-maps-plan.py` compiles a local Markdown plan from schema-compliant JSON.
- [CONFIG] The script is offline and rejects `operations.external_api_calls=true`.
- [CONFIG] The script rejects monetary amounts because this skill covers billing/quota risk without prices.
- [CODE] Positive and negative fixtures live under `scripts/fixtures/`.

## API Selection Rules

| Requirement | Selection | Evidence |
|-------------|-----------|----------|
| `interactive_map` | Maps JavaScript API | [DOC] Client-side web maps and markers. |
| `advanced_markers` | Advanced Markers | [DOC] Requires map ID and supports keyboard/click interaction. |
| `dense_markers` | `@googlemaps/markerclusterer` | [DOC] Groups nearby markers and simplifies dense displays. |
| `location_search` or `place_details` | Places API (New) | [DOC] Search, autocomplete, details, and place IDs. |
| `address_geocoding` or `reverse_geocoding` | Geocoding API | [DOC] Address/coordinate/place ID conversion. |
| `route_directions` | Directions API (Legacy) | [DOC] Route data; Legacy status must be acknowledged. |

## Security And Privacy

- [DOC] Browser keys should use website/referrer restrictions for JavaScript platform traffic.
- [DOC] Server-side web-service keys should not share browser key usage and should use server-appropriate application restrictions.
- [CODE] Each selected service must appear in `api_restrictions` on at least one appropriate key.
- [CONFIG] Precise location collection requires consent, retention policy, redaction policy, and human confirmation.
- [CODE] Places data flow should store place IDs and derived data where possible instead of broad raw payloads.
- [CODE] Geocoding flow should normalize input and cache results instead of re-requesting on each page load.

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Schema compliance | 100% | [CODE] Compiler accepts positive fixture and rejects invalid fixtures. |
| Evidence coverage | 100% | [CODE] Output sections use evidence tags. |
| Offline determinism | 100% | [CODE] Script uses local files only. |
| Security coverage | 100% | [DOC] Key restriction plan includes app and API restrictions. |
| Accessibility coverage | 100% | [CODE] Map summary, keyboard path, marker titles, and list alternative are present. |

## References

- [DOC] Maps JavaScript API overview: https://developers.google.com/maps/documentation/javascript/overview
- [DOC] Advanced Markers overview: https://developers.google.com/maps/documentation/javascript/advanced-markers/overview
- [DOC] Marker clustering: https://developers.google.com/maps/documentation/javascript/marker-clustering
- [DOC] Geocoding API overview: https://developers.google.com/maps/documentation/geocoding/overview
- [DOC] Places API overview: https://developers.google.com/maps/documentation/places/web-service/overview
- [DOC] Directions API overview: https://developers.google.com/maps/documentation/directions/overview
- [DOC] API security best practices: https://developers.google.com/maps/api-security-best-practices
