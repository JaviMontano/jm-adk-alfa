# Example Output

## Summary

Los dos tools tenían contratos genéricos y solapados. La corrección determinística es renombrar ambos tools y declarar formato de entrada, ejemplos de activación, acción aplicada y frontera recíproca.

## Evidence

- `analyze_content` no distingue URL, HTML, archivo o texto arbitrario.
- `analyze_document` no declara PDF/DOCX como formato de entrada.
- Las dos descripciones empiezan con el mismo verbo genérico y no contienen condición `Use when`.

## Rewritten Tools

```json
[
  {
    "name": "extract_web_results",
    "renamed_from": "analyze_content",
    "description": "Extracts search result records from URL or raw HTML input. Use when the request supplies a web page, search results page, or HTML string; for PDF or DOCX files use parse_document instead.",
    "input_format": "URL string or raw HTML string",
    "example_queries": [
      "Extract result titles and links from https://example.test/search?q=ai"
    ],
    "boundary": "For PDF, DOCX, or local file content use parse_document instead.",
    "reciprocal_boundary_to": "parse_document",
    "action": "rename"
  },
  {
    "name": "parse_document",
    "renamed_from": "analyze_document",
    "description": "Extracts structured text and metadata from PDF or DOCX input. Use when the request supplies a local document path, uploaded document bytes, or document MIME type; for URL or raw HTML input use extract_web_results instead.",
    "input_format": "PDF or DOCX path, bytes, or document MIME payload",
    "example_queries": [
      "Parse /tmp/contract.pdf into section headings and text."
    ],
    "boundary": "For URL, web search result pages, or raw HTML use extract_web_results instead.",
    "reciprocal_boundary_to": "extract_web_results",
    "action": "rename"
  }
]
```

## Rename And Split Decisions

- `analyze_content` -> `extract_web_results`: rename obligatorio por nombre confuso.
- `analyze_document` -> `parse_document`: rename recomendado para separar contrato documental de contrato web.
- No se aplica split porque cada tool resultante tiene un solo modo.

## Validation

- No quedan contratos solapados.
- Las fronteras son recíprocas.
- El misroute esperado queda por debajo de 5%.

## Risks And Limits

- Inputs mixtos, como HTML embebido dentro de PDF, requieren decisión explícita de prioridad.
- Si el system prompt usa `document` para páginas web, debe revisarse porque puede reintroducir sesgo de routing.
