# Pristino Calibration

`pristino-calibration` executes the deterministic persona and prompt-optimizer contract emitted by `persona-calibrate.sh`. It reads the injected `PRISTINO-CALIBRATION` block, declares the persona on line 1 unless bypass mode is active, applies the adaptive prompt optimizer, enforces precedence `Veracidad > Seguridad > Objetivo > Formato > Estilo`, and consolidates substantive work in the Canvas output contract.

## Deterministic Contract

The `assets/` directory defines the offline contract for:

- accepted modes and optimizer section rules,
- required injected calibration fields,
- persona line and confidence requirements,
- precedence order,
- evidence tag requirements,
- Canvas sections for substantive work,
- Guardian pass/block decisions.

## Local Validation

```bash
bash skills/pristino-calibration/scripts/check.sh
```

The check validates known-good calibration reports and rejects reports that omit the persona line, misuse mode-specific optimizer sections, invent delegate agents, break precedence, skip evidence tags, omit Canvas sections, or pass Guardian while the contract is broken.
