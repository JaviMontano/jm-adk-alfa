<!--
generated-by: scripts/scaffold-skill.py
generated-for: ab-testing
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Input

Design an A/B test for a SaaS trial signup page.

Context:

- Control: current hero headline says "Start your free trial".
- Variant: new headline says "Launch your first workflow in 10 minutes".
- Audience: new visitors from paid search in the United States.
- Primary metric: completed trial signup.
- Guardrails: demo requests, support tickets, and bounce rate.
- Baseline signup conversion: 6.0%.
- Minimum detectable effect: 10% relative lift.
- Eligible traffic: about 18,000 sessions per week.
- Constraint: team wants a launch/no-launch decision before the next campaign cycle.

Output needed:

Return an experiment brief, readiness state, risks, and decision rule.
