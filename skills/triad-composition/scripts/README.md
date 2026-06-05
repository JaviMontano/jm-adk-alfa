# Triad Composition Scripts

Offline validators for deterministic triad composition packets.

Run:

```bash
bash skills/triad-composition/scripts/check.sh
```

The check validates:

- a Requirements auto-select packet,
- an ambiguous 0.60-0.84 packet,
- a missing-context clarification packet,
- a false-positive jazz triad packet,
- and a failure fixture that omits Guardian validation.
