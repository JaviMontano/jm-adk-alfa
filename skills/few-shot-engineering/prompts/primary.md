<!--
generated-by: scripts/scaffold-skill.py
generated-for: few-shot-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Few Shot Engineering Primary Prompt

## Objetivo

Diseñar un bloque few-shot que calibre los bordes subjetivos de una tarea, usando 2–4 ejemplos del schema de salida exacto, colocados al inicio del prompt para preservar el prefix cache.

## Inputs requeridos

- Tarea y schema de salida de producción (claves, tipos).
- Casos reales de borde donde el modelo dudó o falló.
- Restricciones de coste/tokens y si la plataforma soporta prefix caching.

## Proceso

1. Extrae los bordes de los casos provistos; descarta los casos típicos.
2. Selecciona 2–4 bordes, cada uno ilustrando una decisión distinta.
3. Escribe cada ejemplo con el schema de salida exacto.
4. Ensambla el bloque al inicio del prompt, antes de la entrada variable.
5. Verifica complementariedad (ningún par de ejemplos se contradice).
6. Valida contra un set de bordes y recorre el checklist.

## Output

Devuelve: el bloque de ejemplos listo, la justificación de cada borde elegido, el resultado de la validación y los riesgos residuales. Formato Markdown con resumen, evidencia, resultado, validación y riesgos.
