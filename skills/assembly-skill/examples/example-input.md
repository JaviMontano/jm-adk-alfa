# Example Input

Run `assembly-skill` on `skills/output-contract-enforcer` in `standard` mode.

Context:

- [EXPLICIT] Target path: `skills/output-contract-enforcer`.
- [EXPLICIT] User allows file edits only after reviewing the Gate B plan.
- [EXPLICIT] The run must produce one final Assembly Report and one PR for the target skill only.
- [EXPLICIT] Duration should be reported as `operator-supplied elapsed bucket`, not wall-clock time.
- [OPEN] Trigger optimization is not requested.

Expected behavior:

- Run Phase A diagnostic.
- Present Gate B plan before edits.
- Run Phase C after approved changes.
- Validate the final report with `scripts/validate_assembly_contract.py`.
