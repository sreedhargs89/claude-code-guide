# Cheatsheet — Skill Template

> Copy this into `.claude/skills/your-skill-name/skill.md` and fill in the blanks.

---

## Minimal template

```markdown
---
name: your-skill-name
description: >
  Describe WHEN to use this skill (not just what it does).
  Write as if explaining to another developer when they should invoke it.
  This is used for automatic skill detection from natural language prompts.
---

## Steps

### Step 1 — Setup
[First step — environment setup, validation, prerequisite checks]

### Step 2 — Main task
[The core work this skill performs]

### Step 3 — Save / output
[Where to save results, what format, naming conventions]

### Step 4 — Log
[What to log, where, what information to include]
```

---

## Full template with all optional sections

```markdown
---
name: your-skill-name
description: >
  Use this skill when [clear trigger condition].
  It [does X] using [Y approach].
  Results are saved to [location].
usage: /your-skill-name
---

## Overview
[1-2 sentence plain English description of what this skill accomplishes]

## Steps

### Step 1 — [Name]
[Detailed instructions. Include:
- exact commands to run
- exact file paths
- expected outputs
- what to do if this step fails]

### Step 2 — [Name]
[...]

### Step 3 — Save results
Save output to: [exact path with naming convention]
Format: [CSV / JSON / Parquet / etc.]
Naming: [e.g., YYYY-MM-DD_HH-MM-SS_filename.csv]

### Step 4 — Log
Create a log at: logs/[skill-name]/[timestamp]/[skill-name].log

Log must include:
- Timestamp of each operation
- Success/failure for each step
- Any errors encountered with full messages
- Summary statistics (records processed, files created, etc.)

## Error handling
- If [common error]: [how to handle it]
- If [another error]: [how to handle it]

## Notes
- [Any important caveats or context]
- [Known limitations]
```

---

## YAML metadata rules

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | Must match the folder name exactly |
| `description` | Yes | Used for auto-detection — write it well |
| `usage` | No | Helpful for documentation |

---

## Folder structure

```
.claude/
└── skills/
    └── your-skill-name/
        ├── skill.md          ← required
        ├── scripts/          ← optional: pre-built scripts
        │   └── main.py
        └── references/       ← optional: supporting docs
            └── error-guide.md
```

---

## Pointing to scripts (instead of generating code)

If you have a pre-written, tested script, tell the skill to use it:

```markdown
### Step 2 — Run the fetch script
Run the existing script at .claude/skills/fetch-api/scripts/fetch_data.py
using the .venv Python environment:
  .venv/bin/python .claude/skills/fetch-api/scripts/fetch_data.py

Do NOT rewrite or regenerate this script. Use it as-is.
```

---

## Writing good descriptions

The description determines whether Claude Code auto-detects your skill from a natural language prompt.

**Good:**
```yaml
description: >
  Use this skill when fetching, refreshing, or downloading data from
  external REST API endpoints. Handles async requests with httpx,
  saves CSVs to timestamped directories, and logs all HTTP status codes.
```

**Bad:**
```yaml
description: Fetches API data.
```

The good one answers "when should I invoke this?" The bad one just names the action.

---

## Common skill types to build first

1. **Fetch skill** — pull data from APIs you use regularly
2. **Transform skill** — standardize how you convert between data formats
3. **Review skill** — scan recent code changes for issues
4. **Deploy skill** — wrap your deployment steps
5. **Report skill** — generate summaries of project state
