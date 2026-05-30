<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-context-dilution-mitigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Context Dilution Mitigation Body of Knowledge

## Canon

- **Curva en U de atención.** El mecanismo de atención softmax del transformer distribuye atención de forma no uniforme: los bordes del prompt (inicio y fin) reciben atención alta, el centro se diluye. Es el fenómeno "lost in the middle".
- **Edge placement.** Las reglas críticas (seguridad, compliance, invariantes) se colocan al inicio del prompt como `<rules>critical_policy</rules>` y se repiten al final como `REMINDER:<rules>critical_policy</rules>`. Ambos bordes son zonas de atención alta, así que repetir la misma regla cubre el riesgo de dilución.
- **Datos al centro.** El material rico y voluminoso (contexto, documentos, historial de datos) va al centro, donde la atención baja penaliza menos.
- **Umbral de compactación.** Cuando `usage_fraction(history) > 0.55`, se compacta: `history = compact(history, preserve=['rules','decisions','escalations'])`. El rango 50-60% balancea conservar contexto útil contra evitar que las reglas se hundan en el valle.
- **Compactar ≠ borrar.** La compactación reescribe el historial de forma densa preservando reglas, decisiones tomadas y escaladas. No elimina información crítica; la condensa.

## Conceptos clave

| Concepto | Definición |
|---|---|
| Curva en U | Distribución de atención alta en bordes, baja en el centro |
| Lost in the middle | Degradación silenciosa cuando el contenido crítico queda en el valle |
| Edge placement | Reglas críticas al inicio + reminder al final |
| usage_fraction | Tokens usados / límite de ventana de contexto |
| Compactación | Reescritura densa que preserva reglas, decisiones y escaladas |

## Quality Signals

| Signal | Target |
|---|---|
| Edge placement | Las reglas críticas aparecen al inicio Y al final del prompt |
| Umbral explícito | Existe un gate de compactación en el rango 50-60% |
| Preservación | La compactación conserva reglas, decisiones y escaladas |
| Argumento | El entregable explica la curva U, la regla bordes/centro y el umbral |

## Anti-patrón canónico

```python
system_prompt = f"You are an assistant.\n{big_blob_of_context}\nIMPORTANT: never expose PII.\n...3000 more tokens..."
```

La regla crítica ("never expose PII") queda enterrada en el valle de la U, sin reminder en el borde final. El agente puede respetarla al turno 5 y violarla al turno 30: la pérdida es silenciosa, no genera logs ni errores.

## Open Knowledge

- El umbral exacto (0.55) puede afinarse según modelo y tamaño de ventana; el principio (compactar antes de que las reglas se diluyan) es estable.
