# Prompting And Meta Prompting

Transform intentions into durable prompts, meta-prompts, acceptance criteria, and eval-ready prompt systems.

## Use It For

- Turning vague requests into executable prompts with role, task sequence, constraints, and output contract.
- Creating meta-prompts that review future prompts for objective alignment, safety, output shape, and eval coverage.
- Designing acceptance criteria and eval cases before a prompt is treated as reusable.
- Hardening prompt systems against drift, missing data, credential capture, hidden chain-of-thought requests, and unverifiable outputs.

## Deterministic Contract

The canonical report shape is defined in `assets/prompting-and-meta-prompting-contract.json`. A valid report includes:

- `request`: objective, audience, context, constraints, and missing data.
- `prompt_artifact`: role, task, sequence, output contract, anti-drift rules, and missing-data handling.
- `meta_prompt`: enabled flag and review dimensions.
- `acceptance_criteria`: verifiable criteria with stable ids.
- `eval_cases`: happy path, minimal input, conflicting requirements, and false positive coverage.
- `safety`: no secret capture, no hidden chain-of-thought request, unsafe automation blocked, and evidence requirements.

## Validation

Run the offline validator before treating a prompt-system report as deterministic evidence:

```bash
bash skills/prompting-and-meta-prompting/scripts/check.sh
```

The check passes only when valid fixtures pass and invalid mutations fail for contract, eval, safety, and Guardian consistency reasons.
