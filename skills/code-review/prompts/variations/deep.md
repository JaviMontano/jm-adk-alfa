---
name: code-review-deep
type: variation
version: 2.1.0
description: "Deep deterministic Code Review for high-risk changes."
---

# Code Review - Deep Mode

## When To Use

Use deep mode for security-sensitive, high-blast-radius, data, auth,
compliance, migration, or architecture changes.

## Execution

1. Confirm scope and source boundaries.
2. Inspect changed code, adjacent contracts, tests, and supplied CI/log output.
3. Evaluate all taxonomy categories relevant to the diff.
4. Separate verified code facts from risk inference.
5. Flag missing evidence instead of assuming tests or policies pass.
6. Apply the same severity decision rules as standard mode.

## Output

Use the standard report sections and include `not_verified` items for any
missing tests, missing policy docs, unavailable runtime behavior, or inaccessible
context.
