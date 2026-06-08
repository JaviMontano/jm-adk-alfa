# Example Output

## Summary

- [CODE] Project: `clinic-locator`.
- [INFERENCE] Selected APIs: Maps JavaScript API, Places API (New), Geocoding API, Directions API (Legacy).
- [INFERENCE] Selected map libraries/features: Advanced Markers, `@googlemaps/markerclusterer`.
- [CONFIG] Output is an offline plan only; no external API calls are performed.

## API Key Restrictions

- [CODE] `browser-maps-key` uses HTTP referrer restrictions and authorizes Maps JavaScript API.
- [CODE] `server-location-key` uses IP restrictions and authorizes Places API, Geocoding API, and Directions API.
- [DOC] API security guidance recommends one application restriction and one or more API restrictions per key.

## Data Flow

- [CODE] Places uses session tokens and selected fields: `id`, `displayName`, `formattedAddress`, `location`.
- [CODE] Geocoding caches normalized address results and redacts raw addresses from logs.
- [DOC] Directions API is Legacy, so the plan requires explicit legacy acknowledgement.

## Marker, Accessibility, Privacy

- [DOC] Advanced Markers require a map ID and support keyboard/click interaction.
- [DOC] MarkerClusterer groups dense markers and simplifies map display.
- [CODE] The same clinic results are available in a keyboard-accessible list.
- [CONFIG] Precise location requires consent and human confirmation.

## Validation Checklist

- [CODE] Positive fixture compiles.
- [CODE] Missing confirmation fixture fails.
- [CODE] Unrestricted browser key fixture fails.
- [CODE] Monetary amount fixture fails.
