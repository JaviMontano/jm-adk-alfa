# AI CONOPS Scripts

## `validate_ai_conops_report.py`
Validates a JSON AI CONOPS report packet offline.

It checks:
- schema and required top-level fields
- evidence ids and evidence tags
- stakeholder coverage and decision rights
- interaction level, high-stakes controls, and autonomy bounds
- value/effort quadrant consistency
- metric coverage across technical, business, and UX/ethics pillars
- required operational modes and transition fields
- assumptions and required validation checks

## `check.sh`
Runs the validator against deterministic valid and invalid fixtures.

No network, clock, random, or repository mutation is required.
