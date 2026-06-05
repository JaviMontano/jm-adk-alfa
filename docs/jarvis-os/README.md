# Jarvis OS on Alfa — Capability Pack

Maps the **Trabajar Amplificado / MetodologIA Personal Jarvis OS** method
(`playbook.html` + `runbook.html`, both in this folder) onto Alfa skills,
agents, and scripts.

- Umbrella skill: `skills/jarvis-os/` (COOL, 5 sectors, 12 levels, 8 capabilities).
- Orchestrator: `agents/jarvis-orchestrator.md`.
- Verification tags: `references/verification-tags.md`.
- Operator's private context: `user-context/` (local-private, not tracked).

## Two streams

- **Stream A (this pack, tracked):** generic, reusable capabilities — foundation skills, cadence skills, scaffolders, orchestrator, scripts, docs.
- **Stream B (operator, local-private):** identity, brand routing, Jarvis OS index, preferences, personal skill instances — under `user-context/`.

## Prompt → Alfa component map (P00–P45)

| Prompt(s) | Purpose | Alfa component |
|---|---|---|
| P00 / P01 / P02 | Bootstrap root CLAUDE.md, MEMORY.md, structure | `skills/jarvis-bootstrap`, `scripts/scaffold-jarvis-os.py` |
| P03 / P04 | Voice extraction | `user-context/context/` (operator) `{POR_CONFIRMAR}` |
| P05 / P23 / P24 / P40–P43 | Create stations (universal + dedicated) | `skills/station-create` |
| P06 | Create dedicated station | `skills/station-create` |
| P07 | Create project `P-NNN` | `skills/project-create` |
| P08 | Create Lab session (4 files) | `skills/lab-session` |
| P09 | Daily planning (DBR) | `skills/dbr-daily-plan` |
| P10 | Daily close | `skills/daily-close` |
| P11 | Weekly review (WBR) | `skills/wbr-weekly-review` |
| P12 | Weekly retro | `skills/weekly-retro` |
| P13 | Quarterly review (QBR) | `skills/qbr-quarterly` |
| P14 | Skill from conversation (rule of 3) | `scripts/scaffold-skill.py` |
| P15 / P26 | Validate connectors / config | `scripts/validate-mcp-config.py` |
| P22 | Monthly audit (6 questions) | `skills/monthly-audit` |
| P32 | TAREAS.md by level | `skills/project-create` / `station-create` (NOW ≤ 3) |
| P33 | Sub-task `T-NNN` | `skills/task-subfolder` |
| P34 | Decompose CLAUDE.md (Rule-9) | `skills/jarvis-os` (size limits) |
| P35 | Slot external plugin as mirror | `user-context/personal-skills/_INDICE.md` (sync topology) |
| P36 | Excellence Loop (10 criteria) | `skills/excellence-loop` (core) |
| P16–P21 / P37 / P38 | Capability practices | `skills/jarvis-os` (8 capabilities) |
| P39 / P45 | Supervised scheduled tasks | scheduled-tasks (CAP 07), 14-day trial |
| P44 | Vibe-code mini-app | level 8 (mini-apps) |
| Foundation F1.1–F1.4 | input-analysis, revisor-veracidad, frontload-prompt, cierre-conversacion | `skills/input-analysis` (reuse) + 3 new |

## Quick start

```bash
# Scaffold a fresh Jarvis OS structure at a destination
python3 scripts/scaffold-jarvis-os.py --dest "/path/to/jarvis" --dry-run
python3 scripts/scaffold-jarvis-os.py --dest "/path/to/jarvis" --apply

# Import an EXISTING Jarvis OS tree into Alfa's user-context (re-syncable mirror,
# local-private/gitignored; excludes .git/.obsidian/.codex). --source is required.
python3 scripts/import-jarvis-context.py --source "/path/to/your/jarvis" --dry-run
python3 scripts/import-jarvis-context.py --source "/path/to/your/jarvis" --apply

# Health check
python3 scripts/jarvis-status.py --root "/path/to/jarvis"
```

Imported content lands under `user-context/jarvis-os/` and is loaded per
`user-context/jarvis-os/_ALFA-BRIDGE.md` (rule-stacking, no bulk-load, PII-safe).

Sources: playbook + runbook at https://javimontano.github.io/trabajar-amplificado/ `[DOC]`.
