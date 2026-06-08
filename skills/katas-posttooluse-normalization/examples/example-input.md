# Example Input

Escenario Legacy ERP Integration. Un agente de Customer Support consume `get_order`, `get_invoice` y `get_shipment`. Todas devuelven XML del ERP legacy:

```xml
<OrderResponse><OrderId>A-4471</OrderId><StatusCode>0xA1</StatusCode><Total>1290.50</Total></OrderResponse>
```

Requisitos:

- El modelo nunca debe ver el XML crudo.
- El JSON canónico debe ser `{order_id, status, amount}`.
- `0xA1=paid`, `0xB2=pending`, `0xC3=overdue`.
- Códigos no mapeados deben caer en `unknown`.
- La cobertura debe aplicar a tools legacy nuevas sin editar cada handler.
