# Cheatsheet — MCP Server Configuration

---

## Config file location

```
.claude/
└── settings.json      ← project-level (recommended)

~/.claude/
└── settings.json      ← system-level (all projects)
```

---

## Config format

```json
{
  "mcpServers": {
    "server-name": {
      "command": "uvx",
      "args": ["mcp-server-package-name", "optional-arg"],
      "env": {
        "API_KEY": "${ENV_VAR_NAME}"
      }
    }
  }
}
```

**Always use `${ENV_VAR}` for credentials** — never hardcode tokens in the config file.

---

## Local server patterns

### Python server (uvx)
```json
{
  "mcpServers": {
    "my-server": {
      "command": "uvx",
      "args": ["mcp-server-package-name"]
    }
  }
}
```

### Node.js server (npx)
```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "@scope/mcp-server-name"]
    }
  }
}
```

---

## Hosted server pattern (HTTP)

```json
{
  "mcpServers": {
    "my-hosted-server": {
      "type": "http",
      "url": "https://mcp.service.com/sse",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

---

## Common server configs

### GitHub
```json
"github": {
  "command": "uvx",
  "args": ["mcp-server-github"],
  "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
}
```

### PostgreSQL
```json
"postgres": {
  "command": "uvx",
  "args": ["mcp-server-postgres", "postgresql://user:pass@localhost/dbname"]
}
```

### Snowflake
```json
"snowflake": {
  "command": "uvx",
  "args": ["mcp-server-snowflake"],
  "env": {
    "SNOWFLAKE_ACCOUNT": "${SF_ACCOUNT}",
    "SNOWFLAKE_USER": "${SF_USER}",
    "SNOWFLAKE_PASSWORD": "${SF_PASSWORD}",
    "SNOWFLAKE_WAREHOUSE": "COMPUTE_WH",
    "SNOWFLAKE_DATABASE": "PROD_DB"
  }
}
```

### Filesystem (extended access)
```json
"filesystem": {
  "command": "uvx",
  "args": ["mcp-server-filesystem", "/path/to/allow"]
}
```

### Slack
```json
"slack": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-slack"],
  "env": {
    "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
    "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
  }
}
```

### Notion
```json
"notion": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-notion"],
  "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" }
}
```

### Google Drive
```json
"gdrive": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-gdrive"],
  "env": { "GDRIVE_CREDENTIALS": "${GDRIVE_CREDENTIALS}" }
}
```

---

## Verify a server loaded

After adding a server, restart Claude Code and run:

```
/context
```

Look for the server name under "MCP tools". If it's missing, check:
1. The server package is installed (`pip show mcp-server-name` or `npm list -g`)
2. Environment variables are set in your shell
3. The JSON syntax in settings.json is valid (use a JSON validator)
4. You fully restarted Claude Code (not just reloaded)

---

## Multiple servers in one file

```json
{
  "mcpServers": {
    "github": {
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "postgres": {
      "command": "uvx",
      "args": ["mcp-server-postgres", "postgresql://localhost/mydb"]
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" }
    }
  }
}
```

---

## Where to find servers

| Resource | Best for |
|---|---|
| [smithery.ai](https://smithery.ai) | Curated registry, install commands |
| [skills.mp](https://skills.mp) | Skills + MCPs |
| `github.com/anthropics/mcp-servers` | Official Anthropic servers |
| GitHub: `mcp-server-*` | Community servers |
