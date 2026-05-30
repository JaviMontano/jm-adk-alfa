---
name: few-shot-engineering
version: 1.0.0
description: "Disenar few-shot que calibra bordes subjetivos con 2-4 ejemplos del mismo schema, al inicio para preservar prefix cache."
owner: "JM Labs"
triggers:
  - few-shot engineering
  - edge calibration examples
  - fewshot design
  - subjective calibration
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Few Shot Engineering

## Capacidad

Diseñar few-shot que calibra **bordes subjetivos** de una tarea: en lugar de describir el criterio en prosa abstracta, se muestran 2–4 ejemplos del **mismo schema de salida** que cubren los casos límite (no el centro de la distribución). Los ejemplos van **al inicio del prompt** (zona estática, cache-friendly) para que el prefijo se mantenga estable y el prefix cache no se invalide entre llamadas. El few-shot no reemplaza al schema: lo **complementa** mostrando cómo se resuelven las decisiones que el schema deja ambiguas.

## Cuándo usarla

- La tarea tiene un criterio de juicio difícil de verbalizar (qué cuenta como "spam", "urgente", "fuera de alcance").
- El modelo acierta en el caso típico pero falla en los bordes.
- Hay un schema de salida estable (JSON, clasificación, etiquetado) y se quiere fijar el comportamiento en zonas grises.
- Se quiere reducir varianza sin reentrenar ni escribir reglas frágiles.

No usarla cuando: la regla es expresable de forma cerrada (entonces escribe la regla), o cuando el problema es de conocimiento factual (entonces usa contexto/RAG, no ejemplos).

## Cómo construir

1. **Identifica los bordes.** Recoge casos reales donde el modelo dudó o falló. Esos son los candidatos a ejemplo, no los casos obvios.
2. **Fija el schema de salida.** El ejemplo debe usar exactamente el mismo formato que esperas en producción (mismas claves, mismos tipos). El few-shot enseña forma y juicio a la vez.
3. **Selecciona 2–4 ejemplos.** Cada uno debe ilustrar una decisión de borde distinta. Más de 5 dispersa la atención del modelo y, si los rotas, rompe el cache.
4. **Colócalos al inicio**, antes de la entrada variable del usuario, en la zona estática del prompt.
5. **Verifica complementariedad.** Ningún ejemplo debe contradecir el schema ni a otro ejemplo. Si dos ejemplos sugieren reglas opuestas, el modelo queda peor que sin ellos.
6. **Valida contra un set de bordes** (no el set típico) y mide si la decisión gris mejoró.

## Patrón correcto

```python
# GOOD: 2–4 ejemplos del MISMO schema, bordes, al inicio (estático, cacheable)
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
    # La entrada variable va DESPUÉS del bloque estático -> prefix cache intacto
    return call_model(system=SYSTEM_PROMPT, user=ticket)
```

## Anti-patrón

```python
# ANTI: criterio en prosa abstracta + demasiados ejemplos rotados al final
SYSTEM_PROMPT = """Clasifica el ticket usando tu buen juicio sobre la
urgencia y la categoría más apropiada según el contexto general..."""  # vago

def classify(ticket: str, examples: list) -> dict:
    # 8 ejemplos rotados aleatoriamente y puestos DESPUÉS del input:
    # rompe el prefix cache en cada llamada y dispersa la atención
    shots = random.sample(examples, 8)
    return call_model(user=ticket + "\n".join(format(s) for s in shots))
```

## Checklist de validación

- ¿Los ejemplos usan exactamente el **schema de salida** de producción?
- ¿Cubren **bordes**, no el centro de la distribución?
- ¿Son **2–4** (ni 1, ni más de 5)?
- ¿Están **al inicio**, en la zona estática del prompt?
- ¿**Complementan** el schema sin contradecirlo ni contradecirse entre sí?
- ¿Se validó la mejora contra un set de **casos límite**, no típicos?

## Katas y skills relacionadas

- Kata 14 · `katas-fewshot-edge-calibration`
- Relacionadas: `self-correction-loops`, `evaluation-confidence-design`, `validation-retry-design`
