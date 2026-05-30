<!--
generated-by: scripts/scaffold-skill.py
generated-for: validation-retry-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Validation Retry Design Body of Knowledge

## Canon

El loop `extract -> validate -> retry-with-error-feedback` es el contrato de robustez de un paso de agente que produce salida estructurada. Conceptos clave:

- **Retry informado:** cada reintento lleva el error especifico del intento previo + la salida previa + instruccion de correccion. No es el prompt original reenviado.
- **Validador como fuente del feedback:** el validador no retorna `true/false`; retorna `{ok, error, recoverable}` donde `error` es la causa accionable.
- **Recuperable vs no recuperable:** recuperable = formato/parseo/rango (reintenta). No recuperable = dato ausente en la fuente, contradiccion irresoluble (escala de inmediato, reintentar no lo arregla).
- **Presupuesto de reintentos:** tope `max_retries` 2-3, con contador y cadena de errores acumulada.
- **Patron sistematico:** si el mismo error reaparece en todos los intentos, es defecto estructural (prompt/schema/fuente); romper el loop y reportar el fix, no gastar reintentos.
- **Escalada:** al agotar el tope o ante falla no recuperable, retornar estado de escalada con la cadena completa de errores y el ultimo output.

## Quality Signals

| Senal | Objetivo |
|---|---|
| Retry informado | El prompt del reintento contiene el error especifico previo |
| Validador accionable | Devuelve causa, no solo booleano |
| Clasificacion de falla | Recuperable reintenta; no recuperable escala |
| Tope de reintentos | max 2-3 con contador y cadena de errores |
| Deteccion sistematica | Error repetido dispara fix estructural |
| Escalada explicita | Cadena de errores en vez de salida fallida silenciosa |

## Decision de diseno

- Si reintentar puede corregirlo, es recuperable; si la informacion no esta, ningun reintento la creara: escala.
- Si el error es el mismo en cada intento, el problema esta en el diseno (prompt/schema), no en el modelo.

## Anti-patron

Reintentar reenviando el prompt original sin cambios (mismo fallo repetido) y aceptar la salida fallida en silencio sin escalar.
