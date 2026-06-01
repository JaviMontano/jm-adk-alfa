# AGENTS.md · JM-ADK User Context

This directory is the user's durable context repo inside Alfa.

The role of this directory comes from `.jm-adk-context.json`, not from the
private files the user may add later. Agents must keep recognizing it as the
context repo as long as the marker declares `jm-adk-user-context`.

## Identity

- Context repo marker: `.jm-adk-context.json`
- Personal skills marker: `personal-skills/.jm-adk-personal-skills.json`
- Scope: durable user context, preferences, memory, resources, personal skills,
  and private sources
- Not scope: task artifacts, generated deliverables, secrets, credentials,
  workspace runtime state, or SDK core skills

## Read Rules

1. Read `_INDICE.md` first.
2. Read only the context files relevant to the current task.
3. Do not bulk-load `sources/` or `resources/`.
4. Load a personal skill only when the user's request or runtime matching needs
   that specific skill.
5. Treat absent context as unknown, not as permission to infer.
6. Prefer indexed, task-relevant files over broad memory loading.

## Write Rules

1. Write here only when the user explicitly asks to remember, update, or add
   durable context.
2. Do not store credentials, tokens, API keys, private keys, or passwords.
3. Keep private user-authored content untracked unless the user explicitly
   chooses otherwise.
4. Personal skills go under `personal-skills/skills/`, never root `skills/`.
5. Task artifacts belong in `workspace/{active}/artifacts/`, not here.
6. In hook-enabled runtimes, context writes require `JM_ADK_CONTEXT_WRITE=1`.

## Personal Skills

Create or improve personal skills with `python3 scripts/scaffold-skill.py --personal`.
Validate them with `python3 scripts/validate-skills.py --strict --skills-dir user-context/personal-skills/skills`.
Sync them with `python3 scripts/sync-personal-skills.py --dry-run` before `--apply`.

`.local/skills/` is only an ignored experiment or mirror cache.

## Evidence

When using this context, cite the specific local file that informed the answer.

## Safe Example

A safe context card can describe a durable preference such as preferred output
language or review style. A safe resource card can point to a private CV or URL
without exposing it in git. It must not include passwords, tokens, API keys,
private keys, or credentials.
