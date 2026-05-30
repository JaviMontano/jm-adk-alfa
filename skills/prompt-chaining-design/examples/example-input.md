<!--
generated-by: scripts/scaffold-skill.py
generated-for: prompt-chaining-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

> Tengo un repositorio con 60 archivos de servicio. Necesito un único reporte que liste, por archivo, los endpoints expuestos y los riesgos de seguridad, y al final una síntesis con los 5 riesgos transversales más graves. El repo es demasiado grande para meterlo entero en un solo prompt. Diséñame la cadena multi-pass.

Restricciones:

- Una unidad = un archivo de servicio.
- El reporte final no puede depender de releer el código crudo.
- Un archivo que falle el parseo no debe tumbar el lote.
