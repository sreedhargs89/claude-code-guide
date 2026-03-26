# Module 04 — CLAUDE.md

**Prerequisites:** [Module 03](03-installation.md)  
**Time:** ~20 minutes  
**Next:** [Module 05 — Skills](05-skills.md)

---

## What CLAUDE.md is

`CLAUDE.md` is a markdown file that Claude Code reads automatically at the start of every session. It's your way of giving Claude Code persistent context about your project — without repeating yourself in every prompt.

Think of it as the briefing document you'd hand to a new team member on day one:
- What is this project?
- What are the conventions we follow?
- What tools and libraries do we use?
- What should you always/never do here?

---

## Where to put it

There are two scopes:

### Project-level (recommended)
```
your-project/
└── .claude/
    └── CLAUDE.md
```

Claude Code reads this whenever you start a session inside `your-project/`. Different projects get different CLAUDE.md files with different standards.

### System-level (global)
```
~/.claude/
└── CLAUDE.md
```

This is read for every Claude Code session on your machine, regardless of project. Use this for personal preferences that apply everywhere (your name, preferred language, general code style).

> **Pro tip:** Start with project-level only. Add system-level later when you know what you want globally.

---

## What to put in it

A good CLAUDE.md covers four areas:

### 1. Project overview
Brief description — what the project does, the tech stack, the purpose.

```markdown
## Project
This is a data pipeline project that ingests sales data from REST APIs,
transforms it via PySpark, and loads to a Snowflake data warehouse.

Tech stack: Python 3.11, PySpark 3.5, Apache Airflow 3.0, Snowflake
```

### 2. Standards and conventions
The rules Claude Code should always follow in this project.

```markdown
## Standards
- All Python files must include type hints
- Use async/await for all I/O operations (httpx, not requests)
- DAG files go in dags/, scripts go in scripts/, tests in tests/
- Never hardcode credentials — always use environment variables from .env
- Log all API responses with status codes
```

### 3. Awareness of the project structure
Tell Claude where things live so it doesn't guess.

```markdown
## Project structure
- dags/           Apache Airflow DAG definitions
- scripts/        Standalone Python scripts (fetch, transform, load)
- skills/         Claude Code skill definitions
- data/           Local data files (ignored by git)
- logs/           Runtime logs (ignored by git)
```

### 4. Reminders and restrictions
Things you want Claude Code to always check before acting.

```markdown
## Important
- Always activate the .venv virtual environment before running Python
- Never delete files in data/ without asking first
- Tests must pass before marking any task complete
```

---

## The token cost of CLAUDE.md

Every Claude Code session injects CLAUDE.md into the context window automatically. This means every character in CLAUDE.md costs tokens on every session.

**Practical implication:** Keep CLAUDE.md concise and useful. Don't write an essay. Short bullet points that Claude actually needs are worth far more than long paragraphs it'll skim past.

Run `/context` inside Claude Code to see how many tokens your CLAUDE.md is consuming:

```
System prompt:    5,942 tokens   ← includes CLAUDE.md + skill metadata
System tools:    19,380 tokens   ← built-in tools
Memory files:       220 tokens   ← any memory files at root
```

If your system prompt is ballooning, audit CLAUDE.md and trim anything that isn't necessary.

---

## CLAUDE.md vs skills

A common question: why not just put everything in CLAUDE.md?

| | CLAUDE.md | Skill |
|---|---|---|
| **When loaded** | Every session, always | Only when skill is invoked |
| **Token cost** | Constant overhead | Only when you pay for it |
| **Best for** | Project context, standards, conventions | Step-by-step task instructions |
| **Max useful size** | ~1–2 KB | As long as needed |

If you have a 20-step process for migrating data, that belongs in a skill — not CLAUDE.md. CLAUDE.md should tell Claude *what kind of project this is*. Skills tell it *how to do specific tasks*.

---

## A working template

See [`.claude/CLAUDE.md`](../.claude/CLAUDE.md) in this repo for a full template you can copy into your own project.

---

## Check your understanding

1. What is the difference between project-level and system-level CLAUDE.md?
2. Why does the size of CLAUDE.md affect your API cost?
3. What four categories of information belong in a good CLAUDE.md?
4. If you have a 15-step deployment process, should it go in CLAUDE.md or a skill? Why?

→ Full quiz: [quizzes/module-04.md](../quizzes/module-04.md)  
→ Template: [cheatsheets/claude-md-template.md](../cheatsheets/claude-md-template.md)

---

**Next:** [Module 05 — Skills →](05-skills.md)
