<!--
generated-by: scripts/scaffold-skill.py
generated-for: validation-retry-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Validation Retry Design Primary Prompt

## Objetivo

Disenar e implementar el loop `extract -> validate -> retry-with-error-feedback` para el paso del agente que produce salida estructurada.

## Inputs requeridos

- La tarea/paso que produce la salida y su formato esperado (schema).
- Como se valida (reglas pass/fail).
- Que cuenta como dato ausente (no recuperable) vs error de formato (recuperable).
- Presupuesto de reintentos disponible (default 2-3).
- A donde escalar al agotar el tope.

## Proceso

1. Define el validador que devuelve `{ok, error, recoverable}` con causa accionable.
2. Implementa el loop: en cada reintento reinyecta el error especifico previo + la salida previa, nunca el prompt original intacto.
3. Clasifica modo de falla: recuperable reintenta; no recuperable escala de inmediato.
4. Aplica tope `max_retries` con contador y cadena de errores.
5. Detecta patron sistematico (mismo error repetido) -> reporta fix estructural.
6. Escala con la cadena completa de errores al agotar el tope.

## Output

Diseno del loop + codigo del validador y del retry feedback (EN) + politica de escalada + checklist de validacion marcado.
