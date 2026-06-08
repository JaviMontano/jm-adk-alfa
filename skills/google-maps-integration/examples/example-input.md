# Example Input

[CONFIG] Use `google-maps-integration` to compile an offline Google Maps Platform plan for a web clinic locator.

## Request

[CODE] The app needs an interactive map, clinic search, address autocomplete, geocoding, route directions, 450 clinic markers, custom markers, clustering, consent for current location, and keyboard-accessible non-map results.

## Required Output

[CONFIG] Produce a deterministic Markdown plan using:

```bash
python3 skills/google-maps-integration/scripts/compile-google-maps-plan.py \
  --input skills/google-maps-integration/scripts/fixtures/google-maps-plan-input.json
```

[CONFIG] Do not call Google APIs.
[CONFIG] Do not include monetary prices.
