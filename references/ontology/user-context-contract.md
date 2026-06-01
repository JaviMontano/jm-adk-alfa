# User Context Contract

`user-context/` is the in-kit repo for durable user context.

It is not a nested git repo and it is not workspace state.

## Identity

The directory is recognized by `user-context/.jm-adk-context.json`.

Agents must treat the marker as the source of identity. The user can add,
remove, or reorganize private files inside `user-context/` without changing the
directory's role.

The marker must declare `kind: jm-adk-user-context`. Private user files,
directory population, and manifest contents are never used as the primary
identity signal.

Personal skills have their own marker at
`user-context/personal-skills/.jm-adk-personal-skills.json`. That marker declares
`kind: jm-adk-personal-skills` and identifies the personal skills area, not a
nested git repo.

## Boundaries

| Area | Purpose | Git policy |
|---|---|---|
| `user-context/` scaffold | Context repo identity, docs, schemas | Tracked |
| `user-context/context/` | Durable user background | Ignored by default |
| `user-context/preferences/` | Stable user preferences | Ignored by default |
| `user-context/memory/` | User-approved long-lived notes | Ignored by default |
| `user-context/sources/` | Private source files or indexes | Ignored by default |
| `user-context/resources/` | Curated persistent resources such as CVs, IDs, URLs, and reference documents | Ignored by default |
| `user-context/personal-skills/skills/` | Canonical private source for user-authored skills | Ignored by default except `.gitkeep` |
| `.local/skills/` | Ignored experiment or copy-mirror cache | Never tracked |
| `workspace/` | Task runtime state and artifacts | Ignored except `.gitkeep` |

## Load Rule

Start with `user-context/_INDICE.md`, then read only the files relevant to the
current task. Never bulk-load `sources/` or `resources/`.

If the index is sparse or missing private entries, treat context as unknown. Do
not infer personal facts from filenames, caches, conversations, or workspace
artifacts.

Personal skills are loaded only when the request or runtime matching requires a
specific skill. Do not scan or load every personal skill by default.

## Write Rule

Write to `user-context/` only after explicit durable-context instructions from
the user. In hook-enabled runtimes, context writes require
`JM_ADK_CONTEXT_WRITE=1`. Task artifacts still go to
`workspace/{active}/artifacts/`.

Create or improve personal skills with:

```bash
python3 scripts/scaffold-skill.py --personal --dry-run
```

Sync copies to runtime skill roots only with:

```bash
python3 scripts/sync-personal-skills.py --dry-run
python3 scripts/sync-personal-skills.py --apply
```

Never write user-authored personal skills into root `skills/`, versioned
`.agent/skills`, or `workspace/`.

Safe examples include durable output preferences, stable project background,
user-approved decisions, curated resource cards, and private personal skills.
Unsafe examples include passwords, tokens, API keys, private keys, credentials,
and unapproved PII exports.

## Diagnostics

Run:

```bash
python3 scripts/diagnose-user-context.py --dry-run
python3 scripts/diagnose-personal-skills.py --dry-run
```

The user-context diagnosis reports `disabled`, `missing`, `ready`, or `degraded`
based on marker presence, location, tracked-private-file safety, manifest
validity, known buckets, and secret-like content in autoload files.

The personal-skills diagnosis reports `missing`, `empty`, `ready`, or `degraded`
based on marker validity, tracked-private-file safety, core slug collisions,
unsafe links, and skill validation.
