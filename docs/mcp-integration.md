# MCP Integration Guide

How to extend JM-ADK with Model Context Protocol (MCP) servers for external tools, databases, and APIs.

## What is MCP?

The [Model Context Protocol](https://modelcontextprotocol.io/) allows Claude Code to connect to external services — databases, APIs, search engines, and more — through a standardized interface. JM-ADK can leverage MCP servers to enrich its analysis and development capabilities.

## Supported MCP Server Types

| Type | Transport | Use Case |
|------|-----------|----------|
| `stdio` | Standard I/O | Local tools (file processors, linters, scripts) |
| `sse` | Server-Sent Events | Remote APIs with streaming |
| `http` | HTTP POST | REST-based tool servers |

## Setup

### Option 1: Project-Level Configuration

Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "description": "Up-to-date documentation for any library"
    },
    "firebase-admin": {
      "command": "npx",
      "args": ["-y", "firebase-mcp-server"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "./service-account.json"
      },
      "description": "Direct Firestore/Auth/Storage access"
    }
  }
}
```

### Option 2: Global Configuration

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/github-mcp-server"],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    }
  }
}
```

### Option 3: Plugin-Level MCP

Add `.mcp.json` inside the JM-ADK plugin directory for servers that ship with the kit:

```json
{
  "mcpServers": {
    "skill-search": {
      "command": "python3",
      "args": ["${CLAUDE_PLUGIN_ROOT}/.agent/scripts/search_skills.py", "--mcp"],
      "description": "BM25 skill search over the compatibility skill index"
    }
  }
}
```

## Recommended MCP Servers for JM-ADK

### For Discovery & Analysis

| Server | Purpose | Install |
|--------|---------|---------|
| **Context7** | Library documentation lookup | `npx @upstash/context7-mcp@latest` |
| **GitHub** | Issue/PR/repo analysis | `npx @anthropic/github-mcp-server` |
| **Playwright** | Web scraping for competitive analysis | `npx @anthropic/playwright-mcp-server` |

### For Firebase Development

| Server | Purpose | Install |
|--------|---------|---------|
| **Firebase Admin** | Direct Firestore/Auth/Storage access | `npx firebase-mcp-server` |
| **Google Cloud** | GCP service management | `npx @anthropic/gcloud-mcp-server` |

### For Quality & Testing

| Server | Purpose | Install |
|--------|---------|---------|
| **Lighthouse** | Performance/a11y auditing | `npx lighthouse-mcp-server` |
| **Playwright** | E2E testing and screenshots | `npx @anthropic/playwright-mcp-server` |

### For Google Workspace (Gmail, Calendar, Drive, Docs, Sheets, Slides, Forms, Tasks, Contacts)

| Server | Purpose | Install |
|--------|---------|---------|
| **workspace-mcp** | Unified: Gmail, Calendar, Drive, Docs, Sheets, Slides, Forms, Tasks, Contacts (90+ tools) | `uvx workspace-mcp` |

**Setup guide**: [`docs/google-workspace-mcp-setup.md`](./google-workspace-mcp-setup.md)

**Project `.mcp.json`** includes the unified server with tool-tier `extended`. After OAuth2 setup, these skills are available:

| Skill | Google Service | Key Tools |
|-------|---------------|-----------|
| `gmail-mcp` | Gmail | search, send, draft, labels, filters |
| `google-calendar-mcp` | Calendar | events, calendars, Meet, out-of-office |
| `google-drive-mcp` | Drive | files, folders, search, share, permissions |
| `google-docs-mcp` | Docs | create, edit, format, export, markdown |
| `google-sheets-mcp` | Sheets | read, write, format, create |
| `google-slides-mcp` | Slides | create, update, thumbnails |

Office workflow skills (`follow-up-email`, `acta-formal`, `folio-generator`, `inventory-management`, `sales-tracker`) use these MCP tools through the `office-workflow-runner` orchestrator.

### For Deployment

| Server | Purpose | Install |
|--------|---------|---------|
| **Cloudflare** | DNS and CDN management | `npx @anthropic/cloudflare-mcp-server` |
| **GitHub** | CI/CD and release management | `npx @anthropic/github-mcp-server` |

## Usage Examples

### Example 1: Library Docs During Development

With Context7 configured, JM-ADK agents can pull current documentation:

```
User: /jm-adk:create-component name="data-table" framework=angular

# Behind the scenes, the angular-specialist agent can query:
# context7:query-docs library="angular" topic="signals standalone components"
# to get up-to-date Angular 18+ patterns before generating code
```

### Example 2: Firebase Data During Analysis

With Firebase Admin configured:

```
User: /jm-adk:analyze input="Optimize our Firestore queries for the orders collection"

# The firestore-expert agent can:
# 1. Read actual collection schemas from Firestore
# 2. Analyze existing security rules
# 3. Check index configurations
# 4. Propose optimizations based on real data patterns
```

### Example 3: Competitive Analysis with Playwright

```
User: /jm-adk:analyze input="Build a landing page for our SaaS product"

# The scenario-evaluator agent can:
# 1. Navigate competitor websites via Playwright
# 2. Take screenshots for reference
# 3. Analyze design patterns and features
# 4. Feed findings into the analysis pipeline
```

## Creating a Custom MCP Server

If you need a specialized tool for your workflow:

### 1. Define the Server

```typescript
// my-tool-server.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-custom-tool",
  version: "1.0.0",
});

server.tool(
  "analyze-bundle",
  "Analyze JavaScript bundle size and composition",
  { entryPoint: z.string().describe("Path to the entry point") },
  async ({ entryPoint }) => {
    // Your analysis logic here
    return {
      content: [{ type: "text", text: JSON.stringify(result) }],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### 2. Register It

```json
{
  "mcpServers": {
    "bundle-analyzer": {
      "command": "npx",
      "args": ["tsx", "./tools/my-tool-server.ts"]
    }
  }
}
```

### 3. Use It in a Skill

Reference the tool in your skill's `allowed-tools`:

```yaml
---
name: bundle-optimization
allowed-tools:
  - Read
  - Glob
  - Bash
  - mcp__bundle-analyzer__analyze-bundle
---
```

## Troubleshooting

### Server not connecting

```bash
# Test the server manually
echo '{"jsonrpc":"2.0","method":"initialize","params":{"capabilities":{}},"id":1}' | npx your-mcp-server
```

### Tools not appearing

1. Check server is listed in `.mcp.json` or `settings.json`
2. Restart Claude Code (`exit` + relaunch)
3. Verify with `/mcp` command

### Timeout issues

Add timeout configuration:

```json
{
  "mcpServers": {
    "slow-server": {
      "command": "npx",
      "args": ["slow-mcp-server"],
      "timeout": 30000
    }
  }
}
```

## Security Considerations

- **Never commit** `.mcp.json` files with secrets — add to `.gitignore`
- Use environment variables for tokens: `"env": { "TOKEN": "$MY_TOKEN" }`
- Scope MCP servers to project level when possible (not global)
- Review MCP server source code before installation — they have full tool access

---

*Made with Claude Code and Tons of Love with the Help of Pristino Agent*
