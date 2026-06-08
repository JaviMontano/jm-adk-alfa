# Example Input

Use `google-calendar-mcp` to prepare a safe create-event operation:

- Calendar: `primary`
- Meeting: Portfolio review
- Time: 2026-06-03 15:00-15:45 America/Bogota
- Attendees: `ana@example.com`, `javier@example.com`
- Google Meet: required
- Notifications: send to all guests
- Read-only-first evidence: calendars listed, events checked for the time window, no conflicts found
- Human confirmation: confirmed by Javier after reviewing title, time, timezone, attendees, Meet, and notifications
- Required output: Markdown operation plan plus payload preview; do not call Calendar or MCP from scripts
