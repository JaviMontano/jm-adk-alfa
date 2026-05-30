<!--
generated-by: scripts/scaffold-skill.py
generated-for: self-correction-loops
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Self Correction Loops Body of Knowledge

## Canon

La auto-correccion confiable no "arregla" numeros: los **verifica de forma cruzada** y deja el conflicto a la vista. El patron canonico es comparar el valor **declarado** (lo que la fuente afirma) contra el valor **calculado** (recomputado desde componentes crudos). Si difieren mas alla de un `epsilon` justificado, se emite `mismatch=true` con ambos valores y se escala. La invariante: **nunca corregir un numero en silencio**.

Conceptos clave:

- **Declarado vs calculado:** dos caminos independientes hacia el mismo numero. El calculado nunca debe derivarse del agregado declarado (recomputo circular).
- **Epsilon por tipo de dato:** cero para enteros (conteos, cantidades); tolerancia pequena (centavo, `1e-6`) para moneda y floats por redondeo. El epsilon es una decision documentada, no un default.
- **Mismatch tipado:** estado estructurado (`field`, `declared`, `computed`, `delta`, `mismatch`), no prosa.
- **Escalada en lugar de correccion:** el mismatch enruta a humano con ambos valores visibles; el campo no se sobreescribe.
- **Test estructural:** un caso con mismatch inyectado debe producir el flag.

## Decision de diseno

- Si no existe un recomputo independiente para un campo, ese campo es **no verificable**: marcarlo como tal, no inventar una verificacion falsa.
- El epsilon se elige por unidad y semantica del dato; uno global es un anti-patron.
- La verificacion vive en codigo ejecutable (recomputo determinista), no en la estimacion del modelo.

## Quality Signals

| Signal | Target |
|---|---|
| Cobertura de cruce | Todo agregado verificable tiene recomputo independiente |
| Epsilon justificado | Cero enteros, tolerancia documentada en moneda/floats |
| No-silencio | Mismatch escala con declarado y calculado visibles; nunca sobreescribe |
| Test de mismatch | Caso inyectado produce `mismatch=true` |

## Anti-patron

Confiar en lo declarado sin recomputar, o "corregir" via `total=computed` silencioso: ambos ocultan que la fuente, el calculo o los datos estaban en conflicto y propagan un dato falso con apariencia de validado.

## Open Knowledge

- Anadir referencias especificas del dominio (reglas de redondeo bancario, tolerancias regulatorias) a medida que se estabilicen.
