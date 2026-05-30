<!--
generated-by: scripts/scaffold-skill.py
generated-for: validation-retry-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Validation Retry Design

Capacidad construible para disenar un loop `extract -> validate -> retry-with-error-feedback`: reintenta reinyectando el error especifico, separa fallas recuperables de no recuperables, pone tope (max 2-3) y escala con la cadena de errores en vez de aceptar salida fallida en silencio.

## Resumen ejecutivo

El valor no esta en "reintentar", sino en reintentar **informado**. El validador devuelve un error accionable; ese error alimenta el siguiente intento; el modo de falla decide si reintentar o escalar; el tope acota el costo; el patron sistematico dispara un fix estructural. Es el contrato de robustez de cualquier pipeline de agente que produce salida estructurada.

## Triggers

- validation retry design
- error feedback loop
- recoverable vs not
- retry budget

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

1. Escribe el validador que devuelve `{ok, error, recoverable}`.
2. Envuelve la llamada al modelo en un loop con `max_retries=2-3`.
3. En cada reintento reinyecta el error previo, no el prompt original.
4. Escala con la cadena de errores al agotar el tope o ante falla no recuperable.

## Output Format

Markdown con: diseno del loop, validador (con clasificacion de modo de falla), construccion del retry feedback, politica de escalada y checklist de validacion.
