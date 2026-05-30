<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-critical-self-correction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 15 · Variante profunda

Úsala cuando hay múltiples campos numéricos, epsilons distintos por tipo (enteros vs moneda), o el documento puede no declarar todos los totales.

## Pasos

1. **Inventario de campos verificables:** total, subtotales, impuestos, conteo de líneas, fechas derivadas.
2. **Por campo:** extrae `stated`, recalcula `computed` determinísticamente, elige epsilon (cero para enteros, redondeo de centavos para moneda) y justifícalo.
3. **Caso sin declaración:** si el documento no declara un campo, devuelve `computed` con `stated=null` y `mismatch=false`; no fabriques conflicto.
4. **Agrega resultados:** si CUALQUIER campo discrepa, el documento entero lleva `needs_human_review=true`.
5. **Escalada y origen:** enruta el mismatch a `katas-human-handoff-protocol` y conserva el origen del dato vía `katas-provenance-preservation`.

## Output

Incluye notas de descubrimiento, el epsilon elegido por campo con su racional, la tabla `stated` vs `computed` vs `delta` por campo, y el estado de validación.
