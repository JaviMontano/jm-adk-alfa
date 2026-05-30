<!--
generated-by: scripts/scaffold-skill.py
generated-for: adaptive-investigation-method
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Adaptive Investigation Method Body of Knowledge

## Canon de la capacidad

La investigacion adaptativa es un patron de ingenieria para explorar dominios desconocidos sin quemar el budget de contexto. Se apoya en tres movimientos encadenados:

1. **Mapeo barato.** Construir una vista de la superficie del problema usando operaciones de bajo costo (`Glob` para estructura, `Grep` para senales) en lugar de leer contenido completo. El mapa es una lista de candidatos, no de hechos.
2. **Priorizacion explicita.** Formular hipotesis y ordenarlas por valor esperado / costo. El orden determina donde se invierte el budget escaso.
3. **Deep-dive selectivo + re-plan disciplinado.** Profundizar solo en los nodos top-ranked. Re-priorizar unicamente cuando la evidencia **invalida** una hipotesis, no en cada turno.

El estado vive en un scratchpad tipado con tres campos: `plan`, `hypotheses`, `findings`. Un contador de `budget` (entero) acota el numero de lecturas caras y garantiza terminacion.

## Conceptos clave

- **Budget duro:** cota explicita de lecturas/tokens fijada antes de empezar; sin ella el loop no termina.
- **Mapa de superficie:** estructura barata que enumera candidatos a deep-dive.
- **Hipotesis priorizada:** afirmacion falseable con un nodo asociado que la confirma o invalida.
- **Re-plan tipado:** transicion `hypothesis_invalidated -> reprioritize`, nunca reflejo.
- **Scratchpad persistido:** memoria estructurada que sobrevive a forks y evita razonar desde prosa difusa.

## Senales de calidad

| Senal | Objetivo |
|---|---|
| Budget acotado | Existe cota dura y contador que decrementa por lectura cara |
| Mapeo barato | Exploracion inicial sin lecturas completas (`Glob`/`Grep`) |
| Priorizacion | Hipotesis ordenadas por valor/costo antes del deep-dive |
| Re-plan disciplinado | Re-plan solo ante hipotesis invalidada |
| Persistencia tipada | `plan` y `findings` en scratchpad, no en prosa |
| Terminacion | Condicion de paro garantizada (budget agotado u objetivo resuelto) |

## Decision de diseno

El re-plan reflejo cada turno parece prudente pero produce loops de duda y desperdicia budget re-evaluando lo ya decidido. La regla correcta es: avanza con la hipotesis activa mientras la evidencia la confirme o la deje intacta; re-prioriza solo cuando la invalide. Esto convierte el re-plan en un evento raro y trazable.

## Anti-patron

Plan rigido upfront que no se adapta + `read_all_files()` que quema el contexto + re-plan reflejo en cada turno. Los tres combinados producen un agente caro, lento y que no converge.
