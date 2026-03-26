# Example: Hosted MCP Server

Hosted MCP servers run in the cloud — Claude Code connects over HTTP rather than
executing a local process. This is the newer pattern (streamable HTTP was added
to the MCP spec recently). Not all services have migrated yet.

---

## When to use hosted vs local

| Use hosted when | Use local when |
|---|---|
| The service provides an official hosted MCP URL | You need to access local files or databases |
| You don't want to install packages locally | The server requires local system access |
| You need the latest server version automatically | You want to control the exact version |
| The MCP runs on the vendor's infrastructure | Security policy requires local execution |

---

## Config format for hosted servers

```json
{
  "mcpServers": {
    "server-name": {
      "type": "http",
      "url": "https://mcp.service.com/sse",
      "headers": {
        "Authorization": "Bearer ${SERVICE_API_KEY}"
      }
    }
  }
}
```

The `type: "http"` field distinguishes hosted from local servers.

---

## Example 1: Notion MCP (hosted)

Notion provides an official hosted MCP server.

### Get credentials

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Create a new integration → copy the Internal Integration Token
3. Share the pages/databases you want Claude Code to access with the integration

### Configure

```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/sse",
      "headers": {
        "Authorization": "Bearer ${NOTION_TOKEN}"
      }
    }
  }
}
```

```bash
export NOTION_TOKEN="secret_your_token_here"
```

### Use it

```
What pages do I have in my Engineering workspace?
Create a new page called "Claude Code Notes" in my Personal space
Append these meeting notes to my "Sprint Planning" page
```

---

## Example 2: Anthropic-hosted MCP (via Claude.ai Pro)

Claude.ai Pro and Team plans include pre-connected hosted MCP servers accessible
directly from Claude Code with no configuration.

When using a Pro subscription, run `/plugins` and look for connectors like:
- Google Drive
- Slack
- GitHub (hosted variant)
- Jira/Confluence (Atlassian)

These appear as plugins in the marketplace and configure themselves automatically
once you authorize the connection in the Claude.ai web interface.

---

## Example 3: Custom hosted MCP (self-hosted)

If your organisation runs its own MCP server (e.g., for internal databases or
proprietary tools), the config is the same pattern:

```json
{
  "mcpServers": {
    "internal-data": {
      "type": "http",
      "url": "https://mcp.internal.yourcompany.com/sse",
      "headers": {
        "Authorization": "Bearer ${INTERNAL_MCP_TOKEN}",
        "X-Workspace-ID": "${WORKSPACE_ID}"
      }
    }
  }
}
```

Your platform team provides the URL and auth mechanism.

---

## Mixing local and hosted

You can have both types in one `settings.json`:

```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/sse",
      "headers": { "Authorization": "Bearer ${NOTION_TOKEN}" }
    },
    "github": {
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "postgres": {
      "command": "uvx",
      "args": ["mcp-server-postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

---

## Troubleshooting hosted servers

| Problem | Fix |
|---|---|
| `Connection refused` or timeout | Check the URL is correct; verify the service is reachable |
| `401 Unauthorized` | Token is wrong or expired; regenerate and re-export the env var |
| Server appears in config but not in `/context` | The service may not be running or the URL may have changed |
| `SSL certificate error` | The server's cert may be self-signed; check with your platform team |

---

## Finding hosted MCP servers

Most vendors are still running local-only servers. Check vendor docs specifically for:
- "MCP server" or "Model Context Protocol"
- "Claude Code integration"
- "AI agent integration"

Current services with known hosted MCP support (verify with their latest docs):
- Notion (`mcp.notion.com`)
- Linear (check their integrations page)
- Zapier (via their AI Actions product)

---

## See also

- [Local MCP example](../mcp-local/) — the more common local server setup
- [Cheatsheet](../../cheatsheets/mcp-config.md) — full config reference
