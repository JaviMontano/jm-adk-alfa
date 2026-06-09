# mcp-creator Review

## SkillTicket

- skill activa: `mcp-creator`
- estado ledger inicial: `pending`
- rama: `codex/harden-mcp-creator-dod-20260609`
- scope permitido: `skills/mcp-creator/**`, esta review doc, fila ledger e indices generados
- riesgo deterministico inicial: faltaban `assets/`, ejemplos eran scaffold, `evals/evals.json` no tenia objeto `cases`, no habia validator offline y el flujo podia mezclar planeacion MCP con configuracion viva

## SpokeReport

### Coordinator

- status: pass
- findings: rama creada desde `origin/main` limpio despues de `workspace-setup`
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
- findings: faltaban assets, contrato de plan MCP, politicas de transporte/scope/secretos/preflight, fixtures negativos y checker offline
- coverage_gaps: transporte `sse`, secretos hardcodeados, falta de collision check, URL HTTP insegura, scope project no trackeado, rollback ausente y validacion con red
- recommended_changes: agregar contrato JSON y validator offline
- risk: alto antes del hardening

### Eval Designer

- status: pass
- findings: se reemplazaron evals por 10 casos con stdio, http, project scope, bloqueos, falsos positivos y limite offline
- coverage_gaps: ninguno observado despues del cambio
- recommended_changes: mantener casos de hardcoded secret, sse y missing collision check
- risk: bajo

### Script Engineer

- status: pass
- findings: `validate_mcp_config_plan.py` valida server name, transport, scope, auth, preflight, rollback, evidence y validation checks offline
- coverage_gaps: no prueba conectividad real; valida plan antes de cualquier apply
- recommended_changes: ejecutar `scripts/check.sh` antes de aceptar un plan MCP
- risk: bajo

### Integrator

- status: pass
- findings: cambios confinados a la skill activa, review doc, ledger e indices generados
- coverage_gaps: ninguno observado despues de regenerar adaptadores e indice
- recommended_changes: abrir PR solo con archivos permitidos
- risk: bajo

### Guardian

- status: pass
- findings: DoD por skill, scripts estrictos, repo checks, doc-factory, adversarial, scripts globales y diff check pasan localmente
- coverage_gaps: requiere Quality Gates antes de merge
- recommended_changes: abrir PR solo tras repo checks verdes
- risk: medio hasta CI

## HardeningBrief

- skill: `mcp-creator`
- scope_allowed: `skills/mcp-creator/**`, `docs/audits/skills/mcp-creator-review.md`, fila ledger e indices generados
- required_changes: assets manifest, MCP config plan contract, transport/scope/secret/preflight/evidence policies, evals deterministas, validator offline, fixtures valid/invalid, examples y knowledge especificos
- forbidden_changes: tocar `mcp-engineering` u otras skills, configurar MCP real, ejecutar OAuth/red, hardcodear secretos, aceptar `sse`, escribir `.mcp.json` sin plan validado
- validation_plan: skill checks, repo checks, doc-factory, script checks globales, `git diff --check`
- merge_criteria: validacion local verde, PR listo, Quality Gates verdes, squash merge y limpieza

## Local Evidence

- `bash scripts/adapt.sh all` -> pass (`611 skills indexed`)
- `bash scripts/generate-pristino-index.sh` -> pass (`Skills: 611`, `Components: 1395`)
- `python3 -B scripts/validate-skill-dod.py --skill mcp-creator` -> pass (`errors=0`)
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill mcp-creator` -> pass (`warnings=0`, `errors=0`)
- `bash skills/mcp-creator/scripts/check.sh` -> pass (`valid=2`, `invalid=8`)
- `python3 -B scripts/validate-skills.py --strict` -> pass (`warnings=0`, `errors=0`)
- `python3 -B scripts/count-components.py --check-docs` -> pass (`skills=611`, `components=1395`)
- `bash scripts/check-repo-boundaries.sh` -> pass (`Repo boundaries OK`)
- `python3 -B scripts/qa/run-adversarial-tests.py` -> pass (`passed=11`, `failed=0`, `total=11`)
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` -> pass (`skills_with_scripts=155`, `warnings=0`, `errors=0`)
- `bash scripts/doc-factory/check.sh` -> pass
- `git diff --check` -> pass

## Guardian Decision

Authorized for PR after local skill and repo validations. Do not merge until Quality Gates pass.
