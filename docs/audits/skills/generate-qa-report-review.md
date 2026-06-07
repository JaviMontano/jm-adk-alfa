# generate-qa-report Review

## Estado
- Skill: `generate-qa-report` [CONFIG]
- Rama: `codex/harden-generate-qa-report-dod-20260606` [CONFIG]
- Fecha de referencia: `2026-06-06` [CONFIG]
- Estado ledger inicial: `pending` [CÓDIGO]
- Estado de validación: validaciones locales completas y verdes [CÓDIGO]
- Alcance permitido: `skills/generate-qa-report/**`, este review doc y la fila `generate-qa-report` en `docs/audits/skill-review-ledger.csv` [CONFIG]

## SpokeReport - Ledger Auditor
- status: pass [CÓDIGO]
- findings: la fila de ledger existe como `pending`; el review doc no existía antes de esta implementación [CÓDIGO]
- coverage_gaps: ninguno después de registrar review doc, evidencia local y ledger [CÓDIGO]
- recommended_changes: mantener el cierre limitado a la rama y PR de `generate-qa-report` [CONFIG]
- risk: residual bajo; cambios futuros deben preservar evidencia antes de tocar ledger [INFERENCIA]

## SpokeReport - Determinism Auditor
- status: pass [CÓDIGO]
- findings: la skill describe buen reporte QA, pero faltaban assets, contrato verificable y script offline [CÓDIGO]
- coverage_gaps: cubierto con contrato para fuentes, conteos, TL;DR, findings, severidades y recomendaciones [CÓDIGO]
- recommended_changes: conservar `assets/manifest.json` como índice de contratos de salida [CONFIG]
- risk: residual bajo; el validador prueba reportes JSON, no revalida hallazgos upstream [INFERENCIA]

## SpokeReport - Eval Designer
- status: pass [CÓDIGO]
- findings: `evals/evals.json` no tenía objeto `cases` y mantenía casos scaffold [CÓDIGO]
- coverage_gaps: cubierto con 9 escenarios determinísticos y fixtures de contrato [CÓDIGO]
- recommended_changes: mantener negativos junto al script para detectar regresiones [CONFIG]
- risk: residual bajo; nuevos formatos de fuente deberán ampliar política y fixtures [INFERENCIA]

## SpokeReport - Script Engineer
- status: pass [CÓDIGO]
- findings: no existía `scripts/check.sh` y el DoD no tenía validación offline para reportes QA [CÓDIGO]
- coverage_gaps: cubierto con 2 fixtures válidos y 6 fixtures inválidos ejecutados por `scripts/check.sh` [CÓDIGO]
- recommended_changes: conservar validación offline sin red, tiempo dinámico ni aleatoriedad [CONFIG]
- risk: residual bajo; el script valida reportes QA agregados, no ejecuta auditorías [INFERENCIA]

## HardeningBrief
- skill: `generate-qa-report` [CONFIG]
- scope_allowed: `skills/generate-qa-report/**`, `docs/audits/skills/generate-qa-report-review.md`, fila `generate-qa-report` del ledger [CONFIG]
- required_changes: assets de política, evals con mínimo 8 casos, ejemplos especializados, knowledge/prompts/agents/templates alineados, script offline, fixtures, review doc, evidencia local y ledger [CONFIG]
- forbidden_changes: otras skills, adaptadores generados no relacionados, cambios globales de validator o runtime fuera del alcance [CONFIG]
- validation_plan: ejecutar validaciones por skill, validaciones por repo, freshness de adapters y `git diff --check` [CONFIG]
- merge_criteria: DoD local verde, repo checks verdes, PR listo, Quality Gates verdes, squash merge, limpieza de rama y `main` actualizado [CONFIG]

## Evidencia Local
- PASS: `bash skills/generate-qa-report/scripts/check.sh` (`valid=2 invalid=6`) [CÓDIGO]
- PASS: `python3 -B scripts/validate-skill-dod.py --skill generate-qa-report` (`skill=generate-qa-report dod=pass errors=0`) [CÓDIGO]
- PASS: `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill generate-qa-report` (`skills_with_scripts=1 warnings=0 errors=0`) [CÓDIGO]
- PASS: `python3 -B scripts/validate-skills.py --strict` (`skills=600 warnings=0 errors=0`) [CÓDIGO]
- PASS: `python3 -B scripts/count-components.py --check-docs` (`skills=600 agents=261 commands=267 prompts=256 components=1384`) [CÓDIGO]
- PASS: `bash scripts/check-repo-boundaries.sh` (`Repo boundaries OK`) [CÓDIGO]
- PASS: `python3 -B scripts/qa/run-adversarial-tests.py` (`passed=11 failed=0 total=11`) [CÓDIGO]
- PASS: `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` (`skills_with_scripts=82 warnings=0 errors=0`) [CÓDIGO]
- PASS: `bash scripts/doc-factory/check.sh` (`OK: doc-factory deterministic smoke check passed`) [CÓDIGO]
- PASS: `bash scripts/adapt.sh all` (`ADAPTER-COMPLETE` para targets generados; sin diff de adapters) [CÓDIGO]
- PASS: `git diff --check` (sin salida) [CÓDIGO]

## Decisión Guardian
- Estado: autorizado para PR de `generate-qa-report` [CÓDIGO]
- Condición de autorización: PR listo permitido; la tanda sólo se cierra después de Quality Gates verdes, squash merge, limpieza de rama y `main` actualizado [CONFIG]
