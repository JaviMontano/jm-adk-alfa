# Cierre Conversacion

Deterministic JM Labs closeout skill for harvesting a long or explicitly ended conversation into a reusable handoff packet.

## Triggers

- `cierre-conversacion`
- `session-audit`
- `cosechar-aprendizajes`
- explicit closeout, retrospective, handoff, or learning-harvest request

## Contract

The skill produces a section-complete packet with summary, decisions, completed work, open tasks, learnings, risks, validation evidence, durable update plan, next handoff, and Guardian decision.

Durable writes are not implicit. If tasklog, changelog, memory, or repo docs should change, the packet must say whether authority is `confirmed`, `pending`, or `not-applicable`.

## Assets

- `assets/activation-policy.json`
- `assets/output-contract.json`
- `assets/evidence-policy.json`
- `assets/harvest-checklist.json`
- `assets/durable-update-policy.json`

## Local Validation

```bash
bash skills/cierre-conversacion/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill cierre-conversacion
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill cierre-conversacion
```

## Guardian Rule

Return `block` when validation evidence is missing, a completed task lacks completion evidence, durable writes are unapproved, or CI/merge/deployment status is contradictory.
