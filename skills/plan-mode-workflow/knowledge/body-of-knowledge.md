# Plan Mode Workflow Body of Knowledge

## Canon

La capacidad es un **gate de dos modos aplicado por hook**. Conceptos centrales:

- **Estado de modo**: `mode ∈ {plan, execute}`, dato explícito, arranca en `plan`. No es una intención del modelo.
- **Plan como artefacto**: `plan.md` con objetivo, archivos a tocar, orden de cambios, criterio de aceptación y riesgos. Es el objeto que se firma e identifica por hash.
- **Firma como evento auditable**: `approve_plan(hash, approver, timestamp)`. La aprobación referencia el hash exacto del plan, no un "ok" conversacional.
- **Enforcement por hook**: un `PreToolUse` lee el modo; si `mode == "plan"` y la tool está en la write-list, deniega con motivo. La única ruta a `execute` es firmar el hash.
- **Reversión por cambio**: si `plan.md` cambia tras la firma (hash distinto), el modo vuelve a `plan` y se re-exige aprobación.

## Quality Signals

| Signal | Target |
|---|---|
| Read-only enforcement | Writes bloqueadas por hook mientras `mode == "plan"`, no por convención |
| Approval auditability | Firma = hash + aprobador + timestamp, recuperable como evidencia |
| Re-sign on change | Cambio del plan post-firma revierte a `plan` y re-pide firma |
| Write-tool coverage | El hook enumera todas las tools de mutación (Write/Edit/MultiEdit/NotebookEdit/MCP/Bash mutante) |

## Decisión de diseño

El modo se modela como **estado verificable por un tercero (el hook)**, no como disciplina del agente. Esto convierte el gate en inviolable por construcción: aunque el modelo "decida" escribir, la write-tool se deniega. El plan firmado más el diff resultante forman el rastro de auditoría de qué se autorizó y qué se ejecutó.

## Anti-patrón

`permissionMode: bypassPermissions` con escritura desde el primer turno: sin plan, sin firma, sin hook. El agente muta archivos de blast radius desconocido decidiendo solo, sin rastro auditable ni punto de reversión.

## Open Knowledge

- Interacción con resume/fork: un mundo cambiado invalida el plan firmado.
- Persistencia del estado de modo entre sesiones sin romper prefix cache.
