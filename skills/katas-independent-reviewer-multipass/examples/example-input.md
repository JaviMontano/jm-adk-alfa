<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-independent-reviewer-multipass
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Escenario (Code Gen + CI/CD): el equipo generó con un modelo un PR de 14 archivos que añade un nuevo módulo de pagos. Para acelerar, alguien propone que el mismo modelo revise su propio PR en la misma sesión ("ahora revisa lo que escribiste") y que se consensúen 2 de 3 reviews por mayoría.

Pedido: revisa este PR aplicando el patrón correcto de la Kata 27.

Pista del anti-patrón a evitar:

```python
# ANTI: self-review en la misma sesión + quorum 2-de-3
resp_gen = create(messages=[{"role": "user", "content": "Genera el módulo de pagos"}])
create(messages=[resp_gen, {"role": "user", "content": "Ahora revisa lo que escribiste"}])
# luego: descartar findings que no aparezcan en 2 de 3 reviews
```
