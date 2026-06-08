---
name: google-calendar-mcp
author: JM Labs (Javier Montano)
version: 1.0.0
description: >
  Google Calendar integration via MCP — create, manage, and query calendar events
  with Google Meet support, read-only-first safety, timezone handling, attendees,
  confirmation gates, and least-privilege scopes. [EXPLICIT]
  Trigger: "calendar", "schedule", "meeting", "event", "agenda", "google meet",
  "availability", "invite", "conferenceData"
status: production
tags: [mcp, google-calendar, scheduling, automation, google]
mcp-server: workspace-mcp
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__workspace-mcp__list_calendars
  - mcp__workspace-mcp__get_events
  - mcp__workspace-mcp__manage_event
  - mcp__workspace-mcp__manage_out_of_office
---

# Google Calendar MCP

## TL;DR

Use this skill to safely query Google Calendar agendas, check availability, and create, edit, or cancel events through the local `workspace-mcp` server. Always read first, choose the narrowest Calendar scope, preserve timezone evidence, and require human confirmation before any mutating MCP call. Use `scripts/compile-google-calendar-mcp.py` when a structured offline plan is useful. [EXPLICIT]

## Prerequisites

- Google Workspace MCP server configured (see `docs/google-workspace-mcp-setup.md`)
- Google Calendar API enabled in Google Cloud Console
- OAuth2 credentials authenticated
- Environment variable `GOOGLE_WORKSPACE_CREDENTIALS_PATH` set for local `workspace-mcp`

## Procedure

### Step 1: Discover Read-Only Context
- Verify the user intent: agenda query, availability check, create, edit, cancel, or out-of-office.
- Prefer read-only MCP calls first: `mcp__workspace-mcp__list_calendars` and `mcp__workspace-mcp__get_events`.
- Capture the calendar id, event id, date window, timezone, attendees, and whether Google Meet is requested.
- For agenda searches, use bounded `timeMin`/`timeMax`, `singleEvents=true`, and `orderBy=startTime` when available.

### Step 2: Select Minimum Scope
- Availability-only checks use `https://www.googleapis.com/auth/calendar.freebusy`.
- Agenda/event reads use `https://www.googleapis.com/auth/calendar.events.readonly`.
- Create, edit, or cancel operations use `https://www.googleapis.com/auth/calendar.events`.
- App-owned secondary calendar workflows may use `https://www.googleapis.com/auth/calendar.app.created`.
- Avoid broad `calendar` unless the local MCP configuration already has it and a narrower scope is impossible.

### Step 3: Build the Safe Operation
- Use `assets/` as the deterministic policy source:
  - `assets/scope-policy.json` for scope selection.
  - `assets/calendar-event-payload-policy.json` for event fields, timezone, attendees, and notifications.
  - `assets/conference-data-policy.json` for Google Meet and `requestId` handling.
  - `assets/confirmation-policy.json` for human-confirmation gates.
- For structured work, run `scripts/compile-google-calendar-mcp.py --input <operation.json> --output <plan.md>`.
- The compiler renders a plan only; it never calls Calendar or MCP.

### Step 4: Confirm Before Mutation
- Before `mcp__workspace-mcp__manage_event` or `mcp__workspace-mcp__manage_out_of_office`, show the user the exact operation: summary, calendar id, date/time, timezone, attendees, `sendUpdates`, Meet request, and target event id when editing/cancelling.
- Do not create, edit, cancel, add attendees, or send invitations until the user confirms.
- If Google Meet is requested, require `conferenceDataVersion=1` and a fresh `conferenceData.createRequest.requestId` for the new conference request.

### Step 5: Validate Result
- After a real MCP mutation, read back the event and verify `id`, `htmlLink`, start/end, timezone, attendees, and `hangoutLink` or `conferenceData` when Meet was requested.
- Report tool errors as recoverable execution errors when possible; do not hide failed or partial operations.
- Keep evidence tags on claims: `[CODE]`, `[DOC]`, `[INFERENCE]`, or `[ASSUMPTION]`.

## Quality Criteria

- [ ] Read-only-first check completed before mutation.
- [ ] Minimum Calendar scope selected for the operation.
- [ ] Timed events include RFC3339 date-times with offsets and IANA timezone names.
- [ ] Attendee emails and `sendUpdates` policy are explicit before invitations.
- [ ] Google Meet requests include `conferenceDataVersion=1` and `conferenceData.createRequest.requestId`.
- [ ] Human confirmation captured before create/edit/cancel/out-of-office mutation.
- [ ] Result is verified with a read-back when a real MCP mutation occurs.
- [ ] Evidence tags on all claims.

## Anti-Patterns

- Creating events without confirming date/time with user
- Deleting events without explicit confirmation
- Sending calendar invites without user review
- Scheduling over existing events without checking availability
- Calling mutating MCP tools from scripts or fixtures
- Using account default timezone when the request contains a concrete locale or timezone
- Reusing a Meet `requestId` for a different conference request
- Requesting broad Calendar scopes when a narrow scope satisfies the task

## Related Skills

- `gmail-mcp` — send email follow-ups after scheduling
- `google-workspace-apis` — programmatic Calendar API patterns
- `notification-service` — automated reminders

## Usage

- `/google-calendar-mcp` — interactive calendar management.
- "What meetings do I have tomorrow?"
- "Check whether I am free Friday from 2 to 3 PM America/Bogota."
- "Schedule a 45-minute meeting with Ana next Tuesday at 3 PM with Google Meet."
- "Move the portfolio review to Wednesday and keep the same attendees."
- "Cancel the standup on Friday after I confirm the event id."

## Assumptions & Limits

- Requires authenticated Google Workspace MCP server [EXPLICIT]
- Cannot access calendars from non-authenticated accounts [EXPLICIT]
- Scripts compile offline plans and never call Google Calendar or MCP [EXPLICIT]
- A generated Google Meet conference may be asynchronous and should be read back after mutation [EXPLICIT]
- The skill does not bypass user confirmation for mutating operations [EXPLICIT]
