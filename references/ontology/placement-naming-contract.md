# Placement & Naming Contract

> Single source of truth for *where files go* and *how they are named*. Enforced
> deterministically by `scripts/artifact-placement-guard.sh` (PreToolUse) +
> `references/guardrails/placement-policy.json`. Every agent (Claude Desktop,
> Claude Code, Claude Cowork, Gemini, Antigravity, Codex, Visual Studio, Cursor,
> Windsurf) obeys this — it is not advisory.

## Placement — classify every write by DESTINATION, never by prompt intent

| Bucket | Destination | Rule |
|---|---|---|
| **Task artifact** | `workspace/{active}/artifacts/**` + canonical (`plan.md`, `tasklog.md`, `changelog.md`, `.workspace.json`) | Allowed. This is where deliverables live. |
| **User context repo** | `user-context/**` | Allowed only for explicit durable-context updates (`JM_ADK_CONTEXT_WRITE=1`) or maintainer mode. Identified by `user-context/.jm-adk-context.json`. |
| **Kit internal** | `skills/`, `agents/`, `commands/`, `prompts/`, `scripts/`, `references/`, `docs/`, `hooks/`, root `*.md`/`*.json` | Allowed **only** in maintainer mode (`JM_ADK_MODE=maintainer` or `./.maintainer`). |
| **Ad-hoc** | anywhere else (repo root junk, invented dirs, task-root non-canonical) | **Blocked**; routed to `workspace/{active}/artifacts/`. No active workspace → run `workspace-manager.sh ensure "<task>"`. |

**No mixing.** System files, durable user context, and user deliverables never
share a directory. Generated deliverables go to `artifacts/`; task scaffolding
(`plan.md`/`tasklog.md`/…) stays at task root; durable context goes to
`user-context/` only after explicit user instruction.

## Naming — kebab-case, concise, mnemonic, queryable

- Format: `^[a-z0-9]+(-[a-z0-9]+)*$`, lowercase extension. Accents transliterated (`á→a`, `ñ→n`).
- Slugs (dirs/workspaces): drop ES+EN stopwords + leading filler verbs, dedupe, ≤5 words, ≤40 chars, preserve intent order. `scripts/lib/naming.sh slugify "<text>"` is the only generator.
- Filename validation runs on **new files only** (existing names are never broken).
  Non-kebab new file → blocked with a suggested name.
- Allowlist (exempt): `CLAUDE.md README.md SKILL.md AGENTS.md GEMINI.md CODEX.md MEMORY.md TAREAS.md _INDICE.md _ESTRUCTURA.md _DASHBOARD.md LICENSE`, `_TEMPLATE-*`, dotfiles, `*.gitkeep`.

## For agents without hooks (Gemini, Codex, Visual Studio, Cursor, Windsurf, Antigravity)

The guard cannot run in your runtime. Apply this contract manually: before writing,
pick the destination bucket and a kebab-case name. When in doubt, write to
`workspace/{active}/artifacts/` with a slugified filename.
