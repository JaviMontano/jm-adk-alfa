# Kata 26 · Body of Knowledge — Validación y Retry con Error Feedback

## Canon

Una extracción tipada que falla validación no se reintenta a ciegas. El retry-with-error-feedback reenvía a la API el documento original, la extracción fallida y el error de validación específico, pidiendo corregir solo lo que el error señala. El loop es `extract → validate → (si error) extract+feedback → validate`, con un cap de 2-3 intentos.

## Conceptos clave

- **Retry con feedback específico:** el feedback es el error real de validación (`str(e)`), no un mensaje genérico. Sin esto, el modelo no sabe qué corregir.
- **Error recuperable vs no recuperable:** recuperable = formato/tipo/estructura, corregible en un siguiente intento. No recuperable = el dato no existe en la fuente; reintentar provoca alucinación.
- **Cap de intentos:** máximo 2-3. Más intentos no aportan señal y encarecen.
- **Escalada con cadena de errores:** al agotar `max_retries`, marcar `needs_human_review` y conservar la `error_chain` para el revisor humano.
- **Patrón sistemático:** si el mismo error aparece en ~80% de los casos, el fix es estructural (ajustar schema/prompt o normalizar en post-process), no subir el número de reintentos.

## Taxonomía determinística

| Tipo | Recuperable | Acción |
|---|---:|---|
| `missing_required_field` | Sí | Reintentar si la fuente contiene el dato |
| `type_mismatch` | Sí | Reintentar con path, tipo esperado y valor previo |
| `format_error` | Sí | Reintentar con formato esperado y cita de fuente |
| `enum_mismatch` | Sí | Reintentar si hay normalización inequívoca |
| `transient_parse_error` | Sí | Reintentar una vez con output previo |
| `source_absent` | No | Escalar sin inventar |
| `policy_violation` | No | Bloquear o escalar |
| `unsafe_request` | No | Bloquear |
| `auth_required` | No | Escalar a operador |
| `schema_contract_conflict` | No | Fix estructural de schema/prompt/post-process |

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Feedback específico | Cada retry inyecta el error de validación real, no un mensaje genérico |
| Clasificación de error | Recuperable y no recuperable se ramifican explícitamente |
| Cap de intentos | Máximo 2-3 intentos antes de escalar |
| Escalada trazable | `needs_human_review` + cadena de errores al agotar intentos |
| Contrato downstream | Ninguna salida no validada llega a consumidores del schema |
| Script offline | `scripts/check.sh` acepta fixtures válidos y rechaza mutaciones inválidas |

## Anti-patrón canónico

Reintentar en un `for` con el mismo prompt y sin feedback (`except: continue`), tratando cualquier error como recuperable, y aceptar la salida fallida en silencio cuando el loop se agota. Resultado: ruido, contratos rotos y alucinaciones cuando el dato no estaba en la fuente.
