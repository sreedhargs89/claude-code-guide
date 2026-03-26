# Module 05 — Skills

**Prerequisites:** [Module 04](04-claude-md.md)  
**Time:** ~45 minutes  
**Next:** [Module 06 — Sub-agents](06-agents.md)

---

## Why skills are the backbone

Skills are the single most important concept in modern Claude Code. They transform Claude Code from a capable assistant into a reliable automation platform.

The core idea: you spend time *once* to define exactly how a task should be done. Claude Code then executes that task consistently, every time, without you re-explaining it.

**Without skills:**
```
You: "Fetch data from these 6 APIs using async Python, save each to a
     timestamped folder, log successes and failures..."
Claude Code: <generates something, you hope it follows your conventions>
```

**With skills:**
```
You: /fetch-api
Claude Code: <runs your exact process, follows your standards>
```

---

## The mental model: hiring a specialist

Imagine hiring an expert for each task:
- An API specialist who knows your auth patterns and async conventions
- A data migration expert who knows your file formats and naming conventions
- A visualization specialist who knows your dashboard KPIs and formulas

You spend time onboarding each one — writing down everything they need to know. That's creating a skill. Once it's done, you just call the specialist.

---

## Where skills live

Skills live inside your `.claude/` directory:

```
.claude/
└── skills/
    └── fetch-api/          ← one folder per skill
        ├── skill.md        ← required: the skill definition
        ├── scripts/        ← optional: pre-built scripts the skill can call
        └── references/     ← optional: documentation, error catalogs, etc.
```

The folder name becomes the slash command. A folder named `fetch-api` becomes `/fetch-api`.

---

## Anatomy of skill.md

Every `skill.md` starts with a YAML metadata block, then contains the instructions:

```markdown
---
name: fetch-api
description: >
  Fetch data from configured REST API endpoints using async Python (httpx).
  Saves CSV responses to a timestamped directory. Use this skill when
  fetching or refreshing data from external APIs.
---

# Fetch API skill

## Usage
Invoke with: /fetch-api

## Steps

### Step 1 — Activate environment
Use the .venv virtual environment at .venv/. Run:
`source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)

### Step 2 — Fetch data
Fetch from the following URLs using async Python (httpx, not requests):
- https://api.example.com/data/customers
- https://api.example.com/data/products
- https://api.example.com/data/orders

Use asyncio.gather() to fetch all endpoints concurrently.

### Step 3 — Save results
Save each response as a CSV file in:
  .claude/skills/fetch-api/data/YYYY-MM-DD_HH-MM-SS/

### Step 4 — Log results
Create a log at:
  logs/fetch-api/YYYY-MM-DD_HH-MM-SS/fetch-api.log

The log must include: which endpoints were called, HTTP status codes,
success/failure for each, and any errors encountered.
```

---

## The YAML metadata block

The metadata at the top serves two purposes:

**`name`**: Must match the folder name. Claude Code uses this to register the skill.

**`description`**: This is critical for automatic skill detection. When you write a prompt in natural language and don't specify a skill name, Claude Code uses this description to decide which skill (if any) to invoke automatically. Write it as if you're describing when *to use* this skill.

Good description:
```yaml
description: >
  Use this skill when fetching, refreshing, or downloading data from
  external REST APIs. Handles authentication, async requests, and saves
  results as CSVs.
```

Bad description:
```yaml
description: Fetches API data.
```

The good one tells Claude Code *when* to invoke it from natural language. The bad one is too vague.

---

## Invoking a skill

### Direct invocation (recommended)
```
/fetch-api
```
Fastest. Claude Code loads the full skill.md and executes it.

### Natural language invocation
```
Can you fetch the latest data from our APIs using my skills?
```
Claude Code reads all skill descriptions and picks the most relevant one. Useful when you forget the skill name.

### NLP with skill reference
```
Fetch data from these two new endpoints and use the fetch-api skill as a reference for the code patterns.
```
Combines a new prompt with an existing skill as context. Good for one-off variations.

---

## Extending skills: scripts and references

### scripts/ folder
Pre-written Python scripts that the skill calls instead of generating code from scratch.

**Why use this:** If you've already written and tested a script, you don't want Claude Code to regenerate (and potentially vary) it every time. Point the skill at your existing script.

```markdown
### Step 2 — Run the fetch script
Run the existing script at .claude/skills/fetch-api/scripts/fetch_data.py
using the .venv Python environment. Do not rewrite the script.
```

### references/ folder
Supporting documentation the skill can consult when needed.

Examples of what to put here:
- Error catalog: "when you see error X, do Y"
- Upgrade notes: "as of PySpark 4.0, use this new API instead of the old one"
- Org-specific docs: internal API documentation that isn't publicly available
- Known edge cases specific to your data

Claude Code only loads reference files when it decides they're relevant — so they don't add constant token overhead.

---

## Building your first skill: the process

1. **Pick a task you do repeatedly.** The more repetitive, the more value.
2. **Write down every step.** Be specific — exact file paths, exact conventions.
3. **Create the folder:** `.claude/skills/your-skill-name/`
4. **Create `skill.md`** with the YAML header and step-by-step instructions.
5. **Trigger and test:** Run `/your-skill-name` and watch what happens.
6. **Iterate.** It probably won't be perfect first time. Fix the steps, re-run.
7. **Add scripts/** when you want a step to always use a specific pre-built script.

> **Iteration is expected.** Skills are trained over multiple runs, not written once and assumed perfect. The first run shows you gaps. The third run is usually reliable.

---

## Common skill patterns

### The ETL skill
Steps: activate env → fetch from source → transform → save to destination → log

### The readme generator skill
Steps: scan project files → understand structure → generate README.md → review

### The code review skill
Steps: list recent changed files → analyze each → report issues → suggest fixes

### The deploy skill
Steps: run tests → build → push to staging → smoke test → promote to prod

---

## What skills are NOT

Skills are not:
- Shell aliases (they're full orchestrations with LLM decision-making at each step)
- Static scripts (they adapt — if a step fails, Claude Code tries to fix it)
- Replacements for real CI/CD (for production deployments, use proper tooling)

Skills are best for: developer productivity tasks, data engineering workflows, analysis pipelines, and any multi-step process you do manually more than twice a week.

---

## Ready-to-use skills in this repo

| Skill | Command | What it does |
|---|---|---|
| [fetch-api](../skills/fetch-api/) | `/fetch-api` | Async data fetching from REST APIs |
| [migrate-data](../skills/migrate-data/) | `/migrate-data` | CSV/Parquet/JSON format migration |
| [visualize](../skills/visualize/) | `/visualize` | Generate charts from data files |
| [readme-gen](../skills/readme-gen/) | `/readme-gen` | Auto-generate README for any project |
| [code-review](../skills/code-review/) | `/code-review` | Review changed files for issues |
| [schedule-task](../skills/schedule-task/) | `/schedule-task` | Set up a cron-scheduled Claude Code prompt |

---

## Check your understanding

1. What is the difference between putting task instructions in CLAUDE.md vs a skill?
2. What does the `description` field in the YAML header do?
3. What are the three folders a skill can contain, and when would you use each?
4. When is NLP invocation better than direct `/skill-name` invocation?
5. Why is iteration on skills expected and normal?

→ Full quiz: [quizzes/module-05.md](../quizzes/module-05.md)  
→ Template: [cheatsheets/skill-template.md](../cheatsheets/skill-template.md)

---

**Next:** [Module 06 — Sub-agents & Memory →](06-agents.md)
