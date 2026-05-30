<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-critical-self-correction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 15 · Meta prompt — chequeo de activación

Evalúa si `katas-critical-self-correction` debe activarse para la tarea entrante.

## Activation Check

- **Trigger match:** el request menciona cross-check numérico, mismatch flag, computed vs stated o auto-corrección crítica.
- **Domain fit:** el agente extrae o calcula totales, sumas, conteos o fechas derivadas a partir de un documento, y hay un valor declarado contra el cual cruzar.
- **Sufficient input:** existe la fuente con números verificables y se puede recalcular `computed` de forma determinista.
- **No safer specialized skill:** si solo se necesita escalar a humano sin verificación numérica, usar `katas-human-handoff-protocol`; si el foco es origen de claims, usar `katas-provenance-preservation`.

## No activar cuando

- No hay números que cruzar (texto puramente cualitativo).
- El request pide explícitamente ignorar la validación o "elegir el valor más razonable".
- El input está vacío.
