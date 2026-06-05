# Assets

These assets make `bmad-method` deterministic.

## Files

- `persona-matrix.json`: canonical BMAD persona routing, including core and auxiliary roles.
- `artifact-chain.json`: required artifact flow by project type and phase.
- `readiness-gate-policy.json`: single PASS/CONCERNS/FAIL policy for Phase 4 entry.
- `quick-flow-policy.json`: deterministic Barry Quick Flow criteria.
- `bmad-packet-contract.json`: Markdown packet sections and blocked phrases.
- `deterministic-source-policy.md`: offline source, time, and sampling rules.

Use these assets before producing BMAD guidance, then validate deliverables with `scripts/validate_bmad_packet.py`.
