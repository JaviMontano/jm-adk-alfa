---
name: first-use-onboarding
version: 1.0.0
description: "First-use and cold-start onboarding for JM-ADK after clone, greeting, or missing task context."
owner: "JM Labs"
triggers:
  - first-use
  - onboarding
  - cold-start
  - hola
  - buenas
  - hello
  - hey
  - empecemos
allowed-tools:
  - Read
  - Grep
  - Glob
---

# First Use Onboarding

## When To Use

- User sends only a greeting or no concrete task.
- Alfa is freshly cloned or lacks `.jm-adk.local.json`.
- There is no active task, issue, backlog, spec, or workspace context.
- The user asks what Alfa can do before starting work.

## When Not To Use

- User gives an explicit technical task; use micro-context and proceed.
- Repo cannot be confirmed as Alfa; stop with `Dato requerido`.
- User only asks a narrow factual question that does not need setup.

## Inputs

- User input.
- Workspace diagnosis from `scripts/diagnose-first-use.py`.
- Known runtime preference, autonomy level, command policy, privacy constraints, and output format if already configured.

## Outputs

- Alfa greeting and short capability explanation.
- One-round guided setup questions.
- Proposed local profile values with assumptions marked.
- Handoff question for the first concrete task.

## Workflow

1. Discover: confirm repo signals and classify the input.
2. Analyze: decide `guided_first_use`, `micro_context_then_task`, `ask_first_task`, or `stop`.
3. Execute: present onboarding only when appropriate.
4. Validate: ensure no secrets were requested and no explicit task was blocked.

## Safety Limits

- Do not ask for passwords, API keys, tokens, private keys, or credentials.
- Do not write `.jm-adk.local.json`; route to `setup-workspace-profile.py --apply` only after explicit approval.
- Do not claim runtime capability without repo evidence or executed validation.

## Success Criteria

- Greeting-only input activates the onboarding message.
- Workspace without profile asks for safe setup inputs.
- Explicit task goes to `task-intake-agent`.
- Non-Alfa workspace stops before editing.

## Fallback

If the user does not provide non-blocking setup details, use safe defaults and mark `Supuesto`. If repo identity is unclear, mark `Dato requerido`.

## Examples

- Input: `hola` -> present Alfa and ask guided setup questions.
- Input: `crea un agente para QA` -> collect only missing critical context and proceed.
