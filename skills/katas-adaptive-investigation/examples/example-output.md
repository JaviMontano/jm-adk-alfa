<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-adaptive-investigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Patron correcto (GOOD)

```python
topology = scan_repo(globs=['src/**/*.py'])          # Fase 1: mapeo barato
budget = Budget(files=50, queries=20)
plan = prioritize(topology)                           # Fase 2: ['payments/refund.py', 'payments/charge.py', ...]
while plan and budget.remaining():
    target = plan.pop()
    finding = deep_dive(target, budget)               # Fase 3: deep-dive selectivo
    scratchpad.append('Hallazgos', finding)
    if finding.invalidates(plan):                     # re-plan SOLO si invalida
        plan = re_plan(topology, finding)
```

Traza resultante:

- Topologia: `Glob src/**/*.py` -> 38 archivos; `Grep "refund|charge|payment"` -> 6 candidatos.
- Plan priorizado: `refund.py` (menciona el objetivo), luego `charge.py`, luego `gateway.py`.
- Deep-dive: `refund.py` importa `gateway.process()`; hallazgo invalida la hipotesis de que el flujo vivia en `charge.py` -> re-plan promueve `gateway.py`.
- Presupuesto consumido: 7 / 50 archivos, 4 / 20 queries. Cerrado dentro de budget.

## Anti-patron (ANTI)

```python
plan = make_full_plan_upfront(repo)   # plan rigido sin haber mirado la topologia
for task in plan:
    do(task)                          # sigue ramas muertas; nunca re-prioriza
# o read_all_files()  -> quema 200k tokens y el budget de un golpe
```

## Validation

- Skill activada intencionalmente sobre dominio desconocido.
- Mapeo barato precedio a todo deep-dive; lectura limitada a objetivos priorizados.
- Presupuesto explicito respetado; un unico re-plan, disparado por invalidacion documentada.
- Plan y hallazgos persistidos en scratchpad con evidencia por archivo.
