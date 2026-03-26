# Module 08 — Scheduling with /loop and Cron

**Prerequisites:** [Module 07](07-hooks.md)  
**Time:** ~25 minutes  
**Next:** [Module 09 — MCP Servers](09-mcp.md)

---

## What scheduling means in Claude Code

Claude Code can run a prompt — or a skill — automatically on a schedule. This means you can set up recurring AI-powered tasks without any additional orchestration tool.

Think of it as cron for your AI agent. Instead of scheduling a bash script, you're scheduling a natural language instruction.

> **Requirement:** Claude Code version 2.1.72 or later. Check with `claude --version`.

---

## The /loop command

The syntax is:

```
/loop <interval_or_cron> <your prompt>
```

Examples:

```bash
# Run every 5 minutes
/loop 5m check if the deployment has finished and report status

# Run every hour at :00
/loop 0 * * * * scan the dags/ folder for any new errors and log them

# Run every day at 9am
/loop 0 9 * * * invoke my skill to fetch the latest API data

# Run every Monday at 8:30am
/loop 30 8 * * 1 review all open PRs and send me a brief summary
```

---

## Supported interval shortcuts

| Shorthand | Meaning |
|---|---|
| `30s` | Every 30 seconds |
| `5m` | Every 5 minutes |
| `2h` | Every 2 hours |
| `1d` | Every day |
| `1w` | Every week |

No shorthand = uses standard cron syntax (5 fields: minute, hour, day-of-month, month, day-of-week).

If you omit an interval entirely, the default is **every 10 minutes**.

---

## Cron syntax reference

```
┌───── minute (0–59)
│ ┌───── hour (0–23)
│ │ ┌───── day of month (1–31)
│ │ │ ┌───── month (1–12)
│ │ │ │ ┌───── day of week (0–7, 0=Sunday)
│ │ │ │ │
* * * * *
```

Common patterns:

```
0 9 * * *        Every day at 9:00am
0 9 * * 1-5      Monday–Friday at 9:00am
*/30 * * * *     Every 30 minutes
0 */2 * * *      Every 2 hours on the hour
0 0 * * 0        Every Sunday at midnight
0 8,17 * * 1-5   Weekdays at 8am and 5pm
```

---

## Managing scheduled jobs

### View scheduled jobs
Claude Code logs scheduled jobs. Check `scheduled-tasks.log` in your session directory, or ask Claude Code directly:

```
What scheduled jobs are currently running?
```

### Delete a specific job
Each job gets a unique ID when created. Claude Code shows it at creation:

```
✓ Scheduled: fetch-api every 3 minutes
  Job ID: cron_abc123def456
  Auto-expires: 3 days
```

Delete it:
```
/cron delete cron_abc123def456
```

### Disable all scheduled jobs
Add this to `.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_DISABLE_CRON": "1"
  }
}
```

Or set it in your terminal session:
```bash
export CLAUDE_DISABLE_CRON=1
```

All scheduled tasks stop firing immediately. Remove the variable to re-enable.

---

## Practical scheduling examples

### Data engineering: daily data refresh
```
/loop 0 6 * * * invoke my fetch-api skill to pull fresh data before standup
```

### PR review briefing (Senior dev pattern)
```
/loop 30 8 * * 1-5 check all open PRs in this repository. Summarize each one
in 2-3 sentences covering what changed and if there are any obvious issues.
Save the summary to reports/pr-briefing-today.md
```

### Deployment monitoring
```
/loop 5m check if the latest deployment to staging is healthy.
Check the health endpoint at http://localhost:8080/health.
If it returns anything other than 200, alert me with details.
```

### Weekly DAG health check
```
/loop 0 9 * * 1 scan all DAG files in dags/ for any syntax errors,
deprecated patterns, or missing dependencies. Generate a report at
reports/dag-health-YYYY-MM-DD.md
```

---

## Scheduling a skill (vs a raw prompt)

You can schedule either a raw prompt or a skill invocation. Skill invocations are more reliable because the exact steps are defined in the skill file:

```bash
# Schedule a skill (preferred for repeating tasks)
/loop 0 6 * * * /fetch-api

# Schedule a raw prompt (fine for one-off recurring checks)
/loop 0 9 * * * check if any new CSV files arrived in data/incoming/
```

---

## Important constraints

- **Your machine must be on.** Claude Code runs locally — it can't fire scheduled tasks if your system is off or sleeping.
- **Jobs auto-expire after 3 days** by default. Recreate them or adjust TTL if needed.
- **Keep costs in mind.** A job running every 5 minutes makes 288 LLM calls per day. Use Haiku for cheap monitoring tasks.

---

## Check your understanding

1. What is the minimum Claude Code version needed for scheduling?
2. Write a cron expression for "every weekday at 8:30am".
3. How do you cancel a specific scheduled job?
4. Why is it better to schedule a skill invocation vs a raw prompt for repeating tasks?
5. What constraint means Claude Code can't be used as a true cloud scheduler?

→ Full quiz: [quizzes/module-08.md](../quizzes/module-08.md)  
→ Cheatsheet: [cheatsheets/cron-syntax.md](../cheatsheets/cron-syntax.md)

---

**Next:** [Module 09 — MCP Servers →](09-mcp.md)
