# AI Assisted Testing Body of Knowledge

AI-assisted testing produces reviewable test intent. It does not prove correctness unless tests are actually executed and evidence is supplied.

## Test Types

| type | purpose |
|------|---------|
| unit | verify a function or module in isolation |
| integration | verify contracts between components |
| property | verify invariants across generated inputs |
| fuzz | explore bounded malformed or random inputs safely |
| mutation | evaluate whether tests catch code mutations |
| regression | lock a reproduced defect or prior incident |

## Required Test Fields

Every candidate test needs target, rationale, oracle, evidence IDs, and status.

## Safety Rules

Fuzz only local/offline or approved test targets. Mutation requires a passing baseline. Coverage claims require measured evidence or explicit target-only status.
