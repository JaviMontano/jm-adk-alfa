# Skill Review: prompt-creator

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`prompt-creator` generates deterministic prompt artifacts for agentic ecosystems. For Alfa, that means it must classify prompt type, ground the prompt in source-agent evidence, prevent invented context, and validate generated prompt markdown before downstream use.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | One active skill selected from Phase 1 after `auto-prompt-matching`. | None. | Keep branch/PR scoped to `prompt-creator`. | Low if scope remains isolated. |
| Determinism Auditor | complete | Scaffold README/examples, inconsistent `## When to Activate` references, quick mode weakened evidence, missing no-invention policy, remote font dependency. | Missing date/network/random policy. | Add activation section, no-invention rules, source policy, offline templates, and deterministic script validation. | Medium-high before hardening. |
| Eval Designer | complete | Evals were a 7-item root list with generic activation language and no `expected_checks`. | Missing handled type, redirect, false-positive, duplicate-path, and missing-source coverage. | Convert to DoD `cases` with prompt-type coverage and deterministic checks. | High before hardening because contract regressions could pass. |
| Script Engineer | complete | No script existed to validate generated prompt artifacts. | None after script addition. | Add `validate_prompt_artifact.py`, fixtures, and `check.sh`. | Low after fixture validation. |
| Guardian | complete | Per-skill DoD failed with 5 errors before changes and ledger had no review doc. | None after validation. | Block ledger closure until assets, eval cases, examples, review doc, script checks, and DoD pass. | Low after validation. |

## Hardening Brief

- Replace scaffold companion files with prompt-specific deterministic contracts.
- Add `assets/prompt-contract-checklist.md` and `assets/prompt-type-matrix.json`.
- Add `scripts/validate_prompt_artifact.py`, deterministic fixtures, and `scripts/check.sh`.
- Convert evals to 12 DoD `cases` covering handled prompt types, redirects, missing source, duplicate path, and false positive.
- Remove remote Google Fonts dependency from HTML template and require provided `created_date`.
- Update agents/prompts/knowledge so quick, deep, lead, support, specialist, and guardian all enforce the same contract.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | Added activation section, deterministic contract, no-invention policy, time/network/random policy, assets, and scripts. |
| `README.md` | Replaced scaffold text with triggers, minimum inputs, output contract, and deterministic gate commands. |
| `assets/` | Added checklist, type matrix, README, and manifest. |
| `scripts/` | Added prompt artifact validator, fixture-backed check, and script README. |
| `evals/evals.json` | Replaced root-list evals with 12 DoD cases and required expected checks. |
| `examples/*` | Added realistic handoff prompt input and validated output example. |
| `agents/*` and `prompts/*` | Specialized responsibilities around source evidence, type rules, placeholders, and validation. |
| `templates/*` | Replaced generic markdown output and removed remote font dependency from HTML. |
| `knowledge/*` | Added prompt type families, deterministic inputs, anti-patterns, and graph concepts. |

## No-Regression Check

Observed on 2026-06-05:

```bash
python3 -m json.tool skills/prompt-creator/evals/evals.json
bash skills/prompt-creator/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill prompt-creator
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill prompt-creator
python3 -B scripts/validate-skills.py --strict
python3 -B scripts/count-components.py --check-docs
bash scripts/check-repo-boundaries.sh
python3 -B scripts/qa/run-adversarial-tests.py
python3 -B scripts/validate-skill-scripts.py --strict --run-checks
bash scripts/doc-factory/check.sh
git diff --check
```

Results:

- `json-ok`
- `OK: prompt-creator prompt artifact validator passed`
- `skill=prompt-creator dod=pass errors=0`
- `skills_with_scripts=1 warnings=0 errors=0`
- `skills=585 warnings=0 errors=0`
- `skills=585 agents=260 commands=267 prompts=256 components=1368`
- `Repo boundaries OK`
- `summary: passed=11 failed=0 total=11`
- `skills_with_scripts=23 warnings=0 errors=0`
- `OK: doc-factory deterministic smoke check passed`
- `git diff --check` produced no output

## Decision

Improved now and ready for PR after full repo validation.

## Ledger Completion 2026-06-05

- [CONFIG] Ledger status is `dod-complete` with decision `completed-prompt-creator-dod`.
