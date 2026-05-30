<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-independent-reviewer-multipass
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Independent Reviewer Multipass Deep Variation

Úsala para PRs grandes (muchos archivos) con consecuencias cross-file.

- Pass A completo: una sesión independiente por archivo, salida tipada, paralelizable.
- Pass B obligatorio: integración cross-file sobre los resúmenes del Pass A para detectar interacciones, contratos rotos y duplicados de findings.
- Documenta el argumento de certificación: por qué el self-review es subóptimo, separación Pass A/B, rechazo del quorum N-de-M, sesiones limpias.
- Preserva explícitamente los findings de minoría como señal legítima.
