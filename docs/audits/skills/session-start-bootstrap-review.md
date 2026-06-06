# Skill Review: session-start-bootstrap

Date: 2026-06-06
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`session-start-bootstrap` starts an agent session by verifying environment,
loading minimal required context, initializing guardrails, and producing a
deterministic first-action packet. [CÓDIGO]

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | pass | [CONFIG] `session-start-bootstrap` selected as the third active skill after `pre-compact-context` merged. | [CONFIG] None after clean preflight. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope stays isolated. |
| Determinism Auditor | block | [CÓDIGO] Initial DoD failed because `assets/` was missing, examples retained scaffold markers, and `evals/evals.json` did not expose `cases`. | [CÓDIGO] Missing startup contract, environment policy, context-loading policy, guardrails policy, source precedence, offline validator, fixtures, and review doc. | [CONFIG] Add deterministic startup assets/scripts and replace scaffold artifacts. | [INFERENCIA] High before hardening because sessions could start from wrong repo, dirty tree, or stale context. |
| Eval Designer | pass | [CÓDIGO] Original evals were generic activation checks. | [CÓDIGO] Missing clean-repo, dirty-tree, open-PR, conflicting-instruction, missing-handoff, private-context, false-positive, and script-contract cases. | [CONFIG] Replace evals with deterministic startup scenarios and expected checks. | [INFERENCIA] Medium-high before hardening because activation could pass while startup safety failed. |
| Script Engineer | pass | [CÓDIGO] The skill had no script contract. | [CÓDIGO] Missing local proof for environment shape, dirty-tree blocking, and first-action requirements. | [CONFIG] Add `validate_session_start_packet.py`, `check.sh`, two valid fixtures, and three negative fixtures. | [INFERENCIA] Medium before hardening because packet structure was prose-only. |
| Integrator | pass | [CÓDIGO] Updated only `skills/session-start-bootstrap/**`, this review doc, and the `session-start-bootstrap` ledger row. | [CONFIG] None after integration. | [CONFIG] Do not touch other accelerator skills in this PR. | [CONFIG] Low if validation remains green. |
| Guardian | pass | [CÓDIGO] Per-skill DoD and script validations pass after hardening. | [CONFIG] PR, CI, merge, and branch cleanup evidence remain pending until PR lifecycle runs. | [CONFIG] Open PR only after full repo validation passes. | [INFERENCIA] Low local risk; remote CI remains pending until PR creation. |

## Hardening Brief

- skill: `session-start-bootstrap`
- scope_allowed: `skills/session-start-bootstrap/**`, `docs/audits/skills/session-start-bootstrap-review.md`, and the `session-start-bootstrap` row in `docs/audits/skill-review-ledger.csv`
- required_changes: replace scaffold artifacts, add startup/environment/context/guardrails/source assets, add offline packet validator, add fixtures, add targeted eval cases, and record evidence
- forbidden_changes: no changes to other skills, no unrelated ledger rows, no bulk context loading, no startup pass from dirty environment
- validation_plan: run per-skill validators, repo validators, whitespace check, PR checks, squash merge, branch cleanup, and main update
- merge_criteria: local validations pass, PR CI passes, squash merge succeeds, branch cleanup succeeds, and `main` is updated

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added environment verification, minimal context loading, guardrail initialization, output contract, assets, scripts, quality criteria, and edge cases. |
| `README.md` | [CÓDIGO] Replaced scaffold text with triggers, resources, output sections, validation commands, and safety rules. |
| `assets/` | [CÓDIGO] Added bootstrap contract, environment policy, context-loading policy, guardrails policy, source priority, manifest, and README. |
| `scripts/` | [CÓDIGO] Added offline startup packet validator, check script, two valid fixtures, and three negative fixtures. |
| `evals/evals.json` | [CÓDIGO] Replaced activation evals with 8 `cases` covering clean startup, dirty tree, open PR, conflicts, missing handoff, private context, false positive, and script contract. |
| `examples/*` | [CÓDIGO] Added realistic startup input and evidence-tagged packet output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized roles around environment proof, source precedence, context loading, and guardian blocking. |
| `templates/*` | [CÓDIGO] Replaced generic and remote-font templates with deterministic startup packet sections and offline HTML. |
| `knowledge/*` | [CÓDIGO] Added startup checks, source precedence, anti-patterns, quality metrics, failure modes, and knowledge graph relationships. |

## Local Validation Evidence

- [CÓDIGO] `bash skills/session-start-bootstrap/scripts/check.sh` passed with
  clean-start and blocked-dirty-tree fixtures accepted, and missing-environment,
  dirty-pass, and missing-first-action fixtures rejected.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill session-start-bootstrap`
  passed with `skills_with_scripts=1 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill session-start-bootstrap`
  passed with `skill=session-start-bootstrap dod=pass errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict` passed with
  `skills=600 warnings=0 errors=0`.

## Decision

[CONFIG] Improved and locally DoD-ready. Open a ready PR only after the full
repo validation suite passes.
