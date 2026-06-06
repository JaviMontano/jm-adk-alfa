# Skill Review: pre-compact-context

Date: 2026-06-06
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`pre-compact-context` preserves critical working context before conversation
compaction by producing a deterministic retention map, compression summary,
risk list, validation evidence, and rehydration prompt. [CÓDIGO]

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | pass | [CONFIG] `pre-compact-context` selected as the second active skill after `session-end-cleanup` merged. | [CONFIG] None after clean preflight. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope stays isolated. |
| Determinism Auditor | block | [CÓDIGO] Initial DoD failed because `assets/` was missing, examples retained scaffold markers, and `evals/evals.json` did not expose `cases`. | [CÓDIGO] Missing retention policy, output contract, evidence policy, rehydration checklist, risk policy, offline validator, fixtures, and review doc. | [CONFIG] Add deterministic assets/scripts and replace scaffold artifacts. | [INFERENCIA] High before hardening because compaction could lose hard rules or blockers. |
| Eval Designer | pass | [CÓDIGO] Original evals were generic activation checks. | [CÓDIGO] Missing near-limit, conflicting-state, secret-redaction, false-positive, source-gap, dropped-hard-rule, and machine-packet cases. | [CONFIG] Replace evals with deterministic cases that cover false positives, degradation, and boundaries. | [INFERENCIA] Medium-high before hardening because activation could pass while retention quality failed. |
| Script Engineer | pass | [CÓDIGO] The skill had no script contract. | [CÓDIGO] Missing local proof that P0 retention, DROP safety, secret redaction, and rehydration prompt are enforced. | [CONFIG] Add `validate_pre_compact_packet.py`, `check.sh`, two valid fixtures, and three negative fixtures. | [INFERENCIA] Medium before hardening because packet structure was prose-only. |
| Integrator | pass | [CÓDIGO] Updated only `skills/pre-compact-context/**`, this review doc, and the `pre-compact-context` ledger row. | [CONFIG] None after integration. | [CONFIG] Do not touch other accelerator skills in this PR. | [CONFIG] Low if validation remains green. |
| Guardian | pass | [CÓDIGO] Per-skill DoD and script validations pass after hardening. | [CONFIG] PR, CI, merge, and branch cleanup evidence remain pending until PR lifecycle runs. | [CONFIG] Open PR only after full repo validation passes. | [INFERENCIA] Low local risk; remote CI remains pending until PR creation. |

## Hardening Brief

- skill: `pre-compact-context`
- scope_allowed: `skills/pre-compact-context/**`, `docs/audits/skills/pre-compact-context-review.md`, and the `pre-compact-context` row in `docs/audits/skill-review-ledger.csv`
- required_changes: replace scaffold artifacts, add retention/evidence/rehydration assets, add offline packet validator, add fixtures, add targeted eval cases, and record evidence
- forbidden_changes: no changes to other skills, no unrelated ledger rows, no durable-memory writes, no compaction success claim without packet validation
- validation_plan: run per-skill validators, repo validators, whitespace check, PR checks, squash merge, branch cleanup, and main update
- merge_criteria: local validations pass, PR CI passes, squash merge succeeds, branch cleanup succeeds, and `main` is updated

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added retention classes, source inventory, output contract, assets, scripts, quality criteria, and compaction edge cases. |
| `README.md` | [CÓDIGO] Replaced scaffold text with triggers, resources, output sections, validation commands, and safety rules. |
| `assets/` | [CÓDIGO] Added retention policy, output contract, evidence policy, rehydration checklist, risk policy, manifest, and README. |
| `scripts/` | [CÓDIGO] Added offline packet validator, check script, two valid fixtures, and three negative fixtures. |
| `evals/evals.json` | [CÓDIGO] Replaced activation evals with 9 `cases` covering handoff, token pressure, conflicts, secrets, false positives, source gaps, unsafe drops, no-change, and script contract. |
| `examples/*` | [CÓDIGO] Added realistic pre-compaction input and packet output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized roles around retention mapping, context-loss review, and guardian blocking. |
| `templates/*` | [CÓDIGO] Replaced generic and remote-font templates with deterministic packet sections and offline HTML. |
| `knowledge/*` | [CÓDIGO] Added retention classes, rehydration requirements, anti-patterns, metrics, failure modes, and knowledge graph relationships. |

## Local Validation Evidence

- [CÓDIGO] `bash skills/pre-compact-context/scripts/check.sh` passed with valid
  pre-compact and blocked fixtures accepted, and invalid dropped-P0,
  missing-rehydration, and secret-leak fixtures rejected.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill pre-compact-context`
  passed with `skills_with_scripts=1 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill pre-compact-context`
  passed with `skill=pre-compact-context dod=pass errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict` passed with
  `skills=600 warnings=0 errors=0`.

## Decision

[CONFIG] Improved and locally DoD-ready. Open a ready PR only after the full
repo validation suite passes.
