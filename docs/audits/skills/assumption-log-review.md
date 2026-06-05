# Skill Review: assumption-log

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`assumption-log` tracks project assumptions as deterministic `A-NNN` entries
with allowed statuses, evidence tags, contradiction links, decision links, and
validation queue actions. [CÓDIGO] The hardened skill blocks false validation,
unsupported tags, missing high-impact queue entries, and scaffold output drift.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] `assumption-log` selected as the next Phase 2 quality skill after `certify-skill`; branch created from `origin/main` with zero open PRs. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope stays isolated. |
| Determinism Auditor | complete | [CÓDIGO] Pre-hardening skill had broken activation references, scaffold README/examples/templates/knowledge, broad `Write/Edit` tools, Google Fonts, vague output placeholders, and inconsistent evidence tags. | [CÓDIGO] No machine-readable status taxonomy, activation matrix, negative trigger corpus, golden fixtures, or local validator existed. | [CONFIG] Add assets, offline validator, fixtures, read-only agents, deterministic templates, normalized evidence tags, and explicit activation rules. | [INFERENCIA] High before hardening because production status could still produce non-reproducible logs. |
| Eval Designer | complete | [CÓDIGO] Evals were generic activation checks and used `[OPEN]` despite the skill contract using status values. | [CÓDIGO] Missing tests for `A-NNN` IDs, ID preservation, lifecycle transitions, evidence tags, contradictions, decision links, stale review, threshold warning, and false positives. | [CONFIG] Replace evals with 12 deterministic `cases` and suite-level assertions for IDs, statuses, evidence tags, false positives, and forbidden phrases. | [INFERENCIA] Medium before hardening because generic evals could pass while the assumption contract failed. |
| Guardian | complete | [CÓDIGO] Initial DoD failed with 5 errors: missing `assets/`, scaffold examples, and evals without `cases`; ledger was pending and no review doc existed. | [CÓDIGO] Ledger completion required assets, evals, scripts if added, review evidence, and validation output. | [CONFIG] Block ledger closure until per-skill DoD, scripts, review doc, and PR gates pass. | [INFERENCIA] Low after validation, pending full PR gates. |

## Hardening Brief

- [CONFIG] Add deterministic assets for activation, status lifecycle, output
  contract, evidence policy, and asset manifest.
- [CONFIG] Add `scripts/validate_assumption_log.py`, `scripts/check.sh`, one
  valid fixture, and two negative fixtures for ID gaps and false validation.
- [CONFIG] Replace scaffold README, examples, evals, agents, prompts, templates,
  and knowledge files with assumption-log-specific contracts.
- [CONFIG] Remove mutation tools from skill and agents; keep local `Bash` only
  for deterministic validators.
- [CONFIG] Remove network dependencies from HTML/DOCX templates and avoid
  wall-clock date inference.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added deterministic assets, activation boundaries, input/output contracts, lifecycle process, local validator commands, and read-only limits. |
| `README.md` | [CÓDIGO] Replaced scaffold text with resources, local checks, and decision rule. |
| `assets/` | [CÓDIGO] Added activation policy, status policy, log contract, evidence policy, manifest, and README. |
| `scripts/` | [CÓDIGO] Added offline validator, check script, valid fixture, ID-gap negative fixture, and false-validated negative fixture. |
| `evals/evals.json` | [CÓDIGO] Replaced root-array evals with 12 `cases` covering lifecycle, contradictions, decision links, threshold warnings, empty input, phase separation, and false positives. |
| `examples/*` | [CÓDIGO] Added realistic payment onboarding input and assumption log output. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized read-only roles and prompts around activation, evidence mapping, guardian blocking, and no skipped evidence in quick mode. |
| `templates/*` | [CÓDIGO] Replaced scaffold and remote-font templates with offline Markdown, HTML, and DOCX-oriented templates. |
| `knowledge/*` | [CÓDIGO] Added normalized evidence taxonomy, lifecycle rules, anti-patterns, and an assumption-specific knowledge graph. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
bash skills/assumption-log/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill assumption-log
python3 -B scripts/validate-skill-dod.py --skill assumption-log
python3 -B scripts/validate-skills.py --strict
```

Results:

- [CÓDIGO] `OK: assumption-log reports validated deterministically`
- [CÓDIGO] `skills_with_scripts=1 warnings=0 errors=0`
- [CÓDIGO] `skill=assumption-log dod=pass errors=0`
- [CÓDIGO] `skills=600 warnings=0 errors=0`

## Follow-Up Gap

- [INFERENCIA] The validator proves report structure, IDs, statuses, evidence
  tags, counts, contradictions, decision links, queue coverage, and warning
  thresholds; it does not prove that external evidence supplied by a user is
  factually complete.

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CÓDIGO] `bash skills/assumption-log/scripts/check.sh` passed with valid,
  invalid ID-gap, and invalid false-validated fixtures.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill assumption-log` passed with `warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill assumption-log` passed with `dod=pass errors=0`.

## PR Gate Check 2026-06-05

- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict` passed with `skills=600 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` passed with `skills_with_scripts=42 warnings=0 errors=0`.
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
- [CONFIG] `shellcheck skills/assumption-log/scripts/check.sh` was requested but skipped because `shellcheck` is not installed in this environment (`command not found`).
