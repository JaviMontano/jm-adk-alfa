# Plan Mode Workflow

Capacidad de ingeniería para operar repos o dominios desconocidos en dos modos: un Plan Mode read-only que solo lee y produce un `plan.md`, y un Execute Mode que se habilita únicamente tras una aprobación firmada del hash exacto del plan. La transición la aplica un hook `PreToolUse` que bloquea las tools de escritura mientras el modo sea `plan`.

## Resumen ejecutivo

El valor no está en pedir permiso, sino en hacer el gate verificable por construcción: el modo es estado, la firma es un artefacto auditable (`hash + aprobador + timestamp`), y cualquier edición posterior del plan revierte a `plan` y re-exige firma. El plan firmado más el diff resultante son el rastro de auditoría de qué se autorizó y qué se ejecutó.

## Deterministic Contract

Los assets en `assets/` definen el contrato de salida. Un reporte valido incluye:

- `mode_state` con modo inicial `plan`.
- `read_only_exploration` sin comandos mutantes.
- `plan_artifact` con SHA-256, archivos a tocar, criterios de aceptación y riesgos.
- `approval_event` firmado por el hash exacto del plan o explicitamente ausente.
- `hook_enforcement` activo con `PreToolUse`, write-tools bloqueadas y re-firma por cambio de plan.
- `execution` bloqueado, listo o ejecutado segun evidencia.
- `validation` y `guardian` consistentes con el estado real.

## Local Validation

```bash
bash skills/plan-mode-workflow/scripts/check.sh
```

El check valida fixtures buenos y rechaza mutaciones que escriben en Plan Mode, omiten firma, cambian el hash, desactivan el hook, usan `bypassPermissions` o fuerzan Guardian pass sobre un caso bloqueado.

## Output Format

Markdown con summary, evidence (`plan.md` + hash firmado), result (diff ejecutado o bloqueo), validation (checklist del gate) y risks.
