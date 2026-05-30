<!--
generated-by: scripts/scaffold-skill.py
generated-for: independent-review-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Independent Review Design Body of Knowledge

## Canon

La calidad de una revisión depende de tres decisiones de diseño acopladas: **independencia
del reviewer**, **separación de pases** y **ausencia de quorum supresivo**.

### Conceptos

- **Reviewer independiente.** El revisor opera en una sesión limpia que no vio la
  generación. No recibe el prompt de generación, el razonamiento intermedio ni el
  historial del generador; solo el artefacto y el criterio de revisión. Evita el sesgo de
  confirmación: un revisor que conoce la intención del autor tiende a racionalizar
  defectos.
- **Pase per-file.** Revisión enfocada archivo por archivo: defectos locales, contratos,
  edge cases, evidencia. Detecta clase de defectos localizados.
- **Pase cross-file.** Revisión del set completo: inconsistencias de naming, contratos
  rotos entre módulos, duplicación, supuestos contradictorios. Detecta clase de defectos
  globales que el per-file no puede ver.
- **Sin quorum N-de-M.** Reportar todo hallazgo de cualquier pase. Un quorum (votación
  2-de-3, mayoría) está diseñado para suprimir ruido, pero en revisión la señal rara suele
  ser un defecto real que solo un pase detectó.

### Señales de calidad

| Señal | Target |
|---|---|
| Independencia | El reviewer no tiene acceso al contexto de generación |
| Separación de pases | per-file y cross-file son etapas distintas |
| No supresión | Ningún quorum ni umbral de frecuencia descarta hallazgos |
| Trazabilidad | Cada hallazgo cita archivo/línea y severidad |
| Dedupe seguro | Agrupa por ubicación+categoría, conserva severidad máxima |

### Decisión de diseño

Separar per-file de cross-file porque optimizan objetivos distintos: el per-file maximiza
profundidad local, el cross-file maximiza consistencia global. Fusionarlos diluye ambos.
No imponer quorum porque el costo de un falso negativo (defecto no reportado) supera al de
un falso positivo (hallazgo extra que el humano descarta).

### Anti-patrón

Self-review en la misma sesión (el reviewer hereda el contexto del generador) combinado con
quorum 2-de-3 (suprime issues legítimos detectados por un solo pase). Resultado: revisión
que confirma lo que el generador ya creía y oculta los defectos más raros y costosos.

## Open Knowledge

- Calibrar el costo relativo falso-positivo/falso-negativo según el dominio del artefacto.
