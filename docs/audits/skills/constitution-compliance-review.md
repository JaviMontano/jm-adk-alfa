# Skill Review: constitution-compliance

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`constitution-compliance` validates artifacts against JM-ADK Constitution
v6.0.0 using an 18-principle matrix, G0-G3 gate impact, evidence tags, severity,
remediation, and fail-closed missing-evidence handling. [CÓDIGO] The hardened
skill must block stale-version targets, unsupported pass decisions, missing
evidence, and incomplete principle coverage.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] `constitution-compliance` selected as next Phase 2 quality skill after `benchmark-skill`; branch created from `origin/main`. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope remains isolated. |
| Determinism Auditor | complete | [CÓDIGO] Pre-hardening DoD failed for missing `assets/`, scaffold examples, root-array evals, no scripts, stale v5.2.0 purpose, Google Fonts in HTML, and generic prompts. | [CÓDIGO] No deterministic validator for 18-row matrix, gate impact, missing evidence, or false-pass prevention. | [CONFIG] Add v6.0.0 assets, offline validator, fixtures, eval cases, templates, and read-only agents. | [INFERENCIA] High before hardening because reports could claim compliance without proving it. |
| Eval Designer | complete | [CÓDIGO] Evals lacked `cases` and did not exercise stale version, missing evidence, P0/P1 blocks, full 18-principle coverage, or false positives. | [CÓDIGO] Missing positive, blocked, invalid, and non-activation scenarios. | [CONFIG] Convert evals to 10 structured cases with expected outputs, forbidden outputs, and required DoD checks. | [INFERENCIA] High before hardening because false-positive activation and false pass decisions were unblocked. |
| Guardian | complete | [CÓDIGO] Ledger row was `pending`, review doc absent, assets absent, scripts absent, and supporting files contained scaffold text. | [CONFIG] Full PR gates still required before merge. | [CONFIG] Block ledger closure until assets, scripts, evals, examples, review doc, DoD, and full gates pass. | [INFERENCIA] Low after per-skill validation, pending PR gates. |

## Hardening Brief

- [CONFIG] Update the target to JM-ADK Constitution v6.0.0 and preserve v5.2.0
  only as a stale-version finding.
- [CONFIG] Add machine-readable assets for principles, severity, activation, and
  report contract.
- [CONFIG] Add deterministic validator fixtures for pass, blocked, and invalid
  false-pass reports.
- [CONFIG] Replace scaffold README, examples, evals, prompts, agents, templates,
  and knowledge files with constitution-specific contracts.
- [CONFIG] Remove live web dependencies from templates and keep agent roles
  read-only.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added v6.0.0 activation boundaries, required inputs, 18-principle process, report contract, validation gate, severity policy, and edge cases. |
| `README.md` | [CÓDIGO] Replaced scaffold text with activation guidance, deterministic resources, and local checks. |
| `assets/` | [CÓDIGO] Added manifest, v6.0.0 principle map, severity policy, activation policy, report contract, and README. |
| `scripts/` | [CÓDIGO] Added offline JSON report validator, `check.sh`, and valid pass, valid blocked, and invalid false-pass fixtures. |
| `evals/evals.json` | [CÓDIGO] Replaced root-array evals with 10 DoD `cases` covering pass, stale version, missing evidence, P0 block, conflicts, full matrix coverage, invalid evidence tags, and false positives. |
| `examples/*` | [CÓDIGO] Added realistic audit input and full 18-principle report output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized read-only roles and prompts around v6.0.0, fail-closed missing evidence, and Guardian blocking. |
| `templates/*` | [CÓDIGO] Replaced scaffold and live-font templates with offline Markdown, HTML, and DOCX-oriented report templates. |
| `knowledge/*` | [CÓDIGO] Added canon, operating rules, anti-patterns, and a constitution-specific knowledge graph. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
bash skills/constitution-compliance/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill constitution-compliance
python3 -B scripts/validate-skill-dod.py --skill constitution-compliance
```

Results:

- [CÓDIGO] `OK: constitution-compliance reports validated deterministically`
- [CÓDIGO] `skills_with_scripts=1 warnings=0 errors=0`
- [CÓDIGO] `skill=constitution-compliance dod=pass errors=0`

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
python3 -B scripts/diagnose-user-context.py --dry-run
python3 -B scripts/diagnose-personal-skills.py --dry-run
python3 -B scripts/sync-personal-skills.py --dry-run --target /tmp/alfa-personal-skills-target
bash scripts/generate-pristino-index.sh
git diff --check
```

Results:

- [CÓDIGO] `skills=600 warnings=0 errors=0`
- [CÓDIGO] `skills_with_scripts=39 warnings=0 errors=0`
- [CÓDIGO] `OK: doc-factory deterministic smoke check passed`
- [CÓDIGO] `skills=600 agents=261 commands=267 prompts=256 components=1384`
- [CÓDIGO] `Repo boundaries OK`
- [CÓDIGO] `runtime instructions: passed`
- [CÓDIGO] `ADAPTER-COMPLETE: antigravity (600 skills indexed)`
- [CÓDIGO] `summary: passed=11 failed=0 total=11`
- [CÓDIGO] `OK: confidence calibration, stratified sampling, and FP-criteria checks passed`
- [CÓDIGO] `VALID: 2 annotation(s) conform to annotations.schema.json`
- [CÓDIGO] `USER_CONTEXT_STATUS: ready`
- [CÓDIGO] `PERSONAL_SKILLS_STATUS: empty`
- [CÓDIGO] `Generated: PRISTINO-INDEX.md`
- [CÓDIGO] `shellcheck` was not installed in this environment, so shell lint was
  skipped.

## Follow-Up Gap

- [INFERENCIA] The validator proves report structure, version, principle
  coverage, severity consistency, gate blocking, and false-pass prevention; it
  does not prove the audited artifact itself is correct beyond cited evidence.

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CÓDIGO] `bash skills/constitution-compliance/scripts/check.sh` passed with
  deterministic pass, blocked, and invalid fixtures.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill constitution-compliance` passed with `warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill constitution-compliance` passed with `dod=pass errors=0`.
