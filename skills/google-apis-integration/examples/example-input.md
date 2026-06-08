# Example Input

Plan a customer operations dashboard that reads product metrics from Google
Sheets, writes a kickoff brief into Google Docs, schedules a review event in
Google Calendar, renders customer locations with Maps JavaScript, and reads
public YouTube training videos. The implementation must be offline-planned
before any API call, use least-privilege auth, keep secrets out of client code,
and require human consent before any write. [CODE]

Use the structured fixture:

```bash
python3 skills/google-apis-integration/scripts/compile-google-apis-integration.py \
  --input skills/google-apis-integration/scripts/fixtures/google-apis-integration-input.json
```
