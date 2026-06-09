# katas-adaptive-investigation Review

## SkillTicket

- skill activa: `katas-adaptive-investigation`
- estado ledger inicial: `pending`
- rama: `codex/harden-katas-adaptive-investigation-dod-20260609`
- scope permitido: `skills/katas-adaptive-investigation/**`, esta review doc y fila ledger
- riesgo deterministico inicial: faltaban `assets/`, `evals/evals.json` no exigia `assets` ni `deterministic_scripts`, no habia checker offline y el patron podia aceptar re-plan reflejo o exploracion sin budget

## SpokeReport

### Coordinator

- status: pass
- findings: preflight limpio; `main`, `origin/main`, `HEAD` y remoto `main` estaban alineados en `645e49b380e3703bd16065b55fe81d6fbba1ac7f`
- coverage_gaps: ninguno para crear rama
- recommended_changes: mantener una sola skill activa
- risk: bajo

### Ledger Auditor

- status: warn
- findings: fila ledger existe como `pending`; review doc no existia antes del hardening
- coverage_gaps: evidencia local pendiente hasta ejecutar validaciones
- recommended_changes: actualizar la fila ledger solo despues de checks verdes
- risk: medio antes de validacion

### Determinism Auditor

- status: block
- findings: faltaban contrato de reporte, politicas de budget/replan/evidencia/scratchpad, fixtures negativos y checker offline
- coverage_gaps: no-budget, budget overrun, missing Grep, read-all-files, re-plan por refinamiento, network-required, evidencia ausente y scratchpad ausente
- recommended_changes: agregar assets, validator offline y fixtures deterministas
- risk: alto antes del hardening

### Eval Designer

- status: pass
- findings: evals reemplazados por 10 casos con happy path, budget agotado, falsos positivos, bloqueos y limite offline
- coverage_gaps: ninguno observado despues del cambio
- recommended_changes: mantener casos de re-plan por refinamiento y lectura total sin budget
- risk: bajo

### Script Engineer

- status: pass
- findings: `validate_adaptive_investigation_report.py` valida budget, topologia Glob/Grep, plan derivado, findings, re-plan gate, scratchpad, evidencia y validacion offline
- coverage_gaps: no mide la calidad semantica del analisis; valida estructura y gates deterministas
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

- skill: `katas-adaptive-investigation`
- scope_allowed: `skills/katas-adaptive-investigation/**`, `docs/audits/skills/katas-adaptive-investigation-review.md`, fila ledger
- required_changes: assets manifest, contrato de reporte, politicas de budget/replan/evidencia/scratchpad, evals deterministas, validator offline, fixtures valid/invalid, examples y knowledge especificos
- forbidden_changes: tocar otras skills, usar red/reloj/random como evidencia, re-planificar por refinamiento, aceptar exploracion sin budget o lectura total del repo
- validation_plan: skill checks, repo checks, doc-factory, script checks globales, `git diff --check`
- merge_criteria: validacion local verde, PR listo, Quality Gates verdes, squash merge y limpieza

## Local Evidence

- `python3 -B scripts/validate-skill-dod.py --skill katas-adaptive-investigation` -> pass (`errors=0`)
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill katas-adaptive-investigation` -> pass (`skills_with_scripts=1`, `warnings=0`, `errors=0`)
- `bash skills/katas-adaptive-investigation/scripts/check.sh` -> pass (`valid=2`, `invalid=9`)
- `python3 -B scripts/validate-skills.py --strict` -> pass (`skills=611`, `warnings=0`, `errors=0`)
- `python3 -B scripts/count-components.py --check-docs` -> pass (`skills=611`, `components=1395`)
- `bash scripts/check-repo-boundaries.sh` -> pass (`Repo boundaries OK`)
- `python3 -B scripts/qa/run-adversarial-tests.py` -> pass (`passed=11`, `failed=0`, `total=11`)
- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks` -> pass (`skills_with_scripts=157`, `warnings=0`, `errors=0`)
- `bash scripts/doc-factory/check.sh` -> pass
- `git diff --check` -> pass

## Guardian Decision

Authorized for PR after local skill and repo validations. Do not merge until Quality Gates pass.
