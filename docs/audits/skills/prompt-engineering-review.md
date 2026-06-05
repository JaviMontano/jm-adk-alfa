# Skill Review: prompt-engineering

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`prompt-engineering` designs, audits, and improves LLM instruction packages. For Alfa, the skill must select prompt patterns deterministically, preserve source boundaries, prevent hidden reasoning leakage, define output contracts, and validate prompt engineering packets before downstream use.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | One active Phase 1 skill selected after `prompt-creator`; branch created from `origin/main`. | None. | Keep branch and PR scoped to `prompt-engineering`. | Low if scope remains isolated. |
| Determinism Auditor | complete | DoD failed before changes due missing assets, scaffold examples, root-list evals, vague validation, missing source boundary, missing no-invention policy, and remote font dependency. | Missing time/network/random policy and deterministic packet gate. | Add assets, activation contract, source policy, offline templates, and script-backed validation. | High before hardening. |
| Eval Designer | complete | Evals lacked DoD `cases`, false positives, routing coverage, and structured expected checks. | Missing system instruction, few-shot, reasoning scaffold, RAG-grounded, minimal input, conflict, and false-positive coverage. | Convert evals to explicit cases with expected activation, expected behavior, must include, must not include, and expected checks. | High before hardening because weak evals could pass regressions. |
| Script Engineer | complete | No script existed to validate prompt engineering packets. | None after script addition. | Add `validate_prompt_packet.py`, deterministic fixtures, and `check.sh`. | Low after fixture validation. |
| Guardian | complete | Blocks closure unless assets, eval cases, examples, review doc, packet validator, and DoD pass. | Full PR gates still required before merge. | Update ledger only after per-skill DoD and script checks pass. | Low after per-skill validation, pending PR gates. |

## Hardening Brief

- Replace scaffold companion files with prompt-engineering-specific deterministic contracts.
- Add `assets/prompt-engineering-checklist.md` and `assets/pattern-decision-matrix.json`.
- Add `scripts/validate_prompt_packet.py`, deterministic fixtures, and `scripts/check.sh`.
- Convert evals to DoD `cases` covering structured output, explicit trigger, system instruction, few-shot calibration, private reasoning scaffold, RAG grounding, minimal input, conflicting requirements, prompt-creator routing, and false positives.
- Remove remote Google Fonts dependency from HTML template and require provided creation dates.
- Align agents, prompts, templates, and knowledge graph around the same packet contract.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | Added activation rules, deterministic contract, source boundaries, no-invention policy, time/network/random policy, assets, and scripts. |
| `README.md` | Replaced scaffold text with triggers, required inputs, output packet, and deterministic gate commands. |
| `assets/` | Added checklist, decision matrix, README, and manifest. |
| `scripts/` | Added prompt packet validator, fixture-backed check, and script README. |
| `evals/evals.json` | Replaced root-list evals with DoD cases and required expected checks. |
| `examples/*` | Added realistic prompt engineering input and validated output packet. |
| `agents/*` and `prompts/*` | Specialized responsibilities around pattern selection, guardrails, source boundaries, and validation. |
| `templates/*` | Replaced generic output structure and removed remote font dependency from HTML. |
| `knowledge/*` | Added deterministic prompt packet concepts, no-invention rules, and prompt pattern graph updates. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
bash skills/prompt-engineering/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill prompt-engineering
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill prompt-engineering
```

Results:

- `OK: prompt-engineering prompt packet validator passed`
- `skill=prompt-engineering dod=pass errors=0`
- `skills_with_scripts=1 warnings=0 errors=0`

## PR Gate Check

Observed on 2026-06-05:

```bash
python3 -B scripts/validate-skills.py --strict
python3 -B scripts/count-components.py --check-docs
bash scripts/check-repo-boundaries.sh
python3 -B scripts/qa/run-adversarial-tests.py
python3 -B scripts/validate-skill-scripts.py --strict --run-checks
bash scripts/doc-factory/check.sh
git diff --check
```

Results:

- `skills=585 warnings=0 errors=0`
- `skills=585 agents=260 commands=267 prompts=256 components=1368`
- `Repo boundaries OK`
- `summary: passed=11 failed=0 total=11`
- `skills_with_scripts=24 warnings=0 errors=0`
- `OK: doc-factory deterministic smoke check passed`
- `git diff --check` produced no output

## Decision

Improved now and ready for PR.

## Ledger Completion 2026-06-05

- [CONFIG] Ledger status may be set to `dod-complete` after per-skill DoD and script checks pass, with PR merge still gated by full-repo validation.
