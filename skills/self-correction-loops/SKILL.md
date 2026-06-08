---
name: self-correction-loops
version: 1.0.0
description: "Construir verificacion cruzada declarado vs calculado con mismatch flag y escalada; nunca corregir numeros en silencio."
owner: "JM Labs"
triggers:
  - self-correction loops
  - cross-check verification
  - mismatch flag
  - numeric validation
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Self Correction Loops

## Capacidad

Construir un bucle de verificacion cruzada que compara el valor **declarado** (lo que la fuente afirma) contra el valor **calculado** (lo que recomputas desde los datos crudos). Cuando difieren mas alla de un `epsilon` justificado, el sistema emite `mismatch=true` con ambos valores y escala a un humano. La invariante dura es: **nunca corregir un numero en silencio**. Un mismatch no es un error a parchear; es la senal de que la fuente, el calculo o los datos estan en conflicto, y esa decision pertenece a una persona.

Esto convierte la auto-correccion en un control de integridad auditable, no en un "arreglo" opaco que oculta la discrepancia y propaga un dato falso con apariencia de validado.

## Cuando usarla

- Hay campos numericos que llegan ya agregados (totales, subtotales, balances, conteos) y ademas tienes los componentes para recomputarlos.
- El costo de un numero silenciosamente equivocado es alto: finanzas, facturacion, inventario, reporting regulatorio.
- Quieres que el pipeline distinga "lo recompute y coincide" de "lo recompute y NO coincide" en lugar de confiar ciegamente en lo declarado.
- Necesitas un rastro de auditoria: cada total verificado debe poder mostrar declarado vs calculado.

No la uses para campos sin forma de recomputo independiente (no hay nada contra que cruzar) ni como reemplazo de validacion de formato (eso es `validation-retry-design`).

## Como construir

1. **Identifica los campos numericos verificables.** Para cada uno necesitas dos caminos: el valor declarado y una formula de recomputo desde datos mas primitivos (suma de lineas, balance = debe - haber, conteo de items).
2. **Justifica el epsilon por tipo de dato.** Cero para enteros (conteos, cantidades). Tolerancia pequena para moneda y floats por redondeo (`1e-6` o el centavo segun la unidad). Documenta el porque; un epsilon arbitrario invalida el control.
3. **Recomputa de forma independiente.** No reuses el mismo agregado declarado; deriva el calculado desde los componentes crudos.
4. **Compara y emite estado tipado.** Si `abs(declared - computed) <= epsilon` -> `match`. Si no -> `mismatch=true` con `declared`, `computed`, `delta` y `field`.
5. **Escala, no corrijas.** Ante mismatch, NO sobreescribas el campo. Adjunta el flag al output y deriva a revision humana con ambos valores visibles.
6. **Cubre con un test estructural.** Un caso con mismatch inyectado debe producir `mismatch=true`; jamas un `total=computed` silencioso.

## Patron correcto

```python
from dataclasses import dataclass

@dataclass
class CrossCheck:
    field: str
    declared: float
    computed: float
    epsilon: float

    @property
    def mismatch(self) -> bool:
        return abs(self.declared - self.computed) > self.epsilon

    def to_record(self) -> dict:
        return {
            "field": self.field,
            "declared": self.declared,
            "computed": self.computed,
            "delta": self.declared - self.computed,
            "mismatch": self.mismatch,
        }

def verify_total(invoice: dict) -> dict:
    computed = sum(line["amount"] for line in invoice["lines"])  # recomputo independiente
    check = CrossCheck(
        field="total",
        declared=invoice["total"],          # lo que la fuente afirma
        computed=computed,                  # lo que recalculamos
        epsilon=0.005,                      # medio centavo, justificado por redondeo
    )
    record = check.to_record()
    if check.mismatch:
        record["action"] = "escalate_to_human"   # NO se reescribe el total
    return record
```

## Anti-patron

```python
# ANTI: confiar en lo declarado, o "corregir" en silencio.
def verify_total_bad(invoice: dict) -> dict:
    computed = sum(line["amount"] for line in invoice["lines"])
    invoice["total"] = computed   # sobreescribe sin avisar: oculta el conflicto
    return invoice                # el humano nunca ve que la fuente estaba mal
```

## Checklist de validacion

- [ ] Campos numericos verificables identificados, cada uno con un recomputo independiente.
- [ ] `epsilon` justificado por tipo de dato: cero para enteros, tolerancia pequena para moneda/floats.
- [ ] El valor calculado se deriva de componentes crudos, no del agregado declarado.
- [ ] Ante discrepancia se emite `mismatch=true` con `declared` y `computed` ambos visibles.
- [ ] Un mismatch escala a humano; el campo NO se sobreescribe.
- [ ] Test estructural: caso con mismatch inyectado produce el flag, nunca un `total=computed` silencioso.
- [ ] El reporte cumple `assets/self-correction-loops-contract.json` y pasa `scripts/check.sh` con fixtures validas e invalidas.

## Assets y validacion offline

- `assets/self-correction-loops-contract.json` define los campos obligatorios del reporte JSON.
- `assets/epsilon-policy.json` fija tolerancias permitidas por tipo de dato.
- `assets/mismatch-policy.json` y `assets/escalation-policy.json` obligan a mostrar ambos valores y escalar sin sobreescribir.
- `assets/structural-test-policy.json` declara las pruebas estructurales que deben quedar en `true`.
- `scripts/validate_self_correction_loops.py` valida reportes offline y `scripts/check.sh` ejecuta fixtures deterministicas positivas y negativas.

## Katas y skills relacionadas

- Kata: `katas-critical-self-correction`
- Relacionada: `validation-retry-design`
- Relacionada: `human-escalation-design`
- Relacionada: `provenance-engineering`
