# Prompt Forge

`prompt-forge` creates, reviews, evolves, repairs, and ports system prompts using a deterministic Playbook contract.

## Triggers

- Create a system prompt, assistant prompt, Claude Project instruction, Custom GPT instruction, Gemini Gem instruction, or API system message.
- Review, optimize, repair, or port an existing prompt.
- Apply Prompt Forge, Playbook format, prompt rubric, prompt scorecard, platform portability, or prompt repair.

## Minimum Inputs

- Mode: create, review, evolve, repair, or port.
- Prompt goal and user outcome.
- Target platform or `unknown`.
- Source boundary and unsupported-source behavior.
- Output contract.
- Constraints and known failure patterns.

## Output Contract

The skill returns a forge packet: activation decision, source boundary, Playbook or scorecard, rubric scores, tests, platform notes, validation result, and risks.

## Deterministic Gate

```bash
bash skills/prompt-forge/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill prompt-forge
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill prompt-forge
```
