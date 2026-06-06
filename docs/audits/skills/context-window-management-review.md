# Skill Review: context-window-management

Date: 2026-06-06
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`context-window-management` builds deterministic token budget, priority,
compression, and eviction plans for context-window pressure. [CÓDIGO]

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | pass | [CONFIG] `context-window-management` selected as the eighth active skill after `changelog-management` merged. | [CONFIG] None after clean preflight. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope stays isolated. |
| Determinism Auditor | block | [CÓDIGO] Initial DoD failed because assets were missing, examples were generic, and evals lacked `cases`. | [CÓDIGO] Missing budget, priority, compression, eviction, report contract, and offline validation. | [CONFIG] Preserve token budgeting intent and add deterministic proof. | [INFERENCIA] High before hardening because active instructions could be dropped or over-budget plans could pass. |
| Eval Designer | pass | [CÓDIGO] Original evals were generic activation checks. | [CÓDIGO] Missing under-limit, over-limit, P0 preservation, missing estimates, preservation, response reserve, false-positive, compression expansion, over-budget, and script-contract cases. | [CONFIG] Replace evals with deterministic context-budget scenarios. | [INFERENCIA] Medium before hardening because budget behavior was prose-only. |
| Script Engineer | pass | [CÓDIGO] The skill had no script contract. | [CÓDIGO] Missing local proof for budget arithmetic, P0 protection, compression reduction, preservation fields, and final fit. | [CONFIG] Add validator, check script, two valid fixtures, and five negative fixtures. | [INFERENCIA] Medium before hardening because no offline verifier existed. |
| Integrator | pass | [CÓDIGO] Updated only `skills/context-window-management/**`, this review doc, and the `context-window-management` ledger row. | [CONFIG] None after integration. | [CONFIG] Do not touch other accelerator skills in this PR. | [CONFIG] Low if validation remains green. |
| Guardian | pass | [CÓDIGO] Per-skill DoD and script validations pass after hardening. | [CONFIG] PR, CI, merge, and branch cleanup evidence remain pending until PR lifecycle runs. | [CONFIG] Open PR only after full repo validation passes. | [INFERENCIA] Low local risk; remote CI remains pending until PR creation. |

## Hardening Brief

- skill: `context-window-management`
- scope_allowed: `skills/context-window-management/**`, `docs/audits/skills/context-window-management-review.md`, and the `context-window-management` row in `docs/audits/skill-review-ledger.csv`
- required_changes: add deterministic assets, replace scaffold README/examples/evals, add offline report validator and fixtures, preserve context budgeting intent, and record evidence
- forbidden_changes: no other skills, no unrelated ledger rows, no P0 eviction, no hidden token assumptions, no expanding compression, no non-JM Labs output branding
- validation_plan: run per-skill validators, repo validators, whitespace check, PR checks, squash merge, branch cleanup, and main update
- merge_criteria: local validations pass, PR CI passes, squash merge succeeds, branch cleanup succeeds, and `main` is updated

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added deterministic resources, budget arithmetic, priority tiers, compression/eviction rules, and script validation criterion. |
| `README.md` | [CÓDIGO] Replaced scaffold text with triggers, resources, output sections, validation command, and safety rules. |
| `assets/` | [CÓDIGO] Added budget, priority, compression, eviction, report contract, manifest, and README assets. |
| `scripts/` | [CÓDIGO] Added offline report validator, check script, two valid fixtures, and five negative fixtures. |
| `evals/evals.json` | [CÓDIGO] Replaced activation evals with 10 cases covering budget fit, compression, P0 preservation, missing estimates, preservation fields, response reserve, false positive, and script contract. |
| `examples/*` | [CÓDIGO] Added realistic context budget input and evidence-tagged output. |
| `agents/*`, `prompts/*`, `templates/*`, and `knowledge/*` | [CÓDIGO] Specialized scaffold text for budgeting, priority, compression, eviction, and offline validation. |

## Local Validation Evidence

- [CÓDIGO] `bash skills/context-window-management/scripts/check.sh` passed with valid
  over-budget and at-limit reports accepted, and over-budget-no-plan,
  P0-evicted, compression-expands, missing-preserve, and missing-estimate reports rejected.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill context-window-management`
  passed with `skills_with_scripts=1 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill context-window-management`
  passed with `skill=context-window-management dod=pass errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict` passed with
  `skills=600 warnings=0 errors=0`.

## Decision

[CONFIG] Improved and locally DoD-ready. Open a ready PR only after the full
repo validation suite passes.
