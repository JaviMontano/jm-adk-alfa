<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multiagent-error-propagation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Multiagent Error Propagation Body of Knowledge

## Canon

Arquitectura hub-and-spoke: un coordinador delega búsquedas en subagentes y sintetiza sus resultados. La confiabilidad del synthesis depende de cómo los subagentes propagan sus fallos.

### Conceptos

- **Contrato de propagación estructurada:** todo fallo se serializa con `failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`. El coordinador lee estos campos para decidir alternativas o anotar el gap.
- **Local recovery primero:** el subagente reintenta fallos transitorios (broaden query, longer timeout) antes de escalar al coordinador. Solo propaga cuando el recovery local también falla.
- **Access failure vs valid empty:** un `timeout`/`permission` significa que el sistema no pudo mirar (access failure). Un search OK con 0 matches significa que el sistema miró y no había nada (valid empty, `empty_valid:True`). Son ramas distintas con manejo distinto.
- **Coverage gap annotation:** cuando una fuente no se pudo consultar, el coordinador lo declara explícitamente en el synthesis. No se infiere ausencia de datos a partir de un fallo de acceso.
- **`retryable=False` (permission):** señal explícita de que reintentar la misma query es inútil; el coordinador escala o anota el coverage gap.

### Señales de calidad

| Señal | Objetivo |
|---|---|
| Distinción access/empty | Toda rama separa timeout/permission de 0 matches válidos |
| Local recovery | Transients se reintentan antes de propagar |
| Contexto propagado | Cada fallo lleva attempted_query + suggested_alternatives |
| Coverage gap visible | El synthesis declara fuentes no consultadas, sin huecos silenciosos |
| Sin enmascaramiento | Ningún error retorna como `{results:[]}` |

## Anti-patrón canónico

```python
except Exception:
    return {"results": []}
```

Enmascara cualquier error como success vacío. El coordinador asume "no había info" y produce un report confiado con hueco silencioso. El genérico `'search unavailable'` es la variante opuesta: priva al coordinador del contexto (`attempted_query`, `suggested_alternatives`) para decidir alternativas.

## Open Knowledge

- Añadir referencias específicas del proyecto sobre orquestación multi-agente conforme se estabilicen.
