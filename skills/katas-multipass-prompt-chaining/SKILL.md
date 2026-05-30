---
name: katas-multipass-prompt-chaining
version: 1.0.0
description: "Prompt chaining multi-pass: pase local tipado por unidad y pase de integracion que solo ve resumenes, no las unidades crudas."
owner: "JM Labs"
triggers:
  - prompt chaining
  - multipass chaining
  - local then integrate
  - chaining schema
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Multipass Prompt Chaining

Kata 12 · Prompt Chaining Multi-Pass · escenario Multi-Agent Orchestration.

## Qué es

Cuando una tarea no cabe cognitivamente en un solo prompt (auditar 50 archivos, resumir 200 páginas), se descompone en pases secuenciales. El **pase local** procesa cada unidad de forma independiente y emite una salida tipada y compacta según un schema. El **pase de integración** solo ve los resúmenes tipados del pase 1, nunca las unidades crudas ni la totalidad sin filtrar. Cada pase declara su schema y el siguiente lo consume: los pases se componen como una pipeline.

## Por qué importa (falla que evita)

Pedir "audita estos 50 archivos" en un solo prompt satura la atención del modelo: pierde detalles, alucina relaciones entre archivos y produce un resumen genérico que parece correcto pero no lo es. Encadenar mantiene cada pase enfocado, barato y verificable, y permite paralelizar el pase 1 (un subagente por unidad). El cuello de botella deja de ser la ventana de contexto y pasa a ser el diseño de los schemas de transición.

## Modelo mental

- **Pase 1 (paralelo):** una invocación por unidad, salida tipada y compacta según schema (p. ej. `FileFindings`). Cada unidad se procesa aislada, sin ver a las demás.
- **Pase 2 (integración):** solo consume los outputs tipados del pase 1, no las unidades crudas; nunca ve la totalidad sin filtrar.
- **Schemas declarados:** cada pase tiene un schema de salida; el siguiente pase consume exactamente ese schema. Sin estado de error tipado por unidad, el pase 2 cree que tiene N unidades válidas cuando en realidad tiene N-1: falla silenciosa.
- **Pipeline:** los pases se componen; el límite de contexto de cada pase se respeta por separado.

## Patrón correcto

```python
# Pase 1: por archivo, schema FileFindings (paralelizable)
local = [analyze_file(f, schema=FileFindings) for f in files]
# Pase 2: integración solo sobre resúmenes tipados, no sobre las unidades crudas
report = integrate(local, schema=AuditReport)
```

## Anti-patrón

```python
mega_prompt = "\n\n".join(open(f).read() for f in files)
create(messages=[{"role": "user", "content": f"Audita todo:\n{mega_prompt}"}])
# Satura la atención (Kata 11), no paraleliza, alucina entre archivos.
```

## Argumento de certificación

- Identificar tareas candidatas para chaining versus single-pass (cuándo el overhead de coordinación se justifica y cuándo no).
- Diseñar los schemas de transición entre pases, incluyendo estado de error tipado por unidad.
- Conectar con Kata 4 (subagentes para paralelizar el pase 1) y Kata 11 (cada pase respeta el límite de contexto).

## Cuándo activar

- La tarea no cabe holgadamente en una sola ventana de contexto (muchos archivos, documento largo).
- Se requiere salida tipada y auditable por unidad antes de integrar.
- NO activar cuando la tarea cabe holgadamente y el overhead de coordinación supera el beneficio.

## Skills relacionadas

- `katas-subagents-parallel`
- `katas-context-budget`
- `katas-provenance-preservation`
