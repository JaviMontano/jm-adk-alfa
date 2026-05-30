<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-session-resume-fork
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 25 · Gestión de Sesiones — Body of Knowledge

## Canon

La preservación de contexto entre invocaciones del agente tiene tres patrones, y elegir mal cuesta trabajo basado en una realidad que ya no existe.

- **Resume (`--resume`).** Continúa una sesión nombrada. Correcto cuando el contexto previo sigue siendo válido y la conversación avanza lógicamente: misma investigación, mismos archivos, nada cambió bajo los pies del modelo.
- **Fork (`fork`).** Crea ramas paralelas desde una baseline común. Cada rama es independiente y nombrada; cero interferencia entre ellas. Correcto para explorar enfoques alternativos en paralelo (approach-A vs approach-B).
- **Fresh con summary tipado.** Arranca una sesión nueva e inyecta en el system prompt un summary curado, no el transcript completo. Correcto cuando el mundo cambió desde la última sesión y los tool results previos están stale. Recarga las fuentes actualizadas.

El **scratchpad estructurado (Kata 18)** es la fuente natural del summary tipado. El transcript crudo no lo es: compite por atención (Kata 11) y degrada el caché de prefijo (Kata 10).

## Conceptos clave

- **Stale tool results.** Cuando hubo refactor, migración, deploy o edición masiva entre sesiones, los resultados de herramientas previos describen un estado que ya no existe. Resume sobre ellos induce alucinación.
- **Baseline.** El punto común desde el que un fork deriva ramas. Forks sin disciplina asumen contexto compatible y se mezclan.
- **Summary tipado.** Estructura estable (objetivo, hallazgos, decisiones, estado de archivos, próximos pasos) que el modelo parsea sin ruido.

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Criterio de decisión | Resume / fork / fresh se elige con justificación explícita, no por inercia |
| Detección de staleness | Se identifica refactor/migración/deploy que invalida tool results previos |
| Fuente del summary | El summary proviene del scratchpad estructurado, tipado y curado |
| Rechazo de transcript | No se inyecta el transcript completo viejo |

## Anti-patrón canónico

- Hacer `--resume` después de un refactor masivo: el modelo recuerda los archivos como eran y alucina sobre estado obsoleto.
- Inyectar el transcript completo viejo en una sesión fresh: infla contexto y reintroduce ruido ya resuelto.
