<!--
generated-by: scripts/scaffold-skill.py
generated-for: few-shot-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Resumen

Se calibran 3 bordes con ejemplos del schema exacto, colocados al inicio del system prompt (zona estática) para no invalidar el prefix cache.

## Bordes calibrados

1. Billing aunque el cliente diga que ya no la necesita (sigue siendo categoría billing, prioridad baja).
2. Spam con lenguaje de urgencia falsa (urgencia textual no implica `high`).
3. Fallo intermitente (un 500 ocasional es `technical` + `high`, no `low`).

## Patrón correcto (GOOD)

```python
SYSTEM_PROMPT = """Clasifica tickets de soporte. Devuelve JSON:
{"category": "billing|technical|spam", "priority": "low|high"}

Ejemplos (casos de borde):

Input: "No me llegó la factura pero tampoco la necesito ya"
Output: {"category": "billing", "priority": "low"}

Input: "URGENTE!!! gané un premio click aquí http://..."
Output: {"category": "spam", "priority": "low"}

Input: "El servidor responde 500 a veces, no siempre"
Output: {"category": "technical", "priority": "high"}
"""

def classify(ticket: str) -> dict:
    return call_model(system=SYSTEM_PROMPT, user=ticket)  # input variable al final
```

## Anti-patrón (ANTI)

```python
# Prosa abstracta + 8 ejemplos rotados DESPUÉS del input:
# rompe el prefix cache en cada llamada y dispersa la atención
SYSTEM_PROMPT = "Clasifica usando tu buen juicio sobre urgencia y categoría..."
def classify(ticket, examples):
    shots = random.sample(examples, 8)
    return call_model(user=ticket + "\n".join(map(format, shots)))
```

## Validación (checklist)

- [x] Ejemplos = schema de salida de producción
- [x] Cubren bordes, no el centro
- [x] 3 ejemplos (entre 2 y 4)
- [x] Colocados al inicio (zona estática)
- [x] Complementan el schema sin contradecirse
- [x] Validados contra un set de casos límite

## Riesgos y límites

- Si aparecen nuevos bordes, sustituir un ejemplo en vez de añadir un quinto.
- No usar few-shot para criterios expresables como regla cerrada.
