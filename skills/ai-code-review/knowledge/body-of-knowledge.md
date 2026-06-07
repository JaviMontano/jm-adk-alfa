# AI Code Review - Body of Knowledge

## Canon
AI-assisted code review is useful only when it behaves like a disciplined
reviewer: it reads the changed code, cites exact evidence, distinguishes defects
from preferences, and records uncertainty.

## Review Categories
| Category | Use When | Required Evidence |
|----------|----------|-------------------|
| correctness | behavior diverges from requirements or local invariants | source line plus expected behavior |
| security | access control, injection, secrets, unsafe parsing, or trust boundary issue | vulnerable path and threat impact |
| tests | changed behavior lacks coverage or test result is relevant | source line or command output |
| performance | repeated work, unbounded loops, N+1, blocking I/O, or memory growth | code path and plausible workload |
| maintainability | duplicated root cause, confusing abstraction, brittle API contract | local code evidence |
| data-integrity | migration, persistence, schema, idempotency, or transaction risk | data path and failure mode |
| ai-safety | prompt injection, untrusted model output, tool-use boundary, eval leakage | model/tool boundary evidence |

## Priority Policy
- P0: must block merge; severe security, data loss, or production outage.
- P1: should block merge; confirmed correctness/security regression.
- P2: should fix soon; meaningful risk with clear evidence.
- P3: non-blocking improvement; small maintainability or clarity issue.

## Evidence Rules
- A finding without `file` and `line_start` is not a confirmed finding.
- A test result without a command is not a test result.
- A high-priority finding needs strong evidence and confidence of at least 0.80.
- Clean review is valid only when scope and exclusions are explicit.

## False Positive Controls
- Do not report style preference as a defect.
- Do not infer missing behavior from absent files unless the scope proves absence.
- Do not report generated, vendored, or lockfile changes by default.
- Downgrade speculative risks to `needs-verification`.

## Offline Validation
`scripts/validate_ai_code_review_report.py` validates the JSON packet contract,
evidence references, priorities, file-line requirements, scope inclusion, and
test-status claims without network access or clock-dependent behavior.
