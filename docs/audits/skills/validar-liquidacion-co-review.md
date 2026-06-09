# validar-liquidacion-co Review

## SkillTicket

- skill activa: `validar-liquidacion-co`
- estado ledger inicial: sin fila en `main`
- rama: `codex/harden-validar-liquidacion-co-dod-20260609`
- scope permitido: `skills/validar-liquidacion-co/**`, esta review doc, fila ledger e indices generados
- riesgo deterministico inicial: scaffold importado sin `assets/`, evals genericos, validacion limitada a parseo JSON y riesgo alto por calculos laborales sensibles

## SpokeReport

### Coordinator

- status: pass
- findings: rama creada desde `origin/main` limpio
- coverage_gaps: ninguno para iniciar la skill activa
- recommended_changes: mantener una sola skill activa y no reintroducir `firma-pdf-legal`
- risk: bajo

### Ledger Auditor

- status: warn
- findings: no existia fila ledger para la skill en `main`
- coverage_gaps: registrar fila al cerrar DoD con evidencia local
- recommended_changes: agregar una fila `dod-complete` despues de validaciones por skill
- risk: medio

### Determinism Auditor

- status: block
- findings: faltaban assets, contrato de salida verificable, politica de evidencia, limites legales y fixtures negativos
- coverage_gaps: moneda no COP, componente desviado, neto incorrecto, lenguaje legal-final, uso de red y paz y salvo inseguro
- recommended_changes: agregar contratos JSON, validator offline y casos validos/bloqueados/invalidos
- risk: alto antes del hardening

### Eval Designer

- status: pass
- findings: se reemplazaron evals genericos por 10 casos especificos con activacion positiva, falsos positivos y bloqueos
- coverage_gaps: ninguno observado despues del cambio
- recommended_changes: mantener falsos positivos de invoice/PDF signature y blockers de moneda/legal-final
- risk: bajo

### Script Engineer

- status: pass
- findings: `liquidacion_validator.py` recompone cesantias, intereses, prima, vacaciones, neto y postura de paz y salvo offline
- coverage_gaps: no valida interpretaciones legales no suministradas; las bloquea como preguntas abiertas
- recommended_changes: ejecutar `scripts/check.sh` antes de usar un reporte como evidencia
- risk: medio por dominio legal/financiero, mitigado con limite arithmetic-only

### Integrator

- status: pass
- findings: cambios confinados a la skill activa, review doc, ledger e indices generados
- coverage_gaps: indices pendientes de regeneracion por nueva skill
- recommended_changes: correr adaptadores e indices antes de PR
- risk: bajo

### Guardian

- status: pass
- findings: DoD por skill y scripts estrictos pasan localmente
- coverage_gaps: requiere repo checks y Quality Gates antes de merge
- recommended_changes: abrir PR solo tras repo checks verdes
- risk: medio hasta CI

## HardeningBrief

- skill: `validar-liquidacion-co`
- scope_allowed: `skills/validar-liquidacion-co/**`, `docs/audits/skills/validar-liquidacion-co-review.md`, fila ledger e indices generados
- required_changes: assets manifest, output/formula/tolerance/evidence/paz-y-salvo/legal-boundary policies, evals deterministas, validator offline, fixtures valid/blocked/invalid, ejemplos especializados
- forbidden_changes: tocar otras skills, reintroducir `firma-pdf-legal`, prometer conclusion legal, usar red/reloj, inventar bases salariales, firmar documentos
- validation_plan: skill checks, repo checks, doc-factory, script checks globales, `git diff --check`
- merge_criteria: validacion local verde, PR listo, Quality Gates verdes, squash merge y limpieza

## Local Evidence

- `bash skills/validar-liquidacion-co/scripts/check.sh` -> pass (`valid=2 blocked=2 invalid=6`)
- `python3 -B scripts/validate-skill-dod.py --skill validar-liquidacion-co` -> pass (`errors=0`)
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill validar-liquidacion-co` -> pass (`errors=0`)
- `bash scripts/adapt.sh all` -> pass (`611 skills indexed`)
- `bash scripts/generate-pristino-index.sh` -> pass (`Skills: 611`, `Components: 1395`)
- `python3 -B scripts/count-components.py --check-docs` -> pass (`skills=611`, `components=1395`)
- `python3 -B scripts/validate-skills.py --strict` -> pass (`warnings=0 errors=0`)
- `bash scripts/check-repo-boundaries.sh` -> pass (`Repo boundaries OK`)
- `python3 -B scripts/qa/run-adversarial-tests.py` -> pass (`passed=11 failed=0 total=11`)
- `bash scripts/doc-factory/check.sh` -> pass
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` -> pass (`skills_with_scripts=150 warnings=0 errors=0`)
- `git diff --check` -> pass

## Guardian Decision

Authorized for PR after local skill and repo validations. Do not merge until Quality Gates pass.
