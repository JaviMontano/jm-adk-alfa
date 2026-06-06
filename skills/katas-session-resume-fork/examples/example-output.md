<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-session-resume-fork
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Decisión

`fresh`

## Justificación

No usar `--resume`: hubo refactor grande en `services/` y `storage/`, asi que los tool results previos pueden describir archivos obsoletos. Tampoco es `fork`, porque no se pidieron dos enfoques paralelos desde una baseline comun.

## Comando

```bash
SUMMARY=$(cat .agent/audit-scratchpad.md)
claude -p "Continuamos la auditoria codebase-audit-2026-06. Usa este summary tipado y recarga services/ y storage/ antes de actuar:\n$SUMMARY"
```

## Summary inyectado

- Fuente: `.agent/audit-scratchpad.md`
- Campos: objetivo, hallazgos validados, decisiones, archivos tocados, pendientes
- Fuentes a recargar: `services/`, `storage/`

## Validation

- `resume` descartado por staleness.
- Transcript completo viejo descartado.
- Summary tipado proviene del scratchpad estructurado.
- Fuentes cambiadas se recargan antes de usar resultados previos.

## Riesgos y límites

- Si el scratchpad no incluye el refactor reciente, hay que actualizarlo antes de inyectar el summary.
- Si aparecen dos estrategias incompatibles, abrir forks nombrados desde la nueva baseline.
