# Skill Review: session-end-cleanup

Date: 2026-06-06
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`session-end-cleanup` closes an agent session with a deterministic
evidence-tagged handoff: summary, changes, decisions, open tasks, insights,
risks, validation evidence, durable update plan, next handoff, and guardian
decision. [CÓDIGO]

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | pass | [CONFIG] `session-end-cleanup` was selected as the first active skill in the ordered accelerator queue. | [CONFIG] None after preflight; branch is scoped to one skill. | [CONFIG] Keep branch, PR, merge, and ledger limited to this skill. | [CONFIG] Low if one-skill scope holds. |
| Determinism Auditor | block | [CÓDIGO] Initial DoD failed because `assets/` was missing, examples retained scaffold markers, and `evals/evals.json` did not expose a `cases` list. | [CÓDIGO] Missing activation policy, output contract, evidence policy, closure checklist, update policy, offline scripts, fixtures, and review doc. | [CONFIG] Add deterministic assets/scripts, replace scaffold content, and validate before ledger closure. | [INFERENCIA] High before hardening because closeouts could claim completion without proof. |
| Eval Designer | pass | [CÓDIGO] Existing evals were activation-style prose and did not cover false positives, degraded states, PR lifecycle, or durable-log ambiguity. | [CÓDIGO] Missing failed-validation, no-change, unrelated-local-change, conflicting-evidence, long-session, and machine-report cases. | [CONFIG] Replace evals with at least 8 deterministic cases and expected checks for assets, scripts, and quality criteria. | [INFERENCIA] Medium before hardening because a generic activation test could pass while handoff quality failed. |
| Script Engineer | pass | [CÓDIGO] The skill had no `scripts/` directory, so no offline contract existed. | [CÓDIGO] Missing validator and positive/negative fixtures for session closeout reports. | [CONFIG] Add `validate_session_cleanup_report.py`, `check.sh`, two valid fixtures, and two invalid fixtures. | [INFERENCIA] Medium before hardening because output structure was not machine-checkable. |
| Integrator | pass | [CÓDIGO] Updated only `skills/session-end-cleanup/**`, this review doc, and the `session-end-cleanup` ledger row. | [CONFIG] None after integration. | [CONFIG] Do not touch other accelerator skills in this PR. | [CONFIG] Low if validation remains green. |
| Guardian | pass | [CÓDIGO] Per-skill DoD and script validations pass after hardening. | [CONFIG] PR, CI, merge, and branch cleanup evidence remain outside local hardening until the PR lifecycle runs. | [CONFIG] Open PR only after repo-level validations pass. | [INFERENCIA] Low local risk; remote CI remains pending until PR creation. |

## Hardening Brief

- skill: `session-end-cleanup`
- scope_allowed: `skills/session-end-cleanup/**`, `docs/audits/skills/session-end-cleanup-review.md`, and the `session-end-cleanup` row in `docs/audits/skill-review-ledger.csv`
- required_changes: replace scaffold artifacts, add deterministic assets, add offline report validator, add fixtures, add targeted eval cases, and record evidence
- forbidden_changes: no changes to other skills, no unrelated ledger rows, no claim of PR/CI/merge success before proof
- validation_plan: run per-skill validators, repo validators, whitespace check, PR checks, squash merge, branch cleanup, and main update
- merge_criteria: all local validations pass, PR CI passes, squash merge succeeds, branch cleanup succeeds, and `main` is updated

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added deterministic closeout inputs, procedure, output contract, assets, script entry point, quality criteria, and edge cases. |
| `README.md` | [CÓDIGO] Replaced scaffold text with triggers, required evidence, resources, output format, validation commands, and safety rules. |
| `assets/` | [CÓDIGO] Added activation, output, evidence, closure checklist, update policy, manifest, and README assets. |
| `scripts/` | [CÓDIGO] Added offline JSON report validator, check script, two valid fixtures, and two negative fixtures. |
| `evals/evals.json` | [CÓDIGO] Replaced root-array activation evals with 10 `cases` covering happy path, false positive, degraded states, boundaries, conflicts, and script contract. |
| `examples/*` | [CÓDIGO] Added realistic branch closeout input and evidence-tagged output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized roles around evidence inventory, false completion, durable-log safety, and guardian blocking. |
| `templates/*` | [CÓDIGO] Replaced generic and remote-font templates with deterministic closeout sections and offline HTML. |
| `knowledge/*` | [CÓDIGO] Added closeout concepts, evidence rules, anti-patterns, quality metrics, failure modes, and knowledge graph relationships. |

## Local Validation Evidence

- [CÓDIGO] `bash skills/session-end-cleanup/scripts/check.sh` passed with valid
  closeout and blocked-report fixtures accepted, and invalid missing-validation
  and untagged-task fixtures rejected.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill session-end-cleanup`
  passed with `skills_with_scripts=1 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill session-end-cleanup`
  passed with `skill=session-end-cleanup dod=pass errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict` passed with
  `skills=600 warnings=0 errors=0`.

## Decision

[CONFIG] Improved and locally DoD-ready. Open a ready PR only after the full
repo validation suite passes.
