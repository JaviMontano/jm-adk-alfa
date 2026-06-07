# AI CONOPS

AI CONOPS defines the operational concept for an AI-enabled system before
architecture work begins. The skill produces a stakeholder-backed, metric-bound,
mode-aware concept of operations that can be validated offline.

## Triggers
- ai-conops
- AI CONOPS
- define the AI operational concept
- map AI stakeholders
- design AI-human interaction levels
- assess AI business value
- define AI success metrics
- plan AI operational modes

## Inputs
- System or project name.
- Business problem and current process.
- Stakeholder context.
- Candidate AI capability.
- Known constraints, data readiness, and decision stakes.

## Output
Markdown by default, plus optional JSON packet using
`assets/conops-report-contract.json`.

Required output sections:
- system vision and objectives
- stakeholder and actor map
- AI-human interaction design
- business value matrix placement
- success metrics across three pillars
- operational modes and transitions
- assumptions, risks, and validation status

## Determinism Rules
- Stakeholders must have named roles, concerns, and decision rights.
- Autonomy level must be one integer from 1 to 5 with rationale and controls.
- Value quadrant must match value/effort scores.
- Metrics must cover technical, business, and UX/ethics pillars.
- Operational modes must include normal, degraded, and recovery behavior.
- Open assumptions must remain explicit.

## Local Validation
Run:

```bash
bash skills/ai-conops/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill ai-conops
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill ai-conops
```
