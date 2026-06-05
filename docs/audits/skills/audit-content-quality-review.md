# Skill Review: audit-content-quality

Date: 2026-06-05
Reviewer: Codex multiagent hardening pass
Status: reviewed and improved
Severity: P1

## Intended Purpose

`audit-content-quality` audits `SKILL.md` content contracts with a
deterministic six-dimension rubric, per-skill scorecards, plugin averages,
bottom-skill priorities, systematic gap detection, and report validation.
[CÓDIGO] The hardened skill blocks false grades, missing rationales, hidden weak
skills, generic advice, scaffold drift, and adjacent false activations.

## Spoke Reports

| Spoke | Status | Findings | Coverage Gaps | Recommended Changes | Risk |
|---|---|---|---|---|---|
| Coordinator | complete | [CONFIG] `audit-content-quality` selected as the next Phase 2 quality skill after `assumption-log`; branch created from `origin/main` with zero open PRs. | [CONFIG] None. | [CONFIG] Keep branch and PR scoped to one skill. | [CONFIG] Low if scope stays isolated. |
| Determinism Auditor | complete | [CÓDIGO] Pre-hardening skill had scaffold README/examples/templates/knowledge, no `## When To Activate`, unsafe write-capable agents, remote font template dependency, weak evals, and inconsistent 1-10 versus 0-10 rubric scale. | [CÓDIGO] No deterministic local scorer, report validator, fixtures, or machine-readable report contract existed. | [CONFIG] Add assets, offline validator, fixtures, read-only agents, deterministic templates, normalized rubric, and explicit activation rules. | [INFERENCIA] High before hardening because plausible reports could contain non-reproducible grades. |
| Eval Designer | complete | [CÓDIGO] Evals were a root array of generic activation tests and did not check scoring math, thresholds, bottom ordering, malformed frontmatter, skipped skills, or false positives. | [CÓDIGO] Missing test cases for exact six dimensions, per-score rationales, plugin-average math, systematic gaps, single-skill targets, empty plugins, and adjacent non-skill reviews. | [CONFIG] Replace evals with 13 deterministic `cases` and suite-level assertions for dimensions, score bounds, formulas, thresholds, and false positives. | [INFERENCIA] High before hardening because generic evals could pass while audit math failed. |
| Guardian | complete | [CÓDIGO] Initial DoD failed for missing `assets/`, scaffold examples, and evals without `cases`; script fixtures initially exposed an average mismatch. | [CÓDIGO] Ledger completion required assets, scripts, purpose-specific examples, evals, review evidence, and passing validations. | [CONFIG] Fix valid fixture average to `42.00 / 70.00`, add review doc, and only mark ledger complete after DoD and script gates pass. | [INFERENCIA] Low after local validation, pending full PR gates. |

## Hardening Brief

- [CONFIG] Add deterministic assets for activation, scoring rubric, report
  contract, evidence policy, and asset manifest.
- [CONFIG] Add `scripts/validate_content_quality_report.py`, `scripts/check.sh`,
  one valid fixture, and two negative fixtures for wrong grades and missing
  bottom skills.
- [CONFIG] Replace scaffold README, examples, evals, agents, prompts, templates,
  knowledge files, and rubric reference with skill-specific contracts.
- [CONFIG] Normalize the rubric to `0-10`, total score out of `60`, grade
  thresholds, bottom-skill ordering, and systematic gap threshold.
- [CONFIG] Remove mutation tools from agents and remove remote assets from
  HTML/DOCX templates.

## Improvement Applied

| Area | Change |
|---|---|
| `SKILL.md` | [CÓDIGO] Added deterministic assets, activation boundaries, input/output contract, local validator commands, formula rules, and read-only limits. |
| `README.md` | [CÓDIGO] Replaced scaffold text with local resources, checks, and formula-derived decision rule. |
| `assets/` | [CÓDIGO] Added activation policy, scoring rubric, report contract, evidence policy, manifest, and README. |
| `scripts/` | [CÓDIGO] Added offline report validator, check script, valid fixture, wrong-grade negative fixture, and missing-bottom negative fixture. |
| `evals/evals.json` | [CÓDIGO] Replaced root-array evals with 13 `cases` covering formulas, rationales, thresholds, malformed frontmatter, scaffold detection, bottom ordering, single-skill targets, empty plugin, clarification, and false positives. |
| `examples/*` | [CÓDIGO] Added realistic sample-plugin input and scorecard output with corrected `42.00 / 70.00` average. |
| `agents/*` and `prompts/*` | [CÓDIGO] Specialized read-only roles and prompts around activation, score evidence, formula checks, and no skipped rationales in quick mode. |
| `templates/*` | [CÓDIGO] Replaced scaffold and remote-font templates with offline Markdown, HTML, and DOCX-oriented scorecard templates. |
| `knowledge/*` | [CÓDIGO] Added normalized evidence taxonomy, scoring invariants, anti-patterns, and a content-quality-specific knowledge graph. |
| `references/content-quality-rubric.md` | [CÓDIGO] Replaced inconsistent scale text with a human-readable mirror of `assets/scoring-rubric.json`. |

## Per-Skill No-Regression Check

Observed on 2026-06-05:

```bash
bash skills/audit-content-quality/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill audit-content-quality
python3 -B scripts/validate-skill-dod.py --skill audit-content-quality
python3 -B scripts/validate-skills.py --strict
```

Results:

- [CÓDIGO] `OK: audit-content-quality reports validated deterministically`
- [CÓDIGO] `skills_with_scripts=1 warnings=0 errors=0`
- [CÓDIGO] `skill=audit-content-quality dod=pass errors=0`
- [CÓDIGO] `skills=600 warnings=0 errors=0`

## Follow-Up Gap

- [INFERENCIA] The validator proves output structure, score formulas, grade
  thresholds, averages, bottom-skill ordering, systematic gaps, coverage, and
  rationales; it does not prove semantic truth of a target skill's domain claims.

## Decision

[CONFIG] Improved now and ready for full PR validation.

## Ledger Completion 2026-06-05

- [CÓDIGO] `bash skills/audit-content-quality/scripts/check.sh` passed with
  valid, invalid wrong-grade, and invalid missing-bottom fixtures.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill audit-content-quality` passed with `warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-dod.py --skill audit-content-quality` passed with `dod=pass errors=0`.

## Final Subagent Review 2026-06-05

- [CÓDIGO] Final read-only Guardian reported `PASS_FOR_LEDGER_CLOSURE`.
- [CÓDIGO] The final review found no blocking scaffold remnants, consistent score math, 13 eval `cases`, offline templates, referenced assets/scripts, and a `dod-complete` ledger row.
- [INFERENCIA] Remaining advisory is low risk: `Bash` remains allowed only for local validator execution; mutation tools such as `Write`, `Edit`, and `MultiEdit` are absent.

## PR Gate Check 2026-06-05

- [CÓDIGO] `python3 -B scripts/validate-skills.py --strict` passed with `skills=600 warnings=0 errors=0`.
- [CÓDIGO] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` passed with `skills_with_scripts=43 warnings=0 errors=0`.
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
- [CONFIG] `shellcheck skills/audit-content-quality/scripts/check.sh` was requested but skipped because `shellcheck` is not installed in this environment (`command not found`).
