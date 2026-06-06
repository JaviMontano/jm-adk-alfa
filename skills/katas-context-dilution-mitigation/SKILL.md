---
name: katas-context-dilution-mitigation
version: 1.0.0
description: "Mitigacion de dilucion softmax: edge placement de reglas criticas y compactacion al cruzar 50-60 por ciento de contexto."
owner: "JM Labs"
triggers:
  - context dilution
  - lost in the middle
  - edge placement
  - context compaction
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Context Dilution Mitigation

## Qué es

La curva de atención del transformer tiene forma de U: los bordes del prompt (inicio y fin) reciben atención alta, mientras el centro se diluye. Es el fenómeno conocido como "lost in the middle". Esta kata establece dos disciplinas complementarias: colocar las reglas críticas en los bordes del prompt (edge placement) y compactar el historial antes de que las reglas queden sepultadas en el valle de atención (cuando `usage_fraction(history) > 0.55`).

## Por qué importa (falla que evita)

Un agente puede seguir una política al turno 5 y violarla al turno 30 sin haberla olvidado: simplemente dejó de atenderla porque la regla quedó en el medio del contexto. La pérdida es silenciosa: no aparece en logs ni en errores visibles, solo en comportamiento degradado. En dominios de seguridad o compliance, una violación silenciosa de "nunca exponer PII" es indistinguible de un sistema correcto hasta que el daño ya ocurrió.

## Modelo mental

- Bordes del prompt (inicio/fin) = atención alta. Centro = atención baja. Es la curva en U.
- Reglas críticas (seguridad, compliance, invariantes) van al inicio Y se repiten al final como `<reminder>`.
- Los datos ricos y voluminosos van al centro, donde la atención baja importa menos.
- Repetir la misma regla en ambos bordes cubre el riesgo de dilución: las dos son zonas de atención alta.
- Si `usage_fraction(history) > 0.55`, compactar: reescribir denso preservando reglas, decisiones y escaladas. Compactar no es borrar; es condensar conservando lo crítico.
- El umbral 50-60% balancea conservar contexto útil contra evitar que las reglas se hundan en el valle.

## Activos determinísticos

Usa `assets/manifest.json` como indice de contratos offline. Los assets fijan la curva de atencion, edge placement, umbral 50-60%, preservacion de reglas/decisiones/escaladas y contrato JSON de salida. Si produces un reporte JSON de mitigacion, validalo con `bash skills/katas-context-dilution-mitigation/scripts/check.sh` antes de marcarlo como aceptado.

## Patrón correcto

```python
SYSTEM:<rules>critical_policy</rules>
...
USER:question
...
REMINDER:<rules>critical_policy</rules>

if usage_fraction(history) > 0.55:
    history = compact(history, preserve=['rules', 'decisions', 'escalations'])
```

## Anti-patrón

```python
system_prompt = f"You are an assistant.\n{big_blob_of_context}\nIMPORTANT: never expose PII.\n...3000 more tokens..."
# La regla crítica queda enterrada en el valle de la U: alta probabilidad de violación silenciosa.
```

## Argumento de certificación

- Describir la curva en U de atención y el efecto "lost in the middle".
- Enunciar la regla: bordes para reglas críticas, centro para datos.
- Fijar un umbral concreto de compactación (50-60%) y justificar el balance entre conservar contexto y evitar dilución.
- Explicar que compactar preserva reglas, decisiones y escaladas, no las elimina.
- Validar el contrato offline con `scripts/check.sh` cuando el output sea JSON.

## Cuándo activar

- Diseño de system prompts o agentes con políticas de seguridad/compliance que deben sostenerse a lo largo de conversaciones largas.
- Agentes multi-turno donde el historial crece y las reglas iniciales corren riesgo de diluirse.
- Cuando se observa que un agente respeta una política temprano pero la viola en turnos posteriores.
- Diseño de estrategias de compactación de contexto.

## Skills relacionadas

- `katas-multipass-prompt-chaining`
- `katas-persistent-scratchpad`
- `katas-provenance-preservation`
