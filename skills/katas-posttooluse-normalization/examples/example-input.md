<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-posttooluse-normalization
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Escenario: Legacy ERP Integration en un agente de Customer Support.

Tenemos una tool MCP `get_order(order_id)` que pega a un ERP de 2008 y devuelve XML como:

```xml
<OrderResponse><OrderId>A-4471</OrderId><StatusCode>0xA1</StatusCode><Total>1290.50</Total></OrderResponse>
```

Hay además `get_invoice` y `get_shipment`, todas con el mismo dialecto XML y códigos de estado hexadecimales (`0xA1`=pagado, `0xB2`=pendiente, `0xC3`=vencido). El modelo está quemando budget leyendo el XML y a veces malinterpreta los códigos.

Quiero que el agente nunca vea el XML crudo: que reciba JSON canónico `{order_id, status, amount}`. Necesito que la garantía aplique a las tres tools y a cualquier tool legacy nueva, sin depender de que cada handler recuerde limpiar su salida.
