# _INDICE.md · User Context

This index is intentionally sparse. Add links to user-approved context files as
they are created locally.

Identity is defined by `.jm-adk-context.json`. The private files listed here may
change, move, or be absent without changing this directory's role as the Alfa
context repo.

| Area | Purpose |
|---|---|
| `context/` | Durable background and reusable user context |
| `preferences/` | Stable preferences for output, tooling, autonomy, and privacy |
| `memory/` | Long-lived notes explicitly approved by the user |
| `sources/` | Private source files or source indexes |
| `schemas/` | Context schemas and validation references |

## Loading Rule

Start here, then load only the files needed for the current request.

Do not bulk-load `sources/`. Link to source indexes or specific files only when
the current task needs them.
