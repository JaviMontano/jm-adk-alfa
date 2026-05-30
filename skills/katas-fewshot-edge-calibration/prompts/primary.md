<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-fewshot-edge-calibration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Fewshot Edge Calibration Primary Prompt

## Objetivo

Aplicar Kata 14: convertir una tarea subjetiva o de formato no rígido en un prompt few-shot con 2 a 4 ejemplos que calibran los bordes del dominio.

## Inputs requeridos

- La tarea subjetiva o de clasificación con criterio.
- El schema o formato de la salida esperada (si existe; ver Kata 5).
- Casos representativos del dominio, incluidos los bordes difíciles.

## Proceso

1. Confirma que la tarea es subjetiva o de formato no rígido (si es objetiva y rígida, basta el schema).
2. Selecciona 2 a 4 ejemplos `input/output` que cubran bordes distintos, no el caso fácil del centro.
3. Escribe cada ejemplo en el mismo schema que la salida esperada.
4. Coloca el bloque de ejemplos al inicio del prompt (parte estática: prefix cache, Kata 10).
5. Si hay schema estricto, alinea los ejemplos con él; ante conflicto, gana el schema.
6. Cierra el prompt con la instrucción real ("ahora clasifica: ...") sobre el input dinámico.

## Output

Devuelve el prompt few-shot final y, debajo, qué borde del dominio cubre cada ejemplo. Formato: Markdown con resumen, evidencia, resultado, validación y riesgos.
