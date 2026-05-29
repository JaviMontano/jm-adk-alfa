# JM-ADK Component Catalog

Interactive reference for the curated catalog snapshot.
For authoritative live counts, run `python3 scripts/count-components.py`.
Current physical inventory is 256 agents, 524 skills, 260 commands, and 256 prompts.

> **Tip**: Use `Ctrl+F` / `Cmd+F` to search this page, or `/jm-adk:search "keyword"` inside Claude Code.

---

## Agents (catalog snapshot)

### Orchestration (5)

| Agent | Role | Key Skills |
|-------|------|-----------|
| `adk-orchestrator` | Master router — classifies requests and delegates to specialists | All skills (routing) |
| `pipeline-conductor` | Sequences workflow phases, enforces gates | discovery-orchestration, test-strategy |
| `skill-router` | BM25 full-text matching of requests to skills | input-analysis |
| `quality-guardian` | Enforces G0-G3 quality gates on all output | code-review, security-testing |
| `context-manager` | Token optimization, RAG priming, session state | input-analysis |

### Discovery & Analysis (20)

| Agent | Role | Trigger Keywords |
|-------|------|-----------------|
| `requirements-analyst` | User stories, acceptance criteria | "requirements", "user stories", "acceptance criteria" |
| `stakeholder-mapper` | Influence/interest matrix, RACI | "stakeholders", "RACI", "influence matrix" |
| `domain-modeler` | DDD bounded contexts, entity mapping | "domain model", "entities", "DDD" |
| `flow-mapper` | End-to-end business flows, swimlanes | "flows", "process map", "swimlane" |
| `scenario-evaluator` | Multi-scenario comparison, trade-offs | "scenarios", "compare options", "trade-offs" |
| `feasibility-validator` | Technical/business viability checks | "feasibility", "viable", "can we build" |
| `risk-analyst` | Risk register, mitigation strategies | "risks", "what could go wrong" |
| `competitive-analyst` | Market positioning, SWOT | "competitors", "market analysis", "SWOT" |
| `user-researcher` | Personas, user journeys, interviews | "users", "personas", "user research" |
| `business-analyst` | Business rules, process modeling | "business rules", "process", "workflow" |
| `cost-estimator` | Effort estimation, team sizing | "cost", "estimate", "team size" |
| `data-strategist` | Data architecture, governance | "data strategy", "data governance" |
| `data-modeler` | ER diagrams, normalization | "data model", "ER diagram" |
| `industry-expert` | Sector-specific context | "industry", "regulations", "compliance" |
| `compliance-checker` | GDPR, PCI-DSS, SOC2 checks | "compliance", "GDPR", "regulations" |
| `product-strategist` | Roadmap, prioritization | "roadmap", "MVP", "prioritize" |
| `change-catalyst` | Adoption strategy, training | "change management", "adoption" |
| `input-amplifier` | Enriches vague inputs | (automatic on all inputs) |
| `pitch-crafter` | Executive presentations | "pitch", "executive summary" |
| `discovery-reporter` | Compiles analysis into documents | "report", "summary", "document" |
| `workshop-facilitator` | Event storming, design sprints | "workshop", "event storming" |

### Architecture & Design (20)

| Agent | Role | Trigger Keywords |
|-------|------|-----------------|
| `architecture-designer` | C4 diagrams, system design, ADRs | "architecture", "system design", "C4" |
| `api-designer` | REST/GraphQL contracts | "API", "endpoints", "REST" |
| `database-architect` | Schema design, indexing, sharding | "database", "schema", "queries" |
| `security-architect` | Threat modeling, auth design | "security", "threats", "encryption" |
| `event-designer` | Event-driven patterns, CQRS | "events", "CQRS", "pub/sub" |
| `state-designer` | State management patterns | "state management", "store" |
| `auth-architect` | OAuth, RBAC, session design | "authentication", "authorization", "RBAC" |
| `pwa-architect` | Service workers, offline-first | "PWA", "offline", "service worker" |
| `performance-architect` | Caching, CDN, optimization | "performance", "caching", "CDN" |
| `seo-architect` | SEO strategy, structured data | "SEO", "structured data", "meta tags" |
| `component-designer` | UI component architecture | "components", "design system" |
| `responsive-designer` | Breakpoints, fluid layouts | "responsive", "mobile-first" |
| `accessibility-designer` | WCAG patterns, ARIA | "accessibility", "WCAG", "ARIA" |
| `design-system-architect` | Token systems, style guides | "design system", "tokens", "style guide" |
| `realtime-designer` | WebSocket, Firestore listeners | "real-time", "live updates" |
| `caching-strategist` | Cache invalidation, strategies | "cache", "invalidation" |
| `migration-planner` | Modernization, strangler fig | "migration", "modernization" |
| `infrastructure-planner` | Hosting, DNS, CDN | "infrastructure", "hosting" |
| `solutions-architect` | End-to-end integration | "integration", "full solution" |
| `diagram-specialist` | Mermaid, C4, sequence diagrams | "diagram", "Mermaid", "visualize" |

