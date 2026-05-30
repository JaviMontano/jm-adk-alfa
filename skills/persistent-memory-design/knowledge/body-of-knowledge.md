<!--
generated-by: scripts/scaffold-skill.py
generated-for: persistent-memory-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Persistent Memory Design Body of Knowledge

## Canon

El scratchpad persistente es la memoria duradera del agente: un archivo en disco, no la conversación. Su razón de ser es que la ventana de contexto es volátil y se compacta; un `/compact` o un reset borran la memoria de trabajo, pero el archivo permanece. La capacidad consiste en mover toda conclusión que merezca sobrevivir desde la conversación hacia un archivo estructurado y auditado.

Conceptos clave:

- **Memoria volátil vs persistente.** La conversación es scratchpad efímero; el archivo es scratchpad persistente. El estado de verdad vive en el archivo.
- **Esquema fijo.** Secciones invariantes — `Hypotheses`, `Decisions`, `Findings`, `Open` (Hipótesis / Decisiones / Hallazgos / Pendientes). El esquema no cambia; el contenido sí.
- **Conclusiones validadas únicamente.** Solo entra lo confirmado, con su evidencia mínima (source + fecha). El razonamiento en bruto y los tool dumps no entran.
- **Lectura única + referencia.** Se lee una vez al arranque hacia el contexto; después se referencia. Releer cada turno invalida el prompt cache y desperdicia tokens.
- **Supervivencia verificable.** El criterio de aceptación es reconstruir el estado solo desde el archivo tras `/compact` o reset, sin la conversación previa.

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Solo conclusiones validadas | Sin razonamiento crudo ni tool dumps sin confirmar |
| Esquema fijo de secciones | Hipótesis / Decisiones / Hallazgos / Pendientes presentes y estables |
| Lectura única | El archivo se lee una vez por sesión; después se referencia |
| Supervivencia a compact/reset | Estado reconstruible solo desde el archivo |
| Evidencia por hallazgo | Cada entrada lleva source y fecha visibles |

## Decisión de diseño

- ¿Esta conclusión debe sobrevivir a un compact? Si sí → va al archivo, tipada y con evidencia. Si no → queda en la conversación.
- ¿Es una conclusión validada o razonamiento intermedio? Solo lo validado entra.
- ¿Necesito releer el archivo o basta referenciar lo ya cargado? Por defecto, referenciar.
- ¿La sección correcta es Hipótesis (no confirmada), Decisión (compromiso tomado), Hallazgo (hecho validado) o Pendiente (trabajo abierto)?

## Anti-patrón

Memoria que vive en la conversación; scratchpad sin estructura; archivo releído cada turno (rompe el cache); reescritura completa del archivo en cada paso; volcar tool results crudos como si fueran conclusiones. Resultado típico: tras `/compact` el agente "olvida" y re-deriva todo, duplicando trabajo.
