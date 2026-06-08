# Example Output

## Summary

- [CODE] Operation: `create_event`.
- [CODE] Calendar: `primary`.
- [CODE] Event: Portfolio review, 2026-06-03T15:00:00-05:00 to 2026-06-03T15:45:00-05:00, `America/Bogota`.
- [CODE] Attendees: `ana@example.com`, `javier@example.com`.
- [CODE] Google Meet: requested with `conferenceDataVersion=1`.

## Scope

- [DOC] Minimum selected scope: `https://www.googleapis.com/auth/calendar.events`.
- [DOC] Narrower read-only scopes are insufficient because this operation creates an event.

## Read-Only-First

- [CODE] Calendars listed before mutation.
- [CODE] Events checked for the requested time window.
- [CODE] Conflicts: none reported by the fixture.

## Human Confirmation

- [CODE] Status: `confirmed`.
- [CODE] Confirmation text covered title, date/time, timezone, attendees, Meet, and notifications.

## Payload Preview

```json
{
  "calendarId": "primary",
  "sendUpdates": "all",
  "conferenceDataVersion": 1,
  "resource": {
    "summary": "Portfolio review",
    "start": {
      "dateTime": "2026-06-03T15:00:00-05:00",
      "timeZone": "America/Bogota"
    },
    "end": {
      "dateTime": "2026-06-03T15:45:00-05:00",
      "timeZone": "America/Bogota"
    },
    "attendees": [
      {"email": "ana@example.com"},
      {"email": "javier@example.com"}
    ],
    "conferenceData": {
      "createRequest": {
        "requestId": "portfolio-review-20260603-1500-bogota",
        "conferenceSolutionKey": {"type": "hangoutsMeet"}
      }
    }
  }
}
```

## Validation

- [CODE] Offline compiler rendered this plan without calling Google Calendar or MCP.
- [CODE] Mutating MCP call remains gated by human confirmation.
- [INFERENCE] After a real create call, read back the event to verify `htmlLink`, attendees, timezone, and Meet data.
