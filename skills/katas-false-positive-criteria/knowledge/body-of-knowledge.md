<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-false-positive-criteria
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas False Positive Criteria Body of Knowledge

## Canon

Kata 30 · Criterios Explícitos para Reducir Falsos Positivos. Escenarios: Customer Support, CI/CD, Structured Extraction. Clave de quiz oficial: B·C·B.

### Conceptos

- **Vaguedad no es conservadurismo.** "Sé conservador" y "solo alta confianza" no tienen umbral estable; el modelo los interpreta distinto cada turno y la clasificación se vuelve irreproducible.
- **Criterios categóricos.** Cada criterio se nombra (`categoria.subtipo`), se define operacionalmente ("reporta solo cuando el comentario claim X pero el código hace Y") y trae un ejemplo positivo (qué SÍ dispara) y uno negativo (qué NO dispara).
- **Severidad declarada.** `error` (rompe runtime) vs `warning` (degrada un edge case), no un campo libre.
- **Lista de exclusión explícita.** Se enumera lo que NO se reporta: estilo, patterns "que podrían ser problemáticos".
- **FP rate por categoría.** La métrica útil es la precisión por categoría, no la agregada; el agregado oculta la categoría tóxica.
- **Disable temporal.** Si una categoría arrastra falsos positivos, se deshabilita mientras se afina, preservando la confianza global.
- **"confidence" no es filtro.** El modelo está mal calibrado; un score autoinformado no separa señal de ruido de forma fiable.

### Señales de calidad

| Señal | Objetivo |
|---|---|
| Criterios operacionales | Cada criterio tiene definición sin adjetivos + ejemplo positivo y negativo |
| Severidad tipada | error / warning, no texto libre |
| Métrica por categoría | FP rate medido por categoría, nunca solo agregado |
| Confianza cross-categoría | Política de disable temporal para categorías ruidosas |
| Exclusiones explícitas | Lista de lo que NO se reporta presente |

## Anti-patrón canónico

```text
SYSTEM_VAGUE = "Eres reviewer. Reporta findings de alta confianza. Sé conservador con los flags."
```

Interpretado distinto cada turno. Resultado documentado: si el reviewer marca "potential security issue" en código seguro 1 de cada 5 veces, los devs ignoran TODOS los flags de seguridad, incluso los reales. La precisión es prerrequisito de la utilidad y la confianza es cross-categoría.

## Skills relacionadas

`katas-provenance-preservation`, `katas-multipass-prompt-chaining`, `katas-context-dilution-mitigation`, `katas-prefix-caching`.
