# Triad Composition

`triad-composition` selects Lead, Support, and Guardian roles from the PRISTINO composition matrix.

## Activation

Use for Pristino orchestration, Lead/Support/Guardian routing, domain-to-agent mapping, multiagent execution planning, committee escalation, and degraded-mode decisions.

Do not use for unrelated "triad" meanings such as music chords.

## Deterministic Resources

- `assets/composition-matrix.json`: canonical domain-to-triad matrix.
- `assets/classification-policy.json`: confidence bands and tie-breakers.
- `assets/degraded-mode-policy.json`: fail-explicit partial delivery.
- `assets/triad-output-contract.json`: packet section contract.
- `scripts/validate_triad_packet.py`: offline packet validator.

## Local Checks

```bash
bash skills/triad-composition/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill triad-composition
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill triad-composition
```
