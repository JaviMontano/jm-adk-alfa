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
| `resources/` | Curated persistent resources: CVs, IDs, URLs, reference documents |
| `personal-skills/` | Canonical private source for user-authored skills |
| `schemas/` | Context schemas and validation references |

## Loading Rule

Start here, then load only the files needed for the current request.

Do not bulk-load `sources/` or `resources/`. Link to source indexes, resource
cards, or specific files only when the current task needs them.

Load a personal skill only when its trigger or an explicit user request requires
it. Never scan all personal skills as default context.
