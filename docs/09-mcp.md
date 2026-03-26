# Module 09 — MCP Servers

**Prerequisites:** [Module 08](08-scheduling.md)  
**Time:** ~35 minutes  
**Next:** [Module 10 — Plugins & Marketplace](10-plugins.md)

---

## What MCP is

**MCP (Model Context Protocol)** is an open standard created by Anthropic that lets AI agents connect to external tools and data sources using a consistent interface.

Key point: MCP is not Claude Code-specific. Any AI client (Claude Code, Claude.ai, VS Code, Cursor) can connect to any MCP server using the same protocol. It's a standard — like REST or GraphQL — not a product.

---

## The USB-C analogy

The best way to understand MCP:

> MCP is a USB-C port. External tools are the devices (webcam, microphone, hard drive). The JSON config is the cable. You plug in any device — the protocol is always the same.

```
Claude Code
    │
    │  (one JSON config per server)
    ├──── MCP Server: Gmail    →  read/send emails
    ├──── MCP Server: GitHub   →  repos, PRs, issues
    ├──── MCP Server: Snowflake→  query your data warehouse
    ├──── MCP Server: Browser  →  web browsing, scraping
    └──── MCP Server: Slack    →  messages, channels
```

The same JSON config works in Claude Code, VS Code with Copilot, Cursor, and Claude.ai Pro. Write once, use anywhere.

---

## Local vs hosted MCP servers

### Local MCP servers
The server code runs on your machine. Claude Code executes it via `uvx` (Python) or `npx` (Node.js).

```json
{
  "mcpServers": {
    "github": {
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token-here"
      }
    }
  }
}
```

**Most MCP servers today are local.** The ecosystem is still migrating to hosted.

### Hosted MCP servers
The server runs in the cloud. Claude Code connects over HTTP.

```json
{
  "mcpServers": {
    "my-service": {
      "type": "http",
      "url": "https://mcp.myservice.com/sse",
      "headers": {
        "Authorization": "Bearer your-api-key"
      }
    }
  }
}
```

Hosted servers are newer (streamable HTTP was added recently) and not yet universal. Expect more services to offer hosted MCP over the next year.

---

## The MCP config file

Claude Code reads MCP configuration from `.claude/settings.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "/home/user/projects"]
    },
    "github": {
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "uvx",
      "args": ["mcp-server-postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

After adding a new server to settings.json, restart Claude Code. Use `/context` to verify the new tools appear under "MCP tools".

---

## What MCP enables that skills can't

Skills let you orchestrate Claude Code's *built-in* tools. MCP lets Claude Code interact with *any external system*:

| Without MCP | With MCP |
|---|---|
| Can read/write local files | Can read/write Google Drive, Notion, Confluence |
| Can run local scripts | Can trigger GitHub Actions, Jira tickets, Slack messages |
| Can call public APIs (via custom script) | Can query authenticated internal systems directly |
| Can scrape public websites | Can operate authenticated browser sessions |

---

## Practical MCP setup examples

### Connect to GitHub
```bash
# Install the server
pip install mcp-server-github

# Add to settings.json
```
```json
{
  "mcpServers": {
    "github": {
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": { "GITHUB_TOKEN": "ghp_your_token" }
    }
  }
}
```

Now Claude Code can:
```
List all open PRs assigned to me
Create a GitHub issue for the bug I just found
Review the diff for PR #142 and suggest improvements
```

### Connect to a Postgres database
```json
{
  "mcpServers": {
    "postgres": {
      "command": "uvx",
      "args": ["mcp-server-postgres", "postgresql://user:pass@localhost/mydb"]
    }
  }
}
```

Now Claude Code can:
```
Show me the schema of the fact_sales table
Write a query to find the top 10 customers by revenue this month
Explain why this query is running slowly
```

### Connect to Snowflake (data engineering)
```json
{
  "mcpServers": {
    "snowflake": {
      "command": "uvx",
      "args": ["mcp-server-snowflake"],
      "env": {
        "SNOWFLAKE_ACCOUNT": "your-account",
        "SNOWFLAKE_USER": "your-user",
        "SNOWFLAKE_PASSWORD": "${SNOWFLAKE_PASSWORD}",
        "SNOWFLAKE_WAREHOUSE": "COMPUTE_WH",
        "SNOWFLAKE_DATABASE": "PROD_DB"
      }
    }
  }
}
```

---

## Finding MCP servers

The community has built servers for dozens of tools. Find them at:

- [smithery.ai](https://smithery.ai) — curated registry with install commands
- [skills.mp](https://skills.mp) — skills + MCPs combined
- GitHub: search `mcp-server-*`
- Anthropic's official servers: `github.com/anthropics/mcp-servers`

---

## Security considerations

MCP servers run on your machine with your credentials. Before installing any MCP server:
- Check it's from a trusted source (official Anthropic repos, or well-known community projects)
- Review what permissions it requests
- Use environment variables for credentials — never hardcode them in settings.json
- Use `${ENV_VAR}` syntax to pull from your system environment

---

## Check your understanding

1. What does MCP stand for, and who created it?
2. What is the difference between a local and a hosted MCP server?
3. Explain the USB-C analogy in your own words.
4. What can MCP do that skills alone cannot?
5. How do you verify that a new MCP server was loaded correctly?

→ Full quiz: [quizzes/module-09.md](../quizzes/module-09.md)  
→ Cheatsheet: [cheatsheets/mcp-config.md](../cheatsheets/mcp-config.md)

---

**Next:** [Module 10 — Plugins & Marketplace →](10-plugins.md)
