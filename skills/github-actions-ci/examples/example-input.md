# Example Input

Design a GitHub Actions CI workflow for a Node.js package.

- Existing commands: `npm ci`, `npm run lint`, `npm test`, `npm run build`
- Lockfile: `package-lock.json`
- Branch policy: run CI on pull requests and pushes to `main`
- Matrix: Node.js `20` and `22`
- Deployment: publish package only from `main` after CI passes
- Secrets: `NPM_TOKEN` must be used only for publish
- Desired outcome: deterministic workflow plan with permissions, cache,
  concurrency, deploy gate, and validation evidence
