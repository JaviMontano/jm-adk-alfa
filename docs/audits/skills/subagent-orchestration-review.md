# subagent-orchestration Review

## SkillTicket

- skill activa: `subagent-orchestration`
- estado ledger inicial: `pending`
- rama: `codex/harden-subagent-orchestration-dod-20260609`
- scope permitido: `skills/subagent-orchestration/**`, esta review doc, fila ledger e indices generados
- riesgo deterministico inicial: faltaban `assets/`, no habia script offline, evals no exigian assets ni deterministic scripts, y el contrato de errores podia quedar como prosa no verificable

## SpokeReport

### Coordinator

- status: pass
- findings: rama creada desde `origin/main` limpio
- coverage_gaps: ninguno para iniciar la skill activa
- recommended_changes: mantener una sola skill activa
- risk: bajo

### Ledger Auditor

- status: warn
- findings: fila ledger existia como `pending`
- coverage_gaps: cambiar a `dod-complete` solo con evidencia local
- recommended_changes: agregar review doc y actualizar una sola fila
- risk: medio

### Determinism Auditor

- status: block
- findings: faltaban assets, validator offline, contrato tipado de spoke errors, valid-empty y coverage gaps
- coverage_gaps: contexto compartido, errores swallowed, ausencia de local recovery, fail-fast y falsos positivos de single-pass
- recommended_changes: agregar assets y validator deterministico
- risk: alto antes del hardening

### Eval Designer

- status: pass
- findings: se reemplazaron evals por 10 casos con positivos, falsos positivos, degradacion, limites y bloqueos
- coverage_gaps: ninguno observado despues del cambio
- recommended_changes: mantener casos de `shared_context`, swallowed errors y single-pass
- risk: bajo

### Script Engineer

- status: pass
- findings: `validate_orchestration_plan.py` valida planes hub-and-spoke offline contra contrato deterministico
- coverage_gaps: no ejecuta subagentes reales; valida planes antes de ejecucion
- recommended_changes: ejecutar `scripts/check.sh` antes de usar el plan como evidencia
- risk: bajo

### Integrator

- status: pass
- findings: cambios confinados a la skill activa, review doc, ledger e indices generados
- coverage_gaps: adaptadores pendientes de regeneracion por cambios de descripcion
- recommended_changes: correr adaptadores e indice antes de PR
- risk: bajo

### Guardian

- status: pass
- findings: DoD por skill y scripts estrictos pasan localmente
- coverage_gaps: requiere repo checks y Quality Gates antes de merge
- recommended_changes: abrir PR solo tras repo checks verdes
- risk: medio hasta CI

## HardeningBrief

- skill: `subagent-orchestration`
- scope_allowed: `skills/subagent-orchestration/**`, `docs/audits/skills/subagent-orchestration-review.md`, fila ledger e indices generados
- required_changes: assets manifest, contratos de orchestration/isolation/error/aggregation/anti-pattern/model-tool, evals deterministas, validator offline, fixtures valid/blocked/invalid, review doc
- forbidden_changes: tocar skills relacionadas, reabrir `firma-pdf-legal`, afirmar ejecucion paralela real sin evidencia, aceptar contexto compartido o errores swallowed
- validation_plan: skill checks, repo checks, doc-factory, script checks globales, `git diff --check`
- merge_criteria: validacion local verde, PR listo, Quality Gates verdes, squash merge y limpieza

## Local Evidence

- `bash skills/subagent-orchestration/scripts/check.sh` -> pass (`valid=2 blocked=2 invalid=6`)
- `python3 -B scripts/validate-skill-dod.py --skill subagent-orchestration` -> pass (`errors=0`)
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill subagent-orchestration` -> pass (`errors=0`)
- `bash scripts/adapt.sh all` -> pass (`611 skills indexed`)
- `bash scripts/generate-pristino-index.sh` -> pass (`Skills: 611`, `Components: 1395`)
- `python3 -B scripts/count-components.py --check-docs` -> pass (`skills=611`, `components=1395`)
- `python3 -B scripts/validate-skills.py --strict` -> pass (`warnings=0 errors=0`)
- `bash scripts/check-repo-boundaries.sh` -> pass (`Repo boundaries OK`)
- `python3 -B scripts/qa/run-adversarial-tests.py` -> pass (`passed=11 failed=0 total=11`)
- `bash scripts/doc-factory/check.sh` -> pass
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` -> pass (`skills_with_scripts=151 warnings=0 errors=0`)
- `git diff --check` -> pass

## Guardian Decision

Authorized for PR after local skill and repo validations. Do not merge until Quality Gates pass.
