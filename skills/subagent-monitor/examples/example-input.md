# Example Input

Monitor a deterministic three-agent hardening swarm.

- swarm id: `skill-hardening-session`
- task: audit one active skill and aggregate spoke reports
- agents: coordinator, determinism-auditor, guardian
- timeout budget: 300 seconds per agent
- timeout action: cancel and record typed timeout result
- aggregation: block if any agent reports `block` or `timeout`
- evidence: every agent result must include one evidence tag
