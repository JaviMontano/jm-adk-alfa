# Google Calendar MCP Primary Prompt

## Objective

Handle Google Calendar operations through `workspace-mcp` with read-only-first discovery, least-privilege scope selection, explicit timezone handling, attendee review, Google Meet `conferenceData` safety, and human confirmation before mutation.

## Required Inputs

- Operation type: agenda query, freebusy check, create event, update event, cancel event, or out-of-office.
- Calendar id, or permission to discover calendars.
- Time window with timezone.
- Event payload fields for mutation: summary, start, end, attendees, `sendUpdates`, Meet preference, reminders, recurrence if any.
- Target event id for edit/cancel.
- Human confirmation for any mutating operation.

## Process

1. Read calendars/events before mutation.
2. Select the minimum Calendar scope from `assets/scope-policy.json`.
3. Compile or inspect the safe operation payload.
4. Show tool inputs and ask for confirmation before `manage_event`.
5. Execute only after confirmation when the runtime MCP is available.
6. Read back the result and report evidence, validation, and risks.

## Output

Return Markdown with evidence, scope, read-only-first status, confirmation status, payload preview, MCP operation plan, validation, and residual risks.
