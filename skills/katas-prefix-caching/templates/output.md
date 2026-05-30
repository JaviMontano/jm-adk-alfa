<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-prefix-caching
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Prefix Caching Output

## Summary

{summary · qué bloques eran estáticos vs dinámicos y cómo se reordenó el prompt}

## Evidence

{evidence · usage tokens citados: cache_creation_input_tokens vs cache_read_input_tokens y ahorro estimado (~10x)}

## Result

{result · prompt reordenado: estático arriba con cache_control ephemeral, dinámico al final en <reminder>}

## Validation

{validation · ningún valor dinámico precede a un bloque estable; un cambio de un carácter no invalida la zona estable}

## Risks and Limits

{risks}
