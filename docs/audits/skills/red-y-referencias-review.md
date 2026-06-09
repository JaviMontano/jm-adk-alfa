# red-y-referencias Review

## SkillTicket

- skill activa: `red-y-referencias`
- estado ledger inicial: sin fila en `main`
- rama: `codex/harden-red-y-referencias-dod-20260609`
- scope permitido: `skills/red-y-referencias/**`, esta review doc, fila ledger e indices generados
- riesgo deterministico inicial: scaffold importado sin `assets/`, evals genericos y `check.sh` sin validacion real de consentimiento

## SpokeReport

### Coordinator

- status: pass
- findings: rama creada desde `origin/main` limpio
- coverage_gaps: ninguno para iniciar
- recommended_changes: mantener una sola skill activa
- risk: bajo

### Ledger Auditor

- status: warn
- findings: no existia fila ledger para la skill en `main`
- coverage_gaps: registrar fila al cerrar DoD
- recommended_changes: agregar una fila `dod-complete` con evidencia local
- risk: medio

### Determinism Auditor

- status: block
- findings: faltaban assets, consentimiento verificable, politica de privacidad y calculo deterministico de follow-up
- coverage_gaps: no-consent, fechas relativas, datos directos de contacto, stale follow-up
- recommended_changes: agregar contratos y validator offline
- risk: alto antes del hardening

### Eval Designer

- status: pass
- findings: se reemplazaron evals genericos por 10 casos especificos
- coverage_gaps: ninguno observado despues del cambio
- recommended_changes: mantener falsos positivos de bibliografia/grafo social
- risk: bajo

### Script Engineer

- status: pass
- findings: `reference_network_validator.py` valida packets offline con fixtures validos, bloqueados e invalidos
- coverage_gaps: ninguno observado
- recommended_changes: ejecutar `scripts/check.sh` antes de usar packets como evidencia
- risk: bajo

### Integrator

- status: pass
- findings: cambios confinados a la skill activa, review doc y ledger
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

- skill: `red-y-referencias`
- scope_allowed: `skills/red-y-referencias/**`, `docs/audits/skills/red-y-referencias-review.md`, fila ledger e indices generados
- required_changes: assets manifest, contratos de salida/consentimiento/follow-up/privacidad/red, evals deterministas, validator offline, fixtures, ejemplos especializados
- forbidden_changes: tocar otras skills, consultar redes/email/calendarios, exponer datos directos de contacto, contactar referencias sin consentimiento
- validation_plan: skill checks, repo checks, doc-factory, script checks globales, `git diff --check`
- merge_criteria: validacion local verde, PR listo, Quality Gates verdes, squash merge y limpieza

## Local Evidence

- `bash skills/red-y-referencias/scripts/check.sh` -> pass (`valid=2 blocked=2 invalid=6`)
- `python3 -B scripts/validate-skill-dod.py --skill red-y-referencias` -> pass (`errors=0`)
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill red-y-referencias` -> pass (`errors=0`)
- `bash scripts/adapt.sh all` -> pass (`609 skills indexed`)
- `bash scripts/generate-pristino-index.sh` -> pass (`Skills: 609`, `Components: 1393`)
- `python3 -B scripts/count-components.py --check-docs` -> pass (`skills=609`, `components=1393`)
- `python3 -B scripts/validate-skills.py --strict` -> pass (`warnings=0 errors=0`)
- `bash scripts/check-repo-boundaries.sh` -> pass (`Repo boundaries OK`)
- `python3 -B scripts/qa/run-adversarial-tests.py` -> pass (`passed=11 failed=0 total=11`)
- `bash scripts/doc-factory/check.sh` -> pass
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` -> pass (`skills_with_scripts=148 warnings=0 errors=0`)
- `git diff --check` -> pass

## Guardian Decision

Authorized for repo-wide validation after adapter/index regeneration. Do not merge until Quality Gates pass.
