# Prompt Engineering Checklist

Apply this checklist before returning a prompt optimization packet.

## Source Gate

- Task, target model family, output contract, and safety boundary are explicit.
- Source facts are quoted or path-backed; missing facts are marked `coverage_gap`.
- External research is not claimed fresh unless a source and retrieval date are provided.
- Synthetic fixtures are labeled as fixtures, not production evidence.

## Pattern Gate

- Pattern is selected from `assets/pattern-decision-matrix.json`.
- Rejected alternatives are listed with one reason each.
- Hidden reasoning is not requested or exposed; use concise rationale or decision trace.
- Model-specific syntax is used only when the target model is explicit.

## Packet Gate

- Required fields: `task`, `target_model`, `pattern`, `prompt`, `guardrails`, `output_contract`, `test_cases`, `metrics`, `risks`.
- At least three test cases exist: happy path, edge case, and adversarial/injection.
- Test case IDs are stable (`PE-001`, `PE-002`, ...), sorted, and deterministic.
- Guardrails include injection handling and unsupported-source handling.
- Output contract defines format, refusal/escalation behavior, and validation criteria.

## Decision Gate

- Return `write_packet` when enough evidence exists.
- Return `ask` when task, source boundary, target model, output contract, or success metric is missing.
- Return `handoff` when the requested deliverable is a durable prompt file (`prompt-creator`) or agent constitution (`agent-constitution-creator`).
- Return `decline` when the request asks for unsafe or deceptive prompt behavior.
