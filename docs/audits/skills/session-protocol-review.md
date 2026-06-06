# Skill Review: session-protocol

Date: 2026-06-06
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`session-protocol` initializes a session through ordered context loading, state
recovery, pending closure recommendations, next-step proposal, and confirmation
before work starts. [CÓDIGO]

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | pass | [CONFIG] `session-protocol` selected as the fourth active skill after `session-start-bootstrap` merged. | [CONFIG] None after clean preflight. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope stays isolated. |
| Determinism Auditor | block | [CÓDIGO] Initial DoD failed because assets were missing, examples were generic, and evals lacked `cases`. | [CÓDIGO] Missing context-order, state-recovery, closure, next-step, report-contract assets and offline validation. | [CONFIG] Preserve the existing four-phase intent and add deterministic proof. | [INFERENCIA] High before hardening because tasks could be auto-closed or work could start without confirmation. |
| Eval Designer | pass | [CÓDIGO] Original evals were generic activation checks. | [CÓDIGO] Missing missing-tasklog, stale-task, no-auto-close, open-PR, false-positive, conflicting-context, and machine-report cases. | [CONFIG] Replace evals with deterministic session protocol scenarios. | [INFERENCIA] Medium before hardening because context loading could be skipped silently. |
| Script Engineer | pass | [CÓDIGO] The skill had no script contract. | [CÓDIGO] Missing local proof for context ordering, no auto-closure, and confirmation gate. | [CONFIG] Add validator, check script, two valid fixtures, and three negative fixtures. | [INFERENCIA] Medium before hardening because report shape was prose-only. |
| Integrator | pass | [CÓDIGO] Updated only `skills/session-protocol/**`, this review doc, and the `session-protocol` ledger row. | [CONFIG] None after integration. | [CONFIG] Do not touch other accelerator skills in this PR. | [CONFIG] Low if validation remains green. |
| Guardian | pass | [CÓDIGO] Per-skill DoD and script validations pass after hardening. | [CONFIG] PR, CI, merge, and branch cleanup evidence remain pending until PR lifecycle runs. | [CONFIG] Open PR only after full repo validation passes. | [INFERENCIA] Low local risk; remote CI remains pending until PR creation. |

## Hardening Brief

- skill: `session-protocol`
- scope_allowed: `skills/session-protocol/**`, `docs/audits/skills/session-protocol-review.md`, and the `session-protocol` row in `docs/audits/skill-review-ledger.csv`
- required_changes: add deterministic assets, replace scaffold README/examples/evals, add offline report validator and fixtures, preserve confirmation gate, and record evidence
- forbidden_changes: no other skills, no unrelated ledger rows, no auto-closing tasks, no starting implementation before confirmation
- validation_plan: run per-skill validators, repo validators, whitespace check, PR checks, squash merge, branch cleanup, and main update
- merge_criteria: local validations pass, PR CI passes, squash merge succeeds, branch cleanup succeeds, and `main` is updated

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added deterministic resources, script validation criterion, missing-source rule, and confirmation-safe closure requirements. |
| `README.md` | [CÓDIGO] Replaced scaffold text with triggers, resources, output sections, validation commands, and safety rules. |
| `assets/` | [CÓDIGO] Added context-load-order, state-recovery, closure, next-step, report-contract, manifest, and README assets. |
| `scripts/` | [CÓDIGO] Added offline report validator, check script, two valid fixtures, and three negative fixtures. |
| `evals/evals.json` | [CÓDIGO] Replaced activation evals with 8 cases covering full start, missing tasklog, stale task, no auto-close, open PR, false positive, conflicting context, and script contract. |
| `examples/*` | [CÓDIGO] Added realistic session initialization input and evidence-tagged report output. |
| `templates/*` and `knowledge/*` | [CÓDIGO] Added deterministic report sections, offline HTML, protocol phases, metrics, and knowledge graph. |

## Local Validation Evidence

- [CÓDIGO] `bash skills/session-protocol/scripts/check.sh` passed with valid
  normal and blocked reports accepted, and auto-closure, missing-context, and
  unconfirmed-work reports rejected.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill session-protocol`
  passed with `skills_with_scripts=1 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill session-protocol`
  passed with `skill=session-protocol dod=pass errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict` passed with
  `skills=600 warnings=0 errors=0`.

## Decision

[CONFIG] Improved and locally DoD-ready. Open a ready PR only after the full
repo validation suite passes.
