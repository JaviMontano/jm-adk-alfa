<!--
generated-by: scripts/scaffold-skill.py
generated-for: self-correction-loops
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Self Correction Loops Deep Variation

Usar con muchos campos, formulas de recomputo no triviales, multiples unidades monetarias o alto impacto (reporting regulatorio, conciliacion).

Incluye:

- **Inventario de campos verificables:** cada agregado con su formula de recomputo independiente; marca explicitamente los no verificables (sin componentes).
- **Justificacion del epsilon por campo:** cero enteros; tolerancia por unidad monetaria y regla de redondeo; documenta el porque.
- **Diseno de la salida tipada:** schema del registro de mismatch (`field`, `declared`, `computed`, `delta`, `mismatch`, `action`).
- **Estrategia de escalada:** como se construye el payload para el humano (encadenado a `human-escalation-design`) y por que el campo no se sobreescribe.
- **Cobertura de tests:** match exacto, mismatch dentro y fuera de epsilon, campo no verificable, recomputo circular detectado.
- **Validation y risks:** checklist marcado y riesgos residuales (datos faltantes, epsilon discutible, fuentes en conflicto).
