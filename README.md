# Claude Code Guide 🚀

> **A one-stop study resource for mastering Claude Code** — from first principles to production-ready agentic workflows.

Every concept has a guide, a working skill, a cheatsheet, and a self-test quiz.

---

## Who this is for

| Audience | What you'll get |
|---|---|
| **Complete beginners** | Clear explanations from zero — no prior Claude knowledge needed |
| **Data engineers / analysts** | Real-world skills for Airflow, PySpark, HTTPX APIs, ETL pipelines |
| **General developers** | Generic versions of every example that work in any stack |

---

## What's inside

```
claude-code-guide/
├── docs/               # 10 concept guides (one per module)
├── skills/             # Ready-to-use skill.md templates
├── examples/           # Working code — generic + data-engineering variants
├── quizzes/            # Self-test Q&A per module (with answers)
├── cheatsheets/        # Quick-reference cards
└── .claude/            # A working CLAUDE.md you can copy into your own project
```

---

## Learning path

Follow the modules in order, or jump to what you need:

| # | Module | Docs | Skills | Quiz | Cheatsheet |
|---|---|---|---|---|---|
| 01 | Claude models & ecosystem | [→](docs/01-claude-models.md) | — | [→](quizzes/module-01.md) | — |
| 02 | Claude Code architecture | [→](docs/02-architecture.md) | — | [→](quizzes/module-02.md) | — |
| 03 | Installation & setup | [→](docs/03-installation.md) | — | [→](quizzes/module-03.md) | [→](cheatsheets/commands.md) |
| 04 | CLAUDE.md | [→](docs/04-claude-md.md) | — | [→](quizzes/module-04.md) | [→](cheatsheets/claude-md-template.md) |
| 05 | Skills | [→](docs/05-skills.md) | [fetch-api](skills/fetch-api/) · [migrate](skills/migrate-data/) · [visualize](skills/visualize/) | [→](quizzes/module-05.md) | [→](cheatsheets/skill-template.md) |
| 06 | Sub-agents & memory | [→](docs/06-agents.md) | [readme-gen](skills/readme-gen/) | [→](quizzes/module-06.md) | — |
| 07 | Hooks | [→](docs/07-hooks.md) | [code-review](skills/code-review/) | [→](quizzes/module-07.md) | — |
| 08 | Scheduling | [→](docs/08-scheduling.md) | [schedule-task](skills/schedule-task/) | [→](quizzes/module-08.md) | [→](cheatsheets/cron-syntax.md) |
| 09 | MCP servers | [→](docs/09-mcp.md) | — | [→](quizzes/module-09.md) | [→](cheatsheets/mcp-config.md) |
| 10 | Plugins & marketplace | [→](docs/10-plugins.md) | — | [→](quizzes/module-10.md) | — |

---

## Quick start

**Prerequisites:** Basic Python knowledge. That's it.

```bash
# 1. Clone this repo
git clone https://github.com/sreedhargs89/claude-code-guide.git
cd claude-code-guide

# 2. Read the first concept guide
open docs/01-claude-models.md

# 3. Install Claude Code (see docs/03-installation.md for full walkthrough)
# Windows PowerShell:
iwr https://claude.ai/install | iex

# macOS / Linux:
npm install -g @anthropic-ai/claude-code
```

---

## How to use the skills

Every skill in `skills/` is a drop-in `skill.md` file. Copy it into your own project:

```
your-project/
└── .claude/
    └── skills/
        └── fetch-api/
            └── skill.md   ← copy from this repo
```

Then trigger it inside Claude Code:

```
/fetch-api
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs welcome — especially new skill templates.

---

## License

MIT. Use freely, adapt for your own projects.