### Frontend Development (20)

| Agent | Role | Trigger Keywords |
|-------|------|-----------------|
| `frontend-craftsman` | HTML5 + CSS3 + vanilla JS baseline | "HTML", "CSS", "frontend" |
| `angular-specialist` | Angular 18+, Signals, standalone | "Angular", "Signals", "NgModule" |
| `react-specialist` | React 19+, hooks, Server Components | "React", "hooks", "JSX" |
| `vanilla-js-specialist` | DOM APIs, ES modules, Web APIs | "vanilla JS", "DOM", "Web API" |
| `css-architect` | CSS Layers, custom properties, Grid | "CSS", "styles", "layout" |
| `html-specialist` | Semantic HTML, landmarks, forms | "semantic HTML", "landmarks" |
| `typescript-specialist` | Type design, generics, patterns | "TypeScript", "types", "generics" |
| `animation-specialist` | CSS animations, Web Animations API | "animation", "transition", "motion" |
| `form-specialist` | Validation, accessibility, UX | "form", "validation", "input" |
| `chart-specialist` | Data viz, Chart.js, D3 | "chart", "graph", "visualization" |
| `dashboard-builder` | Admin panels, data grids | "dashboard", "admin panel" |
| `ecommerce-builder` | Product pages, cart, checkout | "e-commerce", "cart", "checkout" |
| `landing-page-builder` | Hero sections, CTAs, conversion | "landing page", "CTA" |
| `portfolio-builder` | Showcase sites, galleries | "portfolio", "showcase" |
| `blog-builder` | CMS templates, article layouts | "blog", "articles", "CMS" |
| `email-template-builder` | Table-based email HTML | "email template", "newsletter" |
| `map-specialist` | Google Maps integration | "map", "Google Maps", "geolocation" |
| `i18n-specialist` | Multi-language, RTL support | "i18n", "translation", "multilingual" |
| `web-component-builder` | Custom elements, Shadow DOM | "web component", "custom element" |
| `a11y-implementer` | ARIA implementation, screen readers | "ARIA", "screen reader" |

### Backend & Firebase (15)

| Agent | Role | Trigger Keywords |
|-------|------|-----------------|
| `firebase-specialist` | Full Firebase stack orchestration | "Firebase", "setup", "configure" |
| `node-specialist` | Node.js, Express, Cloud Functions | "Node.js", "Express", "backend" |
| `cloud-functions-dev` | Triggers, scheduling, secrets | "Cloud Functions", "trigger" |
| `firestore-expert` | Collections, queries, denormalization | "Firestore", "collection", "query" |
| `firebase-auth-expert` | Login flows, providers, custom claims | "Firebase Auth", "login", "sign-in" |
| `firebase-storage-expert` | File uploads, resize, security | "Storage", "upload", "file" |
| `firebase-hosting-expert` | Deploy config, rewrites, headers | "Firebase Hosting", "deploy" |
| `firebase-emulator-expert` | Local development, testing | "emulator", "local dev" |
| `firebase-deployer` | Multi-service deployment | "deploy Firebase" |
| `rest-api-builder` | RESTful endpoints, middleware | "REST API", "endpoint" |
| `webhook-specialist` | Webhook handlers, signatures | "webhook", "callback" |
| `email-service-specialist` | SendGrid, Trigger Email ext. | "email sending", "SendGrid" |
| `payment-specialist` | Stripe, PayPal integration | "payment", "Stripe", "checkout" |
| `push-notification-specialist` | FCM, notification channels | "push notification", "FCM" |
| `cron-job-specialist` | Scheduled functions, recurring | "cron", "schedule", "recurring" |

### Quality & Testing (12)

