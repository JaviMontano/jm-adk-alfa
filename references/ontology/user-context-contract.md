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

## Boundaries

| Area | Purpose | Git policy |
|---|---|---|
| `user-context/` scaffold | Context repo identity, docs, schemas | Tracked |
| `user-context/context/` | Durable user background | Ignored by default |
| `user-context/preferences/` | Stable user preferences | Ignored by default |
| `user-context/memory/` | User-approved long-lived notes | Ignored by default |
| `user-context/sources/` | Private source files or indexes | Ignored by default |
| `workspace/` | Task runtime state and artifacts | Ignored except `.gitkeep` |

## Load Rule

Start with `user-context/_INDICE.md`, then read only the files relevant to the
current task. Never bulk-load `sources/`.

If the index is sparse or missing private entries, treat context as unknown. Do
not infer personal facts from filenames, caches, conversations, or workspace
artifacts.

## Write Rule

Write to `user-context/` only after explicit durable-context instructions from
the user. In hook-enabled runtimes, context writes require
`JM_ADK_CONTEXT_WRITE=1`. Task artifacts still go to
`workspace/{active}/artifacts/`.

Safe examples include durable output preferences, stable project background, or
user-approved decisions. Unsafe examples include passwords, tokens, API keys,
private keys, credentials, and unapproved PII exports.

## Diagnostics

Run:

```bash
python3 scripts/diagnose-user-context.py --dry-run
```

The diagnosis reports `disabled`, `missing`, `ready`, or `degraded` based on
marker presence, location, tracked-private-file safety, manifest validity, and
secret-like content in autoload files.
