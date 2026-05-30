<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-critical-self-correction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 15 · Body of Knowledge — Evaluación Crítica y Auto-Corrección

## Canon

La verificación crítica parte de reconocer **dos fuentes de verdad** para todo número:

- `stated`: el valor que el documento o la fuente declara explícitamente.
- `computed`: el valor que el agente recalcula de forma determinista a partir de las líneas o fuentes subyacentes.

El invariante es simple: ambas deben coincidir dentro de un epsilon. Si no coinciden, no hay decisión que tomar unilateralmente; hay un **conflicto que reportar y escalar**.

### Conceptos clave

- **Cross-check numérico:** comparar `stated` contra `computed` con `abs(stated - computed) > epsilon`. Aplica a totales, sumas, subtotales, conteos y fechas derivadas.
- **Epsilon de tolerancia:** cero para enteros y conteos (igualdad exacta); epsilon pequeño para moneda, porque el redondeo de centavos introduce diferencias legítimas. El valor del epsilon debe justificarse, no asumirse.
- **Mismatch flag:** ante discrepancia se devuelve un objeto tipado con `stated_total`, `computed_total`, `mismatch=true`, `delta` y `needs_human_review=true`. Se preservan AMBOS valores.
- **Caso sin total declarado:** si el documento no declara total, se devuelve `computed_total` con `stated_total=null` y `mismatch=false`. No se fabrica un conflicto.
- **Determinismo del cálculo:** `computed` se obtiene en código (`sum(line.amount for line in doc.lines)`), no delegando la aritmética al modelo.

### Señales de calidad

| Señal | Objetivo |
|---|---|
| Cobertura de campos | Todos los números verificables se cruzan (totales, sumas, conteos, fechas derivadas) |
| Epsilon justificado | Cero para enteros, epsilon de centavos para moneda, con racional explícito |
| Conflicto preservado | `mismatch=true` reporta ambos valores y el delta, no un valor "elegido" |
| Escalada conectada | El mismatch enruta a `katas-human-handoff-protocol`; el origen se preserva con `katas-provenance-preservation` |

## Anti-patrón canónico

```python
# Confía en lo declarado sin recalcular:
total = extract_total(doc)

# O corrige en silencio, ocultando la discrepancia al humano:
if abs(stated - computed) > epsilon:
    total = computed  # corrige silenciosamente
```

Ambas variantes producen la misma falla: el sistema confía en la alucinación más plausible y nadie se entera. En facturación, contabilidad o impuestos eso es un incidente operacional.

## Open Knowledge

- Catálogo de tipos de documento por dominio (factura, recibo, estado de cuenta) y qué campos numéricos exige cruzar cada uno.
- Tabla de epsilons por moneda y por unidad cuando se estabilicen los casos reales.
