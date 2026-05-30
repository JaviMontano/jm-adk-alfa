<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multiagent-error-propagation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Multiagent Error Propagation Primary Prompt

## Objective

Diseñar o revisar la propagación de errores entre subagentes y coordinador en una arquitectura hub-and-spoke, aplicando el patrón de propagación estructurada.

## Required Inputs

- Topología multi-agente (coordinador + subagentes y sus fuentes).
- Código o pseudocódigo del retorno de cada subagente.
- Comportamiento esperado del synthesis del coordinador.

## Process

1. Para cada subagente, define el contrato de retorno tipado: `failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`.
2. Implementa local recovery primero: reintenta transients (broaden, longer timeout) antes de propagar.
3. Separa ramas: `success:True, empty_valid:True` para 0 matches válidos; `success:False` con contexto para timeout/permission.
4. Marca `retryable=False` en permission y asegura que el coordinador escala o anota coverage gap en vez de reintentar.
5. Verifica que el synthesis anota explícitamente cada fuente no consultada y nunca trata un fallo como ausencia de datos.

## Output

Markdown con summary, evidence, result, validation y risks. Incluye el bloque de código del subagente corregido.
