<!--
generated-by: scripts/scaffold-skill.py
generated-for: prompt-chaining-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Prompt Chaining Design Body of Knowledge

## Canon

El encadenamiento multi-pass descompone una tarea grande en una secuencia de pases tipados en lugar de un único prompt masivo. El patrón base es **map → reduce sobre resúmenes**:

- **Pase local (map):** procesa una sola unidad (archivo, ticket, registro) de forma aislada y emite un resumen estructurado contra un schema. Es idempotente, paralelizable, y el fallo de una unidad se tipa como dato (`status: error`), no como excepción global.
- **Schema de transición:** contrato explícito que define qué viaja entre pases. Es una colección tipada de resúmenes. Si el schema del pase local está bien diseñado, el pase de integración nunca necesita un crudo.
- **Pase de integración (reduce):** sintetiza, agrega o decide leyendo solo la colección de resúmenes. Tolera unidades en estado de error.

### Conceptos clave

- **Unidad atómica:** granularidad mínima procesable de forma independiente. Determina paralelismo y aislamiento de error.
- **Schema por pase:** sin un schema tipado por pase no hay cadena, hay concatenación frágil.
- **Estado de error tipado por unidad:** el error es un campo del resumen, no un crash que contamina el lote.
- **Justificación vs single-pass:** el chaining añade overhead; solo se adopta cuando el volumen, el paralelismo o el aislamiento lo pagan.

## Quality Signals

| Signal | Target |
|---|---|
| Aislamiento del pase 2 | El pase de integración nunca lee datos crudos, solo resúmenes |
| Tipado por pase | Cada pase tiene schema de salida explícito |
| Error por unidad | El fallo de una unidad se representa tipado, sin abortar el lote |
| Justificación | El chaining gana de forma medible frente a single-pass |
| Update safety | El trabajo manual existente se preserva |

## Anti-patrón canónico

Mega-prompt que concatena 50 archivos crudos en una sola pasada: satura la atención del modelo, no paraleliza, carece de schema por pase y de estado de error por unidad, y un fallo en un archivo contamina todo el resultado.

## Open Knowledge

- Añadir referencias específicas del proyecto (límites de ventana efectivos, costos por pase) a medida que se estabilicen.
