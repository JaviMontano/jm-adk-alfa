# katas-builtin-tool-selection Scripts

`check.sh` runs deterministic offline fixtures through
`validate_tool_selection_report.py`.

The validator checks tool fit, selective reads, edit-anchor uniqueness, write
fallback safety, evidence, and validation flags. It does not call the network or
use wall-clock/random inputs.
