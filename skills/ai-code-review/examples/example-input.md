# Example Input

Run an AI-assisted code review for the following diff and return a JSON packet
that can be validated offline.

Scope:
- include `src/auth/session.ts`
- include `src/auth/session.test.ts`
- exclude generated files and dependency lockfiles

Review focus:
- correctness
- security
- test evidence

Known context:
- `src/auth/session.ts` now accepts a `rememberMe` flag.
- The test file has not been updated for the new expiration branch.
- Do not claim test execution unless you actually run commands.
