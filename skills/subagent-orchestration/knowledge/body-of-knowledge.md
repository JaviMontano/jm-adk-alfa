# Subagent Orchestration Body of Knowledge

## Canon

La orquestación de subagentes es un patrón hub-and-spoke. El hub descompone la tarea y despacha spokes con `AgentDefinition` + `Task`. Cada spoke es una sesión nueva con contexto vacío, sus propias tools y su propio modelo; el hub recibe únicamente el último mensaje de cada spoke, no su transcript. Esto da dos propiedades verificables: aislamiento de contexto y contención del blast radius.

## Conceptos

- **Aislamiento estructural:** sesión nueva por spoke, contexto vacío, tools y modelo dedicados. El hub solo ve el último mensaje devuelto.
- **Selección de modelo por spoke:** Haiku barato para extracción/clasificación; Sonnet para razonamiento que agrega o decide.
- **Error tipado del spoke:** `failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`. Habilita que el hub interprete el fallo sin adivinar.
- **Local recovery primero:** ante un fallo, el spoke intenta reintento acotado o query alternativa antes de propagar el error.
- **access_failure != valid_empty:** un `[]` por acceso fallido es semánticamente distinto de un `[]` legítimo; el diseño debe distinguirlos.
- **Coverage gap annotation:** el resultado del hub registra explícitamente qué ramas quedaron sin cobertura y por qué.
- **Valid empty:** resultado vacío legítimo con `status="ok"` y `empty_valid=true`; nunca es un fallo.

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Aislamiento | Cada spoke arranca con contexto vacío; el hub solo consume el último mensaje |
| Blast radius | El fallo de un spoke no aborta ni corrompe la agregación |
| Semántica de error | `access_failure` y `valid_empty` quedan distinguibles |
| Trazabilidad de cobertura | Coverage gaps explícitos por rama |
| Costo | Extracción delegada a modelo barato |
| Determinismo | Plan validable offline contra `assets/orchestration-contract.json` |

## Decisión de diseño

Usa hub-and-spoke cuando las subtareas son independientes y se benefician de contexto aislado o de modelos distintos. Si la tarea es secuencial y comparte estado denso, un pase encadenado (`prompt-chaining-design`) puede ser mejor. El umbral práctico: si concatenar todo satura la atención del modelo o impide paralelizar, conviene fan-out.

## Anti-patrón

Un solo agente con todo el contexto concatenado (sin aislamiento, atención saturada, sin paralelización) y un manejo de error tipo `except: return {"results": []}` que vuelve indistinguible un fallo de acceso de un vacío legítimo, oculta el coverage gap y elimina el blast radius.

## Evidencia Requerida

- Contrato de spokes con `AgentDefinition`.
- Uso de `Task` como dispatch tool.
- Política de aislamiento `fresh_session`.
- Contrato de error con cuatro campos mínimos.
- Política de local recovery.
- Política de agregación con coverage gaps.
