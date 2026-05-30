<!--
generated-by: scripts/scaffold-skill.py
generated-for: tool-use-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

> Nuestro agente de soporte sobre el repo tiene tres tools y elige mal: a veces lee todo el repo antes de tocar nada y se queda sin contexto. Las descripciones actuales son:
>
> - `search`: `"Searches the codebase."`
> - `read`: `"Reads code."`
> - `modify`: `"Modifies a file."`
>
> Rediseña estas descripciones para que el modelo enrute sin pedir aclaración y deja claro cómo operar sin cargar el repo entero. El runtime es el SDK de Anthropic; `modify` se implementa con un Edit por anchor.
