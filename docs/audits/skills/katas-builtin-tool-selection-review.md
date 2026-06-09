# katas-builtin-tool-selection Review

## SkillTicket

- skill activa: `katas-builtin-tool-selection`
- estado ledger inicial: `pending`
- rama: `codex/harden-katas-builtin-tool-selection-dod-20260609`
- scope permitido: `skills/katas-builtin-tool-selection/**`, esta review doc y fila ledger
- riesgo deterministico inicial: faltaban `assets/`, evals no exigian `assets` ni `deterministic_scripts`, no habia validator offline y el patron podia aceptar tool mismatch, `Read` masivo o `Edit` con anchor ambiguo

## SpokeReport

### Coordinator

- status: pass
- findings: rama creada desde `origin/main` limpio despues de `katas-adaptive-investigation`
- coverage_gaps: ninguno para iniciar
- recommended_changes: mantener una sola skill activa
- risk: bajo

### Ledger Auditor

- status: warn
- findings: fila ledger existia como `pending` y review doc no existia antes del hardening
- coverage_gaps: evidencia local pendiente hasta ejecutar validaciones
- recommended_changes: actualizar ledger solo despues de checks verdes
- risk: medio antes de validacion

### Determinism Auditor

- status: block
- findings: faltaban contrato de reporte, politicas de tool-fit, economia de lectura, anchor/fallback, evidencia, fixtures negativos y checker offline
- coverage_gaps: Grep para path, Glob para contenido, lectura masiva upfront, Read antes de search, anchor ambiguo, Write sin full Read, network-required y evidencia ausente
- recommended_changes: agregar assets, validator offline y fixtures deterministas
- risk: alto antes del hardening

### Eval Designer

- status: pass
- findings: evals reemplazados por 10 casos con happy path, path search, fallback, bloqueos, falso positivo y limite offline
- coverage_gaps: ninguno observado despues del cambio
- recommended_changes: mantener casos de tool mismatch y lectura masiva
- risk: bajo

### Script Engineer

- status: pass
- findings: `validate_tool_selection_report.py` valida tool-fit, read economy, edit anchor safety, fallback policy, evidence y validation flags offline
- coverage_gaps: no mide calidad semantica del diff final; valida el plan/report de seleccion de tools
- recommended_changes: ejecutar `scripts/check.sh` antes de aceptar handoffs criticos
- risk: bajo

### Integrator

- status: pass
- findings: cambios confinados a la skill activa y review doc hasta completar validaciones
- coverage_gaps: ledger pendiente hasta evidencia verde
- recommended_changes: no tocar skills relacionadas
- risk: bajo

### Guardian

- status: pass
- findings: DoD por skill, scripts estrictos, repo checks, doc-factory, adversarial, scripts globales y diff check pasan localmente
- coverage_gaps: requiere Quality Gates antes de merge
- recommended_changes: abrir PR solo tras repo checks verdes
- risk: medio hasta CI

## HardeningBrief

- skill: `katas-builtin-tool-selection`
- scope_allowed: `skills/katas-builtin-tool-selection/**`, `docs/audits/skills/katas-builtin-tool-selection-review.md`, fila ledger
- required_changes: assets manifest, contrato de reporte, politicas de tool-fit/read-economy/edit-anchor/evidence, evals deterministas, validator offline, fixtures valid/invalid, examples y knowledge especificos
- forbidden_changes: tocar otras skills, aceptar `Read` masivo upfront, usar `Grep` para paths, usar `Glob` para contenido, editar con anchor ambiguo, usar `Write` sin lectura completa previa
- validation_plan: skill checks, repo checks, doc-factory, script checks globales, `git diff --check`
- merge_criteria: validacion local verde, PR listo, Quality Gates verdes, squash merge y limpieza

## Local Evidence

- `python3 -B scripts/validate-skill-dod.py --skill katas-builtin-tool-selection` -> pass (`errors=0`)
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill katas-builtin-tool-selection` -> pass (`skills_with_scripts=1`, `warnings=0`, `errors=0`)
- `bash skills/katas-builtin-tool-selection/scripts/check.sh` -> pass (`valid=3`, `invalid=9`)
- `python3 -B scripts/validate-skills.py --strict` -> pass (`skills=611`, `warnings=0`, `errors=0`)
- `python3 -B scripts/count-components.py --check-docs` -> pass (`skills=611`, `components=1395`)
- `bash scripts/check-repo-boundaries.sh` -> pass (`Repo boundaries OK`)
- `python3 -B scripts/qa/run-adversarial-tests.py` -> pass (`passed=11`, `failed=0`, `total=11`)
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` -> pass (`skills_with_scripts=158`, `warnings=0`, `errors=0`)
- `bash scripts/doc-factory/check.sh` -> pass
- `git diff --check` -> pass

## Guardian Decision

Authorized for PR after local skill and repo validations. Do not merge until Quality Gates pass.
