# Learning Path

A structured journey from zero to confident Claude Code developer. Each phase builds on the previous one.

---

## Phase 1 — Foundation (Days 1–3)
*Understand what Claude Code is and get it running on your machine.*

### Day 1: The ecosystem
- Read [Module 01 — Claude models](docs/01-claude-models.md)
- Read [Module 02 — Architecture](docs/02-architecture.md)
- Take [Quiz 01](quizzes/module-01.md) and [Quiz 02](quizzes/module-02.md)

**Goal:** Be able to explain in one sentence what Claude Code is and why it's different from Claude.ai.

### Day 2: Installation
- Read [Module 03 — Installation](docs/03-installation.md)
- Follow the setup steps for your OS
- Open Claude Code in VS Code and run your first prompt
- Take [Quiz 03](quizzes/module-03.md)

**Goal:** Claude Code opens in your terminal. You can run a simple prompt.

### Day 3: CLAUDE.md
- Read [Module 04 — CLAUDE.md](docs/04-claude-md.md)
- Copy [`.claude/CLAUDE.md`](.claude/CLAUDE.md) into a test project
- Experiment with adding standards and watching Claude follow them
- Take [Quiz 04](quizzes/module-04.md)

**Goal:** You have a working CLAUDE.md in a project. Claude Code reads it on startup.

---

## Phase 2 — Core tools (Days 4–7)
*Build real skills and automate your actual work.*

### Day 4–5: Skills (the most important module)
- Read [Module 05 — Skills](docs/05-skills.md) carefully — this is the backbone
- Try the [generic fetch-api skill](skills/fetch-api/) in a test project
- If you're a data engineer, try the [data-engineering variant](examples/fetch-api/data-engineering/)
- Build one skill for a task you do every day
- Take [Quiz 05](quizzes/module-05.md)

**Goal:** You have created and successfully triggered your own `skill.md`.

### Day 6: Sub-agents
- Read [Module 06 — Sub-agents](docs/06-agents.md)
- Try the [readme-gen skill](skills/readme-gen/) on an existing project
- Understand the difference between a skill call and an agent delegation
- Take [Quiz 06](quizzes/module-06.md)

**Goal:** You've used Claude Code to auto-generate a README for a real project.

### Day 7: Hooks
- Read [Module 07 — Hooks](docs/07-hooks.md)
- Set up a post-edit hook that auto-runs linting
- Take [Quiz 07](quizzes/module-07.md)

**Goal:** At least one hook is configured and firing automatically.

---

## Phase 3 — Automation (Days 8–10)
*Schedule work and integrate with the world.*

### Day 8: Scheduling
- Read [Module 08 — Scheduling](docs/08-scheduling.md)
- Use the `/loop` command to schedule a skill on a 5-minute timer
- Practice deleting specific cron jobs by ID
- Take [Quiz 08](quizzes/module-08.md)

**Goal:** A scheduled prompt is running. You can create and cancel cron jobs.

### Day 9–10: MCP + Plugins
- Read [Module 09 — MCP servers](docs/09-mcp.md)
- Read [Module 10 — Plugins](docs/10-plugins.md)
- Connect one local MCP server (use the config in [cheatsheets/mcp-config.md](cheatsheets/mcp-config.md))
- Browse the marketplace and install one plugin
- Take [Quiz 09](quizzes/module-09.md) and [Quiz 10](quizzes/module-10.md)

**Goal:** Claude Code can talk to at least one external tool via MCP.

---

## After the 10 days

- Revisit [Quiz answers](quizzes/answers.md) for any questions you got wrong
- Check [Slash commands cheatsheet](cheatsheets/commands.md) — keep it open while you work
- Build a skill for something real in your job
- Explore [smithery.ai](https://smithery.ai) and [skills.mp](https://skills.mp) for community skills

---

## Time estimates

| Phase | Time investment | Outcome |
|---|---|---|
| Phase 1 | ~3 hours | Claude Code installed and configured |
| Phase 2 | ~6 hours | First real skills built and running |
| Phase 3 | ~4 hours | Automated pipelines, MCP connected |
| **Total** | **~13 hours** | **Confident daily driver** |
