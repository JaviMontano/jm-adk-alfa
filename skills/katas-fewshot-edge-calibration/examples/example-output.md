<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-fewshot-edge-calibration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Resumen

Se reemplaza el párrafo abstracto por 3 ejemplos `input/output` que cubren bordes distintos del dominio (billing/high, feedback/low, auth/high). Los ejemplos van al inicio del prompt como bloque estático.

## Bordes cubiertos

- billing / high → factura/cobro con impacto sostenido.
- feedback / low → aporte sin urgencia operativa.
- auth / high → bloqueo de acceso, urgente.

## Patrón correcto (GOOD)

```python
prompt = (
    "Clasifica el ticket. Ejemplos:\n"
    "ticket:'no me llega la factura desde hace 3 meses' clase:'billing',urgencia:'high'\n"
    "ticket:'tengo una sugerencia para la app' clase:'feedback',urgencia:'low'\n"
    "ticket:'no puedo entrar, token expirado' clase:'auth',urgencia:'high'\n"
    "ahora clasifica:\n"
    "ticket:'{user_text}'"
)
```

## Anti-patrón (ANTI)

```python
prompt = (
    "Clasifica usando criterio profesional, considerando urgencia, dominio, "
    "impacto, severidad operacional, prioridad SLA y política interna."
)
```

## Validación

- La tarea es subjetiva: few-shot supera a la prosa (quiz P1).
- 3 ejemplos (dentro del rango 2 a 4); no satura atención ni rompe cache.
- Si luego se añade un schema estricto (Kata 5) y choca con un ejemplo, gana el schema y se reescribe el ejemplo (quiz P2).
- Ejemplos al inicio = bloque estático: prefix cache (Kata 10) y borde de atención alta (Kata 11) (quiz P3).
