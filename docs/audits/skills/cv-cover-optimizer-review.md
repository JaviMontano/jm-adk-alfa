# Cv Cover Optimizer Review

## SpokeReport - Ledger Auditor

- status: pass
- findings: `cv-cover-optimizer` was imported from a multi-skill branch and did not exist in `main`.
- coverage_gaps: No ledger row or review doc existed for the isolated import.
- recommended_changes: Add only the active skill, review doc, ledger row, and generated indexes required by CI.
- risk: The remote import branch contains other skills and must not be merged wholesale.

## SpokeReport - Determinism Auditor

- status: pass
- findings: The imported skill had a useful `ats_lint.py` but retained generic examples, generic knowledge, no assets directory, and generic evals.
- coverage_gaps: ATS keyword policy, section policy, brand voice policy, privacy policy, and output contract were missing.
- recommended_changes: Add deterministic assets and specialize examples, prompts, agents, evals, and fixtures.
- risk: User-facing career edits can overclaim if non-invention rules are not enforced.

## SpokeReport - Eval Designer

- status: pass
- findings: Evals now cover CV and cover happy paths, missing job description, keyword gaps, false positive, false negative, minimal CV, unsafe contact examples, hustle language, and offline lint contract.
- coverage_gaps: None remaining for current DoD scope.
- recommended_changes: Keep false-positive and false-negative cases when activation triggers change.
- risk: ATS expectations may vary by platform; this skill validates deterministic local signals only.

## SpokeReport - Script Engineer

- status: pass
- findings: `check.sh` now runs `ats_lint.py` against two valid and four invalid fixtures instead of only parsing JSON.
- coverage_gaps: The linter validates text packets, not DOCX/PDF parsing.
- recommended_changes: Keep fixture text synthetic and offline.
- risk: Future document parsing should remain outside this script unless deterministic fixtures are added.

## HardeningBrief

- skill: cv-cover-optimizer
- scope_allowed: `skills/cv-cover-optimizer/**`, `docs/audits/skills/cv-cover-optimizer-review.md`, and the `cv-cover-optimizer` ledger row.
- required_changes: Import one skill, add deterministic assets, eval cases, examples, knowledge, agents, prompts, stronger script fixtures, review doc, ledger row, and generated indexes/count docs if required by validation.
- forbidden_changes: other imported selection skills, unrelated review docs, unrelated ledger rows, and wholesale merge of `origin/codex/import-seleccion-skills-20260608`.
- validation_plan: Skill DoD, skill scripts, local check script, repo strict validation, count docs, repo boundaries, adversarial tests, global script checks, doc-factory, adapter freshness, PRISTINO freshness, runtime checks, and diff whitespace.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/cv-cover-optimizer/scripts/check.sh`: `cv-cover-optimizer check passed: valid=2 invalid=4`.
- `python3 -B scripts/validate-skill-dod.py --skill cv-cover-optimizer`: `skill=cv-cover-optimizer dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill cv-cover-optimizer`: `skills_with_scripts=1 warnings=0 errors=0`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=603 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=603 agents=261 commands=267 prompts=256 components=1387`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/qa/run-confidence-fp-tests.py`: `OK: confidence calibration, stratified sampling, and FP-criteria checks passed`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=142 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `python3 -B scripts/validate-runtime-instructions.py`: `runtime instructions: passed`.
- `python3 -B scripts/post_annotations.py --validate-only references/schemas/annotations.example.json`: `VALID: 2 annotation(s) conform to annotations.schema.json`.
- `bash scripts/adapt.sh all`: adapter outputs regenerated for 603 skills.
- `scripts/generate-pristino-index.sh` hit a local Codex host `fork` limit, so the equivalent deterministic Python mirror regenerated `PRISTINO-INDEX.md`: `Agents: 261 | Skills: 603 | Commands: 267 | Prompts: 256 | Components: 1387`.
- `git diff --check origin/main...HEAD && git diff --check`: passed with no whitespace errors.

## Guardian Decision

- status: pass
- decision: Local validation, ledger, review doc, generated adapters, and PRISTINO index passed; authorize ready PR and merge only after Quality Gates pass.
- remaining_risks: CI status is unknown before PR creation; remote import branch still contains 9 other selection skills and must remain extraction-only.
