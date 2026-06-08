# Self Correction Loops Scripts

`check.sh` runs the offline fixture suite through `validate_self_correction_loops.py`.

The validator checks:

- required contract fields from `assets/self-correction-loops-contract.json`;
- epsilon limits by numeric data type;
- independent declared vs computed records;
- mismatch flag derivation from `abs(declared - computed) > epsilon`;
- human escalation for every mismatch;
- rejection of silent overwrite behavior.
