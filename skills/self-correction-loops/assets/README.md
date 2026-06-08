# Self Correction Loops Assets

These assets make the skill output deterministic and locally checkable.

- `self-correction-loops-contract.json` defines the JSON report shape.
- `cross-check-policy.json` lists required field metadata for independent recomputation.
- `epsilon-policy.json` fixes tolerated epsilon by data type.
- `mismatch-policy.json` forbids silent overwrites and defines allowed actions.
- `escalation-policy.json` requires human escalation for each mismatch.
- `structural-test-policy.json` defines boolean tests that must pass before Guardian approval.

The local validator in `scripts/validate_self_correction_loops.py` reads these files and runs without network access, wall-clock input, or randomness.
