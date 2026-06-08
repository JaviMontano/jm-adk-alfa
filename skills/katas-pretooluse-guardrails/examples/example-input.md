# Example Input

Escenario Financial Compliance. Un agente de Customer Support tiene una tool `process_refund` con side-effects reales. La política de negocio prohíbe reembolsos mayores a 1000 sin aprobación humana.

Estado actual:

- La regla está escrita sólo en `system_prompt`.
- Un cliente insistente logró que el agente intentara `process_refund({"amount": 4500, "currency": "USD"})`.
- La política debe poder cambiar sin reiniciar el agente.

Petición:

```text
Convierte esta regla en un guardarraíl determinístico con PreToolUse. Debe negar amount > 1000 antes de ejecutar process_refund, permitir amount <= 1000 y devolver una razón accionable al modelo.
```