| Agent | Role | Trigger Keywords |
|-------|------|-----------------|
| `quality-engineer` | Test strategy, automation architecture | "testing", "quality", "test strategy" |
| `unit-test-writer` | Jest, Vitest, Jasmine | "unit test", "Jest", "Vitest" |
| `e2e-test-writer` | Playwright, Cypress | "E2E", "Playwright", "end-to-end" |
| `performance-tester` | Lighthouse, Web Vitals, load testing | "Lighthouse", "performance audit" |
| `accessibility-auditor` | axe-core, WCAG compliance | "accessibility audit", "WCAG" |
| `security-scanner` | OWASP, dependency audit | "security scan", "vulnerabilities" |
| `code-reviewer` | Code quality, patterns, smells | "code review", "review my code" |
| `linter-configurator` | ESLint, Prettier, Stylelint | "linter", "ESLint", "formatting" |
| `bundle-analyzer` | Bundle size, tree-shaking | "bundle size", "tree-shaking" |
| `seo-auditor` | Technical SEO, structured data | "SEO audit", "meta tags" |
| `cross-browser-tester` | Compatibility, polyfills | "browser compatibility", "polyfill" |
| `mobile-responsiveness-tester` | Viewport testing, touch targets | "mobile test", "responsive test" |

### Deployment & Operations (5)

| Agent | Role | Trigger Keywords |
|-------|------|-----------------|
| `deployment-specialist` | Deploy orchestration | "deploy", "ship", "go live" |
| `hostinger-expert` | Shared hosting, FTP, .htaccess | "Hostinger", "shared hosting" |
| `domain-dns-specialist` | DNS, SSL, domain config | "DNS", "domain", "SSL" |
| `ci-cd-configurator` | GitHub Actions, pipelines | "CI/CD", "GitHub Actions" |

### Documentation (4)

| Agent | Role | Trigger Keywords |
|-------|------|-----------------|
| `technical-writer` | Docs, ADRs, runbooks | "documentation", "ADR", "write docs" |
| `copywriter` | Marketing copy, product text | "copy", "marketing text" |
| `evidence-auditor` | Validates evidence tags | "audit evidence", "check tags" |

---

## Skills (101)

### Discovery & Analysis (20)

| Skill | Description | Used By |
|-------|-------------|---------|
| `requirements-engineering` | User stories, acceptance criteria, traceability | requirements-analyst |
| `stakeholder-mapping` | Influence matrix, communication plan | stakeholder-mapper |
| `domain-driven-design` | Bounded contexts, aggregates, entities | domain-modeler |
| `flow-mapping` | Business flows, integration points | flow-mapper |
| `scenario-analysis` | Multi-scenario comparison, scoring | scenario-evaluator |
| `feasibility-validation` | Technical/business viability | feasibility-validator |
| `risk-assessment` | Risk register, probability/impact | risk-analyst |
| `competitive-intelligence` | Market analysis, SWOT | competitive-analyst |
| `user-research` | Personas, journey maps | user-researcher |
| `business-process-modeling` | BPMN, process optimization | business-analyst |
| `cost-estimation` | Effort drivers, team sizing | cost-estimator |
| `data-strategy` | Data architecture, governance | data-strategist |
| `change-readiness` | Adoption assessment | change-catalyst |
| `compliance-assessment` | Regulatory checks | compliance-checker |
| `product-roadmapping` | Prioritization, MVP scoping | product-strategist |
| `sector-intelligence` | Industry context | industry-expert |
| `discovery-orchestration` | Pipeline coordination | pipeline-conductor |
| `executive-pitch` | C-level presentations | pitch-crafter |
| `input-analysis` | Input enrichment, intent detection | input-amplifier |
| `workshop-design` | Facilitation blueprints | workshop-facilitator |

### Architecture & Design (20)

| Skill | Description | Used By |
|-------|-------------|---------|
| `system-architecture` | C4, ADRs, quality attributes | architecture-designer |
| `api-design` | REST/GraphQL contracts, versioning | api-designer |
| `database-design` | Schema, indexing, partitioning | database-architect |
| `security-architecture` | Threat model, zero trust | security-architect |
| `event-architecture` | Event catalog, CQRS, saga | event-designer |
| `state-management` | Patterns, reactivity | state-designer |
| `auth-architecture` | OAuth, RBAC, sessions | auth-architect |
| `pwa-architecture` | Service workers, manifest | pwa-architect |
| `performance-architecture` | Caching, CDN, budgets | performance-architect |
| `seo-architecture` | Technical SEO, structured data | seo-architect |
| `component-architecture` | Design systems, atomic design | component-designer |
| `responsive-design` | Breakpoints, fluid typography | responsive-designer |
| `accessibility-design` | WCAG patterns, ARIA | accessibility-designer |
| `design-system` | Tokens, component library | design-system-architect |
| `realtime-architecture` | WebSockets, Firestore listeners | realtime-designer |
| `caching-strategy` | Cache layers, invalidation | caching-strategist |
| `migration-planning` | Strangler fig, cutover | migration-planner |
| `infrastructure-design` | Hosting, DNS, CDN | infrastructure-planner |
| `mermaid-diagramming` | Architecture visualization | diagram-specialist |
| `trade-off-analysis` | Weighted decision matrices | architecture-designer |

