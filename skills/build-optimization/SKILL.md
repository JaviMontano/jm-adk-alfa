---
name: build-optimization
description: Vite/Webpack config tuning with tree shaking, code splitting, dynamic imports, Brotli/gzip compression, and source maps
version: 1.0.0
status: production
owner: Javier Montaño
tags: [devops, build, vite, webpack, tree-shaking, code-splitting, compression]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 095 — Build Optimization {DevOps}

## Purpose
Optimize the build pipeline to produce the smallest, fastest-loading bundles possible. Configure tree shaking, code splitting, compression, and source maps for production deployments. [EXPLICIT]

## Physics — 3 Immutable Laws

1. **Law of Minimal Payload**: Every byte shipped to the browser must justify its existence. Unused code is eliminated. Large dependencies are lazy-loaded. [EXPLICIT]
2. **Law of Parallel Loading**: Code splitting enables parallel chunk downloads. Route-based splitting ensures users only load code for the current page. [EXPLICIT]
3. **Law of Compression**: All production assets are Brotli-compressed (preferred) or gzip-compressed. Uncompressed production deploys are a bug. [EXPLICIT]

## Protocol

### Phase 1 — Bundler Configuration
1. Vite: configure `vite.config.ts` with `build.rollupOptions.output.manualChunks` for vendor splitting. [EXPLICIT]
2. Webpack: configure `optimization.splitChunks` with `cacheGroups` for vendor/common/async chunks. [EXPLICIT]
3. Enable tree shaking: ensure `"sideEffects": false` in `package.json` for all pure modules. [EXPLICIT]
4. Set `build.target: 'es2020'` — no unnecessary transpilation for modern browsers. [EXPLICIT]

### Phase 2 — Code Splitting Strategy
1. Route-based splitting: `React.lazy(() => import('./pages/Dashboard'))` for each route. [EXPLICIT]
2. Feature-based splitting: heavy features (charts, editors) loaded on demand. [EXPLICIT]
3. Vendor splitting: separate chunks for `react`, `firebase`, `lodash-es`. [EXPLICIT]
4. Shared chunk: common utilities used by 3+ routes go into shared chunk. [EXPLICIT]

### Phase 3 — Compression & Source Maps
1. Install `vite-plugin-compression` or `compression-webpack-plugin`. [EXPLICIT]
2. Generate Brotli (`.br`) and gzip (`.gz`) for all assets > 1KB. [EXPLICIT]
3. Firebase Hosting auto-compresses, but pre-compressed assets are faster. [EXPLICIT]
4. Source maps: `hidden-source-map` for production — uploaded to error tracker, not served to users. [EXPLICIT]

## I/O

| Input | Output |
|-------|--------|
| Application source code | Optimized production bundle |
| Vite/Webpack config | Split chunks (vendor, routes, shared) |
| Built assets | Brotli/gzip compressed files |
| Source maps config | Hidden source maps for error tracking |

## Quality Gates — 5 Checks

1. **Initial bundle < 250KB gzipped** — measured by `size-limit`. [EXPLICIT]
2. **No single chunk > 100KB gzipped** — split further if exceeding. [EXPLICIT]
3. **Tree shaking verified** — `import { specific }` not `import *` for all dependencies. [EXPLICIT]
4. **Brotli compression enabled** — verify `.br` files in build output. [EXPLICIT]
5. **No source maps in production CDN** — `hidden-source-map` mode only. [EXPLICIT]

## Edge Cases

- **Firebase SDK size**: Firebase modular SDK (`firebase/firestore/lite`) reduces bundle by ~60%.
- **Dynamic import failures**: Add error boundary around `React.lazy` with retry logic.
- **CSS extraction**: Use `mini-css-extract-plugin` or Vite's built-in CSS splitting.
- **Polyfills**: Only include polyfills for features actually used. Use `@vitejs/plugin-legacy` only if supporting IE11.

## Self-Correction Triggers

- Bundle exceeds 250KB → run bundle analyzer (skill 099), identify and split large deps.
- Chunk exceeds 100KB → add manual chunk splitting or dynamic import.
- Tree shaking not working → check `sideEffects` field, verify ESM imports.
- Build time exceeds 60s → enable caching (`vite` default), use `esbuild` for transpilation.

## Usage

Example invocations:

- "/build-optimization" — Run the full build optimization workflow
- "build optimization on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
