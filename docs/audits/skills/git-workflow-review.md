# git-workflow Review

## Estado
- Skill: `git-workflow` [CONFIG]
- Rama: `codex/harden-git-workflow-dod-20260606` [CONFIG]
- Fecha de referencia: `2026-06-06` [CONFIG]
- Estado ledger inicial: `pending` [CÓDIGO]
- Estado de validación: validaciones locales completas y verdes [CÓDIGO]
- Alcance permitido: `skills/git-workflow/**`, este review doc y la fila `git-workflow` en `docs/audits/skill-review-ledger.csv` [CONFIG]

## SpokeReport - Ledger Auditor
- status: pass [CÓDIGO]
- findings: la fila de ledger existe como `pending`; el review doc no existía antes de esta implementación [CÓDIGO]
- coverage_gaps: ninguno después de registrar review doc, evidencia local y ledger [CÓDIGO]
- recommended_changes: mantener el cierre limitado a la rama y PR de `git-workflow` [CONFIG]
- risk: residual bajo; cambios futuros deben preservar evidencia antes de tocar ledger [INFERENCIA]

## SpokeReport - Determinism Auditor
- status: pass [CÓDIGO]
- findings: `SKILL.md` era genérico y no bloqueaba explícitamente dirty tree, base desalineada ni comandos destructivos [CÓDIGO]
- coverage_gaps: cubierto con contratos para repo state, branch policy, command safety, PR policy y release tags [CÓDIGO]
- recommended_changes: conservar `assets/manifest.json` como índice de contratos de salida [CONFIG]
- risk: residual bajo; el validador prueba planes JSON, no ejecuta Git real ni verifica permisos remotos [INFERENCIA]

## SpokeReport - Eval Designer
- status: pass [CÓDIGO]
- findings: `evals/evals.json` no tenía objeto `cases` y mantenía casos scaffold [CÓDIGO]
- coverage_gaps: cubierto con 9 escenarios determinísticos y fixtures de contrato [CÓDIGO]
- recommended_changes: mantener negativos junto al script para detectar regresiones [CONFIG]
- risk: residual bajo; nuevos comandos permitidos deberán ampliar política y fixtures [INFERENCIA]

## SpokeReport - Script Engineer
- status: pass [CÓDIGO]
- findings: no existía `scripts/check.sh` y el DoD no tenía validación offline para planes Git [CÓDIGO]
- coverage_gaps: cubierto con 2 fixtures válidos y 6 fixtures inválidos ejecutados por `scripts/check.sh` [CÓDIGO]
- recommended_changes: conservar validación offline sin red, tiempo dinámico ni aleatoriedad [CONFIG]
- risk: residual bajo; el script valida planes Git, no muta repositorios [INFERENCIA]

## HardeningBrief
- skill: `git-workflow` [CONFIG]
- scope_allowed: `skills/git-workflow/**`, `docs/audits/skills/git-workflow-review.md`, fila `git-workflow` del ledger [CONFIG]
- required_changes: assets de política, evals con mínimo 8 casos, ejemplos especializados, knowledge/prompts/agents/templates alineados, script offline, fixtures, review doc, evidencia local y ledger [CONFIG]
- forbidden_changes: otras skills, adaptadores generados no relacionados, cambios globales de validator o runtime fuera del alcance [CONFIG]
- validation_plan: ejecutar validaciones por skill, validaciones por repo, freshness de adapters y `git diff --check` [CONFIG]
- merge_criteria: DoD local verde, repo checks verdes, PR listo, Quality Gates verdes, squash merge, limpieza de rama y `main` actualizado [CONFIG]

## Evidencia Local
- PASS: `bash skills/git-workflow/scripts/check.sh` (`valid=2 invalid=6`) [CÓDIGO]
- PASS: `python3 -B scripts/validate-skill-dod.py --skill git-workflow` (`skill=git-workflow dod=pass errors=0`) [CÓDIGO]
- PASS: `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill git-workflow` (`skills_with_scripts=1 warnings=0 errors=0`) [CÓDIGO]
- PASS: `python3 -B scripts/validate-skills.py --strict` (`skills=600 warnings=0 errors=0`) [CÓDIGO]
- PASS: `python3 -B scripts/count-components.py --check-docs` (`skills=600 agents=261 commands=267 prompts=256 components=1384`) [CÓDIGO]
- PASS: `bash scripts/check-repo-boundaries.sh` (`Repo boundaries OK`) [CÓDIGO]
- PASS: `python3 -B scripts/qa/run-adversarial-tests.py` (`passed=11 failed=0 total=11`) [CÓDIGO]
- PASS: `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` (`skills_with_scripts=81 warnings=0 errors=0`) [CÓDIGO]
- PASS: `bash scripts/doc-factory/check.sh` (`OK: doc-factory deterministic smoke check passed`) [CÓDIGO]
- PASS: `bash scripts/adapt.sh all` (`ADAPTER-COMPLETE` para targets generados; sin diff de adapters) [CÓDIGO]
- PASS: `git diff --check` (sin salida) [CÓDIGO]

## Decisión Guardian
- Estado: autorizado para PR de `git-workflow` [CÓDIGO]
- Condición de autorización: PR listo permitido; no avanzar a `generate-qa-report` hasta Quality Gates verdes, squash merge, limpieza de rama y `main` actualizado [CONFIG]
