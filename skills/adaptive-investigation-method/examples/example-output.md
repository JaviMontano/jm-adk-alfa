<!--
generated-by: scripts/scaffold-skill.py
generated-for: adaptive-investigation-method
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Objetivo

Localizar la validacion de autenticacion de requests entrantes y el manejo de token expirado en un monorepo de ~4.000 archivos.

## Budget

Consumido 3 de 8 lecturas caras.

## Mapa de superficie (barato)

`Grep "verifyToken|authenticate|expired"` -> 14 hits, concentrados en `packages/api/middleware/` y `packages/auth/`. `Glob "**/middleware/*.ts"` -> 6 archivos. No se leyo contenido completo todavia.

## Hipotesis priorizadas

1. (alto valor) La validacion vive en `packages/api/middleware/auth.ts` (nombre + densidad de hits).
2. (medio) La logica de expiracion esta en `packages/auth/token.ts`.
3. (bajo) Hay un guard duplicado en el gateway.

## Findings

- `packages/api/middleware/auth.ts:42` -> `authenticate()` llama a `verifyToken()` y rechaza con 401 si falla. [confirma H1]
- `packages/auth/token.ts:88` -> `verifyToken()` lanza `TokenExpiredError`; el middleware lo mapea a `401 + {code: "TOKEN_EXPIRED"}`. [confirma H2]
- Deep-dive #3 no fue necesario: H1 y H2 resolvieron el objetivo; budget restante 5.

## Decisiones de re-plan

Ninguna. Las dos primeras hipotesis se confirmaron; no hubo invalidacion, asi que no se re-planifico (se evita el re-plan reflejo).

## Deliverable

La autenticacion se valida en `packages/api/middleware/auth.ts:42` via `authenticate()`. Si el token expira, `verifyToken()` (`packages/auth/token.ts:88`) lanza `TokenExpiredError` y el cliente recibe `401 {code: "TOKEN_EXPIRED"}`.

## Riesgos y limites

- No se exploro el path del gateway (H3); si existe un segundo guard, no esta cubierto. Riesgo bajo dado el budget restante.

---

## ANTI (lo que NO se debe construir)

```python
# Plan rigido + read_all_files + re-plan reflejo
plan = make_full_plan_upfront(goal)
data = read_all_files()        # 4.000 archivos -> contexto desbordado
for step in plan:
    plan = make_full_plan_upfront(goal)  # re-plan en cada turno -> loop de duda
    act(step, data)
```

Resultado: agente lento, caro y sin condicion de paro; pierde la senal entre 4.000 archivos.
