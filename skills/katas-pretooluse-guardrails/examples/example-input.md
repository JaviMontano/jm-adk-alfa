<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-pretooluse-guardrails
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Escenario Financial Compliance. Tenemos un agente de Customer Support con una tool `process_refund(amount)`. La política de negocio prohíbe reembolsos mayores a $1000 sin aprobación humana. Hoy esa regla está escrita en el `system_prompt`, pero un cliente insistente logró que el agente aprobara un reembolso de $4500.

Pide: convertir esa regla en un guardarraíl determinista con un hook `PreToolUse` que la bloquee antes de ejecutar, dejando la política en un `dict` recargable.
