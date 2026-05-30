<!--
generated-by: scripts/scaffold-skill.py
generated-for: context-window-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Context Window Engineering Primary Prompt

## Objective

Diseña el ensamblado de la ventana de contexto del agente para maximizar prefix caching y minimizar dilución softmax.

## Required Inputs

- Bloques de contexto actuales (rol, herramientas, políticas, esquema, historial, recordatorios).
- Qué datos cambian por-turno (timestamp, contadores, estado, último mensaje).
- Reglas críticas que el modelo no puede olvidar.
- Límite de contexto del modelo y, si existe, métrica de cache-hit actual.

## Process

1. Particiona en bloques estáticos vs dinámicos.
2. Ordena estático-first: prefijo byte-idéntico, sin valores por-turno.
3. Empuja el estado volátil a un `<reminder>` final.
4. Coloca reglas críticas en bordes (inicio + reafirmadas al final).
5. Fija un umbral de compactación (>55%) que preserve los bordes.
6. Valida con cache-hit rate + prueba de retención.

## Output

Devuelve el diseño en este formato: resumen, bloque GOOD del context assembler, evidencia (cache-hit / retención), validación contra el checklist y riesgos.
