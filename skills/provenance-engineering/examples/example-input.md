<!--
generated-by: scripts/scaffold-skill.py
generated-for: provenance-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

Estamos consolidando el perfil de una entidad para onboarding KYC a partir de tres documentos:

- `doc-A` — Certificado de constitución (fecha 2021-03-12): dirección "Carrera 7 #71-21, Bogotá".
- `doc-B` — Estado financiero (fecha 2024-09-30): dirección "Cra 7 No 71-21, Bogotá D.C.", ingresos USD 4.2M.
- `doc-C` — Reporte de auditoría (fecha 2025-02-15): ingresos USD 4.8M.

El output lo usa un analista que aprueba o rechaza la cuenta. Necesitamos que cada dato sea trazable a su documento, con fecha, y que las contradicciones queden visibles para que el analista decida. El pipeline actual entrega un resumen en prosa y promedia los ingresos.

Pide: rediseñar con `Claim` tipado (invariante "no hay claim sin source"), marcar el conflicto de ingresos sin promediar, escalarlo al analista, y un test estructural que falle si algún claim queda sin source.
