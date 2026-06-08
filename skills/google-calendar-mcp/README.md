# Google Calendar MCP

Google Calendar MCP is the safe scheduling skill for querying agendas, checking availability, and creating, editing, or cancelling Calendar events through the local `workspace-mcp` server.

## Triggers

- calendar, agenda, schedule, scheduling, meeting, event, invite, availability
- Google Calendar, Google Meet, conferenceData, out of office
- create event, edit event, move event, cancel event, list today's meetings

## Allowed Tools

- `Read`
- `Write`
- `Bash`
- `mcp__workspace-mcp__list_calendars`
- `mcp__workspace-mcp__get_events`
- `mcp__workspace-mcp__manage_event`
- `mcp__workspace-mcp__manage_out_of_office`

## Safety Contract

1. Start read-only: list calendars or fetch relevant events before any create, update, or cancel operation.
2. Use the narrowest scope that fits the operation:
   - availability only: `https://www.googleapis.com/auth/calendar.freebusy`
   - agenda/event reading: `https://www.googleapis.com/auth/calendar.events.readonly`
   - create/edit/cancel events: `https://www.googleapis.com/auth/calendar.events`
   - app-created calendars/events only: `https://www.googleapis.com/auth/calendar.app.created`
3. Require explicit human confirmation before calling a mutating MCP tool.
4. Preserve timezone evidence with IANA names and RFC3339 timestamps with offsets.
5. For Google Meet, set `conferenceDataVersion=1` and include `conferenceData.createRequest.requestId`.
6. Scripts in `scripts/` are offline compilers only; they never call Google Calendar or MCP.

## Deterministic Assets

- `assets/google-calendar-operation-schema.json` defines supported operations and required structured fields.
- `assets/scope-policy.json` maps each operation to the minimum recommended Calendar scope.
- `assets/calendar-event-payload-policy.json` documents event payload, timezone, attendee, and notification rules.
- `assets/conference-data-policy.json` documents Google Meet `conferenceData` constraints and request idempotency.
- `assets/confirmation-policy.json` defines human-confirmation gates for mutating operations.
- `assets/read-only-first-checklist.md` is the operational checklist used before MCP mutation.
- `assets/google-calendar-operation-template.md` is rendered by `scripts/compile-google-calendar-mcp.py`.

## Script Contract

Run the offline compiler against structured JSON:

```bash
python3 skills/google-calendar-mcp/scripts/compile-google-calendar-mcp.py \
  --input skills/google-calendar-mcp/scripts/fixtures/google-calendar-mcp-input.json \
  --output /tmp/google-calendar-plan.md
```

Run deterministic checks:

```bash
bash skills/google-calendar-mcp/scripts/check.sh
```

## Output Format

Return Markdown with evidence, selected scope, read-only-first status, human confirmation status, event payload preview, MCP operation plan, validation, and residual risks.
