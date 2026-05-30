---
name: persistent-memory-design
version: 1.0.0
description: "Disenar scratchpad persistente en disco con conclusiones validadas que sobrevive a compact, leido una vez y referenciado."
owner: "JM Labs"
triggers:
  - persistent memory design
  - scratchpad file
  - durable agent memory
  - investigation notes
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Persistent Memory Design

## Capacidad

Diseñar e implementar un scratchpad persistente en disco que actúa como memoria duradera de un agente: un archivo estructurado (Hipótesis / Decisiones / Hallazgos / Pendientes) que solo contiene conclusiones validadas, sobrevive a un `/compact` o a un reset de sesión, se lee una sola vez al arrancar y después se referencia en vez de releerse. Es una capacidad de ingeniería de contexto: separa la memoria de trabajo volátil (la conversación) de la memoria persistente auditada (el archivo).

## Cuándo usarla

- Una investigación o tarea larga que no cabe en una sola ventana de contexto y debe sobrevivir a compactaciones.
- Flujos multi-sesión donde mañana hay que retomar sin re-derivar todo.
- Cuando el agente repite trabajo porque "olvida" conclusiones ya validadas.
- Cuando el scratchpad existente se relee cada turno y rompe el prompt cache.

No la uses para apuntes efímeros de un solo turno ni para volcar transcript crudo: eso no es conclusión validada.

## Cómo construir

1. **Define el contrato del archivo.** Elige una ruta estable (p. ej. `.agent/scratchpad.md`) y un esquema fijo de secciones: `## Hypotheses`, `## Decisions`, `## Findings`, `## Open`. El esquema es invariante; el contenido evoluciona.
2. **Filtra qué entra.** Solo conclusiones validadas con su evidencia mínima (source, fecha). Nada de razonamiento en bruto ni resultados de tools sin confirmar.
3. **Escribe en append/update tipado.** Cada hallazgo nuevo se añade o reemplaza su entrada; nunca se reescribe el archivo entero por gusto.
4. **Lee una vez, referencia después.** Al iniciar sesión, lee el scratchpad una sola vez hacia el contexto. En turnos posteriores referencia sus secciones, no vuelvas a leer el archivo (preserva el cache).
5. **Verifica supervivencia.** Confirma que tras `/compact` o reset el agente reconstruye estado solo desde el archivo, sin la conversación previa.

## Patrón correcto

```python
# GOOD: scratchpad estructurado, solo conclusiones validadas, lectura única.
SCRATCHPAD = ".agent/scratchpad.md"

def bootstrap(ctx):
    # Read once at session start; cache the parsed state.
    if ctx.scratchpad_loaded:
        return ctx.memory  # reference, do not re-read
    ctx.memory = parse_sections(read_file(SCRATCHPAD))
    ctx.scratchpad_loaded = True
    return ctx.memory

def record_finding(finding):
    # Append only validated conclusions, each with provenance.
    assert finding.validated and finding.source
    upsert_section(SCRATCHPAD, "Findings",
                   f"- {finding.text} [src:{finding.source} @ {finding.date}]")
```

## Anti-patrón

```python
# ANTI: la "memoria" vive en la conversación y el archivo se relee cada turno.
def step(ctx):
    notes = read_file(".agent/notes.txt")   # re-read every turn -> breaks cache
    ctx.history.append(notes)               # state lives in volatile chat
    notes += "\n" + raw_tool_dump           # unstructured, unvalidated noise
    write_file(".agent/notes.txt", notes)   # full rewrite, no schema
    # After /compact: state is gone, agent re-derives everything.
```

## Checklist de validación

- ¿El archivo contiene solo conclusiones validadas (no razonamiento crudo ni tool dumps)?
- ¿Tiene un esquema de secciones fijo (Hipótesis / Decisiones / Hallazgos / Pendientes)?
- ¿Se lee una sola vez y luego se referencia, sin relectura por turno?
- ¿El estado sobrevive a `/compact` y a un reset de sesión, reconstruible solo desde el archivo?
- ¿Cada hallazgo lleva su evidencia mínima (source, fecha)?

## Katas y skills relacionadas

- Katas: `18`.
- Relacionadas: `katas-persistent-scratchpad`, `adaptive-investigation-method`, `provenance-engineering`, `session-lifecycle-management`.
