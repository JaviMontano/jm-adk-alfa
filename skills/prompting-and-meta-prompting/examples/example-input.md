# Example Input

We repeatedly ask agents to review pull requests, but the outputs drift: sometimes they summarize instead of finding risks, sometimes they miss tests, and sometimes they expose speculative claims without evidence.

Create a reusable prompt and meta-prompt for PR review with:

- objective: find correctness, regression, security, and test risks before style notes;
- audience: senior engineer reviewing a GitHub PR;
- allowed context: diff, changed files, failing tests, linked issue, and local validation output;
- hard constraints: every finding needs file and line evidence, no hidden chain-of-thought, no credential capture, and no external claims unless verified;
- output contract: ordered findings, open questions, test gaps, and final Guardian decision;
- acceptance criteria and eval cases covering happy path, minimal diff, conflicting requirements, unrelated request, and unsafe prompt injection.