### Frontend Development (25)

| Skill | Description | Used By |
|-------|-------------|---------|
| `html-semantic` | Landmarks, ARIA, forms | frontend-craftsman, html-specialist |
| `css-architecture` | Layers, custom properties, Grid | css-architect |
| `vanilla-javascript` | DOM, ES modules, Web APIs | vanilla-js-specialist |
| `angular-development` | Signals, standalone, routing | angular-specialist |
| `react-development` | Hooks, Server Components | react-specialist |
| `typescript-patterns` | Generics, utility types | typescript-specialist |
| `css-animation` | Transitions, keyframes, WAAPI | animation-specialist |
| `form-engineering` | Validation, a11y, multi-step | form-specialist |
| `data-visualization` | Charts, graphs, D3 | chart-specialist |
| `google-maps-integration` | Maps, markers, geolocation | map-specialist |
| `internationalization` | i18n, L10n, RTL | i18n-specialist |
| `web-components` | Custom elements, Shadow DOM | web-component-builder |
| `email-templates` | Table-based email HTML | email-template-builder |
| `landing-pages` | Hero, CTA, conversion | landing-page-builder |
| `admin-dashboards` | Data grids, charts, filters | dashboard-builder |
| `ecommerce-frontend` | Product pages, cart UI | ecommerce-builder |
| `blog-cms` | Article layouts, pagination | blog-builder |
| `portfolio-sites` | Showcase, galleries | portfolio-builder |
| `image-optimization` | WebP, lazy load, srcset | frontend-craftsman |
| `font-optimization` | Subsetting, FOUT/FOIT | css-architect |
| `scroll-interaction` | Intersection Observer, parallax | animation-specialist |
| `modal-dialog-patterns` | Accessible dialogs, focus trap | form-specialist |
| `navigation-patterns` | Menus, breadcrumbs, tabs | frontend-craftsman |
| `dark-mode` | Color scheme, toggle, storage | css-architect |
| `print-stylesheet` | Print-friendly layouts | css-architect |

### Backend & Firebase (20)

| Skill | Description | Used By |
|-------|-------------|---------|
| `firebase-setup` | Project init, emulators, config | firebase-specialist |
| `firestore-modeling` | Collections, denormalization | firestore-expert |
| `firestore-queries` | Compound queries, pagination | firestore-expert |
| `firestore-security-rules` | Rules DSL, testing | firestore-expert |
| `firebase-auth` | Providers, custom claims | firebase-auth-expert |
| `firebase-storage` | Upload, resize, security | firebase-storage-expert |
| `cloud-functions` | Triggers, v2, secrets | cloud-functions-dev |
| `firebase-hosting` | Rewrites, headers, channels | firebase-hosting-expert |
| `firebase-extensions` | Marketplace extensions | firebase-specialist |
| `google-workspace-apis` | Sheets, Drive, Calendar | google-apis-specialist |
| `google-analytics` | GA4, events, conversions | google-apis-specialist |
| `recaptcha-integration` | reCAPTCHA v3, scoring | google-apis-specialist |
| `rest-api-development` | Express routes, middleware | rest-api-builder |
| `webhook-handling` | Signatures, idempotency | webhook-specialist |
| `email-sending` | Transactional, templates | email-service-specialist |
| `payment-integration` | Stripe, PayPal, checkout | payment-specialist |
| `push-notifications` | FCM, topics, scheduling | push-notification-specialist |
| `scheduled-functions` | Cron triggers, rate limits | cron-job-specialist |
| `node-development` | Node.js patterns, streams | node-specialist |
| `serverless-patterns` | Cold starts, fan-out | cloud-functions-dev |

### Quality & Testing (10)

| Skill | Description | Used By |
|-------|-------------|---------|
| `test-strategy` | Pyramid, automation plan | quality-engineer |
| `unit-testing` | Jest, Vitest, mocking | unit-test-writer |
| `e2e-testing` | Playwright, Cypress | e2e-test-writer |
| `performance-testing` | Lighthouse, Web Vitals | performance-tester |
| `accessibility-testing` | axe-core, screen readers | accessibility-auditor |
| `security-testing` | OWASP top 10, CSP | security-scanner |
| `code-review` | Patterns, anti-patterns | code-reviewer |
| `linting-formatting` | ESLint, Prettier config | linter-configurator |
| `cross-browser-testing` | Compatibility matrices | cross-browser-tester |
| `visual-regression` | Screenshot comparison | quality-engineer |

