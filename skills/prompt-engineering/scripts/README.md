# Scripts

`prompt-engineering` uses deterministic scripts to validate prompt optimization packets.

- `validate_prompt_packet.py`: validates JSON packets for pattern, prompt, guardrails, output contract, metrics, and test cases.
- `check.sh`: runs deterministic positive and negative fixture checks.
- `fixtures/*.json`: sample prompt engineering packets used by the check script.
