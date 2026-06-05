# Skill Review: workflow-creator

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`workflow-creator` creates deterministic 17-field workflow definitions with
ordered step contracts, DoD, QA, RACI, KPIs, fallback, escalation, and local
validation evidence. [CÓDIGO] The hardened skill must reject generic checklists,
avoid invented owners, keep missing catalog context `[OPEN]`, and prove
workflow structure with offline fixtures when JSON is available.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] One Phase 1 skill selected after `task-engine`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to `workflow-creator`. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | complete | [CÓDIGO] Pre-hardening DoD failed with missing `assets/`, scaffold examples, root-array evals, incomplete script path, and prompt drift. [CÓDIGO] Quick mode skipped evidence tagging and deep mode referenced nonexistent `references/`. | [CÓDIGO] No executable validator proved the 17-field and 12-step-field workflow contract. | [CONFIG] Add assets, offline validator, fixtures, eval `cases`, concrete examples, and prompt alignment. | [INFERENCIA] High before hardening because vague workflow specs could pass narrative review. |
| Eval Designer | complete | [CÓDIGO] Evals used vague `expected_behavior` prose instead of deterministic checks. | [CÓDIGO] Missing tests for absent owner, duplicate workflow, invalid ID, missing step spec, step bounds, vague fields, RACI, KPIs, and workflow-adjacent false positives. | [CONFIG] Convert evals to at least 10 `cases` with `expected_activation`, `expected_outputs`, `forbidden_outputs`, and required DoD checks. | [INFERENCIA] High before hardening because false positives and weak specs were unblocked. |
| Guardian | complete | [CÓDIGO] Intermediate snapshots failed DoD until assets, scripts, evals, examples, review doc, and ledger evidence were completed. | [CONFIG] Full PR gates still required before merge. | [CONFIG] Block ledger closure until `check.sh`, script contract, and DoD pass. | [INFERENCIA] Low after per-skill validation, pending PR gates. |

## Hardening Brief

- [CONFIG] Add `assets/workflow-definition-contract.json`,
  `assets/activation-policy.json`, `assets/quality-gates.json`, and
  `assets/workflow-output-template.md`.
- [CONFIG] Add `scripts/validate_workflow_spec.py`, `scripts/check.sh`, and
  positive/negative JSON fixtures.
- [CONFIG] Replace scaffold README, examples, evals, agents, prompts,
  knowledge, and templates with workflow-specific deterministic contracts.
- [CONFIG] Remove remote font dependency from HTML and prohibit dynamic
  timestamps unless explicitly requested.
- [CONFIG] Update only the `workflow-creator` ledger row after per-skill gates
  pass.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added deterministic assets, activation boundaries, required inputs, output contract, creation process, validation gate, and edge cases. |
| `README.md` | [CÓDIGO] Replaced scaffold text with activation, deterministic resources, and local checks. |
| `assets/` | [CÓDIGO] Added contract, activation policy, quality gates, output template, README, and manifest. |
| `scripts/` | [CÓDIGO] Added offline JSON validator, `check.sh`, and pass/fail fixtures for workflow specs. |
| `evals/evals.json` | [CÓDIGO] Replaced root-array evals with 10 DoD `cases` covering happy path, gaps, invalid IDs, duplicates, absent step spec, step bounds, vague fields, RACI, and false positives. |
| `examples/*` | [CÓDIGO] Added realistic skill-hardening handoff request and full 17-field workflow output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Aligned Lead, Support, Specialist, Guardian, primary, meta, quick, and deep prompts with evidence and asset-backed validation. |
| `templates/*` | [CÓDIGO] Replaced scaffold templates with offline Markdown, HTML, and DOCX outline templates. |
| `knowledge/*` | [CÓDIGO] Added workflow contract metrics, anti-patterns, and graph relationships. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
bash skills/workflow-creator/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill workflow-creator
python3 -B scripts/validate-skill-dod.py --skill workflow-creator
```

Results:

- [CÓDIGO] `OK: workflow-creator specs validated deterministically`
- [CÓDIGO] `skills_with_scripts=1 warnings=0 errors=0`
- [CÓDIGO] `skill=workflow-creator dod=pass errors=0`

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
- [CÓDIGO] `skills_with_scripts=37 warnings=0 errors=0`
- [CÓDIGO] `OK: doc-factory deterministic smoke check passed`
- [CÓDIGO] `skills=600 agents=261 commands=267 prompts=256 components=1384`
- [CÓDIGO] `Repo boundaries OK`
- [CÓDIGO] `runtime instructions: passed`
- [CÓDIGO] `adapt-clean`
- [CÓDIGO] `summary: passed=11 failed=0 total=11`
- [CÓDIGO] `OK: confidence calibration, stratified sampling, and FP-criteria checks passed`
- [CÓDIGO] `VALID: 2 annotation(s) conform to annotations.schema.json`
- [CÓDIGO] `shellcheck not installed; skipping shell lint`
- [CÓDIGO] `git diff --check` and `git diff --cached --check` passed.

## Follow-Up Gap

- [INFERENCIA] The validator proves structure, step completeness, RACI/KPI
  concreteness, and fail-closed wording; it does not prove the workflow is the
  strategically best decomposition for every domain.

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CÓDIGO] `bash skills/workflow-creator/scripts/check.sh` passed with
  deterministic positive and negative fixtures.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill workflow-creator` passed with `warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill workflow-creator` passed with `dod=pass errors=0`.
