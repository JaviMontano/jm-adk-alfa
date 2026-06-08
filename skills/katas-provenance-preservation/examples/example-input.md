# Example Input

Tres subagentes leyeron documentos distintos sobre una empresa objetivo y devolvieron datos. Agrega los hechos en un reporte factual auditable usando `katas-provenance-preservation`.

Fuentes:

- `doc-A` · "Annual Report" · `2025-12-01` → ARR Q3 2025 = 12M USD; headcount end-2025 = 450.
- `doc-B` · "Investor Deck" · `2025-09-15` → ARR Q3 2025 = 12M USD.
- `doc-C` · "Press Release" · `2026-01-10` → headcount end-2025 = 462.

Pregunta factual:

```text
¿Cuál es el ARR de Q3 2025 y el headcount a fin de 2025?
```

Requisito: no emitir claims sin source y no resolver contradicciones por promedio, fecha más reciente ni elección del modelo.
