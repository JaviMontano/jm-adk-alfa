<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-path-conditional-rules
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Tenemos un monorepo con código Python en `src/` e infraestructura Terraform en `infra/`. Hoy nuestro `CLAUDE.md` importa todas las reglas a la vez: estilo Python, testing Python, convenciones Terraform y una política de seguridad. Cuando un agente solo edita el `README.md`, igual carga las 2000 líneas de todas las reglas.

Aplica `katas-path-conditional-rules`: clasifica cada regla como universal o condicional por glob, reescribe el `CLAUDE.md` para que las heurísticas de lenguaje se carguen solo al editar sus archivos, deja la seguridad siempre cargada, y estima el ahorro de tokens entre editar un README y editar un `.py`.
