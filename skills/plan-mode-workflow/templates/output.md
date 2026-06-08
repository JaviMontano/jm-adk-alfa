# Plan Mode Workflow Output

## Summary

{summary_del_gate_de_dos_modos}

## Evidence

- Plan firmado: `plan.md` (hash `{plan_hash}`, aprobado por `{approver}` el `{timestamp}`).
- Write-tools bloqueadas en Plan Mode: `{write_tool_list}`.

## Result

{diff_ejecutado_en_execute_mode}

## Validation

- [ ] Escritura deshabilitada por hook mientras `mode == "plan"`.
- [ ] Aprobación = hash + aprobador + timestamp (artefacto auditable).
- [ ] Cambio del plan post-firma revierte a `plan` y re-pide firma.
- [ ] El hook enumera todas las tools de escritura.

## Risks and Limits

{riesgos_residuales}
