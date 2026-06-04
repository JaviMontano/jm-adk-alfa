# Adaptive Investigation Method

Capacidad de ingenieria para construir agentes que investigan dominios desconocidos con **mapeo barato, budget de exploracion acotado y re-plan disciplinado** (solo al invalidar una hipotesis). Evita los dos fallos clasicos: el plan rigido upfront que no se adapta y el `read_all_files()` que quema el contexto.

## Resumen ejecutivo

El patron construible es un loop con scratchpad tipado (`plan` / `hypotheses` / `findings`), un contador de budget que se decrementa por cada lectura cara, y una regla de re-plan que solo dispara ante `hypothesis_invalidated`. El resultado es una investigacion acotada, trazable y terminable.

## Triggers

- adaptive investigation method
- dynamic decomposition
- exploration budget
- disciplined replan

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Invoca esta skill cuando el agente deba entender un repositorio o corpus grande antes de actuar, leerlo todo sea inviable, y el costo de exploracion deba estar acotado por diseno. Define primero el budget, mapea barato con `Glob`/`Grep`, prioriza hipotesis y haz deep-dive selectivo con `Read`.

## Output Format

Markdown con: objetivo, budget consumido, mapa de superficie, hipotesis priorizadas, findings con referencia a nodo, decisiones de re-plan y deliverable final.
