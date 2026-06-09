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

## Reporte JSON validable

```json
{
  "schema": "jm-labs.katas-adaptive-investigation.report.v1",
  "skill": "katas-adaptive-investigation",
  "objective": "Trazar procesamiento de pagos antes de editar.",
  "scope": "src/payments",
  "hypothesis": "Refund processing vive en charge.py.",
  "budget": {
    "files": {"limit": 50, "used": 7},
    "queries": {"limit": 20, "used": 4},
    "minutes": {"limit": 30, "used": 12},
    "status": "complete",
    "pending_questions": []
  },
  "topology": {
    "cheap_mapping": [
      {"tool": "Glob", "pattern": "src/payments/**/*.py", "result_count": 38, "evidence_tag": "[CODIGO]"},
      {"tool": "Grep", "pattern": "refund|charge|gateway", "result_count": 6, "evidence_tag": "[CODIGO]"}
    ],
    "candidates": ["src/payments/refund.py", "src/payments/charge.py", "src/payments/gateway.py"]
  },
  "prioritized_plan": [
    {"priority": 1, "target": "src/payments/refund.py", "rationale": "Coincide con el objetivo.", "source": "topology"}
  ],
  "findings": [
    {
      "id": "refund-delegates-gateway",
      "target": "src/payments/refund.py",
      "summary": "refund.py delega en gateway.process_refund.",
      "source": "src/payments/refund.py",
      "evidence_tag": "[CODIGO]",
      "invalidates_hypothesis": true,
      "deep_dive_after_mapping": true
    }
  ],
  "replans": [
    {
      "trigger_finding_id": "refund-delegates-gateway",
      "invalidated_hypothesis": "Refund processing vive en charge.py.",
      "new_plan_order": ["src/payments/gateway.py", "src/payments/charge.py"],
      "evidence_tag": "[CODIGO]"
    }
  ],
  "scratchpad": {
    "persisted": true,
    "source": "scratchpad/adaptive-investigation.md",
    "sections": ["topology", "plan", "findings", "budget", "risks"]
  },
  "evidence": [
    {"claim": "El re-plan se disparo por invalidacion.", "evidence_tag": "[CODIGO]", "source": "replans[0]"}
  ],
  "validation": {
    "status": "pass",
    "offline": true,
    "network_required": false,
    "deterministic": true,
    "uses_randomness": false,
    "checks": ["assets", "deterministic_scripts", "quality_criteria", "exploration_budget", "cheap_mapping_before_deep_dive", "selective_deep_dive", "replan_gate", "evidence_required", "scratchpad_persistence"]
  },
  "risks": {"remaining": [], "forbidden_patterns": []}
}
```
