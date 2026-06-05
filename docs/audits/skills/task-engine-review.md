# Skill Review: task-engine

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`task-engine` applies deterministic DSVSR reasoning: Decompose, Solve, Verify, Synthesize, and Reflect with calibrated confidence, explicit evidence gaps, and no fake certainty. [CÓDIGO] The hardened skill must choose full DSVSR vs fast path deterministically, avoid network research by default, preserve confidence metadata, and block outputs that skip verification or hide weaknesses.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] One Phase 1 skill selected after `triad-composition`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to `task-engine`. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | complete | [CÓDIGO] Pre-hardening DoD failed with missing `assets/`, scaffold examples, root-list evals, and untracked scripts/assets during iteration. [CÓDIGO] WebSearch/WebFetch were allowed before hardening. | [CÓDIGO] No asset-backed activation policy, confidence scale, reflection policy, packet contract, or script fixture evidence. | [CONFIG] Add deterministic assets, offline validator, fixture contract, examples, eval cases, and remove network-by-default. | [INFERENCIA] Medium-high before hardening. |
| Eval Designer | complete | [CÓDIGO] Evals were broad prose activation cases. [CÓDIGO] DSVSR stages and metadata were not asserted. | [CÓDIGO] Missing decomposition, verify, synthesize, reflect, confidence calibration, missing context, false positive, blocked phrases, under-specification, and delegation fallback coverage. | [CONFIG] Convert evals to 10 DoD cases with exact expected checks and negative assertions. | [INFERENCIA] Medium-high before hardening. |
| Guardian | complete | [CÓDIGO] Ledger row was `pending`; review doc absent; DoD failed during intermediate snapshots until examples/evals/assets/scripts were restored. | [CONFIG] Full PR gates still required before merge. | [CONFIG] Block ledger closure until assets, evals, examples, scripts, review doc, DoD, and full PR gates pass. | [INFERENCIA] Low after per-skill validation, pending PR gates. |

## Hardening Brief

- [CONFIG] Add `assets/activation-policy.json`, `assets/confidence-scale.json`, `assets/reflection-policy.json`, and `assets/dsvsr-packet-contract.json`.
- [CONFIG] Add `scripts/validate_dsvsr_packet.py`, `scripts/check.sh`, Markdown packet fixtures, and `scripts/fixtures/fixture-contract.json`.
- [CONFIG] Replace scaffold README, examples, evals, agents, prompts, knowledge, reference, and templates with DSVSR-specific deterministic contracts.
- [CONFIG] Remove `WebSearch` and `WebFetch` from allowed tools; network research requires explicit user request and approved sources.
- [CONFIG] Replace missing reference-file list with existing assets and `references/domain-knowledge.md`.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added single-line trigger description, deterministic assets, validation commands, network guardrail, and actual reference list. |
| `README.md` | [CÓDIGO] Replaced scaffold text with activation, deterministic resources, and local checks. |
| `assets/` | [CÓDIGO] Added activation policy, confidence scale, reflection policy, packet contract, README, and manifest. |
| `scripts/` | [CÓDIGO] Added offline packet validator, JSON fixture contract, pass/fail Markdown fixtures, and `check.sh`. |
| `evals/evals.json` | [CÓDIGO] Replaced root-list evals with 10 DoD `cases` covering every DSVSR stage and false-certainty prevention. |
| `examples/*` | [CÓDIGO] Added realistic checkout rebuild input and DSVSR packet output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized roles around DSVSR activation, verification, confidence penalties, and Guardian blocking. |
| `templates/*` | [CÓDIGO] Replaced scaffold templates with packet-shaped offline templates. |
| `knowledge/*` and `references/*` | [CÓDIGO] Added DSVSR quality metrics, graph, heuristics, calibration, and stop conditions. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
python3 -m json.tool skills/task-engine/assets/manifest.json
python3 -m json.tool skills/task-engine/evals/evals.json
bash skills/task-engine/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill task-engine
python3 -B scripts/validate-skill-dod.py --skill task-engine
python3 -B scripts/validate-skills.py --strict
```

Results:

- [CÓDIGO] Asset, eval, knowledge graph, and fixture JSON parsed successfully.
- [CÓDIGO] `OK: task-engine DSVSR packets validated`
- [CÓDIGO] `skills_with_scripts=1 warnings=0 errors=0`
- [CÓDIGO] `skill=task-engine dod=pass errors=0`
- [CÓDIGO] `skills=600 warnings=0 errors=0`

## PR Gate Check

Observed on 2026-06-05:

```bash
python3 scripts/validate-skills.py --strict
python3 scripts/validate-skill-scripts.py --strict --run-checks
bash scripts/doc-factory/check.sh
python3 scripts/count-components.py --check-docs
bash scripts/check-repo-boundaries.sh
python3 scripts/validate-runtime-instructions.py
bash scripts/adapt.sh all
python3 scripts/qa/run-adversarial-tests.py
python3 scripts/qa/run-confidence-fp-tests.py
python3 scripts/post_annotations.py --validate-only references/schemas/annotations.example.json
bash scripts/generate-pristino-index.sh
git diff --check
git diff --cached --check
```

Results:

- [CÓDIGO] `skills=600 warnings=0 errors=0`
- [CÓDIGO] `skills_with_scripts=36 warnings=0 errors=0`
- [CÓDIGO] `OK: doc-factory deterministic smoke check passed`
- [CÓDIGO] `skills=600 agents=261 commands=267 prompts=256 components=1384`
- [CÓDIGO] `Repo boundaries OK`
- [CÓDIGO] `runtime instructions: passed`
- [CÓDIGO] `summary: passed=11 failed=0 total=11`
- [CÓDIGO] `OK: confidence calibration, stratified sampling, and FP-criteria checks passed`
- [CÓDIGO] `VALID: 2 annotation(s) conform to annotations.schema.json`
- [CÓDIGO] `shellcheck not installed; skipping shell lint`
- [CÓDIGO] `workflow-local-pass`

## Follow-Up Gap

- [DOC] Newton observed a repository-level README component-total drift (`1368` vs current `1384`). [CONFIG] That is outside this one-skill PR and should be handled in a separate repo-docs consistency PR if required by maintainers.

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CONFIG] Ledger status may be set to `dod-complete` after per-skill DoD and script checks pass, with PR merge still gated by full-repo validation.
