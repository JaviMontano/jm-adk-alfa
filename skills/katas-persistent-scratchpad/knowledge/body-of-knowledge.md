<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-persistent-scratchpad
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Persistent Scratchpad Body of Knowledge

## Canon

Kata 18 · Scratchpad Persistente (escenario: Developer Productivity).

Un archivo `investigation-scratchpad.md` externo a la conversación donde el agente vuelca descubrimientos durables: hipótesis confirmadas, decisiones, hallazgos de archivos y pendientes. Sobrevive a `/compact` y a reinicios de sesión.

### Conceptos clave

- **Memoria volátil vs persistente:** la conversación puede compactarse o resetearse; el scratchpad en disco es la fuente de verdad de lo validado.
- **Curaduría, no volcado:** el agente escribe SOLO conclusiones validadas. No persiste monólogo interno, hipótesis sin confirmar ni dudas pasajeras.
- **Estructura fija:** secciones `## Decisiones`, `## Hallazgos`, `## Pendientes`, con entradas fechadas y trazables a la evidencia que las confirmó.
- **Leer una vez, referenciar después:** al inicio de sesión se lee el scratchpad una sola vez; durante la sesión se anexa y se referencia, sin re-leer cada turno, para preservar el cache de prefijo (Kata 10).
- **Conexiones:** motivado por la compactación (Kata 11); consumido y alimentado por la investigación adaptativa (Kata 19).

## Quality Signals

| Signal | Target |
|---|---|
| Persistencia | Las conclusiones críticas viven en disco, no solo en el historial |
| Curaduría | Solo entran conclusiones validadas; sin monólogo ni hipótesis no confirmadas |
| Estructura | Secciones fijas, entradas fechadas y trazables |
| Cache-friendly | Lectura única al inicio; después referenciar/anexar (Kata 10) |

## Anti-patrón canónico

- Confiar en la conversación como memoria de largo plazo: tras `/compact` el hallazgo desaparece.
- Scratchpad sin estructura o re-leído cada turno, lo que rompe el cache de prefijo.
- Volcar monólogo interno, hipótesis no confirmadas o dudas pasajeras al scratchpad.

## Open Knowledge

- Añadir referencias específicas del proyecto (rutas, convenciones de secciones) a medida que se estabilicen.
