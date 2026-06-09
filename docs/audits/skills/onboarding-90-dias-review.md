# Onboarding 90 Dias Review

## SkillTicket

- skill activa: onboarding-90-dias
- estado ledger: new row added as dod-complete after local validation evidence
- rama: codex/harden-onboarding-90-dias-dod-20260608
- riesgos de determinismo esperados: aspirational plans without evidence, relative-date ambiguity, unverifiable tasks, performance guarantees, always-on language, and calendar/network assumptions.
- archivos esperados: `skills/onboarding-90-dias/**`, `docs/audits/skills/onboarding-90-dias-review.md`, generated adapter/index files required by component counts, and one `onboarding-90-dias` ledger row.
- validaciones locales: skill DoD, skill script checks, local check script, strict repo validation, component counts, repo boundaries, adversarial tests, global script checks, doc-factory check, adapter regeneration, PRISTINO index regeneration, and whitespace diff check.
- criterio de merge: local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## SpokeReport - Ledger Auditor

- status: pass
- findings: `onboarding-90-dias` was imported from `origin/codex/import-seleccion-skills-20260608` and did not exist on `origin/main`.
- coverage_gaps: No ledger row or review doc existed for the isolated import.
- recommended_changes: Add only the active skill, review doc, one ledger row, and generated indexes required by validation.
- risk: The source import branch contains additional skills and must remain extraction-only.

## SpokeReport - Determinism Auditor

- status: pass
- findings: The imported scaffold had a useful anti-burnout script idea but generic docs, generic evals, no assets directory, and fixtures that only parsed JSON.
- coverage_gaps: Missing phase contract, burnout policy, evidence policy, validation policy, output contract, overload fixtures, and unsupported promise blockers.
- recommended_changes: Add deterministic assets and harden scripts, prompts, agents, examples, knowledge, evals, and fixtures around evidence-backed 30/60/90 planning.
- risk: Onboarding plans can overpromise promotion, impact, stakeholder availability, or sustainable capacity unless evidence and guardrails are explicit.

## SpokeReport - Eval Designer

- status: pass
- findings: Evals now cover happy path, explicit trigger, missing role, overload hours, too many priorities, missing validation signals, always-on language, guaranteed promotion boundary, and false positives.
- coverage_gaps: None remaining for current DoD scope.
- recommended_changes: Keep false-positive cases distinct from employee handbooks and product user onboarding when triggers evolve.
- risk: Time estimates remain user-supplied planning data, not live workload telemetry.

## SpokeReport - Script Engineer

- status: pass
- findings: `check.sh` now executes `plan_30_60_90.py` against two valid fixtures, two blocked fixtures, and six invalid fixtures.
- coverage_gaps: The validator does not read calendars, HR systems, or live company tools.
- recommended_changes: Keep validation offline; add paired fixtures for any new phase rule, blocked phrase, or validation signal.
- risk: Future org-specific onboarding requirements should remain evidence-driven instead of encoded as hidden defaults.

## HardeningBrief

- skill: onboarding-90-dias
- scope_allowed: `skills/onboarding-90-dias/**`, `docs/audits/skills/onboarding-90-dias-review.md`, the `onboarding-90-dias` ledger row, and generated adapter/index files required by repo component counts.
- required_changes: Import one skill, add deterministic assets, eval cases, examples, knowledge, agents, prompts, output template, offline validator, valid/blocked/invalid fixtures, review doc, ledger row, and generated index/count updates.
- forbidden_changes: other selection skills, unrelated skill rows, unrelated review docs, and wholesale merge of `origin/codex/import-seleccion-skills-20260608`.
- validation_plan: Skill DoD, skill scripts, local check script, repo strict validation, component count docs, repo boundaries, adversarial tests, global script checks, doc-factory check, adapter freshness, PRISTINO freshness, and whitespace diff check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/onboarding-90-dias/scripts/check.sh`: `onboarding-90-dias check passed: valid=2 blocked=2 invalid=6`.
- `python3 -B scripts/validate-skill-dod.py --skill onboarding-90-dias`: `skill=onboarding-90-dias dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill onboarding-90-dias`: `skills_with_scripts=1 warnings=0 errors=0`.
- `bash scripts/adapt.sh all`: adapter outputs regenerated for 607 skills.
- `bash scripts/generate-pristino-index.sh`: `Agents: 261 | Skills: 607 | Commands: 267 | Prompts: 256 | Components: 1391`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=607 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=607 agents=261 commands=267 prompts=256 components=1391`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=146 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `git diff --check`: passed with no whitespace errors.

## Guardian Decision

- status: pass
- decision: Local validation, ledger, review doc, generated adapters, and PRISTINO index passed; authorize ready PR and merge only after Quality Gates pass.
- remaining_risks: CI status is unknown before PR creation; the source import branch still contains other selection skills and must not be merged wholesale.
