# Example Input

Run Constitution compliance on this release packet before merge:

- Target: JM-ADK Constitution v6.0.0
- Artifact: `skills/workflow-creator` hardening PR packet
- Gate: G0 pre-flight plus G3 release-readiness
- Evidence:
  - `python3 -B scripts/validate-skill-dod.py --skill workflow-creator`
  - `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill workflow-creator`
  - `python3 scripts/validate-skills.py --strict`
  - Quality Gates passed remotely
- Known caveat: runtime behavior beyond structure was not measured
