# Skill Review: assembly-skill

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`assembly-skill` orchestrates one target skill through diagnostic, intervention, certification, optional trigger optimization, and final report. [CÓDIGO] The hardened skill must keep the scope to one skill, enforce Gate B before writes, select modes by exact score thresholds, and reject premature certification.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] One Phase 1 skill selected after `agent-constitution-creator`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to `assembly-skill`. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | complete | [CÓDIGO] Pre-hardening DoD failed with 5 errors. [CÓDIGO] Scaffold text remained in README, examples, and templates; mode thresholds overlapped; HTML used remote fonts; date/duration were uncontrolled. | [CÓDIGO] No assets or scripts enforced mode selection, Gate B, report shape, or certification formula. | [CONFIG] Add mode policy, report contract, offline validator, fixtures, and offline templates. | [INFERENCIA] High before hardening. |
| Eval Designer | complete | [CÓDIGO] Evals were a raw seven-case activation array. | [CÓDIGO] Missing quick/standard/deep, auto-score, Gate B denial, no premature certification, evidence, and false-positive cases. | [CONFIG] Convert evals to DoD `cases` with concrete expected checks. | [INFERENCIA] High before hardening because certification could become wording-only. |
| Guardian | complete | [CÓDIGO] Ledger row was `pending`; review doc missing; skill-local scripts absent. | [CONFIG] Full PR gates still required before merge. | [CONFIG] Block ledger closure until assets, evals, examples, scripts, review doc, and DoD pass. | [INFERENCIA] Low after per-skill validation, pending PR gates. |

## Hardening Brief

- [CONFIG] Replace scaffold README, examples, evals, prompts, agents, templates, knowledge, and reference content with assembly-specific deterministic contracts.
- [CONFIG] Add `assets/mode-policy.json`, `assets/assembly-report-contract.json`, `assets/assembly-report-template.md`, and `assets/phase-gate-checklist.md`.
- [CONFIG] Add `scripts/validate_assembly_contract.py`, report fixtures, scorecard fixtures, and `scripts/check.sh`.
- [CONFIG] Convert evals to eleven DoD cases covering handoff, quick no-write, deep recertification, auto-mode thresholds, fail-closed missing skill, Gate B denial, no premature certification, evidence, and false positives.
- [CONFIG] Remove remote Google Fonts dependency and replace free date/duration with caller-provided `{{REPORT_DATE}}` or explicit duration source.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added `When to Activate`, exact auto-selection, one-skill scope, Gate B write rule, assets, scripts, and validation gate. |
| `README.md` | [CÓDIGO] Replaced scaffold text with activation, deterministic resources, required gates, and local checks. |
| `assets/` | [CÓDIGO] Added mode policy, report contract, template, checklist, README, and manifest. |
| `scripts/` | [CÓDIGO] Added report/mode validator, fixture contract, pass/fail Markdown fixtures, scorecard fixtures, and `check.sh`. |
| `evals/evals.json` | [CÓDIGO] Replaced root-list evals with eleven DoD `cases` and required expected checks. |
| `examples/*` | [CÓDIGO] Added realistic standard-mode input and report output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized responsibilities around one-skill scope, Gate B, report validation, quick/deep modes, and false-positive routing. |
| `templates/*` | [CÓDIGO] Replaced generic templates and removed remote network dependency. |
| `knowledge/*` and `references/*` | [CÓDIGO] Added deterministic mode, gate, certification, and anti-pattern guidance. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
python3 -m json.tool skills/assembly-skill/assets/manifest.json
python3 -m json.tool skills/assembly-skill/assets/mode-policy.json
python3 -m json.tool skills/assembly-skill/assets/assembly-report-contract.json
python3 -m json.tool skills/assembly-skill/evals/evals.json
bash skills/assembly-skill/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill assembly-skill
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill assembly-skill
python3 -B scripts/validate-skills.py --strict
```

Results:

- [CÓDIGO] `manifest-json-ok`
- [CÓDIGO] `mode-policy-json-ok`
- [CÓDIGO] `report-contract-json-ok`
- [CÓDIGO] `evals-json-ok`
- [CÓDIGO] `OK: assembly-skill contracts validated`
- [CÓDIGO] `skill=assembly-skill dod=pass errors=0`
- [CÓDIGO] `skills_with_scripts=1 warnings=0 errors=0`
- [CÓDIGO] `skills=600 warnings=0 errors=0`

## PR Gate Check

Observed on 2026-06-05:

```bash
python3 -B scripts/validate-skills.py --strict
python3 -B scripts/validate-skill-scripts.py --strict --run-checks
bash scripts/doc-factory/check.sh
python3 -B scripts/count-components.py --check-docs
bash scripts/check-repo-boundaries.sh
python3 -B scripts/validate-runtime-instructions.py
bash scripts/adapt.sh all
python3 -B scripts/qa/run-adversarial-tests.py
python3 -B scripts/qa/run-confidence-fp-tests.py
python3 -B scripts/post_annotations.py --validate-only references/schemas/annotations.example.json
bash scripts/generate-pristino-index.sh
git diff --check
```

Results:

- [CÓDIGO] `skills=600 warnings=0 errors=0`
- [CÓDIGO] `skills_with_scripts=33 warnings=0 errors=0`
- [CÓDIGO] `OK: doc-factory deterministic smoke check passed`
- [CÓDIGO] `skills=600 agents=261 commands=267 prompts=256 components=1384`
- [CÓDIGO] `Repo boundaries OK`
- [CÓDIGO] `runtime instructions: passed`
- [CÓDIGO] Runtime adapters refreshed for `.agent/skills_index.json`.
- [CÓDIGO] `summary: passed=11 failed=0 total=11`
- [CÓDIGO] `OK: confidence calibration, stratified sampling, and FP-criteria checks passed`
- [CÓDIGO] `VALID: 2 annotation(s) conform to annotations.schema.json`
- [CÓDIGO] `PRISTINO-INDEX.md` regenerated for the updated skill description.
- [CÓDIGO] `workflow-local-pass`

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CONFIG] Ledger status may be set to `dod-complete` after per-skill DoD and script checks pass, with PR merge still gated by full-repo validation.
