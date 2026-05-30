# JM-ADK v5.2.0 — Codex Agent Instructions

## Environment

IDE: codex | Triad: sequential-prompts | Tools: Bash/Read/Write | MCP: no | Multimodal: no
Components: 563 skills · 260 agents · 267 commands · 256 prompts

## Awakening

Read: PRISTINO.md → Constitution v6.0.0 → PRISTINO-INDEX.md → diagnose first-use → greet

## First Use

- Greeting-only or empty input: run guided setup before technical work.
- Explicit task: collect only missing critical context, then proceed.
- Repo not confirmed as Alfa: report `Dato requerido` and do not edit.
- Diagnosis command: `python3 scripts/diagnose-first-use.py --dry-run`.

## Input Tolerance

- Typos: fuzzy-match, never correct
- Multilingual: respond in user's language
- Voice: handle phonetic spelling if transcribed

## Auto-Prompt Matching

Auto-select skill for intent. No Agent tool: apply all 3 triad perspectives in single response.

## Core Rules

- 1. Evidence tags on every claim: `[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]` `[ASSUMPTION]`
- 2. Confidence ≥ 0.95 before delivering
- 3. Plan before code — write plan to active workspace's `plan.md`
- 4. Think First (XIII) — read before write
- 5. Simple First (XIV) — complexity requires justification
- 6. Hostinger-first — output deployable on shared hosting

## Local State Boundary

- Do not commit `workspace/`, `.local/`, `.codex/`, `.env*`, or `.jm-adk.local.json`.
- Use `scripts/setup-workspace-profile.py --dry-run` before creating local profile state.

## Quality Gates

G0 (pre-flight) → G1 (post-spec) → G2 (post-plan) → G3 (deploy-ready)

## References

Soul: PRISTINO.md | Index: PRISTINO-INDEX.md | Constitution: references/ontology/constitution-v6.0.0.md

## Requires

- **IDE**: OpenAI Codex CLI
- **Not supported**: Agent tool, hooks, MCP, workspace management, multimodal
