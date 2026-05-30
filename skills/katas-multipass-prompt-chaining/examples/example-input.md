<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multipass-prompt-chaining
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Escenario Multi-Agent Orchestration. El usuario pide:

> "Audita los 50 archivos `*.py` del directorio `src/` y entrégame un informe único de hallazgos de seguridad."

Esto no cabe cognitivamente en un solo prompt. Aplica Kata 12.

## Camino correcto (GOOD)

Encadenar dos pases con schemas tipados:

```python
# Pase 1: por archivo, schema FileFindings (paralelizable vía subagentes)
local = [analyze_file(f, schema=FileFindings) for f in files]
# Pase 2: integración solo sobre los resúmenes tipados
report = integrate(local, schema=AuditReport)
```

Cada `FileFindings` incluye `status: ok | failed` para que el pase 2 sepa cuántas unidades válidas tiene.

## Anti-patrón (ANTI)

Concatenar todo en un mega-prompt:

```python
mega_prompt = "\n\n".join(open(f).read() for f in files)
create(messages=[{"role": "user", "content": f"Audita todo:\n{mega_prompt}"}])
```

Satura la atención (Kata 11), no paraleliza y alucina relaciones entre archivos.
