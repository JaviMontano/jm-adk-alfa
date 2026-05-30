---
name: adaptive-investigation-method
version: 1.0.0
description: "Investigar dominios desconocidos con mapeo barato, budget acotado y re-plan disciplinado solo al invalidar la hipotesis."
owner: "JM Labs"
triggers:
  - adaptive investigation method
  - dynamic decomposition
  - exploration budget
  - disciplined replan
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Adaptive Investigation Method

## Capacidad

Construir agentes que investigan dominios desconocidos (codebases, datasets, documentos) sin quemar el budget de contexto. La capacidad combina tres movimientos de ingenieria: mapeo barato de la superficie del problema, priorizacion explicita de donde invertir, y deep-dive selectivo solo en los nodos prometedores. El re-plan no es reflejo de cada turno; se dispara unicamente cuando una hipotesis queda invalidada por evidencia. Un budget duro (numero de lecturas o tokens) actua como cota de seguridad para que la investigacion termine aunque el dominio sea infinito.

El artefacto construible es un loop de investigacion con: (1) un scratchpad persistido que separa `plan`, `hypotheses` y `findings`; (2) un contador de budget que se decrementa por cada lectura cara; (3) una regla de re-plan tipada que solo se ejecuta ante `hypothesis_invalidated`.

## Cuando usarla

- Un agente debe entender un repositorio o corpus grande antes de actuar y leerlo todo es inviable.
- El costo de exploracion debe estar acotado por diseno (latencia, tokens, llamadas a herramientas).
- Quieres evitar que el agente re-planifique en cada turno y entre en loops de duda.
- Necesitas trazabilidad: por que se exploro un area y por que se descarto otra.

NO la uses cuando el dominio es pequeno y leerlo entero es mas barato que mapearlo, ni cuando la tarea es determinista y no requiere descubrimiento.

## Como construir

1. **Define el budget duro.** Fija una cota explicita antes de empezar: `budget = N` lecturas caras o tokens. Persiste el contador en el scratchpad. Sin esto, el loop no tiene condicion de paro.
2. **Mapea barato.** Usa `Glob` y `Grep` (no lecturas completas) para construir un mapa de la superficie: estructura de carpetas, nombres, entrypoints. Cada item del mapa es candidato a deep-dive, no contenido leido.
3. **Formula hipotesis priorizadas.** Escribe en el scratchpad una lista de hipotesis ordenadas por valor esperado / costo. Cada hipotesis apunta a los nodos del mapa que la confirmarian o invalidarian.
4. **Deep-dive selectivo.** Lee en detalle solo los nodos top-ranked. Cada `Read` decrementa el budget. Registra `findings` con referencia al nodo.
5. **Re-plan disciplinado.** Tras cada deep-dive evalua: si la evidencia invalida la hipotesis activa, re-prioriza la lista. Si solo la confirma o la deja intacta, continua con el siguiente nodo sin re-planificar.
6. **Cierra al agotar budget o resolver el objetivo.** Emite el deliverable desde `findings`, no desde memoria de trabajo difusa.

## Patron correcto

```python
# GOOD: cheap map -> ranked hypotheses -> selective deep-dive -> disciplined replan
def adaptive_investigate(goal, budget=8):
    scratch = {"plan": [], "hypotheses": rank(initial_hypotheses(goal)), "findings": []}
    surface = cheap_map()  # glob/grep only, no full reads
    while budget > 0 and not goal_resolved(scratch):
        hyp = scratch["hypotheses"][0]
        node = pick_node(surface, hyp)
        evidence = deep_dive(node)   # one expensive Read
        budget -= 1
        scratch["findings"].append({"node": node, "evidence": evidence})
        if invalidates(evidence, hyp):
            scratch["hypotheses"] = rank(reprioritize(scratch["hypotheses"], evidence))
        # else: keep going, do NOT replan reflexively
        persist(scratch)
    return synthesize(scratch["findings"])
```

## Anti-patron

```python
# ANTI: rigid upfront plan, read everything, reflexive replan every turn
def naive_investigate(goal):
    plan = make_full_plan_upfront(goal)   # rigid, no adaptation
    data = read_all_files()               # blows the context budget
    for step in plan:
        plan = make_full_plan_upfront(goal)  # reflexive replan each turn -> loop of doubt
        act(step, data)
    return summarize(data)
```

## Checklist de validacion

- ¿Existe un budget de exploracion duro y un contador que se decrementa por lectura cara?
- ¿El mapeo inicial es barato (`Glob`/`Grep`), sin lecturas completas?
- ¿Las hipotesis estan priorizadas por valor/costo antes del deep-dive?
- ¿El criterio de re-plan es explicito y solo se dispara ante hipotesis invalidada?
- ¿El plan y los findings se persisten en un scratchpad tipado (no en prosa difusa)?
- ¿Hay condicion de paro garantizada (budget agotado u objetivo resuelto)?

## Katas y skills relacionadas

- Kata 19 (investigacion adaptativa con budget).
- Skill relacionada: `katas-adaptive-investigation`.
- Complementarias: `provenance-engineering` para trazar cada finding a su fuente, `session-lifecycle-management` para decidir fork vs fresh cuando el mundo cambia.
