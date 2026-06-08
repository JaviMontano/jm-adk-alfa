# Mcp Engineering Body of Knowledge

## Canon

La integración MCP en producción se sostiene sobre dos decisiones de diseño: **dónde vive la config** y **cómo se comunica el fallo**.

### Conceptos

- **Scope de configuración.** `.mcp.json` es config de equipo, versionada en el repo, heredada por todos. `~/.claude.json` es config personal del desarrollador, fuera del repo. La pregunta de diseño es: ¿quién debe heredar este servidor?
- **Expansión de env-var.** La config referencia `${ENV_VAR}`; el valor real vive en el entorno del proceso. El archivo nunca contiene el secreto literal, así puede versionarse sin fuga.
- **Contrato de error tipado.** El servidor expone `isError`, `errorCategory` (auth / rate_limit / transient / fatal), `isRetryable` y `retryAfterSeconds`. El consumidor lee campos, no interpreta prosa.
- **Frontera reintento cliente vs modelo.** La política de reintento (backoff, límite, respeto de `retryAfterSeconds`) vive en el código del cliente. El modelo no implementa backoff razonando.
- **Remediación de secretos.** Un secreto filtrado se rota en el proveedor y se purga del historial con `git filter-repo`. Añadirlo a `.gitignore` después NO borra lo ya commiteado.
- **MCP vs built-in.** MCP solo cuando ningún tool built-in (Read, Grep, Bash) cubre la necesidad.

## Taxonomía determinística de errores

| errorCategory | isRetryable | retryAfterSeconds | Acción cliente |
|---|---:|---:|---|
| `auth` | false | null | No reintentar; pedir credencial válida o reautenticación |
| `rate_limit` | true | requerido | Reintentar con backoff y cap |
| `transient` | true | opcional | Reintentar con backoff corto y cap |
| `fatal` | false | null | No reintentar; devolver error tipado |

El modelo no decide retry. El cliente consume esos campos y aplica una política acotada.

## Quality Signals

| Señal | Objetivo |
|---|---|
| Scope correcto | Config de equipo en `.mcp.json`, personal en `~/.claude.json` |
| Credenciales seguras | Todo secreto por `${ENV}`; cero literales versionados |
| Error accionable | Cada error con categoría + `isRetryable` (+ `retryAfterSeconds`) |
| Reintento en cliente | La política de retry no depende del juicio del modelo |
| Minimalismo de tooling | MCP solo cuando un built-in no aplica |
| Script offline | `scripts/check.sh` acepta fixtures válidos y rechaza mutaciones inválidas |

## Decisión de diseño

Ante un fallo de un servidor MCP, ¿quién decide reintentar? El **cliente**, leyendo `isRetryable` y `retryAfterSeconds` del contrato tipado. El modelo nunca debe adivinar a partir de un string de error.

## Anti-patrón

Token literal en archivo versionado (fuga garantizada) y error como string genérico ("Something went wrong, please try again") que obliga al modelo a adivinar si reintenta un fatal o ignora un transient.

## Open Knowledge

- Mapear `errorCategory` a códigos concretos de cada servidor a medida que se estabilizan.
