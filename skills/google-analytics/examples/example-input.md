# Example Input

Compile an offline GA4/GTM measurement plan for a B2B SaaS website that needs:

- GA4 web stream readiness checklist.
- Event taxonomy for `sign_up`, `generate_lead`, and a custom product engagement event.
- Key-event plan for `generate_lead`.
- GTM tag checklist with consent checks.
- Privacy review that excludes email, phone, full name, and form field values from GA4 parameters.
- Debug plan covering GTM Preview, Tag Assistant, GA4 DebugView, Realtime, and browser network review.
- Human confirmation before recommending any tag/container or key-event mutation.

Structured fixture:

```bash
python3 skills/google-analytics/scripts/compile-google-analytics.py \
  --input skills/google-analytics/scripts/fixtures/google-analytics-input.json
```
