<!--
generated-by: scripts/scaffold-skill.py
generated-for: subagent-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Subagent Orchestration Body of Knowledge

## Canon

La orquestación de subagentes es un patrón hub-and-spoke. El hub (coordinador) descompone la tarea y despacha spokes (subagentes) con `AgentDefinition` + `Task`. Cada spoke es una sesión nueva con contexto vacío, sus propias tools y su propio modelo; el hub recibe únicamente el último mensaje de cada spoke, no su transcript. Esto da dos propiedades: aislamiento de contexto (el ruido de un spoke no contamina a los demás) y contención del blast radius (el fallo de un spoke no tumba al resto).

## Conceptos

- **Aislamiento estructural:** sesión nueva por spoke, contexto vacío, tools y modelo dedicados. El hub solo ve el último mensaje devuelto.
- **Selección de modelo por spoke:** Haiku barato para extracción/clasificación; Sonnet para razonamiento que agrega o decide.
- **Error tipado del spoke:** `failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`. Habilita que el hub interprete el fallo sin adivinar.
- **Local recovery primero:** ante un fallo, el spoke intenta reintento acotado o query alternativa antes de propagar el error.
- **access_failure != valid_empty:** un `[]` por acceso fallido es semánticamente distinto de un `[]` legítimo; el diseño debe distinguirlos.
- **Coverage gap annotation:** el resultado del hub registra explícitamente qué ramas quedaron sin cobertura y por qué.

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Aislamiento | Cada spoke arranca con contexto vacío; el hub solo consume el último mensaje |
| Blast radius | El fallo de un spoke no aborta ni corrompe la agregación |
| Semántica de error | `access_failure` y `valid_empty` quedan distinguibles |
| Trazabilidad de cobertura | Coverage gaps explícitos por rama |
| Costo | Extracción delegada a modelo barato |

## Decisión de diseño

Usa hub-and-spoke cuando las subtareas son independientes y se benefician de contexto aislado o de modelos distintos. Si la tarea es secuencial y comparte estado denso, un pase encadenado (`prompt-chaining-design`) puede ser mejor. El umbral práctico: si concatenar todo satura la atención del modelo o impide paralelizar, conviene fan-out.

## Anti-patrón

Un solo agente con todo el contexto concatenado (sin aislamiento, atención saturada, sin paralelización) y un manejo de error tipo `except: return {"results": []}` que vuelve indistinguible un fallo de acceso de un vacío legítimo, oculta el coverage gap y elimina el blast radius.

## Open knowledge

- Añadir referencias específicas del proyecto (límites de fan-out, políticas de reintento) a medida que se estabilicen.
