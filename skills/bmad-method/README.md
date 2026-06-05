# BMAD Method

`bmad-method` teaches and applies the BMAD documentation-first lifecycle for AI-driven software development.

## Activation

Use for BMAD, PRD, architecture, story generation, sprint planning with AI agents, agent-as-code workflows, implementation readiness, greenfield project setup, brownfield adoption, or Quick Flow triage.

Do not use for general agile coaching without AI-agent artifact flow.

## Deterministic Resources

- `assets/persona-matrix.json`: canonical persona routing.
- `assets/artifact-chain.json`: greenfield, brownfield, and quick-flow artifact order.
- `assets/readiness-gate-policy.json`: PASS/CONCERNS/FAIL and Phase 4 entry rule.
- `assets/quick-flow-policy.json`: Barry Quick Flow criteria.
- `assets/bmad-packet-contract.json`: output packet contract.
- `scripts/validate_bmad_packet.py`: offline packet validator.

## Local Checks

```bash
bash skills/bmad-method/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill bmad-method
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill bmad-method
```
