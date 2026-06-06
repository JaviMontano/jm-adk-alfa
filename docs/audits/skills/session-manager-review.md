# Skill Review: session-manager

Date: 2026-06-06
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`session-manager` manages `.specify/context.json`, cold-start priming, stage
computation, authorized persistence, and project next-action reporting. [CÓDIGO]

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | pass | [CONFIG] `session-manager` selected as the fifth active skill after `session-protocol` merged. | [CONFIG] None after clean preflight. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope stays isolated. |
| Determinism Auditor | block | [CÓDIGO] Initial DoD failed because assets were missing, examples were generic, and evals lacked `cases`. | [CÓDIGO] Missing state contract, stage policy, priming policy, persistence policy, source boundary, and offline validation. | [CONFIG] Preserve the existing `.specify/context.json` intent and add deterministic proof. | [INFERENCIA] High before hardening because state could be inferred from memory or silently persisted. |
| Eval Designer | pass | [CÓDIGO] Original evals were generic activation checks. | [CÓDIGO] Missing missing-context, stage-skip, unauthorized-write, implementing-without-tasks, false-positive, and machine-report cases. | [CONFIG] Replace evals with deterministic session-state scenarios. | [INFERENCIA] Medium before hardening because stage transitions were prose-only. |
| Script Engineer | pass | [CÓDIGO] The skill had no script contract. | [CÓDIGO] Missing local proof for stage delta, context presence, task evidence, and write authorization. | [CONFIG] Add validator, check script, two valid fixtures, and four negative fixtures. | [INFERENCIA] Medium before hardening because no offline verifier existed. |
| Integrator | pass | [CÓDIGO] Updated only `skills/session-manager/**`, this review doc, and the `session-manager` ledger row. | [CONFIG] None after integration. | [CONFIG] Do not touch other accelerator skills in this PR. | [CONFIG] Low if validation remains green. |
| Guardian | pass | [CÓDIGO] Per-skill DoD and script validations pass after hardening. | [CONFIG] PR, CI, merge, and branch cleanup evidence remain pending until PR lifecycle runs. | [CONFIG] Open PR only after full repo validation passes. | [INFERENCIA] Low local risk; remote CI remains pending until PR creation. |

## Hardening Brief

- skill: `session-manager`
- scope_allowed: `skills/session-manager/**`, `docs/audits/skills/session-manager-review.md`, and the `session-manager` row in `docs/audits/skill-review-ledger.csv`
- required_changes: add deterministic assets, replace scaffold README/examples/evals, add offline report validator and fixtures, preserve `.specify/context.json` state-management intent, and record evidence
- forbidden_changes: no other skills, no unrelated ledger rows, no silent context initialization, no stage skip, no unauthorized writes
- validation_plan: run per-skill validators, repo validators, whitespace check, PR checks, squash merge, branch cleanup, and main update
- merge_criteria: local validations pass, PR CI passes, squash merge succeeds, branch cleanup succeeds, and `main` is updated

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added deterministic resources, stage policy, source-boundary rules, authorized persistence rules, and script validation criterion. |
| `README.md` | [CÓDIGO] Replaced scaffold text with triggers, resources, output sections, validation command, and safety rules. |
| `assets/` | [CÓDIGO] Added state contract, stage policy, priming policy, persistence policy, source boundary, manifest, and README assets. |
| `scripts/` | [CÓDIGO] Added offline report validator, check script, two valid fixtures, and four negative fixtures. |
| `evals/evals.json` | [CÓDIGO] Replaced activation evals with 10 cases covering cold start, missing context, stage transitions, stage skip, unauthorized write, false positive, and script contract. |
| `examples/*` | [CÓDIGO] Added realistic `.specify/context.json` input and evidence-tagged output. |
| `agents/*`, `prompts/*`, `templates/*`, and `knowledge/*` | [CÓDIGO] Specialized scaffold text for session state, stage computation, persistence, and offline validation. |

## Local Validation Evidence

- [CÓDIGO] `bash skills/session-manager/scripts/check.sh` passed with valid
  planned and blocked reports accepted, and missing-context-pass, stage-skip,
  implementing-without-tasks, and unauthorized-write reports rejected.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill session-manager`
  passed with `skills_with_scripts=1 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill session-manager`
  passed with `skill=session-manager dod=pass errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict` passed with
  `skills=600 warnings=0 errors=0`.

## Decision

[CONFIG] Improved and locally DoD-ready. Open a ready PR only after the full
repo validation suite passes.
