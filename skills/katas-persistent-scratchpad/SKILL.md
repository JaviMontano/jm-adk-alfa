---
name: katas-persistent-scratchpad
version: 1.0.0
description: "Scratchpad persistente en disco curado por el agente; sobrevive a compact y reinicios, leido una vez y referenciado despues."
owner: "JM Labs"
triggers:
  - persistent scratchpad
  - investigation scratchpad
  - durable memory
  - scratchpad file
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Persistent Scratchpad

## Qué es

Un archivo externo a la conversación (`investigation-scratchpad.md`) donde el agente vuelca descubrimientos durables: hipótesis confirmadas, decisiones, hallazgos de archivos y pendientes. Sobrevive a `/compact` y a reinicios de sesión. Es memoria persistente en disco, curada por el propio agente, no un volcado del historial conversacional.

## Por qué importa (falla que evita)

Cuando el contexto se compacta (Kata 11 · compactación), se pierde detalle. Si un descubrimiento crítico vivía solo en el historial conversacional, desaparece sin dejar rastro. El scratchpad es la red de seguridad: memoria persistente curada por el agente que sobrevive a cualquier compactación o reset de sesión, de modo que las conclusiones validadas nunca dependen de la ventana de contexto.

## Modelo mental

- Conversación = memoria volátil: puede compactarse o resetearse en cualquier momento.
- Scratchpad = memoria persistente en disco: la fuente de verdad de lo que el agente ya validó.
- El agente escribe SOLO conclusiones validadas: hipótesis confirmadas, decisiones, hallazgos, pendientes. No vuelca monólogo interno, hipótesis sin confirmar ni dudas pasajeras.
- Estructura fija por secciones (`## Decisiones`, `## Hallazgos`, `## Pendientes`) para que sea anexable y legible.
- Al inicio de cada sesión el agente lee el scratchpad UNA vez; después referencia y anexa, no re-lee cada turno (preserva el prefijo de cache, Kata 10).

## Patrón correcto

```markdown
# Investigation Scratchpad
## Decisiones
- 2026-04-25: usar pydantic v2 (T-19 confirmó compat).
## Hallazgos
- src/legacy/parser.py bug offset línea 142 (replicado).
## Pendientes
- Verificar si --strict rompe tests integration
```

```python
def append_scratchpad(section, entry):
    """Anexa una conclusión validada a la sección indicada del scratchpad."""
    path = "investigation-scratchpad.md"
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(f"\n## {section}\n- {entry}\n")
```

## Anti-patrón

- Confiar en la conversación como memoria de largo plazo: tras `/compact` el hallazgo desaparece.
- Scratchpad sin estructura, o re-leído cada turno: rompe el cache de prefijo (Kata 10) y ensucia la señal.
- Volcar monólogo interno, hipótesis no confirmadas o dudas pasajeras al scratchpad: contamina la memoria persistente con ruido no validado.

## Argumento de certificación

- Describir la diferencia entre memoria conversacional (volátil) y persistente (scratchpad en disco).
- Enunciar qué se escribe (hipótesis confirmadas, decisiones, hallazgos, pendientes) y qué NO (monólogo, hipótesis sin confirmar, dudas pasajeras).
- Conectar con Kata 11 (compactación, que motiva la persistencia) y Kata 19 (investigación adaptativa, que consume y alimenta el scratchpad).

## Cuándo activar

- Una investigación larga o multisesión donde el detalle no puede perderse al compactar.
- El usuario pide persistir hallazgos, retomar una investigación, o mantener memoria durable entre reinicios.
- Triggers: `persistent scratchpad`, `investigation scratchpad`, `durable memory`, `scratchpad file`.

## Skills relacionadas

- `katas-compaction-boundary`
- `katas-adaptive-investigation`
- `katas-cache-aware-context`
