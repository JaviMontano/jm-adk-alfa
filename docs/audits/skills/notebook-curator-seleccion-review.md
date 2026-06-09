# Notebook Curator Seleccion Review

## SkillTicket

- skill activa: notebook-curator-seleccion
- estado ledger: new row added as dod-complete after local validation evidence
- rama: codex/harden-notebook-curator-seleccion-dod-20260608
- riesgos de determinismo esperados: subjective curation, inferred source contents, duplicate canonical slots, missing source evidence, NotebookLM live-sync dependency, and URL/network fetch assumptions.
- archivos esperados: `skills/notebook-curator-seleccion/**`, `docs/audits/skills/notebook-curator-seleccion-review.md`, generated adapter/index files required by component counts, and one `notebook-curator-seleccion` ledger row.
- validaciones locales: skill DoD, skill script checks, local check script, strict repo validation, component counts, repo boundaries, adversarial tests, global script checks, doc-factory check, adapter regeneration, PRISTINO index freshness, and whitespace diff check.
- criterio de merge: local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## SpokeReport - Ledger Auditor

- status: pass
- findings: `notebook-curator-seleccion` was imported from `origin/codex/import-seleccion-skills-20260608` and did not exist on `origin/main`.
- coverage_gaps: No ledger row or review doc existed for the isolated import.
- recommended_changes: Add only the active skill, review doc, one ledger row, and generated indexes required by validation.
- risk: The source import branch contains additional skills and must remain extraction-only.

## SpokeReport - Determinism Auditor

- status: pass
- findings: The imported scaffold had a useful archetype validator idea but generic docs, generic evals, no assets directory, and fixtures that only parsed JSON.
- coverage_gaps: Missing canonical slot contract, evidence policy, curation policy, offline boundary policy, output contract, duplicate-slot cases, and NotebookLM/network blockers.
- recommended_changes: Add deterministic assets and harden scripts, prompts, agents, examples, knowledge, evals, and fixtures around exported offline source inventories.
- risk: Notebook curation can imply source contents or live NotebookLM state unless source evidence and offline boundaries are explicit.

## SpokeReport - Eval Designer

- status: pass
- findings: Evals now cover complete inventory, explicit trigger, missing offer slot, duplicate interview notes, URL-only fetch request, title-only degradation, unsupported destructive action, minimal input, and false positives.
- coverage_gaps: None remaining for current DoD scope.
- recommended_changes: Keep false-positive coverage separate from generic notebooks and Jupyter notebooks when triggers evolve.
- risk: The validator confirms inventory readiness, not the truth of source content.

## SpokeReport - Script Engineer

- status: pass
- findings: `check.sh` now executes `validate_archetype.py` against two valid fixtures, one blocked fixture, and six invalid fixtures.
- coverage_gaps: The validator does not call NotebookLM or inspect live external documents.
- recommended_changes: Keep validation offline; add paired fixtures for any new slot, evidence type, or curation action.
- risk: Future live-sync workflows must remain outside this offline validator or add explicit non-DoD integration tests.

## HardeningBrief

- skill: notebook-curator-seleccion
- scope_allowed: `skills/notebook-curator-seleccion/**`, `docs/audits/skills/notebook-curator-seleccion-review.md`, the `notebook-curator-seleccion` ledger row, and generated adapter/index files required by repo component counts.
- required_changes: Import one skill, add deterministic assets, eval cases, examples, knowledge, agents, prompts, output template, offline validator, valid/blocked/invalid fixtures, review doc, ledger row, and generated index/count updates.
- forbidden_changes: other selection skills, unrelated skill rows, unrelated review docs, and wholesale merge of `origin/codex/import-seleccion-skills-20260608`.
- validation_plan: Skill DoD, skill scripts, local check script, repo strict validation, component count docs, repo boundaries, adversarial tests, global script checks, doc-factory check, adapter freshness, PRISTINO freshness, and whitespace diff check.
- merge_criteria: Local validation green, PR ready, Quality Gates green, squash merge, branch cleanup, and updated `main`.

## Local Evidence

- `bash skills/notebook-curator-seleccion/scripts/check.sh`: `notebook-curator-seleccion check passed: valid=2 blocked=1 invalid=6`.
- `python3 -B scripts/validate-skill-dod.py --skill notebook-curator-seleccion`: `skill=notebook-curator-seleccion dod=pass errors=0`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill notebook-curator-seleccion`: `skills_with_scripts=1 warnings=0 errors=0`.
- `bash scripts/adapt.sh all`: adapter outputs regenerated for 606 skills.
- `bash scripts/generate-pristino-index.sh`: `Agents: 261 | Skills: 606 | Commands: 267 | Prompts: 256 | Components: 1390`.
- `python3 -B scripts/validate-skills.py --strict`: `skills=606 warnings=0 errors=0`.
- `python3 -B scripts/count-components.py --check-docs`: `skills=606 agents=261 commands=267 prompts=256 components=1390`.
- `bash scripts/check-repo-boundaries.sh`: `Repo boundaries OK`.
- `python3 -B scripts/qa/run-adversarial-tests.py`: `summary: passed=11 failed=0 total=11`.
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks`: `skills_with_scripts=145 warnings=0 errors=0`.
- `bash scripts/doc-factory/check.sh`: `OK: doc-factory deterministic smoke check passed`.
- `git diff --check`: passed with no whitespace errors.

## Guardian Decision

- status: pass
- decision: Local validation, ledger, review doc, generated adapters, and PRISTINO index passed; authorize ready PR and merge only after Quality Gates pass.
- remaining_risks: CI status is unknown before PR creation; the source import branch still contains other selection skills and must not be merged wholesale.
