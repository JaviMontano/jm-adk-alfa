<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-independent-reviewer-multipass
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Independent Reviewer Multipass Body of Knowledge

## Canon

Kata 27 · Multi-Pass Review e Independent Reviewer (escenarios: Code Gen, CI/CD).

Conceptos clave:

- **Sesgo de generación:** el modelo que generó código retiene el contexto de su razonamiento y tiende a auto-justificarse; es mal revisor de sí mismo.
- **Independent reviewer:** una instancia en sesión limpia, sin la cadena de generación, que ve solo el código resultante y detecta más issues reales.
- **Pass A (per-file):** deep dive por archivo, atención concentrada, salida tipada.
- **Pass B (cross-file):** integración que opera solo sobre los resúmenes del Pass A; detecta interacciones entre módulos y duplicados de findings.
- **Quorum N-de-M:** anti-solución; "consensuar 2 de 3 reviews" suprime issues raros legítimos en lugar de compensar el sesgo de contexto.

## Quality Signals

| Señal | Objetivo |
|---|---|
| Sesión limpia | El reviewer NO comparte sesión con el generador |
| Separación de pases | Pass A per-file y Pass B cross-file claramente distintos |
| Preservación de minoría | Findings reportados por un solo reviewer se conservan, no se descartan |
| Sin quorum | No se filtra señal por mayoría N-de-M |

## Anti-patrón canónico

- Self-review en la misma sesión: `resp_gen` seguido de "Ahora revisa lo que escribiste" (contexto sesgado).
- Quorum 2-de-3 que descarta un finding genuino reportado por un solo reviewer.
- Single-pass sobre 14 archivos que dispersa la atención y diluye los hallazgos.

## Quiz oficial

Respuestas: B · B · B.

- P1: el quorum filtra señal genuina rara; no compensa el contexto sesgado.
- P2: el reviewer independiente trabaja en sesión limpia y solo ve el código resultante.
- P3: Pass A per-file deep dive + Pass B cross-file integration.
