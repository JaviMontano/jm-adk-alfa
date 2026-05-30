<!--
generated-by: scripts/scaffold-skill.py
generated-for: structured-output-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Structured Output Design Quick Variation

Úsala cuando los campos y la fuente ya están claros y solo falta el schema.

Entrega directo:

1. El `input_schema` defensivo (opcionales `nullable`, enums con `'other'`+`details`, `required` reales).
2. La línea de `tool_choice` (forzado o no, con una frase de por qué).
3. La línea de parseo desde `tool_use.input`.
4. El checklist marcado en una línea por punto.

Sin exploración extensa. Si detectas un falso `required` o un default `''`, corrígelo y dilo en una frase.
