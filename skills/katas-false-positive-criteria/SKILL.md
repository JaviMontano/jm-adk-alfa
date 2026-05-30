---
name: katas-false-positive-criteria
version: 1.0.0
description: "Criterios categoricos con ejemplos positivos y negativos por severidad para reducir falsos positivos; disable temporal por categoria."
owner: "JM Labs"
triggers:
  - false positive criteria
  - categorical criteria
  - fp rate by category
  - explicit criteria
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas False Positive Criteria

Kata 30 · Criterios Explícitos para Reducir Falsos Positivos. Escenarios canónicos: Customer Support, CI/CD, Structured Extraction.

## Qué es

Las instrucciones vagas ("be conservative", "only high-confidence", "reporta findings de alta confianza") fallan porque el modelo las interpreta de forma distinta en cada turno: no hay un umbral estable detrás de esas palabras. La alternativa que funciona son criterios categóricos con ejemplos positivos y negativos por nivel de severidad, que producen clasificación consistente turno tras turno. Un punto clave del kata: un alto FP rate en UNA sola categoría destruye la confianza en TODAS las categorías, por lo que conviene deshabilitar temporalmente la categoría problemática mientras se afina, en vez de tolerar ruido.

## Por qué importa (falla que evita)

Si el reviewer reporta "potential security issue" sobre código seguro 1 de cada 5 veces, los desarrolladores terminan ignorando TODOS los flags de seguridad, incluso los reales. La precisión es prerrequisito de la utilidad: un clasificador ruidoso no es un clasificador débil, es un clasificador inservible, porque la confianza es cross-categoría y se erosiona globalmente con cualquier categoría ruidosa.

## Modelo mental

- "confidence" como filtro no funciona: el modelo está mal calibrado y un mismo caso recibe scores distintos.
- Criterios categóricos en vez de adjetivos: "reporta solo cuando el comentario claim X pero el código hace Y", no "reporta inconsistencias".
- Severidad declarada con ejemplos de código positivo y negativo por cada criterio (qué SÍ dispara, qué NO).
- Se mide FP rate POR CATEGORÍA, nunca el agregado: el agregado esconde la categoría tóxica.
- Si una categoría arrastra FPs, se deshabilita temporalmente mientras se afina; así se preserva la confianza global cross-categoría.

## Patrón correcto

```text
SYSTEM_EXPLICIT = """
Reporta findings SOLO si cumplen UNO de estos criterios:
- security.hardcoded_secret: literal API key en código.
    Positivo: OPENAI_KEY='sk-abc...'
    Negativo: OPENAI_KEY=os.environ['OPENAI_KEY']
- bug.null_deref: dereferencia un value sin chequeo cuando puede ser None.
NO reportes: estilo, patterns 'que podrían ser problemáticos'.
Severidad: error (rompe runtime), warning (degrada edge case).
"""
```

## Anti-patrón

```text
SYSTEM_VAGUE = "Eres reviewer. Reporta findings de alta confianza. Sé conservador con los flags."
# interpretado distinto cada turno: 'conservador' y 'alta confianza' no tienen umbral estable.
```

## Argumento de certificación

- Reescribir prompts vagos en criterios categóricos con ejemplos positivos y negativos por severidad.
- Medir FP rate POR CATEGORÍA, no agregada.
- Usar disable temporal de categorías problemáticas para preservar la confianza cross-categoría.
- Argumentar por qué "confidence" como filtro no funciona (modelo mal calibrado).

## Cuándo activar

- Reescribir un prompt de clasificación/review que usa lenguaje vago de confianza.
- Diagnosticar por qué los devs ignoran los flags de un reviewer automático.
- Diseñar criterios de severidad con ejemplos para extracción estructurada o pipelines CI/CD.
- Decidir qué hacer con una categoría que dispara demasiados falsos positivos.

## Skills relacionadas

- `katas-provenance-preservation`
- `katas-multipass-prompt-chaining`
- `katas-context-dilution-mitigation`
