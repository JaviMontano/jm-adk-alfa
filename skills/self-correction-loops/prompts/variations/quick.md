<!--
generated-by: scripts/scaffold-skill.py
generated-for: self-correction-loops
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Self Correction Loops Quick Variation

Usar cuando hay uno o pocos campos numericos bien definidos y el recomputo es trivial (una suma, un conteo).

1. Recomputa el agregado desde sus componentes.
2. Compara con lo declarado usando el `epsilon` del tipo (cero entero, centavo moneda).
3. Devuelve el registro: `field`, `declared`, `computed`, `mismatch`.
4. Si `mismatch=true`, marca `escalate_to_human` y NO sobreescribas. No reportes correccion silenciosa.
