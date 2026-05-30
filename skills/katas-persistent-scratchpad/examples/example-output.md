<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-persistent-scratchpad
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## GOOD · scratchpad persistente curado

Escribir solo conclusiones validadas a `investigation-scratchpad.md`, estructurado por secciones, y leerlo una vez al reanudar.

```markdown
# Investigation Scratchpad
## Decisiones
- 2026-04-25: usar pydantic v2 (T-19 confirmó compat).
## Hallazgos
- src/legacy/parser.py bug offset línea 142 (replicado).
## Pendientes
- Verificar si --strict rompe tests integration
```

```python
def append_scratchpad(section, entry):
    with open("investigation-scratchpad.md", "a", encoding="utf-8") as fh:
        fh.write(f"\n## {section}\n- {entry}\n")
```

Al reanudar mañana: leer el archivo una vez, reconstruir el estado y seguir anexando (sin re-leer cada turno, para no romper el cache de prefijo · Kata 10).

## ANTI · conversación como memoria de largo plazo

Confiar en el historial conversacional para recordar que "se decidió pydantic v2" y "el bug está en la línea 142". Tras `/compact` (Kata 11) ese detalle desaparece y la investigación reinicia a ciegas. Igual de malo: un scratchpad sin estructura o re-leído en cada turno, que rompe el cache y mezcla monólogo interno con conclusiones validadas.

## Validation

- Activación intencional: investigación larga con riesgo de pérdida por compactación.
- Se persisten solo conclusiones validadas (decisiones, hallazgos, pendientes); no monólogo ni hipótesis sin confirmar.
- Lectura única al inicio; después referenciar/anexar (Kata 10).
- Conexión explícita con Kata 11 (compactación) y Kata 19 (investigación adaptativa).
