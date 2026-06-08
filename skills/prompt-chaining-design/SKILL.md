---
name: prompt-chaining-design
version: 1.0.0
description: "Descomponer tareas grandes en pase local tipado y pase de integracion sobre resumenes, con schemas de transicion entre pases."
owner: "JM Labs"
triggers:
  - prompt chaining design
  - multipass decomposition
  - transition schema
  - chained passes
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Prompt Chaining Design

## Capacidad

Diseñar e implementar el procesamiento de una tarea grande como una **cadena de pases** en lugar de un único mega-prompt. El patrón canónico tiene dos etapas: un **pase local tipado** que procesa cada unidad (archivo, ticket, registro) de forma aislada y emite un resumen estructurado contra un schema, y un **pase de integración** que solo consume esos resúmenes —nunca los datos crudos— para producir el resultado final. Entre pases existe un **schema de transición** explícito que define qué viaja, en qué forma, y cómo se representa el error por unidad. La capacidad sustituye saturación de atención y costo cuadrático por paralelización tipada y trazable.

## Cuándo usarla

- La tarea requiere consumir más unidades de las que caben con calidad en una sola ventana de atención (decenas de archivos, cientos de registros).
- Las unidades son procesables de forma independiente y solo se integran al final (map → reduce).
- Necesitas paralelizar el pase local y aislar fallos por unidad sin abortar todo el lote.
- El resultado final depende de una síntesis sobre resúmenes, no de cada byte crudo.
- NO usarla cuando un single-pass cabe holgado y razona mejor con el contexto completo: el chaining añade overhead de schemas y debe justificarse.

## Cómo construir

1. **Delimita la unidad atómica.** Define qué es "una unidad" del pase local (un archivo, un commit, un documento). El pase local nunca debe ver más de una unidad por invocación.
2. **Define el schema de salida del pase local.** Tipa el resumen que cada unidad produce: campos obligatorios, tipos, y un campo de estado (`ok` / `error`) con detalle del fallo. Sin schema no hay cadena, hay pegamento.
3. **Define el schema de transición.** Especifica el contrato que el pase de integración recibe: una colección tipada de resúmenes. El pase 2 jamás recibe los crudos.
4. **Implementa el pase local idempotente y aislado.** Cada unidad se procesa sin depender de otra; el error de una unidad se tipa y se propaga como dato, no como excepción que tumba el lote.
5. **Implementa el pase de integración sobre resúmenes.** Sintetiza, agrega o decide leyendo solo la colección tipada. Si necesita un crudo, eso indica que el schema del pase local está incompleto: corrígelo, no abras un atajo.
6. **Justifica vs single-pass.** Documenta por qué el chaining gana (volumen, paralelismo, aislamiento de error). Si no hay ganancia medible, colapsa a single-pass.

## Patrón correcto

```python
# GOOD: pase local tipado por unidad + integración solo sobre resúmenes.
from pydantic import BaseModel
from typing import Literal

class UnitSummary(BaseModel):
    unit_id: str
    status: Literal["ok", "error"]
    findings: list[str] = []
    error_detail: str | None = None

def local_pass(unit: SourceFile) -> UnitSummary:
    # Ve UNA sola unidad. El fallo se tipa, no se lanza.
    try:
        findings = analyze(unit.content)
        return UnitSummary(unit_id=unit.id, status="ok", findings=findings)
    except AnalysisError as exc:
        return UnitSummary(unit_id=unit.id, status="error", error_detail=str(exc))

# Schema de transición: colección tipada de resúmenes (nunca crudos).
summaries: list[UnitSummary] = [local_pass(u) for u in units]  # paralelizable

def integration_pass(summaries: list[UnitSummary]) -> Report:
    ok = [s for s in summaries if s.status == "ok"]
    failed = [s for s in summaries if s.status == "error"]
    # El pase 2 razona SOLO sobre resúmenes tipados.
    return synthesize(ok, failures=failed)
```

## Anti-patrón

```python
# ANTI: mega-prompt que concatena todos los crudos en una sola pasada.
# Satura la atención, no paraleliza, y un fallo en un archivo contamina todo.
blob = "\n\n".join(read(f) for f in fifty_files)   # 50 archivos crudos juntos
result = model(f"Analiza todo esto y dame el reporte:\n{blob}")
# Sin schema por pase, sin estado de error por unidad, sin transición tipada.
```

## Checklist de validación

- ¿El pase de integración nunca ve los datos crudos, solo resúmenes?
- ¿Cada pase tiene un schema de salida explícito y tipado?
- ¿El estado de error está tipado por unidad (no una excepción global)?
- ¿El pase local procesa una sola unidad y es paralelizable e idempotente?
- ¿Existe un schema de transición que define qué viaja entre pases?
- ¿Se justifica el chaining frente a un single-pass (volumen / paralelismo / aislamiento)?

## Assets y validación offline

- `assets/` define el contrato determinístico para justificación vs single-pass, unidad atómica, schema local, schema de transición, integración sobre resúmenes y errores tipados.
- `scripts/check.sh` valida fixtures locales sin red, tiempo real ni aleatoriedad.
- `scripts/validate_prompt_chaining_design.py` rechaza diseños donde el pase de integración consume crudos, falta schema, el pase local procesa varias unidades, no hay error tipado o Guardian aprueba un diseño bloqueado.

## Katas y skills relacionadas

- `katas-multipass-prompt-chaining`
- `workflow-forge`
- `output-engineering`
