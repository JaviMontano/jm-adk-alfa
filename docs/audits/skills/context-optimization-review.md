# Skill Review: context-optimization

Date: 2026-06-06
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`context-optimization` configures progressive loading, relevance-based routing,
safe pruning, lazy loading, and session-state persistence for token-efficient
agent workflows. [CÓDIGO]

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | pass | [CONFIG] `context-optimization` selected as the ninth active skill after `context-window-management` merged. | [CONFIG] None after clean preflight. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope stays isolated. |
| Determinism Auditor | block | [CÓDIGO] Initial DoD failed because assets were missing, examples were generic, and evals lacked `cases`. | [CÓDIGO] Missing loading level, relevance, pruning, session state, report contract, and offline validation. | [CONFIG] Preserve progressive MOAT loading intent and add deterministic proof. | [INFERENCIA] High before hardening because multiple L3 skills or risky pruning could pass. |
| Eval Designer | pass | [CÓDIGO] Original evals were generic activation checks. | [CÓDIGO] Missing progressive-loading, lazy-load, session-state, two-L3, low-relevance-L3, risky-prune, no-improvement, unauthorized-persist, false-positive, and script-contract cases. | [CONFIG] Replace evals with deterministic context optimization scenarios. | [INFERENCIA] Medium before hardening because optimization metrics were not machine-checked. |
| Script Engineer | pass | [CÓDIGO] The skill had no script contract. | [CÓDIGO] Missing local proof for L3 limit, relevance thresholds, prune safety, persistence authorization, utilization, and improvement metrics. | [CONFIG] Add validator, check script, two valid fixtures, and five negative fixtures. | [INFERENCIA] Medium before hardening because no offline verifier existed. |
| Integrator | pass | [CÓDIGO] Updated only `skills/context-optimization/**`, this review doc, and the `context-optimization` ledger row. | [CONFIG] None after integration. | [CONFIG] Do not touch other accelerator skills in this PR. | [CONFIG] Low if validation remains green. |
| Guardian | pass | [CÓDIGO] Per-skill DoD and script validations pass after hardening. | [CONFIG] PR, CI, merge, and branch cleanup evidence remain pending until PR lifecycle runs. | [CONFIG] Open PR only after full repo validation passes. | [INFERENCIA] Low local risk; remote CI remains pending until PR creation. |

## Hardening Brief

- skill: `context-optimization`
- scope_allowed: `skills/context-optimization/**`, `docs/audits/skills/context-optimization-review.md`, and the `context-optimization` row in `docs/audits/skill-review-ledger.csv`
- required_changes: add deterministic assets, replace scaffold README/examples/evals, add offline report validator and fixtures, preserve progressive-loading intent, and record evidence
- forbidden_changes: no other skills, no unrelated ledger rows, no more than one L3 active skill, no risky prune, no unauthorized session-state persistence, no fake improvement metrics
- validation_plan: run per-skill validators, repo validators, whitespace check, PR checks, squash merge, branch cleanup, and main update
- merge_criteria: local validations pass, PR CI passes, squash merge succeeds, branch cleanup succeeds, and `main` is updated

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added deterministic resources and script validation criterion while preserving progressive MOAT loading intent. |
| `README.md` | [CÓDIGO] Replaced scaffold text with triggers, resources, output sections, validation command, and safety rules. |
| `assets/` | [CÓDIGO] Added loading-level, relevance, pruning, session-state, report contract, manifest, and README assets. |
| `scripts/` | [CÓDIGO] Added offline report validator, check script, two valid fixtures, and five negative fixtures. |
| `evals/evals.json` | [CÓDIGO] Replaced activation evals with 10 cases covering progressive loading, lazy load, session state, L3 limits, relevance, pruning, metrics, authorization, false positive, and script contract. |
| `examples/*` | [CÓDIGO] Added realistic optimization input and evidence-tagged output. |
| `agents/*`, `templates/*`, and `knowledge/*` | [CÓDIGO] Specialized scaffold text for loading levels, pruning, session state, metrics, and offline validation. |

## Local Validation Evidence

- [CÓDIGO] `bash skills/context-optimization/scripts/check.sh` passed with valid
  standard and lazy-load reports accepted, and two-L3, low-relevance-L3,
  risky-prune, no-improvement, and unauthorized-persist reports rejected.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill context-optimization`
  passed with `skills_with_scripts=1 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill context-optimization`
  passed with `skill=context-optimization dod=pass errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict` passed with
  `skills=600 warnings=0 errors=0`.

## Decision

[CONFIG] Improved and locally DoD-ready. Open a ready PR only after the full
repo validation suite passes.
