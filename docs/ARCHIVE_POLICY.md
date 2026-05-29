# Archive Policy

## Purpose

Local process evidence can inform Alfa, but it must not become runtime instruction by accident.

## Archive-Only Inputs

- Screenshots.
- UX snapshots.
- Transcripts.
- Logs.
- Temporary reports.
- Build audits.
- Backups.
- Zips.
- Generated semantic nodes with degraded or placeholder status.

## Migration Rule

If process evidence contains a durable rule, migrate only the rule to the correct owner artifact and record the source in `docs/audits/`. Do not copy the full source into runtime docs.

## Owner Artifacts

- Runtime behavior: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `CODEX.md`, `ANTIGRAVITY.md`.
- Operational guide: `docs/`.
- Reusable capability: `skills/`.
- Responsibility: `agents/`.
- User entrypoint: `commands/`.
- Executable check: `scripts/` or `evals/`.
