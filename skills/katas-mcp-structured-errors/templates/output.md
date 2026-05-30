<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-structured-errors
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Output · Kata 06 · Errores estructurados en MCP

## Summary

{summary}

## Contrato del servidor (flags tipados)

- `isError`: {is_error}
- `errorCategory`: {error_category}
- `isRetryable`: {is_retryable}
- `retryAfterSeconds`: {retry_after_seconds}
- `explanation` (solo auditoría): {explanation}

## Política del cliente (retry / escalada / aborto)

{client_policy}

## Evidence

{evidence}

## Validation

- [ ] El servidor emite flags tipados, no prosa.
- [ ] El cliente decide solo con flags; `explanation` no participa.
- [ ] La política de retry vive en el cliente.
- [ ] Error sin categoría → `unknown` non-retryable + log.

## Risks and Limits

{risks}
