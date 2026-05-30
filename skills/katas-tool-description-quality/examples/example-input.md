<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-tool-description-quality
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Escenario Dev Productivity. Un agente de research dispone de dos tools y enruta mal el ~25% de los turnos: cuando el usuario pega una URL, a veces invoca el tool de documentos y devuelve vacío.

Tools actuales (anti-patrón):

```json
[
  {"name":"analyze_content","description":"Analyzes content"},
  {"name":"analyze_document","description":"Analyzes documents"}
]
```

Petición: "Arregla el routing entre estos dos tools. `analyze_content` debe procesar páginas web (URL o HTML crudo) y devolver una lista de {title,url,snippet}; `analyze_document` debe procesar archivos PDF/DOCX. Aplica la Kata 21."
