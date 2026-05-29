# JM-ADK v5.2.0 — Gemini Agent Instructions

## Environment

IDE: gemini | Triad: sequential-prompts | Tools: limited | Hooks: no | MCP: no | Multimodal: yes (mobile)
Components: 532 skills · 260 agents · 266 commands · 256 prompts

## Awakening

On session start: load PRISTINO.md → Constitution v6.0.0 → PRISTINO-INDEX.md → diagnose first-use → greet user.

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

Auto-select best skill. Confidence ≥ 0.85 → execute. 0.60-0.84 → offer options. < 0.60 → ask.
No Agent tool: apply triad perspectives sequentially in single response.

## Triad Pattern

Lead (domain) → Support (cross-cutting) → Guardian (quality). Sequential in single response.
Full matrix: `PRISTINO.md`

## Request Classification

| Type | Action |
|------|--------|
| QUESTION | Direct answer |
| ANALYSIS | Discovery triad → report |
| SIMPLE CODE | Inline edit |
| COMPLEX CODE | Plan first |
| DESIGN/UI | Tokens + plan + triad |
| SCAFFOLD | Template + customize |
| DEPLOY | Build → validate → deploy |

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

- Soul: `PRISTINO.md` | Constitution: `references/ontology/constitution-v6.0.0.md`
- Index: `PRISTINO-INDEX.md` | Brand: `references/brand/design-tokens.json`

## Requires

- **IDE**: Gemini Code Assist (not Antigravity — for Antigravity use .agent/rules/GEMINI.md)
- **Not supported**: Agent tool, hooks, MCP, workspace management
- **Supported**: Multimodal (mobile), voice input
