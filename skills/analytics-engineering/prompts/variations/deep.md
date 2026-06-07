---
name: analytics-engineering-deep
type: variation
variant: deep
---
# Analytics Engineering — Deep Analysis

Full depth execution. Load all `references/` files from canonical. Run L3 progressive loading.
Apply all Validation Gate criteria strictly.

Required additions:
- Build a source-to-target table for every source and mart.
- Map every non-staging model to upstream models or sources.
- Specify materialization, grain, owner, tests, contract status, and documentation for every production mart.
- Use the `assets/` contract as the checklist and `scripts/check.sh` fixtures as the offline oracle pattern.
