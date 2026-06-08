# Example Input

Escenario Dev Productivity. Un agente de research dispone de dos tools y enruta mal aproximadamente 25% de los turnos: cuando el usuario pega una URL, a veces invoca el tool de documentos y devuelve vacío.

Tools actuales:

```json
[
  {
    "name": "analyze_content",
    "description": "Analyzes content"
  },
  {
    "name": "analyze_document",
    "description": "Analyzes documents"
  }
]
```

Petición:

```text
Arregla el routing entre estos dos tools. analyze_content debe procesar páginas web, URL o HTML crudo, y devolver una lista de {title,url,snippet}. analyze_document debe procesar archivos PDF o DOCX. Aplica la kata sin cambiar implementación.
```

Evidencia disponible:

- Trazas de URL enviadas a `analyze_document`.
- Trazas de PDF enviado a `analyze_content`.
- No hay `input_format`, `example_queries` ni frontera recíproca en las descripciones actuales.
