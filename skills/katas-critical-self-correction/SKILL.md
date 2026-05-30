---
name: katas-critical-self-correction
version: 1.0.0
description: "Evaluacion critica: cross-check numerico declarado vs calculado, mismatch flag con ambos valores, sin corregir en silencio."
owner: "JM Labs"
triggers:
  - critical self-correction
  - numeric cross-check
  - mismatch flag
  - computed vs stated
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Kata 15 · Evaluación Crítica y Auto-Corrección

## Qué es

Cuando el modelo extrae números (totales, sumas, fechas calculadas), debe cruzar lo calculado versus lo que la fuente declara. Si discrepan más allá de un epsilon, no decide arbitrariamente: emite un flag de conflicto con ambos valores y enruta a revisión humana. Escenarios típicos: Customer Support y Structured Extraction.

## Por qué importa (falla que evita)

Un total de factura calculado por el modelo puede coincidir con el declarado, o no. Sin verificación cruzada, el sistema confía silenciosamente en la alucinación más plausible. En facturación, contabilidad o impuestos, eso es un incidente operacional, no un detalle estético.

## Modelo mental

- Hay dos fuentes de verdad: lo declarado en el documento (`stated`) y lo calculado por el agente (`computed`).
- Ambas deben coincidir dentro de un epsilon de tolerancia.
- Si difieren, marcar `mismatch=true` con ambos valores y el delta. Nunca "elegir el más razonable".
- Aplica a totales numéricos, sumas, conteos y fechas derivadas.
- Un `mismatch` escala vía Kata 16 (handoff humano); el origen del dato se preserva vía Kata 20 (provenance).

## Patrón correcto

```python
stated = extract_stated_total(doc)
computed = sum(line.amount for line in doc.lines)
if abs(stated - computed) > epsilon:
    return {
        "stated_total": stated,
        "computed_total": computed,
        "mismatch": True,
        "delta": stated - computed,
        "needs_human_review": True,
    }
```

## Anti-patrón

```python
# Confía ciegamente en lo declarado, sin recalcular:
total = extract_total(doc)

# O peor: corrige en silencio y oculta la discrepancia:
if abs(stated - computed) > epsilon:
    total = computed  # corrige silenciosamente
```

## Argumento de certificación

- Identificar los campos numéricos sujetos a verificación cruzada.
- Definir el epsilon de tolerancia (cero para enteros, epsilon pequeño para monedas por redondeo de centavos) y justificarlo.
- Conectar con Kata 16 (escalada humana) y Kata 20 (provenance).

## Cuándo activar

- Cuando el modelo extrae o calcula totales, sumas, conteos o fechas derivadas a partir de un documento.
- En pipelines de facturación, contabilidad, impuestos o cualquier extracción donde un número incorrecto sea un incidente.
- Cuando una fuente declara un total y el agente puede recalcularlo a partir de sus líneas.

## Skills relacionadas

- `katas-human-handoff-protocol`
- `katas-provenance-preservation`
- `katas-validation-retry-feedback`
- `katas-confidence-stratified-sampling`
