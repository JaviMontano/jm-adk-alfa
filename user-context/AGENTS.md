# AGENTS.md · JM-ADK User Context

This directory is the user's durable context repo inside Alfa.

The role of this directory comes from `.jm-adk-context.json`, not from the
private files the user may add later. Agents must keep recognizing it as the
context repo as long as the marker declares `jm-adk-user-context`.

## Identity

- Context repo marker: `.jm-adk-context.json`
- Scope: durable user context, preferences, memory, and private sources
- Not scope: task artifacts, generated deliverables, secrets, credentials, or
  workspace runtime state

## Read Rules

1. Read `_INDICE.md` first.
2. Read only the context files relevant to the current task.
3. Do not bulk-load `sources/`.
4. Treat absent context as unknown, not as permission to infer.
5. Prefer indexed, task-relevant files over broad memory loading.

## Write Rules

1. Write here only when the user explicitly asks to remember, update, or add
   durable context.
2. Do not store credentials, tokens, API keys, private keys, or passwords.
3. Keep private user-authored content untracked unless the user explicitly
   chooses otherwise.
4. Task artifacts belong in `workspace/{active}/artifacts/`, not here.
5. In hook-enabled runtimes, context writes require `JM_ADK_CONTEXT_WRITE=1`.

## Evidence

When using this context, cite the specific local file that informed the answer.

## Safe Example

A safe context card can describe a durable preference such as preferred output
language or review style. It must not include passwords, tokens, API keys,
private keys, or credentials.
