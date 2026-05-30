<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-fewshot-edge-calibration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Fewshot Edge Calibration Body of Knowledge

> Canon de Kata 14 · "Few-Shot para Calibrar Bordes".

## Conceptos canónicos

- **Few-shot calibra distribución:** 2 a 4 ejemplos `input/output` desplazan la distribución del modelo hacia el formato deseado más rápido y barato que un párrafo de instrucciones.
- **Tareas objetivo:** subjetivas (tono, formato no estándar, juicio estético) o de clasificación con criterio, donde la prosa zero-shot deja al modelo en su default genérico.
- **Mismo schema:** los ejemplos son del mismo schema que la salida esperada; no son explicaciones, son instancias.
- **Bordes, no centro:** los ejemplos cubren los bordes del dominio (casos difíciles), no el caso fácil.
- **2 a 4 es el rango útil:** más de 5 dispersa atención (Kata 11) y rompe caches (Kata 10) sin mejorar calidad.
- **Few-shot complementa al schema (Kata 5):** el schema impone forma, los ejemplos calibran juicio. No reemplaza.
- **Conflicto schema vs few-shot:** gana el schema (restricción sintáctica dura); se reescriben los ejemplos para alinearlos.
- **Posición:** ejemplos al inicio = parte estática del prompt; maximiza prefix cache (Kata 10) y queda en el borde de atención alta (Kata 11).

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Cobertura de bordes | Los ejemplos cubren casos difíciles del dominio, no solo el centro |
| Mismo schema | Cada ejemplo tiene la forma exacta de la salida esperada |
| Conteo | Entre 2 y 4 ejemplos; nunca más de ~5 |
| Composición con schema | Si hay schema estricto, los ejemplos lo respetan; ante conflicto, gana el schema |
| Posición estática | Ejemplos al inicio para prefix cache y atención alta |

## Anti-patrón canónico

Párrafo abstracto sin ejemplos, p. ej.: "Clasifica usando criterio profesional, considerando urgencia, dominio, impacto, severidad operacional, prioridad SLA y política interna." El modelo lo interpreta distinto en cada llamada y no converge al formato esperado. El reemplazo correcto es mostrar 3 ejemplos de cómo se ve el output.

## Quiz de referencia (B·B·B)

- P1: few-shot supera a la prosa cuando la tarea es subjetiva o de formato no rígido; mostrar ejemplos comunica ground truth mejor que describirlo.
- P2: si few-shot contradice el schema, gana el schema (restricción sintáctica dura); re-escribir los ejemplos.
- P3: ejemplos al inicio = parte estática → maximiza prefix cache (Kata 10) y queda en el borde de atención alta (Kata 11).
