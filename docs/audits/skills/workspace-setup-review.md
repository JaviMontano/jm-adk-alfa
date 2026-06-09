# workspace-setup Review

## SkillTicket

- skill activa: `workspace-setup`
- estado ledger inicial: `pending`
- rama: `codex/harden-workspace-setup-dod-20260609`
- scope permitido: `skills/workspace-setup/**`, esta review doc, fila ledger e indices generados
- riesgo deterministico inicial: faltaban `assets/`, ejemplos y knowledge eran genericos, evals no exigian assets ni deterministic scripts, y no existia validator offline para planes de setup local

## SpokeReport

### Coordinator

- status: pass
- findings: rama creada desde `origin/main` limpio despues de merge verde previo
- coverage_gaps: ninguno para iniciar
- recommended_changes: mantener una sola skill activa
- risk: bajo

### Ledger Auditor

- status: pass
- findings: fila ledger existia como `pending` y fue actualizada solo despues de validaciones locales verdes
- coverage_gaps: ninguno observado
- recommended_changes: mantener una sola fila modificada
- risk: bajo

### Determinism Auditor

- status: block
- findings: faltaban assets, contrato de perfil local, politicas de privacidad/comandos/escritura, fixtures negativos y checker offline
- coverage_gaps: overwrite sin force, almacenamiento de secretos, comandos destructivos permitidos, validacion con red, target file inseguro y evidencia ausente
- recommended_changes: agregar contrato JSON, politicas y validator offline
- risk: alto antes del hardening

### Eval Designer

- status: pass
- findings: se reemplazaron evals scaffold por 10 casos con happy paths, apply guard, command policy, privacy, bloqueos, falsos positivos y limite offline
- coverage_gaps: ninguno observado despues del cambio
- recommended_changes: mantener casos de overwrite sin force, secret storage y network-required
- risk: bajo

### Script Engineer

- status: pass
- findings: `validate_workspace_setup_plan.py` valida target local, runtime preferences, command policy, privacy, write policy, evidence y validation checks offline
- coverage_gaps: no escribe perfiles reales; valida planes antes de aplicar
- recommended_changes: ejecutar `scripts/check.sh` antes de aceptar un plan de setup
- risk: bajo

### Integrator

- status: pass
- findings: cambios confinados a la skill activa, review doc, ledger e indices generados
- coverage_gaps: ninguno observado despues de regenerar adaptadores e indice
- recommended_changes: abrir PR solo con los archivos permitidos
- risk: bajo

### Guardian

- status: pass
- findings: DoD por skill, scripts estrictos, repo checks, doc-factory, adversarial, scripts globales y diff check pasan localmente
- coverage_gaps: requiere Quality Gates antes de merge
- recommended_changes: abrir PR solo tras repo checks verdes
- risk: medio hasta CI

## HardeningBrief

- skill: `workspace-setup`
- scope_allowed: `skills/workspace-setup/**`, `docs/audits/skills/workspace-setup-review.md`, fila ledger e indices generados
- required_changes: assets manifest, setup plan contract, runtime/command/privacy/write/evidence policies, evals deterministas, validator offline, fixtures valid/invalid, examples y knowledge especificos
- forbidden_changes: tocar `workspace-governance` u otras skills, escribir estado local real, registrar secretos, permitir overwrite sin `force`, depender de red/tiempo/random
- validation_plan: skill checks, repo checks, doc-factory, script checks globales, `git diff --check`
- merge_criteria: validacion local verde, PR listo, Quality Gates verdes, squash merge y limpieza

## Local Evidence

- `bash scripts/adapt.sh all` -> pass (`611 skills indexed`)
- `bash scripts/generate-pristino-index.sh` -> pass (`Skills: 611`, `Components: 1395`)
- `python3 -B scripts/validate-skill-dod.py --skill workspace-setup` -> pass (`errors=0`)
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill workspace-setup` -> pass (`warnings=0`, `errors=0`)
- `bash skills/workspace-setup/scripts/check.sh` -> pass (`valid=2`, `invalid=7`)
- `python3 -B scripts/validate-skills.py --strict` -> pass (`warnings=0`, `errors=0`)
- `python3 -B scripts/count-components.py --check-docs` -> pass (`skills=611`, `components=1395`)
- `bash scripts/check-repo-boundaries.sh` -> pass (`Repo boundaries OK`)
- `python3 -B scripts/qa/run-adversarial-tests.py` -> pass (`passed=11`, `failed=0`, `total=11`)
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` -> pass (`skills_with_scripts=154`, `warnings=0`, `errors=0`)
- `bash scripts/doc-factory/check.sh` -> pass
- `git diff --check` -> pass

## Guardian Decision

Authorized for PR after local skill and repo validations. Do not merge until Quality Gates pass.
