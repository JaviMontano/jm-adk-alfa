# simulador-entrevista Review

## SkillTicket

- skill activa: `simulador-entrevista`
- estado ledger inicial: sin fila en `main`
- rama: `codex/harden-simulador-entrevista-dod-20260609`
- scope permitido: `skills/simulador-entrevista/**`, esta review doc, fila ledger e indices generados
- riesgo deterministico inicial: scaffold importado sin `assets/`, evals genericos y scoring sin evidencia de comportamiento

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
- findings: faltaban assets, evidencia por score, one-question mode y bloqueo de promedios
- coverage_gaps: multiple questions, success guarantee, fabricated experience, unsupported language
- recommended_changes: agregar contratos y validator offline
- risk: alto antes del hardening

### Eval Designer

- status: pass
- findings: se reemplazaron evals genericos por 10 casos especificos
- coverage_gaps: ninguno observado despues del cambio
- recommended_changes: mantener falsos positivos y limites de scoring
- risk: bajo

### Script Engineer

- status: pass
- findings: `interview_sim_validator.py` valida feedback offline con fixtures validos, bloqueados e invalidos
- coverage_gaps: ninguno observado
- recommended_changes: ejecutar `scripts/check.sh` antes de usar feedback como evidencia
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

- skill: `simulador-entrevista`
- scope_allowed: `skills/simulador-entrevista/**`, `docs/audits/skills/simulador-entrevista-review.md`, fila ledger e indices generados
- required_changes: assets manifest, contratos de salida/rubrica/pregunta/feedback/safety, evals deterministas, validator offline, fixtures, ejemplos especializados
- forbidden_changes: tocar otras skills, promediar scores, prometer contratacion, inventar experiencia, usar red/reloj
- validation_plan: skill checks, repo checks, doc-factory, script checks globales, `git diff --check`
- merge_criteria: validacion local verde, PR listo, Quality Gates verdes, squash merge y limpieza

## Local Evidence

- `bash skills/simulador-entrevista/scripts/check.sh` -> pass (`valid=2 blocked=2 invalid=6`)
- `python3 -B scripts/validate-skill-dod.py --skill simulador-entrevista` -> pass (`errors=0`)
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill simulador-entrevista` -> pass (`errors=0`)
- `bash scripts/adapt.sh all` -> pass (`610 skills indexed`)
- `bash scripts/generate-pristino-index.sh` -> pass (`Skills: 610`, `Components: 1394`)
- `python3 -B scripts/count-components.py --check-docs` -> pass (`skills=610`, `components=1394`)
- `python3 -B scripts/validate-skills.py --strict` -> pass (`warnings=0 errors=0`)
- `bash scripts/check-repo-boundaries.sh` -> pass (`Repo boundaries OK`)
- `python3 -B scripts/qa/run-adversarial-tests.py` -> pass (`passed=11 failed=0 total=11`)
- `bash scripts/doc-factory/check.sh` -> pass
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` -> pass (`skills_with_scripts=149 warnings=0 errors=0`)
- `git diff --check` -> pass

## Guardian Decision

Authorized for repo-wide validation after adapter/index regeneration. Do not merge until Quality Gates pass.
