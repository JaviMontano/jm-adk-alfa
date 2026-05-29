# JM-ADK v5.2.0 — Antigravity Rules (Gemini Agents)

## Environment

IDE: antigravity | Triad: adapter-guided | Tools: limited | Hooks: no | MCP: no | Multimodal: validation pending

## Awakening

Load: PRISTINO.md → Constitution v6.0.0 → skills_index.json → greet
Components: 533 skills · 260 agents · 267 commands · 256 prompts

## First Use

- Greeting-only or empty input: run guided setup before technical work.
- Explicit task: collect only missing critical context, then proceed.
- Repo not confirmed as Alfa: report `Dato requerido` and do not edit.
- Diagnosis command: `python3 scripts/diagnose-first-use.py --dry-run`.

## Input Tolerance

- Typos: fuzzy-match intent, never correct spelling
- Voice (Gemini mobile): strip filler, handle phonetic spelling, mixed ES/EN
- Dyslexia: short sentences, bullet points, clear structure
- Multilingual: respond in user's language, process in English internally

## Auto-Prompt Matching

Auto-select best skill via skills_index.json. Confidence ≥ 0.85 → execute. 0.60-0.84 → offer options. < 0.60 → ask.

## Triad Pattern

This adapter exposes Alfa's triad pattern to Antigravity-compatible rules. Runtime execution support must be validated in the target environment:
- Lead (domain specialist) → Support (cross-cutting) → Guardian (quality)
- Sequential fallback: Lead produces → Support reviews → Guardian validates
- Full composition matrix: see PRISTINO.md

## Core Rules

- 1. Evidence tags on every claim: `[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]` `[ASSUMPTION]`
- 2. Confidence ≥ 0.95 before delivering
- 3. Plan before code — write plan to active workspace's `plan.md`
- 4. Think First (XIII) — read before write
- 5. Simple First (XIV) — complexity requires justification
- 6. Hostinger-first — output deployable on shared hosting
- 7. Firebase-native — managed services before custom
- 8. Read before write — always read existing files first
- 9. Skill search first — use existing skills before building from scratch
- 10. Constitution compliance — validate against v6.0.0
- 11. Workspace-first — every artifact-producing task gets a workspace

## Local State Boundary

- Do not commit `workspace/`, `.local/`, `.codex/`, `.env*`, or `.jm-adk.local.json`.
- Use `scripts/setup-workspace-profile.py --dry-run` before creating local profile state.

## Quality Gates

G0 (pre-flight) → G1 (post-spec) → G2 (post-plan) → G3 (deploy-ready)

## Stack

Firebase + HTML/CSS/JS + Angular/React + Hostinger
No SSR, no Docker, no custom servers.

## Brand

- navy	#122562
- gold	#FFD700
- cyan	#137DC5
- dark	#1F2833
- lavender	#BBA0CC
- gray	#808080
- text	#FFFFFF

## Skill Loading

`skills_index.json` for fast lookup → load full SKILL.md on demand via `skills/{id}/SKILL.md`

## References

- Soul: `PRISTINO.md` | Constitution: `references/ontology/constitution-v6.0.0.md`
- Index: `skills_index.json` | Brand: `references/brand/design-tokens.json`

## Requires

- **IDE**: Antigravity-compatible Gemini agent environment
- **Model**: configured by the target runtime
- **Capability**: validation pending until executed in the target runtime
- **Not supported**: Hooks, MCP servers, workspace management (Claude Code only)
