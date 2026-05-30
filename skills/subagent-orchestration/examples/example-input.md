<!--
generated-by: scripts/scaffold-skill.py
generated-for: subagent-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

Necesito un coordinador que enriquezca una lista de 200 empresas. Para cada una hay que: (1) buscar su sitio en la web y (2) extraer el sector y el headcount del HTML. Las búsquedas a veces fallan por rate limit o porque la empresa no tiene sitio. Quiero que el resultado distinga "no encontré sitio" de "el sitio existe pero no declara headcount", y que un fallo en una empresa no rompa el batch completo. La extracción debe ir a un modelo barato; la priorización final, a uno más capaz.

Restricciones: tolerante a latencia (offline), presupuesto de costo ajustado, el resultado agregado debe listar explícitamente qué empresas quedaron sin cubrir y por qué.
