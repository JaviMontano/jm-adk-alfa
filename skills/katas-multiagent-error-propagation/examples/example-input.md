<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multiagent-error-propagation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Escenario Customer Support / Multi-Agent. Un coordinador delega en tres subagentes de búsqueda (docs internos, base de tickets, web pública) y sintetiza un report para el usuario. Hoy cada subagente captura todo con un `except` genérico y devuelve la lista de resultados:

```python
def search_subagent(query):
    try:
        return {"results": http_search(query, timeout=10)}
    except Exception:
        return {"results": []}
```

Petición: el subagente de docs internos a veces hace timeout y otras veces devuelve un permission denied, y el report final salió "completo" omitiendo silenciosamente esa fuente. Corrige la propagación de errores para que el coordinador pueda distinguir un fallo de acceso de un resultado vacío legítimo y anotar el coverage gap.
