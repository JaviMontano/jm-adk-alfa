# Billing And Quota Risk Checklist

- [DOC] Confirm that billing ownership, quota ownership, and monitoring ownership are assigned.
- [DOC] Configure budget alerts and quota alerts before exposing public map traffic.
- [DOC] Review API key usage by credential before tightening or rotating a key.
- [DOC] Restrict keys to selected APIs only and disable unused services.
- [CODE] Define application-side rate limits for autocomplete, geocoding, and route requests.
- [CODE] Cache geocoding outputs instead of re-requesting on every page load.
- [CODE] Use Places session tokens for autocomplete sessions.
- [CONFIG] Do not include monetary prices, currency amounts, or per-request amounts in the skill output.
- [INFERENCE] Treat sudden traffic increases, missing referrer restrictions, and shared browser/server keys as billing exposure risks.
