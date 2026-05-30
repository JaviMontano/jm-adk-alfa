<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-tool-description-quality
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Los dos tools tenían contratos genéricos y solapados (`Analyzes content` / `Analyzes documents`), causa del misroute del ~25%. Se aplicó rename + frontera recíproca: `analyze_content` → `extract_web_results` con input format, ejemplo de query y frontera hacia `parse_document`, y se reescribió el par documental con la frontera inversa.

## Evidence

- Anti-patrón detectado: mismo verbo (`Analyzes`), sustantivos casi sinónimos (`content`/`documents`), cero input format, cero frontera.
- El nombre `analyze_content` no distingue web de documento; rename supera a "explicar más".

## Result

```json
[
  {
    "name": "extract_web_results",
    "description": "Parses HTML pages from a search query into a list of {title,url,snippet}. Use when input is a URL or raw HTML; for PDF/DOCX use parse_document instead."
  },
  {
    "name": "parse_document",
    "description": "Extracts structured text from PDF or DOCX files. Use when input is a file path or document bytes; for URLs or raw HTML use extract_web_results instead."
  }
]
```

## Validation

- No queda contrato solapado: cada description declara su input format distinto.
- Las fronteras son recíprocas: `extract_web_results` envía PDF/DOCX a `parse_document` y este devuelve URLs/HTML a aquel.
- Misroute esperado por debajo del 5% tras el cambio.

## Risks and Limits

- Si el system prompt contiene keywords como "document" para referirse a páginas web, podría reintroducir sesgo; conviene revisarlo.
- Inputs mixtos (HTML embebido en un PDF) quedan fuera de la frontera actual y requieren una decisión explícita.
