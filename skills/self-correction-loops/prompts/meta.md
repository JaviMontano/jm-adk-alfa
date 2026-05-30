<!--
generated-by: scripts/scaffold-skill.py
generated-for: self-correction-loops
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Self Correction Loops Meta Prompt

Decide si `self-correction-loops` debe activarse, si el alcance es seguro y que agentes de apoyo participan.

## Activation Check

- Hay valores numericos agregados (totales, balances, conteos) que pueden recomputarse desde componentes crudos.
- Existe un recomputo independiente real; si no hay nada contra que cruzar, el campo es no verificable y la skill no aplica a ese campo.
- El costo de un numero silenciosamente equivocado justifica el control (finanzas, facturacion, inventario, reporting).
- No es solo validacion de formato (eso es `validation-retry-design`) ni provenance de claims textuales (eso es `provenance-engineering`).

## Routing de agentes

- `lead`: construye el bucle (campos, epsilon, comparacion, escalada).
- `support`: caza agregados sin cruzar, epsilon mal calibrado y recomputo circular.
- `guardian`: valida el checklist y bloquea el `total=computed` silencioso.
- `specialist`: salida estructurada del mismatch, recomputo en `Bash`, encadenado a escalada.
