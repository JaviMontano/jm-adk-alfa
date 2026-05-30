# Mitigación de Dilución Softmax (Kata 11)

> Curva de atención en U: los bordes (inicio/fin) reciben atención alta; el centro se diluye ("lost in the middle").

## Reglas

1. **Edge placement.** Las reglas críticas (seguridad, compliance, políticas irreversibles) van al **inicio Y se repiten al final** como `<reminder>`. Los datos ricos van al centro.
2. **Compactación con umbral.** Si `usage_fraction(history) > 0.55`, compactar el historial: reescribir denso **preservando** reglas, decisiones y escaladas; nunca borrar señal operativa.

La pérdida por dilución es **silenciosa**: un agente puede cumplir una política al turno 5 y violarla al turno 30 sin haberla olvidado — solo dejó de atenderla porque quedó en el medio. No aparece en logs.

## Patrón

```text
SYSTEM:   <rules>critical_policy</rules>     # borde de atención alta (inicio)
...datos ricos en el centro...
REMINDER: <rules>critical_policy</rules>     # borde de atención alta (fin)
```

```python
if usage_fraction(history) > 0.55:
    history = compact(history, preserve=["rules", "decisions", "escalations"])
```

## Anti-patrón

```python
system_prompt = f"""You are an assistant.
{big_blob_of_context}
IMPORTANT: never expose PII.   # <- regla crítica enterrada en el valle de la U
...3000 more tokens..."""
```

## Por qué repetir la regla no es redundancia inútil

Inicio y fin son **ambas** zonas de atención alta; repetir cubre el riesgo de dilución desde los dos extremos. Romper el prefix cache (Kata 10) NO es el objetivo — la repetición es estructural, no decorativa.

## Aplicación en JM-ADK

- Las 18 reglas de la Constitution y los gates G0–G3 son "reglas críticas" → inicio + reminder final.
- Cuando una sesión cruza ~55% de contexto, el orquestador compacta preservando decisiones y escaladas, y vuelca lo durable al scratchpad (Kata 18).

Relacionado: `katas-context-dilution-mitigation`, `katas-multipass-prompt-chaining`, `katas-persistent-scratchpad`.
