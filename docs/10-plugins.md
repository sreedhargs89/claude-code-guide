# Module 10 — Plugins & Marketplace

**Prerequisites:** [Module 09](09-mcp.md)  
**Time:** ~15 minutes  

---

## What plugins are

Plugins are packaged extensions for Claude Code — pre-built skills, MCP integrations, and utilities created by Anthropic, third-party providers, or the community. They're installed through a marketplace system.

The relationship:
- **Skill** = something you build for your own project
- **Plugin** = a skill (or MCP integration) packaged for anyone to install

Under the hood, a plugin is usually just a well-packaged skill or MCP server with metadata that makes it discoverable and installable via the marketplace.

---

## Installing plugins

From inside Claude Code:

```
/plugins
```

This opens the plugin browser. You'll see plugins from:
- Anthropic (official, curated)
- Verified community contributors
- Third-party services (Figma, Notion, GitHub, etc.)

To install:
```
/plugins install notion
/plugins install figma-mcp
/plugins install skill-creator
```

---

## Marketplace sources

Beyond the built-in marketplace, the community maintains additional registries:

### smithery.ai
Best for MCP servers. Each listing includes:
- What the server connects to
- Install command (usually one line)
- Usage examples

### skills.mp
Best for Claude Code skills. Browse by category: data engineering, DevOps, frontend, writing, etc. Download a `skill.md` and drop it into your `.claude/skills/` folder.

### GitHub
Search `claude-code-skills` or `mcp-server` on GitHub. Many well-maintained servers live here before making it into the official registry.

---

## Notable plugins

| Plugin | Type | What it does |
|---|---|---|
| `skill-creator` | Skill | Helps you build, test, and iterate on new skills |
| `figma` | MCP | Connect Claude Code to Figma for design work |
| `notion` | MCP | Read/write Notion pages and databases |
| `github` | MCP | Full GitHub integration (PRs, issues, repos) |
| `simplify` | Built-in skill | Rewrites complex code for clarity |
| `debug` | Built-in skill | Systematic debugging workflow |
| `badge` | Built-in skill | Generates README badges |

---

## Creating your own plugin

If you've built a skill that's useful beyond your own project, you can package and share it.

A minimal plugin directory:

```
my-skill/
├── skill.md          ← the skill definition
├── README.md         ← description and usage instructions
├── package.json      ← metadata (name, version, author, description)
└── scripts/          ← any supporting scripts
```

`package.json` for a skill plugin:
```json
{
  "name": "mcp-skill-snowflake-helper",
  "version": "1.0.0",
  "description": "Claude Code skill for common Snowflake operations",
  "author": "your-username",
  "keywords": ["claude-code", "skill", "snowflake", "data-engineering"],
  "claudeCode": {
    "type": "skill",
    "command": "snowflake-helper"
  }
}
```

Publish to npm, then submit to smithery.ai or skills.mp for discoverability.

---

## Built-in bundled skills

Claude Code ships with a small set of bundled skills that don't require installation:

| Command | What it does |
|---|---|
| `/simplify` | Rewrites selected code to be more readable |
| `/debug` | Runs a structured debugging workflow |
| `/badge` | Generates shield.io badges for your README |

These are always available regardless of your `.claude/skills/` contents.

---

## The ecosystem is growing fast

The MCP and skills ecosystem is early-stage and expanding quickly. What's true today:
- Most popular dev tools have at least one community MCP server
- The quality varies — read the source before installing anything with sensitive access
- Anthropic is actively curating an official registry

Recommendations:
- Start with the skills in this repo (they're battle-tested)
- Add MCP servers one at a time, verify each works before adding the next
- Check smithery.ai monthly — new high-quality servers appear constantly

---

## Check your understanding

1. What is the difference between a skill you build yourself and a plugin from the marketplace?
2. Name two community registries where you can find Claude Code skills and MCP servers.
3. What command opens the plugin browser in Claude Code?
4. What are the three built-in bundled skills that ship with Claude Code?

→ Full quiz: [quizzes/module-10.md](../quizzes/module-10.md)

---

## You've completed the course

You now have the full picture:

```
Models → Architecture → Install → CLAUDE.md
→ Skills → Agents → Hooks → Scheduling → MCP → Plugins
```

The next step is to build something real. Pick one task you do every week, create a skill for it, and run it for a month. That's when it clicks.

Revisit [LEARNING_PATH.md](https://github.com/sreedhargs89/claude-code-guide/blob/main/LEARNING_PATH.md) for recommended practice exercises.
