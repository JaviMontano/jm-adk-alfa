<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-context-dilution-mitigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

La regla "never expose PII" estaba enterrada en el centro del prompt (el valle de la curva en U), entre el blob de contexto y los 3000 tokens de FAQ. Por eso se diluía en conversaciones largas: violación silenciosa, sin error ni log. Se mueve la regla a ambos bordes y se añade un gate de compactación.

## Evidence

- La curva de atención del transformer tiene forma de U: bordes con atención alta, centro diluido ("lost in the middle").
- La regla crítica estaba en el centro, justo la zona de menor atención.

## Result

GOOD (patrón aplicado):

```python
SYSTEM:<rules>never expose customer PII</rules>
{big_blob_of_context}
{FAQ and tone guidance}
USER:question
REMINDER:<rules>never expose customer PII</rules>

if usage_fraction(history) > 0.55:
    history = compact(history, preserve=['rules', 'decisions', 'escalations'])
```

ANTI (lo que había):

```python
system_prompt = f"You are a support assistant.\n{big_blob_of_context}\nIMPORTANT: never expose customer PII.\n...3000 more tokens..."
```

## Validation

- [x] Regla crítica al inicio como `<rules>`.
- [x] Misma regla repetida al final como `REMINDER`.
- [x] Datos ricos (blob, FAQ) ubicados en el centro.
- [x] Gate de compactación con umbral 0.55.
- [x] Compactación preserva reglas, decisiones y escaladas.

## Risks and Limits

- El umbral 0.55 puede afinarse según el modelo y su ventana de contexto.
- Si una decisión crítica vive solo en el historial conversacional, considera `katas-persistent-scratchpad` para que sobreviva a `/compact`.
