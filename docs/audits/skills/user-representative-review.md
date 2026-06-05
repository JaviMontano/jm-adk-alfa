# Skill Review: user-representative

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`user-representative` reviews stakeholder deliverables from the reader and end-user perspective. For Alfa, the skill must produce deterministic review packets with evidence-tagged audience assumptions, a five-dimension scorecard, five micro-adjustments, adoption risks, bias flags, and a verdict derived from explicit score rules.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] One Phase 1 skill selected after `output-contract-enforcer`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to `user-representative`. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | complete | [CÓDIGO] DoD failed before changes: missing `assets/`, scaffold examples, root-list evals, remote font dependency, broad tools, and prompt section mismatch. | [CÓDIGO] No executable review packet validator or fixture-backed score/verdict check existed. | [CONFIG] Add assets, offline templates, narrowed tools, fixed score algorithm, and deterministic validator. | [INFERENCIA] Medium-high before hardening. |
| Eval Designer | complete | [CÓDIGO] Evals were seven generic activation cases without `expected_checks`. | [CÓDIGO] Missing anti-invention, missing-context, conflicting constraints, evidence mapping, and adjacent false-positive coverage. | [CONFIG] Convert evals to DoD `cases` with concrete include/exclude checks and script coverage. | [INFERENCIA] High before hardening because subjective reviews could pass. |
| Script Engineer | complete | [CÓDIGO] No script existed to validate review packet shape, scores, evidence tags, or verdict. | [CÓDIGO] None after script addition. | [CONFIG] Add `validate_user_representative_review.py`, fixture contract, and `check.sh`. | [INFERENCIA] Low after fixture validation. |
| Guardian | complete | [CÓDIGO] Ledger row was `pending` and review doc was absent; focused DoD failed with 5 errors before hardening. | [CONFIG] Full PR gates still required before merge. | [CONFIG] Block ledger closure until assets, evals, examples, script checks, review doc, and DoD pass. | [INFERENCIA] Low after per-skill validation, pending PR gates. |

## Hardening Brief

- [CONFIG] Replace scaffold README, examples, evals, templates, roles, prompts, and knowledge with a User Representative-specific deterministic contract.
- [CONFIG] Add `assets/user-representative-checklist.md` and `assets/review-rubric.json`.
- [CONFIG] Add `scripts/validate_user_representative_review.py`, `scripts/check.sh`, and pass/fail fixtures.
- [CONFIG] Convert evals to ten DoD `cases` covering source-grounded modeling, missing context, conflicting constraints, evidence maps, open success targets, adoption risk, validator behavior, and false positives.
- [CONFIG] Remove remote Google Fonts dependency from HTML and replace `{{DATE}}` with caller-provided `{{REVIEW_DATE}}`.
- [CONFIG] Narrow allowed tools to read-only tools because the skill reviews and proposes micro-adjustments rather than editing source deliverables.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added deterministic contract, assets, evidence tags, no-invention policy, fixed verdict algorithm, and script validation command. |
| `README.md` | [CÓDIGO] Replaced scaffold text with activation, required inputs, output contract, assets, scripts, and local gates. |
| `assets/` | [CÓDIGO] Added checklist, rubric, README, and manifest. |
| `scripts/` | [CÓDIGO] Added Markdown review packet validator, JSON contract fixture, pass/fail Markdown fixtures, and `check.sh`. |
| `evals/evals.json` | [CÓDIGO] Replaced root-list evals with ten DoD `cases` and required expected checks. |
| `examples/*` | [CÓDIGO] Added realistic executive rollout review input and a deterministic `CONDITIONAL` output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized responsibilities around evidence extraction, scorecard validation, routing, and no-invention behavior. |
| `templates/*` | [CÓDIGO] Replaced generic Markdown/DOCX templates and removed HTML network font dependency. |
| `knowledge/*` | [CÓDIGO] Added evidence rules, dimensions, anti-patterns, and graph concepts. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
bash skills/user-representative/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill user-representative
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill user-representative
python3 -m json.tool skills/user-representative/evals/evals.json
```

Results:

- [CÓDIGO] `OK: user-representative review validator fixtures passed`
- [CÓDIGO] `skill=user-representative dod=pass errors=0`
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
- [CÓDIGO] `skills_with_scripts=30 warnings=0 errors=0`
- [CÓDIGO] `OK: doc-factory deterministic smoke check passed`
- [CÓDIGO] `git diff --check` produced no output

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CONFIG] Ledger status may be set to `dod-complete` after per-skill DoD and script checks pass, with PR merge still gated by full-repo validation.
