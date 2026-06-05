# Skill Review: benchmark-skill

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`benchmark-skill` compares two skill states or one skill against a benchmark
standard using inventory deltas, 10-dimension scoring, 13 gates, regression
detection, trade-off analysis, and a policy-backed net assessment. [CÓDIGO]
The hardened skill must not fabricate missing baselines, must keep compared
states read-only, and must block unsupported `IMPROVED` conclusions.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] First Phase 2 skill selected after `workflow-creator`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to `benchmark-skill`. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | complete | [CÓDIGO] Pre-hardening DoD failed with missing `assets/`, scaffold examples, root-array evals, no scripts, Google Fonts in HTML, prompt heading drift, and agent tool drift. | [CÓDIGO] No deterministic fixture-backed proof for score deltas, gates, or assessment labels. | [CONFIG] Add assets, validator, fixtures, eval cases, offline templates, and read-only agent tools. | [INFERENCIA] High before hardening because benchmark reports could sound persuasive without proving improvement. |
| Eval Designer | complete | [CÓDIGO] Evals were prose activation checks and did not test dimensions, deltas, net labels, missing baselines, transformed states, or false positives. | [CÓDIGO] Missing deterministic cases for improved, regressed, lateral, transformed, identical, against-standard, missing baseline, missing `SKILL.md`, and non-skill comparisons. | [CONFIG] Convert evals to 10 `cases` with expected outputs, forbidden outputs, and required DoD checks. | [INFERENCIA] High before hardening because inflated improvement labels were unblocked. |
| Guardian | complete | [CÓDIGO] Ledger row was `pending`, review doc absent, assets absent, examples scaffold, evals root array, and agents had write tools despite read-only purpose. | [CONFIG] Full PR gates still required before merge. | [CONFIG] Block ledger closure until assets, scripts, evals, examples, review doc, DoD, and full gates pass. | [INFERENCIA] Low after per-skill validation, pending PR gates. |

## Hardening Brief

- [CONFIG] Add `assets/benchmark-rubric.json`, `assets/gate-policy.json`,
  `assets/net-assessment-policy.json`, and `assets/report-contract.json`.
- [CONFIG] Add `scripts/validate_benchmark_report.py`, `scripts/check.sh`, and
  pass/fail JSON report fixtures.
- [CONFIG] Replace scaffold README, examples, evals, agents, prompts,
  knowledge, and templates with benchmark-specific deterministic contracts.
- [CONFIG] Remove Google Fonts and dynamic date dependency from templates.
- [CONFIG] Align all benchmark agents to read-only tools.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added deterministic assets, activation boundaries, input modes, benchmark process, report contract, net assessment rules, validation gate, and failure modes. |
| `README.md` | [CÓDIGO] Replaced scaffold text with activation, deterministic resources, and local checks. |
| `assets/` | [CÓDIGO] Added rubric, gate policy, net assessment policy, report contract, README, and manifest. |
| `scripts/` | [CÓDIGO] Added offline report validator, `check.sh`, valid improved report fixture, inflated-label negative fixture, and missing-baseline negative fixture. |
| `evals/evals.json` | [CÓDIGO] Replaced root-array evals with 10 DoD `cases` covering improved, regressed, lateral, transformed, identical, against-standard, missing baseline, missing `SKILL.md`, and false positives. |
| `examples/*` | [CÓDIGO] Added realistic before/after benchmark input and full report output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized read-only roles around scoring, evidence, deltas, and Guardian blocking. |
| `templates/*` | [CÓDIGO] Replaced scaffold and live-font templates with offline benchmark templates. |
| `knowledge/*` | [CÓDIGO] Added scoring discipline, quality metrics, anti-patterns, and benchmark graph. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
bash skills/benchmark-skill/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill benchmark-skill
python3 -B scripts/validate-skill-dod.py --skill benchmark-skill
```

Results:

- [CÓDIGO] `OK: benchmark-skill reports validated deterministically`
- [CÓDIGO] `skills_with_scripts=1 warnings=0 errors=0`
- [CÓDIGO] `skill=benchmark-skill dod=pass errors=0`

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
- [CÓDIGO] `skills_with_scripts=38 warnings=0 errors=0`
- [CÓDIGO] `OK: doc-factory deterministic smoke check passed`
- [CÓDIGO] `skills=600 agents=261 commands=267 prompts=256 components=1384`
- [CÓDIGO] `Repo boundaries OK`
- [CÓDIGO] `runtime instructions: passed`
- [CÓDIGO] `adapt-clean`
- [CÓDIGO] `summary: passed=11 failed=0 total=11`
- [CÓDIGO] `OK: confidence calibration, stratified sampling, and FP-criteria checks passed`
- [CÓDIGO] `VALID: 2 annotation(s) conform to annotations.schema.json`
- [CÓDIGO] `pristino-clean`
- [CÓDIGO] `shellcheck not installed; skipping shell lint`

## Follow-Up Gap

- [INFERENCIA] The validator proves report consistency, score math, gate
  coverage, and label policy; it does not prove runtime behavior changes. Use
  task-level eval transcripts when behavioral benchmark evidence is required.

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CÓDIGO] `bash skills/benchmark-skill/scripts/check.sh` passed with
  deterministic positive and negative fixtures.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill benchmark-skill` passed with `warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill benchmark-skill` passed with `dod=pass errors=0`.
