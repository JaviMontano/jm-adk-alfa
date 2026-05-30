---
name: independent-review-design
version: 1.0.0
description: "Disenar revision con reviewer independiente en sesion limpia, pases per-file y cross-file, sin quorum que suprima senal rara."
owner: "JM Labs"
triggers:
  - independent review design
  - clean session reviewer
  - per-file cross-file
  - no quorum
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Independent Review Design

## Capacidad

Capacidad de ingeniería para diseñar la etapa de revisión de un pipeline de generación
(código, documentos, hallazgos) de modo que el reviewer sea **independiente**: opera en
una sesión limpia que nunca vio la generación, ejecuta un pase **per-file** y un pase
separado **cross-file**, y reporta sin un **quorum N-de-M** que suprima señal rara pero
legítima. El objetivo de diseño es maximizar la detección de defectos reales sin que el
contexto de generación contamine el juicio del revisor.

## Cuándo usarla

- Estás construyendo un agente o pipeline que genera artefactos y luego los revisa.
- El revisor actual comparte sesión/contexto con el generador (self-review) y sospechas
  sesgo de confirmación.
- Implementaste un mecanismo de votación (2-de-3, mayoría) y notas que issues legítimos
  desaparecen porque solo un pase los detectó.
- Necesitas separar análisis local (un archivo) de análisis de consistencia global
  (entre archivos) porque ambos detectan clases distintas de defectos.

## Cómo construir

1. **Aísla la sesión del reviewer.** Arranca el revisor en un proceso/contexto nuevo que
   reciba únicamente el artefacto a revisar y el criterio de revisión, nunca el prompt de
   generación, el razonamiento intermedio ni el historial del generador.
2. **Diseña el pase per-file.** Por cada archivo, ejecuta una revisión enfocada: defectos
   locales, contratos, edge cases, evidencia. Cada hallazgo cita archivo y línea.
3. **Diseña el pase cross-file por separado.** Con el set completo, busca inconsistencias
   de naming, contratos rotos entre módulos, duplicación y supuestos contradictorios. No
   fusiones este pase con el per-file: detectan clases distintas de defectos.
4. **No impongas quorum.** Reporta todo hallazgo de cualquier pase. Un issue detectado por
   un único pase es señal, no ruido; el quorum lo filtraría.
5. **Normaliza y deduplica los hallazgos** sin descartar por baja frecuencia: agrupa por
   ubicación + categoría, conserva la severidad máxima observada.
6. **Valida con el checklist** antes de cerrar el diseño.

## Patrón correcto

```python
# GOOD: reviewer independiente, per-file + cross-file separados, sin quorum
def review(artifacts: list[Artifact], criteria: Criteria) -> list[Finding]:
    # Sesion limpia: el reviewer NO recibe generation_prompt ni reasoning trace.
    reviewer = Reviewer(session=Session.fresh(), criteria=criteria)

    findings: list[Finding] = []
    for art in artifacts:                       # Pase 1: per-file
        findings += reviewer.review_file(art)

    findings += reviewer.review_cross_file(artifacts)  # Pase 2: cross-file (separado)

    # Sin quorum: cada hallazgo legitimo se conserva, aunque venga de un solo pase.
    return dedupe_keep_max_severity(findings)
```

## Anti-patrón

```python
# ANTI: self-review en misma sesion + quorum que suprime senal rara
def review_bad(artifacts, gen_session):
    # El reviewer hereda la sesion del generador -> sesgo de confirmacion.
    reviewer = Reviewer(session=gen_session)

    votes = collections.Counter()
    for _ in range(3):                          # 3 pases mezclados, sin separar per/cross
        for f in reviewer.review_all(artifacts):
            votes[f.key] += 1

    # Quorum 2-de-3: descarta issues reales que solo un pase vio.
    return [f for f in votes if votes[f] >= 2]
```

## Checklist de validación

- ¿El reviewer corre en sesión limpia, sin acceso a la generación?
- ¿El pase per-file y el pase cross-file están separados (no fusionados)?
- ¿No hay quorum N-de-M que suprima issues legítimos detectados por un solo pase?
- ¿Cada hallazgo cita archivo/línea y conserva su severidad?
- ¿La deduplicación agrupa sin descartar por baja frecuencia?

## Katas y skills relacionadas

- Kata 27.
- Relacionadas: `katas-independent-reviewer-multipass`.
