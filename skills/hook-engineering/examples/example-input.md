<!--
generated-by: scripts/scaffold-skill.py
generated-for: hook-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

Tenemos un agente de soporte que puede invocar la tool `transfer_funds`. El negocio exige
que cualquier transferencia mayor a 10000 USD sea rechazada por el runtime, sin importar
lo que el modelo decida. El limite cambia por trimestre, asi que debe poder editarse sin
redeployar el agente. Disena el hook que garantice este enforcement de forma auditable.
