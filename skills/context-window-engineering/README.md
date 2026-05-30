<!--
generated-by: scripts/scaffold-skill.py
generated-for: context-window-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Context Window Engineering

Capacidad construible para ensamblar la ventana de contexto de un agente con **prefix caching estático-first** (KV cache reutilizado ~10x) y **mitigación de dilución softmax** mediante edge placement (curva en U) y compactación por umbral. No es entrenamiento: es cómo se diseña, implementa y valida el context assembler en producción.

## Resumen ejecutivo

Un agente paga (en latencia y costo) por re-procesar su prefijo en cada turno y "olvida" reglas críticas cuando el contexto crece. Esta skill resuelve ambos problemas: ordena el contexto estático-first para que el prefijo se cachee, empuja el estado volátil a un `<reminder>` final, ubica las reglas críticas en los bordes y fija un umbral de compactación.

## Triggers

- context window engineering
- prefix cache optimization
- context dilution
- edge placement

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

1. Particiona el contexto en estático vs dinámico.
2. Estático-first (prefijo byte-idéntico, cacheable) + dinámico-last (`<reminder>`).
3. Reglas críticas en bordes (inicio + reafirmadas al final).
4. Fija umbral de compactación (>55%).
5. Valida con cache-hit rate + prueba de retención.

## Output Format

Markdown con resumen, diseño del context assembler (GOOD), evidencia (cache-hit / retención), validación contra el checklist y riesgos.
