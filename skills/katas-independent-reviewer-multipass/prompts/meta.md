<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-independent-reviewer-multipass
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Independent Reviewer Multipass Meta Prompt

Decide si `katas-independent-reviewer-multipass` debe activarse para esta tarea.

## Chequeo de activación

- ¿Hay un PR o changeset de varios archivos por revisar? → activa.
- ¿El código fue generado por un modelo al que ahora se le pediría revisar (riesgo de self-review)? → activa.
- ¿Alguien propone "consensuar 2 de 3 reviews" / quorum N-de-M? → activa para rechazarlo.
- ¿El pedido es un single-pass trivial de un solo archivo pequeño sin riesgo? → NO activa (overhead innecesario).
- Input vacío o tema ajeno a revisión de código → NO activa.

## Verificación de sesión limpia

Confirma que el reviewer NO comparte sesión con el generador antes de proceder.
