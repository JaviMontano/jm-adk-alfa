# Scripts

`prompt-creator` uses deterministic scripts to validate generated prompt artifacts before ledger closure or downstream execution.

- `validate_prompt_artifact.py`: validates frontmatter, required sections, placeholder quality, and type-specific prompt rules.
- `check.sh`: runs deterministic fixture checks for one valid handoff prompt and two invalid prompt artifacts.
- `fixtures/*.json`: inline prompt artifacts used by `check.sh`.

