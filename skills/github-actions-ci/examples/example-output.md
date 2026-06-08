# Example Output

## Pipeline Surface

- Project type: Node.js package. [EXPLICIT]
- Commands: `npm ci`, `npm run lint`, `npm test`, `npm run build`.
  [EXPLICIT]
- Lockfile: `package-lock.json`. [EXPLICIT]

## Triggers

- Pull requests run lint, test, and build. [EXPLICIT]
- Pushes to `main` run lint, test, build, and publish gate. [EXPLICIT]
- Manual dispatch is optional and must not bypass validation. [EXPLICIT]

## Jobs

- `ci`: runs on `ubuntu-latest`, matrix Node.js `20` and `22`, executes install,
  lint, test, and build. [EXPLICIT]
- `publish`: needs `ci`, runs only on `main`, and uses the protected
  environment `npm-production`. [EXPLICIT]

## Permissions

- Default permissions: `contents: read`. [EXPLICIT]
- Publish job adds only the package permission required by the target registry.
  [EXPLICIT]

## Actions And Cache

- Third-party actions must be pinned to immutable SHA references before release
  readiness. [EXPLICIT]
- Cache key uses OS, Node.js version, and `package-lock.json` hash. [EXPLICIT]

## Secrets And Environments

- `NPM_TOKEN` is referenced by secret name only and scoped to the publish job.
  [EXPLICIT]
- `npm-production` requires reviewer approval before publish. [EXPLICIT]

## Validation Evidence

- Local commands: `npm ci`, `npm run lint`, `npm test`, `npm run build`.
  [EXPLICIT]
- CI evidence: PR status check for `ci` and protected environment approval for
  `publish`. [EXPLICIT]

## Guardian Decision

- Status: pass for workflow plan. [EXPLICIT]
- Remaining risk: actual GitHub run evidence is still required after YAML is
  committed. [EXPLICIT]
