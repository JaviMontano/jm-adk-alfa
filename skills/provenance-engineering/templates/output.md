<!--
generated-by: scripts/scaffold-skill.py
generated-for: provenance-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Provenance Engineering Output

## Summary

{summary}

## Evidence (claims con provenance)

| attribute | value | source_id | locator | as_of | conflict |
|---|---|---|---|---|---|
| {attribute} | {value} | {source_id} | {locator} | {as_of} | {conflict} |

> Conflictos (`conflict=true`) listados con todas sus fuentes y escalados a revisión humana, no resueltos.

## Result

{result}

## Validation

- [ ] Cada claim con `source[]` no vacío (id + ubicación + fecha)
- [ ] Conflictos marcados `conflict=true` con todas las fuentes
- [ ] Conflictos escalados a humano, no promediados
- [ ] `as_of` visible para el humano
- [ ] Test estructural de provenance en verde

## Risks and Limits

{risks}
