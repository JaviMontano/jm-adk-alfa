# Example Input

Create `/jm:skill-audit-ready` as a repeatable workflow for reviewing one skill
and deciding whether it is ready for a granular PR.

Constraints:

- First phase must clarify the target skill and branch.
- Middle phases should inspect the skill package, apply scoped improvements, and
  prepare a review document.
- Final phase must run DoD, script checks, `check.sh`, and scoped whitespace
  validation.
- Agents should include a lead, support, and guardian.
- Do not touch the ledger.
