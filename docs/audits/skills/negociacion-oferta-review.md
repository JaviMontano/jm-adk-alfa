# Negociacion Oferta Review

## SkillTicket

- skill activa: negociacion-oferta
- estado ledger: new row added as dod-complete after local validation evidence
- rama: codex/harden-negociacion-oferta-dod-20260608
- riesgos de determinismo esperados: invented compensation numbers, unsupported market-rate claims, fabricated competing offers, pressure language, unverified exclusivity exceptions, and ranking offers that fail hard filters.
- archivos esperados: `skills/negociacion-oferta/**`, `docs/audits/skills/negociacion-oferta-review.md`, generated adapter/index files required by component counts, and one `negociacion-oferta` ledger row.
- validaciones locales: skill DoD, skill script checks, local check script, strict repo validation, component counts, repo boundaries, adversarial tests, global script checks, doc-factory check, adapter regeneration, PRISTINO index regeneration, and whitespace diff check.
- criterio de merge: local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## SpokeReport - Ledger Auditor

- status: pass
- findings: `negociacion-oferta` was imported from `origin/codex/import-seleccion-skills-20260608` and did not exist on `origin/main`.
- coverage_gaps: No ledger row or review doc existed for the isolated import.
- recommended_changes: Add only the active skill, review doc, one ledger row, and generated indexes required by validation.
- risk: The source import branch contains additional skills and must remain extraction-only.

## SpokeReport - Determinism Auditor

- status: pass
- findings: The imported scaffold had a useful scoring script idea but generic docs, generic evals, no assets directory, and a script check that only parsed JSON fixtures.
- coverage_gaps: Missing acceptance filters, PIVOTE rubric, evidence policy, counterproposal boundaries, output contract, and negative fixtures for fabricated leverage or unsupported market claims.
- recommended_changes: Add deterministic assets and harden scripts, prompts, agents, examples, knowledge, evals, and fixtures around supplied offer facts only.
- risk: Offer negotiation can drift into legal, tax, immigration, financial, or live-market claims unless evidence boundaries are explicit.

## SpokeReport - Eval Designer

- status: pass
- findings: Evals now cover happy ranking, explicit counterproposal, salary floor edge, low PIVOTE dimension, missing compensation, fabricated competing offer, unsupported market claim, no passing offers, and false positives.
- coverage_gaps: None remaining for current DoD scope.
- recommended_changes: Keep false-positive cases separate from liquidation and generic negotiation topics when triggers evolve.
- risk: PIVOTE scores are user-supplied; the skill validates structure and thresholds, not the objective truth of each score.

## SpokeReport - Script Engineer

- status: pass
- findings: `check.sh` now executes `score_oferta.py` against two valid fixtures, one blocked fixture, and seven invalid fixtures.
- coverage_gaps: The validator does not fetch salary benchmarks, exchange rates, tax data, or contract law.
- recommended_changes: Keep validation offline; add paired fixtures for any new blocked phrase, evidence type, or acceptance filter.
- risk: Future counterproposal patterns may require additional evidence types to avoid overblocking legitimate cases.

## HardeningBrief

- skill: negociacion-oferta
- scope_allowed: `skills/negociacion-oferta/**`, `docs/audits/skills/negociacion-oferta-review.md`, the `negociacion-oferta` ledger row, and generated adapter/index files required by repo component counts.
- required_changes: Import one skill, add deterministic assets, eval cases, examples, knowledge, agents, prompts, output template, offline validator, valid/blocked/invalid fixtures, review doc, ledger row, and generated index/count updates.
- forbidden_changes: other selection skills, unrelated skill rows, unrelated review docs, and wholesale merge of `origin/codex/import-seleccion-skills-20260608`.
- validation_plan: Skill DoD, skill scripts, local check script, repo strict validation, component count docs, repo boundaries, adversarial tests, global script checks, doc-factory check, adapter freshness, PRISTINO freshness, and whitespace diff check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/negociacion-oferta/scripts/check.sh`: `negociacion-oferta check passed: valid=2 blocked=1 invalid=7`.
- `python3 -B scripts/validate-skill-dod.py --skill negociacion-oferta`: `skill=negociacion-oferta dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill negociacion-oferta`: `skills_with_scripts=1 warnings=0 errors=0`.
- `bash scripts/adapt.sh all`: adapter outputs regenerated for 605 skills.
- `bash scripts/generate-pristino-index.sh`: `Agents: 261 | Skills: 605 | Commands: 267 | Prompts: 256 | Components: 1389`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=605 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=605 agents=261 commands=267 prompts=256 components=1389`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=144 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `git diff --check`: passed with no whitespace errors.

## Guardian Decision

- status: pass
- decision: Local validation, ledger, review doc, generated adapters, and PRISTINO index passed; authorize ready PR and merge only after Quality Gates pass.
- remaining_risks: CI status is unknown before PR creation; the source import branch still contains other selection skills and must not be merged wholesale.
