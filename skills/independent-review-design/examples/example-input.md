<!--
generated-by: scripts/scaffold-skill.py
generated-for: independent-review-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

Tenemos un agente que genera parches de código y luego los revisa. Hoy el revisor corre en
la misma sesión que el generador (reusa el mismo `Session`), hace tres pasadas mezclando
revisión por archivo y entre archivos, y solo reporta un issue si aparece en al menos dos
de las tres pasadas (quorum 2-de-3). Notamos que defectos reales de naming entre módulos no
se reportan. Rediseña la etapa de revisión con `independent-review-design`.

Artefactos: `src/payments.py`, `src/orders.py`, `src/common/money.py`.
Criterio: corrección, contratos entre módulos, edge cases de redondeo monetario.
