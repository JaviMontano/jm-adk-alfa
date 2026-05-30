---
name: katas-fewshot-edge-calibration
version: 1.0.0
description: "Few-shot para calibrar bordes subjetivos con 2-4 ejemplos del mismo schema; complementa, no reemplaza, al schema."
owner: "JM Labs"
triggers:
  - few-shot calibration
  - edge examples
  - fewshot prompting
  - subjective calibration
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Fewshot Edge Calibration

> Kata 14 · "Few-Shot para Calibrar Bordes" · escenario base: Structured Extraction.

## Qué es

Cuando la tarea es subjetiva (tono, formato no estándar, juicio estético), una descripción zero-shot deja al modelo en su default genérico. Entre 2 y 4 ejemplos `input/output` desplazan su distribución hacia el formato deseado más rápido y barato que un párrafo de instrucciones. Few-shot es la forma más eficiente de comunicar ground truth para casos sin definición rígida, y se compone con schema (Kata 5).

## Por qué importa (falla que evita)

Decir "responde en estilo casual chileno" o "clasifica usando criterio profesional" no produce el resultado deseado: el modelo interpreta la prosa abstracta distinto cada vez. Mostrar 3 ejemplos de cómo se ve el output sí lo produce. La prosa vaga genera salidas inconsistentes turno a turno; los ejemplos fijan el ground truth observable.

## Modelo mental

- Los ejemplos son del **mismo schema** que la salida esperada.
- Cubren los **bordes del dominio**, no el caso fácil del centro.
- 2 a 4 suelen bastar; más de 5 dispersa atención (Kata 11) y rompe caches (Kata 10) sin mejorar calidad.
- Few-shot **complementa, no reemplaza**, al schema: el schema impone forma, los ejemplos calibran juicio.
- Si few-shot contradice el schema, **gana el schema** (restricción sintáctica dura): re-escribir los ejemplos para alinearlos.
- Ejemplos al inicio = parte estática del prompt: maximiza prefix cache (Kata 10) y queda en el borde de atención alta (Kata 11).

## Patrón correcto

```python
prompt = (
    "Clasifica el ticket. Ejemplos:\n"
    "ticket:'no me llega la factura desde hace 3 meses' clase:'billing',urgencia:'high'\n"
    "ticket:'tengo una sugerencia para la app' clase:'feedback',urgencia:'low'\n"
    "ticket:'no puedo entrar, token expirado' clase:'auth',urgencia:'high'\n"
    "ahora clasifica:\n"
    "ticket:'{user_text}'"
)
```

Los tres ejemplos cubren bordes distintos (billing/high, feedback/low, auth/high) y van al inicio como bloque estático.

## Anti-patrón

```python
prompt = (
    "Clasifica usando criterio profesional, considerando urgencia, dominio, "
    "impacto, severidad operacional, prioridad SLA y política interna."
)
```

Párrafo abstracto sin ejemplos: el modelo lo interpreta de forma distinta en cada llamada y no converge al formato esperado.

## Argumento de certificación

- Identificar cuándo few-shot supera a instrucciones en prosa.
- Diseñar ejemplos que cubran **bordes** y no el centro del dominio.
- Combinar few-shot con schema (Kata 5) para tareas subjetivas con formato estricto, sin saturar atención.

## Cuándo activar

- Tarea subjetiva: tono, formato no estándar, juicio estético, clasificación con criterio.
- La descripción en prosa no logra el formato deseado de forma consistente.
- Se necesita comunicar ground truth para casos sin definición rígida.

## Skills relacionadas

- `katas-schema-tool-extraction` (Kata 5: el schema impone forma)
- `katas-prefix-caching` (Kata 10: ejemplos estáticos al inicio maximizan cache)
- `katas-context-dilution-mitigation` (Kata 11: bordes de atención alta, no saturar con >5 ejemplos)
