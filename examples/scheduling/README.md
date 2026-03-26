# Example: Scheduling with /loop

Practical patterns for scheduling Claude Code tasks using the `/loop` command.
Each example is ready to copy and run.

---

## Data engineering patterns

### Daily data refresh (before standup)
```
/loop 0 6 * * 1-5 /fetch-api
```
Fetches fresh data from all configured APIs every weekday at 6am.
The data is ready by the time you arrive for your 9am standup.

---

### Hourly pipeline health check
```
/loop 0 * * * * check the logs/ directory for any ERROR lines in the last hour. If any are found, summarise them and save to reports/hourly-health.md
```
Scans logs every hour and writes a summary. Check `reports/hourly-health.md` when something looks wrong.

---

### Weekly DAG review (Monday morning)
```
/loop 30 8 * * 1 scan all DAG files in dags/ and check for: deprecated operators, missing task dependencies, tasks with no retry policy. Save findings to reports/dag-review-YYYY-MM-DD.md
```
Every Monday at 8:30am, before your week starts.

---

### Daily data quality report
```
/loop 0 7 * * * scan the data/ directory for the most recent timestamped folder. Check each CSV for: zero-row files, files larger than 100MB, and files older than 24 hours. Report findings to reports/data-quality-YYYY-MM-DD.md
```

---

## Developer productivity patterns

### PR review briefing
```
/loop 30 8 * * 1-5 list all open pull requests in this repository. For each PR, provide: title, author, number of files changed, and a 2-sentence summary of what changed. Save the briefing to reports/pr-briefing-today.md
```
Arrives in `reports/pr-briefing-today.md` every weekday at 8:30am.

---

### Deployment monitoring
```
/loop 5m check if the file deploy-status.txt exists in the project root. If it says "deploying", check if more than 30 minutes have passed since it was created and alert me if so.
```
Useful when monitoring a deployment that writes status to a file.

---

### Weekly code quality scan
```
/loop 0 9 * * 5 /code-review
```
Runs your `/code-review` skill every Friday at 9am. Good for end-of-week housekeeping.

---

## General patterns

### One-time reminder (runs once, expires)
```
/loop 0 15 * * * check if the feature branch feature/new-pipeline has been merged to main. If not, remind me with a note in .claude/reminders.md
```
Note: jobs auto-expire after 3 days, so this runs daily until it expires or you delete it.

---

### Cost tracking
```
/loop 0 18 * * * check the logs/ directory for today's activity, estimate rough token usage from log file sizes, and append a daily summary line to logs/cost-estimates.log
```

---

## Managing your scheduled jobs

### Keep a job log

When creating important scheduled jobs, note the IDs:

```markdown
# .claude/scheduled-jobs.md (maintained manually)

| Job ID | Schedule | Task | Created |
|---|---|---|---|
| cron_abc123 | 0 6 * * 1-5 | /fetch-api | 2025-03-15 |
| cron_def456 | 30 8 * * 1 | Weekly DAG review | 2025-03-15 |
```

Or use the `/schedule-task` skill which maintains this file automatically.

---

### Cancel a specific job
```
/cron delete cron_abc123
```

### Disable all jobs temporarily
Add to `.claude/settings.json`:
```json
{ "env": { "CLAUDE_DISABLE_CRON": "1" } }
```
Remove the line to re-enable all previously created jobs.

---

## Cost guide for scheduling

| Model | Cost | Best for |
|---|---|---|
| Haiku | ~$0.001–0.01 per run | Monitoring, health checks, simple scans |
| Sonnet | ~$0.05–0.20 per run | Analysis, reporting, reviews |
| Opus | ~$0.50+ per run | Only if quality is critical |

A `/fetch-api` run on Haiku: ~$0.002. Running it daily for a month: ~$0.06.
A weekly PR review on Sonnet: ~$0.10/week = ~$0.40/month.

Switch to Haiku before creating high-frequency schedules:
```
/model   → select haiku
/loop 5m your monitoring prompt
```

---

## See also

- [Docs: Module 08 — Scheduling](../../docs/08-scheduling.md)
- [Cheatsheet: Cron syntax](../../cheatsheets/cron-syntax.md)
- [Skill: schedule-task](../../skills/schedule-task/skill.md)
