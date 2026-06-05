# Skill Review: ux-writing

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`ux-writing` audits and improves interface and deliverable copy. For Alfa, the skill must produce deterministic UX Writing Audit packets grounded in supplied source text, with before/after rewrites, accessibility and readability checks, evidence tags, and no unsupported product claims.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] One Phase 1 skill selected after `user-representative`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to `ux-writing`. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | complete | [CÓDIGO] DoD failed before changes: missing `assets/`, scaffold examples, root-list evals, remote font dependency, `{{DATE}}`, broad tools, and prompt section mismatch. | [CÓDIGO] No deterministic fixture validated microcopy specificity, readability, accessibility language, or no-invention boundaries. | [CONFIG] Add assets, offline templates, narrowed tools, fixed packet contract, and deterministic validator. | [INFERENCIA] High before hardening. |
| Eval Designer | complete | [CÓDIGO] Evals were seven generic activation cases without `expected_checks`. | [CÓDIGO] Missing microcopy, error recovery, empty state, CTA, accessibility language, reading-level, false-positive, and no-invention cases. | [CONFIG] Convert evals to DoD `cases` with concrete checks. | [INFERENCIA] High before hardening because weak evals could pass. |
| Guardian | complete | [CÓDIGO] Ledger row was `pending`; focused DoD failed with 5 errors before hardening. | [CONFIG] Full PR gates still required before merge. | [CONFIG] Block ledger closure until assets, evals, examples, scripts, review doc, and DoD pass. | [INFERENCIA] Low after per-skill validation, pending PR gates. |

## Hardening Brief

- [CONFIG] Replace scaffold README, examples, evals, templates, roles, prompts, and knowledge with UX-writing-specific deterministic contracts.
- [CONFIG] Add `assets/ux-writing-checklist.md`, `assets/microcopy-patterns.json`, and `assets/readability-rubric.json`.
- [CONFIG] Add `scripts/validate_ux_writing_packet.py`, a fixture contract, and pass/fail Markdown fixtures.
- [CONFIG] Convert evals to ten DoD `cases` covering microcopy rewrites, error recovery, empty states, CTA clarity, accessibility language, executive readability, bilingual Spanish-first helper text, script validation, false positives, and no invented claims.
- [CONFIG] Remove remote Google Fonts dependency and replace `{{DATE}}` with caller-provided `{{REVIEW_DATE}}`.
- [CONFIG] Narrow allowed tools to read-only tools because the skill audits copy and proposes rewrites rather than editing source artifacts directly.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added deterministic contract, assets, evidence tags, no-invention policy, date policy, offline rule, and script validation command. |
| `README.md` | [CÓDIGO] Replaced scaffold text with activation, required inputs, output contract, assets, scripts, and local gates. |
| `assets/` | [CÓDIGO] Added checklist, microcopy contract, readability rubric, README, and manifest. |
| `scripts/` | [CÓDIGO] Added Markdown audit packet validator, JSON contract fixture, pass/fail Markdown fixtures, and `check.sh`. |
| `evals/evals.json` | [CÓDIGO] Replaced root-list evals with ten DoD `cases` and required expected checks. |
| `examples/*` | [CÓDIGO] Added realistic billing dashboard copy audit input and source-grounded output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized responsibilities around source extraction, before/after rewrites, routing, and no-invention behavior. |
| `templates/*` | [CÓDIGO] Replaced generic Markdown/DOCX templates and removed HTML network font dependency. |
| `knowledge/*` | [CÓDIGO] Added evidence rules, microcopy patterns, anti-patterns, and graph concepts. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
bash skills/ux-writing/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill ux-writing
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ux-writing
python3 -m json.tool skills/ux-writing/evals/evals.json
```

Results:

- [CÓDIGO] `OK: ux-writing packet validator fixtures passed`
- [CÓDIGO] `skill=ux-writing dod=pass errors=0`
- [CÓDIGO] `skills_with_scripts=1 warnings=0 errors=0`
- [CÓDIGO] `json-ok`

## PR Gate Check

Observed on 2026-06-05:

```bash
python3 -B scripts/validate-skills.py --strict
python3 -B scripts/count-components.py --check-docs
python3 -B scripts/validate-mcp-config.py
python3 -B scripts/check-devkit-readiness.py
bash scripts/check-repo-boundaries.sh
python3 -B scripts/qa/run-adversarial-tests.py
python3 -B scripts/validate-skill-scripts.py --strict --run-checks
bash scripts/doc-factory/check.sh
git diff --check
```

Results:

- [CÓDIGO] `skills=600 warnings=0 errors=0`
- [CÓDIGO] `skills=600 agents=261 commands=267 prompts=256 components=1384`
- [CÓDIGO] `mcp config: passed`
- [CÓDIGO] `devkit readiness: passed`
- [CÓDIGO] `Repo boundaries OK`
- [CÓDIGO] `summary: passed=11 failed=0 total=11`
- [CÓDIGO] `skills_with_scripts=31 warnings=0 errors=0`
- [CÓDIGO] `OK: doc-factory deterministic smoke check passed`
- [CÓDIGO] `git diff --check` produced no output

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CONFIG] Ledger status may be set to `dod-complete` after per-skill DoD and script checks pass, with PR merge still gated by full-repo validation.
