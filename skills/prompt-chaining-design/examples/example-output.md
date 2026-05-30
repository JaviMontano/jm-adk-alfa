<!--
generated-by: scripts/scaffold-skill.py
generated-for: prompt-chaining-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Cadena de dos pases: un pase local que analiza un archivo a la vez y emite un `FileSummary` tipado, y un pase de integración que solo consume la colección de `FileSummary` para producir el reporte y la síntesis de riesgos transversales. El pase de integración nunca relee el código crudo.

## Result — patrón correcto (GOOD)

```python
from pydantic import BaseModel
from typing import Literal

class FileSummary(BaseModel):
    file: str
    status: Literal["ok", "error"]
    endpoints: list[str] = []
    risks: list[str] = []
    error_detail: str | None = None

def local_pass(svc: ServiceFile) -> FileSummary:
    # Ve UN archivo. El fallo de parseo se tipa, no se lanza.
    try:
        return FileSummary(
            file=svc.path,
            status="ok",
            endpoints=extract_endpoints(svc.code),
            risks=scan_security(svc.code),
        )
    except ParseError as exc:
        return FileSummary(file=svc.path, status="error", error_detail=str(exc))

# Schema de transicion: coleccion tipada de resumenes (paralelizable, sin crudos).
summaries: list[FileSummary] = [local_pass(s) for s in services]

def integration_pass(summaries: list[FileSummary]) -> Report:
    ok = [s for s in summaries if s.status == "ok"]
    failed = [s for s in summaries if s.status == "error"]
    top5 = rank_cross_cutting_risks(ok)   # razona solo sobre resumenes
    return Report(per_file=ok, top_risks=top5, skipped=failed)
```

## Anti-patrón (ANTI) — lo que NO se entrega

```python
# Mega-prompt: 60 archivos crudos concatenados en una sola pasada.
blob = "\n\n".join(read(s.path) for s in services)
report = model(f"Lista endpoints, riesgos y los 5 transversales:\n{blob}")
# Satura atencion, no paraleliza, sin estado de error por archivo:
# un parseo roto contamina todo el reporte.
```

## Validation

- [x] El pase de integración nunca ve crudos, solo `FileSummary`.
- [x] Cada pase tiene schema explícito (`FileSummary` / `Report`).
- [x] El estado de error está tipado por archivo (`status="error"`).
- [x] El pase local es aislado, idempotente y paralelizable.
- [x] Existe schema de transición (`list[FileSummary]`).
- [x] Justificado: 60 archivos no caben con calidad en single-pass.

## Risks and Limits

- Si la síntesis de riesgos transversales requiere un detalle no capturado en `FileSummary`, ampliar el schema del pase local; no abrir un atajo al crudo.
- La deriva de schema entre versiones del pase local y el de integración debe versionarse.
