# Code Review Report

## Scope

- Review type: pull request diff. [CONFIG]
- Sources reviewed: `app/billing/address.py` diff and supplied pytest output. [CÓDIGO]
- Minimum inputs missing: full test suite output and authorization policy document. [CONFIG]
- Depth: standard. [CONFIG]

## Findings

| ID | Severity | Category | Evidence | Claim | Suggested action |
|---|---|---|---|---|---|
| CR-001 | BLOCKER | correctness | `app/billing/address.py:3` [CÓDIGO] | The removed `user is None` guard lets anonymous calls reach `save_address(user.id, normalized)`, which can crash or bypass the stated login requirement. [INFERENCIA] | Restore the guard or reject anonymous updates before normalization, then add a failure-path test for `user is None`. |

## Positive Patterns

- `normalize_address(address)` remains before persistence, preserving the existing normalization step. [CÓDIGO]

## Validation

- Checks run: inspected supplied diff and author-provided pytest output. [CÓDIGO]
- Coverage notes: only one happy-path test was supplied. [CONFIG]
- Not verified: full billing authorization policy and complete test suite. [CONFIG]

## Decision

- Release decision: `request_changes`. [CONFIG]
- Reason: one `BLOCKER` correctness finding exists. [CÓDIGO]
- Next action: restore anonymous-user protection and add a failure-path test. [CONFIG]

## Risks and Limits

- This report does not prove behavior outside the supplied diff and test output. [CONFIG]
