# Read-Only-First Checklist

- [CODE] Identify the target calendar id or confirm `primary`.
- [CODE] List accessible calendars when calendar identity is ambiguous.
- [CODE] Query the relevant event window before mutation.
- [CODE] Confirm write access for create/edit/cancel operations.
- [CODE] For update or cancel, identify the target event id from read-only evidence.
- [CODE] For create, check the requested time window for conflicts or record why conflict checking is unavailable.
- [CODE] Build the proposed payload with timezone, attendees, notifications, and Meet fields visible.
- [CODE] Ask for human confirmation before any mutating MCP tool call.
- [CODE] After mutation, read back the event and verify Calendar response fields.
