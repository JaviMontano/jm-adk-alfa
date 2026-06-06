---
name: katas-session-resume-fork
version: 1.0.0
description: "Gestion de sesiones: resume vs fork vs fresh con summary tipado; detectar cuando los tool results estan stale."
owner: "JM Labs"
triggers:
  - session resume
  - session fork
  - fresh summary session
  - stale tool results
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Kata 25 · Gestión de Sesiones (Resume y Fork)

## Qué es

Tres patrones de preservación de contexto entre invocaciones del agente, y el criterio para elegir entre ellos:

- `--resume` continúa una sesión nombrada: el contexto previo sigue siendo válido y la conversación avanza lógicamente.
- `fork` crea ramas paralelas desde una baseline común: dos caminos independientes, cero interferencia entre ramas.
- Sesión nueva con summary tipado inyectado en el system prompt: preferible cuando los tool results previos pueden estar stale, porque el mundo cambió desde la última sesión.

El scratchpad estructurado (Kata 18) es la fuente natural del summary que se inyecta en la sesión fresh.

## Por qué importa (falla que evita)

Resumir una sesión vieja cuyos tool results están stale lleva al modelo a referenciar archivos que ya no son lo que cree que son: recuerda el código como estaba antes de un refactor masivo y alucina sobre estado obsoleto. Los forks sin disciplina se mezclan asumiendo contexto compatible cuando no lo es. Inyectar transcripts completos viejos infla el contexto y reintroduce ruido ya resuelto. El costo es trabajo basado en una realidad que ya no existe.

## Modelo mental

- **Resume = contexto válido.** La conversación sigue lógicamente; nada del mundo cambió bajo los pies del modelo. Misma investigación, mismos archivos.
- **Fork = dos caminos desde la misma baseline.** Cada rama es independiente y nombrada; cero interferencia entre ellas. Sirve para explorar enfoques alternativos en paralelo.
- **Summary fresh = el mundo cambió.** Arranca limpio con un summary tipado en el system prompt, no con el transcript completo. Recarga las fuentes actualizadas.
- **Scratchpad estructurado (Kata 18) es la fuente del summary.** No se pega la conversación entera: se inyecta el resumen curado de hallazgos.
- **Señal de stale:** si hubo refactor, migración o edición masiva entre sesiones, los tool results previos están stale y resume es la elección incorrecta.

## Activos determinísticos

Usa `assets/manifest.json` como indice de contratos offline. Los assets fijan la matriz de decision `resume|fork|fresh`, senales de staleness, aislamiento de forks, summary tipado y contrato JSON de salida. Si produces un reporte JSON de la kata, validalo con `bash skills/katas-session-resume-fork/scripts/check.sh` antes de marcarlo como aceptado.

## Patrón correcto

```bash
# Misma investigación, contexto válido → resume
claude --resume codebase-audit-2025-04

# Dos enfoques en paralelo desde una baseline → fork a sesiones nombradas
claude --fork codebase-audit-2025-04 --new-name approach-A
claude --fork codebase-audit-2025-04 --new-name approach-B

# El mundo cambió → sesión fresh con summary tipado del scratchpad
SUMMARY=$(cat investigation-scratchpad.md)
claude -p "Continuamos. Hallazgos previos:\n$SUMMARY"
```

## Anti-patrón

```bash
# ANTI: resume después de un refactor masivo
# el modelo recuerda los archivos como eran y alucina sobre estado obsoleto
claude --resume codebase-audit-2025-04   # tras reescribir media base de código

# ANTI: inyectar el transcript completo viejo
# infla contexto y reintroduce ruido ya resuelto
SUMMARY=$(cat full-old-transcript.log)   # 40k tokens de conversación cruda
claude -p "Continuamos. Conversación previa:\n$SUMMARY"
```

## Argumento de certificación

- Decide entre resume, fork y fresh con criterio explícito, no por inercia.
- Identifica cuándo los tool results previos están stale (refactor, migración, edición masiva).
- Conecta el patrón con el scratchpad estructurado (Kata 18) como fuente del summary tipado.
- Rechaza pegar transcripts completos viejos; defiende el summary curado en su lugar.
- Valida reportes JSON con `scripts/check.sh` contra los contratos en `assets/`.

## Cuándo activar

Activa cuando el usuario pregunte por continuar una sesión previa, ramificar enfoques alternativos, o cuando haya señales de que el estado del proyecto cambió desde la última corrida (refactor, deploy, migración) y haya que decidir cómo reanudar el trabajo sin arrastrar contexto stale.

## Skills relacionadas

- `katas-structured-scratchpad`
- `katas-human-handoff`
- `katas-context-attention-budget`
