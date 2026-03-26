---
name: schedule-task
description: >
  Use this skill to set up a recurring scheduled Claude Code task using
  the /loop command with cron syntax. Invoke when asked to "schedule a
  task", "run this daily", "automate this on a timer", or "set up a
  recurring job".
usage: /schedule-task
---

# Schedule Task skill

Guides the creation of a scheduled Claude Code task using /loop and cron.
Stores job IDs for later management. Validates the schedule before creating it.

## Steps

### Step 1 — Understand the request
From the user's prompt, extract:
- **What to run**: a skill name (e.g., `/fetch-api`) or a raw prompt
- **When to run**: frequency or specific time
- **Duration**: one-off, indefinite, or until a date

If any of these are unclear, ask before proceeding.

### Step 2 — Translate to cron syntax
Convert the user's description to a cron expression.
Always prefer cron syntax over shorthand for clarity.

| User says | Cron expression |
|---|---|
| Every day at 9am | `0 9 * * *` |
| Every weekday at 8:30am | `30 8 * * 1-5` |
| Every hour | `0 * * * *` |
| Every Monday at 8am | `0 8 * * 1` |
| Every 30 minutes | `*/30 * * * *` |
| First of month at 6am | `0 6 1 * *` |

Show the user the cron expression and confirm it's correct before creating.

### Step 3 — Check version compatibility
Run: `claude --version`

Scheduling requires version 2.1.72 or later.
If the version is older, stop and tell the user to upgrade first:
```
claude update
```

### Step 4 — Create the scheduled job
Run the /loop command with the confirmed cron expression:

```
/loop <cron_expression> <prompt_or_skill>
```

Examples:
```
/loop 0 9 * * * /fetch-api
/loop 30 8 * * 1-5 /code-review and save report to reports/
/loop 0 6 1 * * review all log files from last month and summarize
```

### Step 5 — Log the job
After creation, Claude Code shows a Job ID. Save it to a log file:

Append to `.claude/scheduled-jobs.md`:
```markdown
## [Date created]
- **Job ID**: cron_xxxxxxxxxxxx
- **Schedule**: [cron expression] = [human-readable description]
- **Task**: [what it does]
- **Created**: [timestamp]
- **Status**: active
```

Create `.claude/scheduled-jobs.md` if it doesn't exist.

### Step 6 — Confirm to user
Report:
- The Job ID (important — needed to cancel later)
- The schedule in plain English
- The first time it will run
- How to cancel: `/cron delete [job-id]`

## Notes
- Jobs auto-expire after 3 days by default
- The machine must be on and Claude Code running for jobs to fire
- For cheap monitoring tasks (status checks, health pings), use Haiku model
  to reduce cost: the scheduled prompt inherits the current model setting
- Always save the Job ID — without it you can't cancel the specific job
- To disable ALL jobs quickly: add `CLAUDE_DISABLE_CRON=1` to settings.json
