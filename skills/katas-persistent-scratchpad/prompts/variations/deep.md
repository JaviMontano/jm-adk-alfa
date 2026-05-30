<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-persistent-scratchpad
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Persistent Scratchpad Deep Variation

Úsala al iniciar o reanudar una investigación larga y multisesión.

- Si el scratchpad existe, léelo una vez y reconstruye el estado completo (decisiones, hallazgos, pendientes); si no, créalo con la estructura canónica.
- Define el helper de anexado (`append_scratchpad(section, entry)`) y la convención de entradas fechadas y trazables.
- Documenta cómo sobrevive el estado a `/compact` (Kata 11) y cómo alimenta la investigación adaptativa (Kata 19).
- Explicita qué entra al scratchpad y qué no, y cómo evitas re-lecturas que rompan el cache (Kata 10).
- Incluye notas de descubrimiento, decisiones tomadas, validación y riesgos residuales.
