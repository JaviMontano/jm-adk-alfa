# Skill Review: certify-skill

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`certify-skill` is the final read-only certification gate for JM-ADK skills.
It evaluates a target skill with structural checks, content checks, systemic
coherence, rubric scoring, MOAT checks, and formula-derived certification
levels. [CÓDIGO] The hardened skill must block false certification levels,
ambiguous thresholds, skipped evidence, and self-certification drift.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] `certify-skill` selected as the next Phase 2 quality skill after `quality-gatekeeper`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | complete | [CÓDIGO] Pre-hardening DoD failed for missing `assets/`, scaffold examples, root-array evals, no scripts, tool drift, stale prompt heading references, `grep -P` portability risk, and Google Fonts in HTML. | [CÓDIGO] No deterministic validator for certification report schema, phase rows, rubric thresholds, or false-certified reports. | [CONFIG] Add assets, offline validator, fixtures, eval cases, offline templates, read-only agents, and portable check guidance. | [INFERENCIA] Medium-high before hardening because runtimes could disagree on structural evidence and formulas. |
| Eval Designer | complete | [CÓDIGO] Evals were 7 prose activation checks and did not test MOAT, CERTIFIED, CONDITIONAL, BLOCKED, threshold edges, single-file N/A, or false positives. | [CÓDIGO] Missing deterministic report schema assertions, rubric formula assertions, and exact phase row counts. | [CONFIG] Convert evals to 10 `cases` with expected certifications, expected checks, fixtures, and forbidden outputs. | [INFERENCIA] High before hardening because false certifications could pass evals. |
| Guardian | complete | [CÓDIGO] The skill required evidence for all phases but lacked assets, executable report validation, review evidence, ledger closure, and a completion gate. | [CONFIG] Full PR gates still required before merge. | [CONFIG] Block ledger closure until assets, scripts, evals, examples, review doc, DoD, and full gates pass. | [INFERENCIA] Low after per-skill validation, pending PR gates. |

## Hardening Brief

- [CONFIG] Add deterministic assets for certification phases, level policy,
  report contract, evidence policy, and activation routing.
- [CONFIG] Add `scripts/validate_certification_report.py`, `scripts/check.sh`,
  and MOAT, CONDITIONAL, and invalid false-certified fixtures.
- [CONFIG] Replace scaffold README, examples, evals, prompts, agents, templates,
  and knowledge files with certification-specific contracts.
- [CONFIG] Correct S9 stale-path wording and replace non-portable `grep -P`
  guidance with a portable Python extraction pattern.
- [CONFIG] Remove live web dependencies from templates and keep agents read-only.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added deterministic assets, activation boundaries, portable structural check guidance, validation script invocation, and clarified optional quality-rubric handling. |
| `README.md` | [CÓDIGO] Replaced scaffold text with activation, deterministic resources, local checks, and formula decision rule. |
| `assets/` | [CÓDIGO] Added manifest, certification phases, certification level policy, report contract, evidence policy, activation policy, and README. |
| `scripts/` | [CÓDIGO] Added offline certification report validator, `check.sh`, MOAT fixture, CONDITIONAL fixture, and invalid false-certified fixture. |
| `evals/evals.json` | [CÓDIGO] Replaced root-array evals with 10 DoD `cases` covering MOAT, CERTIFIED, CONDITIONAL, BLOCKED, threshold edges, single-file systemic N/A, and false positives. |
| `examples/*` | [CÓDIGO] Added realistic certification input and CONDITIONAL report output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized read-only roles and prompts around phase evidence, formulas, rubric thresholds, and Guardian blocking. |
| `templates/*` | [CÓDIGO] Replaced scaffold and live-font templates with offline Markdown, HTML, and DOCX-oriented certification templates. |
| `knowledge/*` | [CÓDIGO] Added canon, formula rules, anti-patterns, and a certification-specific knowledge graph. |
| `references/certification-checklist.md` | [CÓDIGO] Clarified that plural `references/` is valid and M1b accepts distinct `id` or `name` fields. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
bash skills/certify-skill/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill certify-skill
python3 -B scripts/validate-skill-dod.py --skill certify-skill
```

Results:

- [CÓDIGO] `OK: certify-skill reports validated deterministically`
- [CÓDIGO] `skills_with_scripts=1 warnings=0 errors=0`
- [CÓDIGO] `skill=certify-skill dod=pass errors=0`

## Follow-Up Gap

- [INFERENCIA] The validator proves report structure, phase coverage, rubric
  average math, level formula, and false-pass prevention; it does not prove the
  certified target skill's runtime behavior beyond supplied evidence.

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CÓDIGO] `bash skills/certify-skill/scripts/check.sh` passed with
  deterministic MOAT, CONDITIONAL, and invalid false-certified fixtures.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill certify-skill` passed with `warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill certify-skill` passed with `dod=pass errors=0`.

## PR Gate Check 2026-06-05

- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict` passed with `skills=600 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` passed with `skills_with_scripts=41 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/count-components.py --check-docs` passed with `skills=600 agents=261 commands=267 prompts=256 components=1384`.
- [CÓDIGO] `bash scripts/check-repo-boundaries.sh` passed with `Repo boundaries OK`.
- [CÓDIGO] `python3 -B scripts/validate-runtime-instructions.py` passed with `runtime instructions: passed`.
- [CÓDIGO] `python3 -B scripts/qa/run-adversarial-tests.py` passed with `summary: passed=11 failed=0 total=11`.
- [CÓDIGO] `python3 -B scripts/qa/run-confidence-fp-tests.py` passed with `OK: confidence calibration, stratified sampling, and FP-criteria checks passed`.
- [CÓDIGO] `python3 -B scripts/post_annotations.py --validate-only references/schemas/annotations.example.json` passed with schema-valid annotations.
- [CÓDIGO] `bash scripts/doc-factory/check.sh` passed with `VALIDATION PASSED`, `VERIFICATION PASSED`, and deterministic smoke output.
- [CÓDIGO] `python3 -B scripts/diagnose-user-context.py --dry-run` reported `USER_CONTEXT_STATUS: ready`.
- [CÓDIGO] `python3 -B scripts/diagnose-personal-skills.py --dry-run` reported `PERSONAL_SKILLS_STATUS: empty`.
- [CÓDIGO] `python3 -B scripts/sync-personal-skills.py --dry-run --target /tmp/alfa-personal-skills-target` reported `files=0`.
- [CÓDIGO] `bash scripts/adapt.sh all` regenerated runtime adapters with `Total skills: 600`.
- [CÓDIGO] `bash scripts/generate-pristino-index.sh` regenerated `PRISTINO-INDEX.md` with `Agents: 261 | Skills: 600 | Commands: 267 | Prompts: 256 | Components: 1384`.
- [CÓDIGO] `git diff --check` passed with no whitespace errors.
- [CONFIG] `shellcheck skills/certify-skill/scripts/check.sh` was requested but skipped because `shellcheck` is not installed in this environment (`command not found`).
