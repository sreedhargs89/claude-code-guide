# Example: Local MCP Server

Step-by-step setup for the most common local MCP servers.
Each section takes ~5 minutes to set up.

---

## Prerequisites

```bash
# Python-based servers need uv
pip install uv

# Node.js-based servers need npx (comes with Node.js)
node --version   # verify Node.js is installed
```

---

## Example 1: File system MCP (simplest — start here)

Gives Claude Code extended file system access beyond its working directory.

### Install and configure

Add to `.claude/settings.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "uvx",
      "args": [
        "mcp-server-filesystem",
        "/Users/yourname/Documents",
        "/Users/yourname/Downloads"
      ]
    }
  }
}
```

Replace the paths with directories you want Claude Code to access.

### Verify it works

Restart Claude Code, then run `/context`. You should see `filesystem` under MCP tools.

Try:
```
List all PDF files in my Documents folder
```

---

## Example 2: GitHub MCP

Lets Claude Code read repos, list PRs, create issues, and more.

### Get a GitHub token

1. GitHub → Settings → Developer Settings → Personal access tokens → Fine-grained tokens
2. Create token with: repo (read/write), issues (read/write), pull_requests (read/write)
3. Copy the token

### Configure

```json
{
  "mcpServers": {
    "github": {
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

Set the env var in your shell (add to `.bashrc` / `.zshrc` / PowerShell profile):

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### Verify and use

Restart Claude Code. Then try:
```
List all open PRs in this repository
What issues are currently assigned to me?
Create a GitHub issue: "Add Parquet compression to migrate-data skill"
```

---

## Example 3: SQLite MCP (local database — no server needed)

Perfect for local data work without a running database server.

### Install and configure

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./data/local.db"]
    }
  }
}
```

### Use it

```
Create a table called sales with columns: id, date, amount, region
Insert 5 sample rows into the sales table
Show me the top 3 regions by total amount
```

---

## Example 4: PostgreSQL MCP (production database)

### Configure

```json
{
  "mcpServers": {
    "postgres": {
      "command": "uvx",
      "args": [
        "mcp-server-postgres",
        "postgresql://${PG_USER}:${PG_PASSWORD}@${PG_HOST}/${PG_DATABASE}"
      ]
    }
  }
}
```

Set env vars:
```bash
export PG_USER="your_user"
export PG_PASSWORD="your_password"
export PG_HOST="localhost"
export PG_DATABASE="your_db"
```

### Use it

```
Show me all tables in the public schema
How many rows are in the fact_sales table?
Write a query to find customers who haven't ordered in 90 days
Explain why this query might be slow: SELECT * FROM orders WHERE LOWER(status) = 'pending'
```

---

## Full settings.json with multiple servers

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "/Users/yourname/projects"]
    },
    "github": {
      "command": "uvx",
      "args": ["mcp-server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./data/local.db"]
    }
  },
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "command",
        "command": "echo \"$(date): wrote $CLAUDE_TOOL_INPUT_PATH\" >> logs/tool-usage.log"
      }]
    }]
  }
}
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Server not in `/context` | Fully restart Claude Code (not just reload) |
| `uvx: command not found` | Run `pip install uv` |
| Auth error on GitHub | Check token has correct permissions; export env var in same shell |
| DB connection refused | Check DB is running; verify host/port/credentials |
| `mcp-server-X not found` | Run `uvx mcp-server-X --help` to trigger install |

---

## See also

- [Hosted MCP example](../mcp-hosted/) — connecting to cloud-hosted MCP servers
- [Cheatsheet](../../cheatsheets/mcp-config.md) — full config reference
