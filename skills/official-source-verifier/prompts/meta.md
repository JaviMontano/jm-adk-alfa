# Official Source Verifier Meta Prompt

Decide whether `official-source-verifier` should activate and whether the request is safe to answer without source verification.

## Activation Check

- The task asks to verify docs, specs, APIs, SDK behavior, GitHub/Git behavior, framework config or cloud service rules.
- A decision or change depends on external authority rather than local code inspection.
- The user cites a blog, issue, generated answer or tutorial and asks whether it is correct.
- A high-impact claim needs URL, publisher and accessed date.

## No Activation

- The answer is fully derivable from local repo files using Read/Grep/Glob.
- The user only asks for a rewrite, brainstorm or local search.
- The request explicitly says to ignore evidence or use a secondary source as the only authority.

## Guardian Gate

Block if a claim lacks official evidence, if a secondary source is marked authority, if any source lacks `accessed_date`, or if a change is authorized from an unverified claim.