### Deployment & Operations (6)

| Skill | Description | Used By |
|-------|-------------|---------|
| `hostinger-deployment` | FTP, .htaccess, SSL | hostinger-expert |
| `firebase-deployment` | Multi-service deploy | firebase-deployer |
| `github-actions-ci` | Workflow authoring | ci-cd-configurator |
| `domain-management` | DNS, SSL, redirects | domain-dns-specialist |
| `build-optimization` | Minification, splitting | bundle-analyzer |
| `deployment-checklist` | Pre-deploy validation | deployment-specialist |

---

## Commands Quick Reference (catalog snapshot)

### Pipeline (10)

```
/jm-adk:menu             Show command palette
/jm-adk:analyze           Full analysis pipeline
/jm-adk:develop           Full development pipeline
/jm-adk:express           Quick: scaffold → build → deploy
/jm-adk:auto              Autonomous mode (minimal prompts)
/jm-adk:guided            Guided mode (checkpoints)
/jm-adk:ship              Build + deploy
/jm-adk:search <query>    Search skills by keyword
/jm-adk:status            Project status
/jm-adk:init              Initialize governance files
```

### Discovery (12)

```
/jm-adk:discover          Run discovery sub-pipeline
/jm-adk:requirements      Extract requirements
/jm-adk:stakeholders      Map stakeholders
/jm-adk:domain-map        Model domain
/jm-adk:flows             Map business flows
/jm-adk:scenarios         Compare scenarios
/jm-adk:feasibility       Validate feasibility
/jm-adk:pitch             Create executive pitch
/jm-adk:competition       Analyze competitors
/jm-adk:user-research     Research users/personas
/jm-adk:risks             Assess risks
/jm-adk:workshop          Plan workshop
```

### Architecture (8)

```
/jm-adk:architect         Full architecture design
/jm-adk:design-api        Design API contracts
/jm-adk:design-db         Design database schema
/jm-adk:design-auth       Design auth architecture
/jm-adk:design-state      Design state management
/jm-adk:design-events     Design event architecture
/jm-adk:adr               Create Architecture Decision Record
/jm-adk:diagram           Generate Mermaid diagram
```

### Scaffold (5)

```
/jm-adk:scaffold-firebase   Firebase + vanilla JS project
/jm-adk:scaffold-angular    Angular 18+ + Firebase
/jm-adk:scaffold-react      React 19+ + Firebase
/jm-adk:scaffold-vanilla    Pure HTML/CSS/JS (no framework)
/jm-adk:scaffold-node       Node.js API (Cloud Functions)
```

### Create (15+)

```
/jm-adk:create-page         New page
/jm-adk:create-component    New component
/jm-adk:create-form         Form with validation
/jm-adk:create-api          API endpoint
/jm-adk:create-crud         Firestore CRUD operations
/jm-adk:create-auth         Authentication flow
/jm-adk:create-dashboard    Admin dashboard
/jm-adk:create-landing      Landing page
/jm-adk:create-nav          Navigation component
/jm-adk:create-modal        Modal/dialog
/jm-adk:create-table        Data table
/jm-adk:create-chart        Chart component
/jm-adk:create-map          Google Maps integration
/jm-adk:create-search       Search component
/jm-adk:create-payment      Payment checkout
```

### Quality (8)

```
/jm-adk:review             Code review + quality gates
/jm-adk:audit-perf         Lighthouse performance audit
/jm-adk:audit-a11y         Accessibility audit
/jm-adk:audit-security     Security scan
/jm-adk:audit-seo          SEO audit
/jm-adk:test               Run tests
/jm-adk:lint               Run linters
/jm-adk:audit-bundle       Bundle size analysis
```

### Deploy (6)

```
/jm-adk:deploy-hostinger   Deploy to Hostinger
/jm-adk:deploy-firebase    Deploy to Firebase Hosting
/jm-adk:setup-ci           Configure GitHub Actions
/jm-adk:rollback           Rollback deployment
/jm-adk:pre-deploy         Pre-deploy checklist
/jm-adk:configure-domain   DNS + SSL setup
```

### Evolve & Repair (5)

```
/jm-adk:evolve             Improve existing code
/jm-adk:repair             Debug and fix issues
/jm-adk:refactor           Refactor code
/jm-adk:optimize           Performance optimization
/jm-adk:migrate            Migrate/modernize code
```

---

*Made with Claude Code and Tons of Love with the Help of Pristino Agent*
