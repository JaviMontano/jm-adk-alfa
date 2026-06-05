# Assumption Log Body of Knowledge

## Canon

An assumption is a project claim that influences decisions but is not yet fully
proven by supplied evidence. The log makes those claims explicit, testable, and
traceable.

## Evidence Tags

| Tag | Meaning | Strength |
|---|---|---|
| `[CODE]` | Source code, tests, scripts, or local command output | strong |
| `[CONFIG]` | Configuration, policy, manifest, or environment contract | strong |
| `[DOC]` | Documented decision, requirement, ADR, or source note | strong |
| `[INFERENCE]` | Reasoned conclusion from available evidence | weak |
| `[ASSUMPTION]` | Unvalidated claim or explicit evidence gap | weak |

## Lifecycle

- `unvalidated`: open claim with no strong proof.
- `validating`: evidence collection is in progress.
- `validated`: strong evidence supports the claim.
- `invalidated`: strong evidence contradicts the claim.
- `superseded`: a newer assumption or decision replaced the claim.
- `blocked`: validation cannot proceed without an external input.
- `stale`: previously accepted evidence needs review because supplied context changed.

## Determinism Rules

- IDs are assigned once and preserved.
- New IDs are gapless and ascending.
- Closed statuses require strong evidence and a source reference.
- High-impact open entries must appear in the validation queue.
- A warning is mandatory when more than 30% of entries use `[ASSUMPTION]`.

## Anti-Patterns

- Treating assumptions as facts.
- Using unsupported statuses such as `[OPEN]`.
- Renumbering existing assumptions without reason.
- Validating an assumption with only inference.
- Hiding high-impact open assumptions outside the queue.
