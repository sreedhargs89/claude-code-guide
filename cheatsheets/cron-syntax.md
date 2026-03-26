# Cheatsheet — Cron Syntax for /loop

---

## Syntax

```
/loop <interval> <your prompt or /skill-name>
```

The `<interval>` is either a shorthand or a standard 5-field cron expression.

---

## Shorthand intervals

| Shorthand | Every... |
|---|---|
| `30s` | 30 seconds |
| `1m` | 1 minute |
| `5m` | 5 minutes |
| `15m` | 15 minutes |
| `30m` | 30 minutes |
| `1h` | 1 hour |
| `2h` | 2 hours |
| `6h` | 6 hours |
| `12h` | 12 hours |
| `1d` | 1 day |
| `1w` | 1 week |

---

## Cron syntax

```
┌───── minute        (0–59)
│  ┌───── hour       (0–23)
│  │  ┌───── day     (1–31)
│  │  │  ┌───── month (1–12)
│  │  │  │  ┌───── weekday (0–7, 0 and 7 = Sunday)
│  │  │  │  │
*  *  *  *  *
```

### Special characters
| Character | Meaning | Example |
|---|---|---|
| `*` | Any value | `* * * * *` = every minute |
| `,` | List | `0 9,17 * * *` = 9am and 5pm |
| `-` | Range | `0 9 * * 1-5` = Mon–Fri at 9am |
| `/` | Step | `*/15 * * * *` = every 15 min |

---

## Common patterns

```bash
# Every minute
* * * * *

# Every 15 minutes
*/15 * * * *

# Every hour on the hour
0 * * * *

# Every day at 9am (local time)
0 9 * * *

# Every weekday at 9am
0 9 * * 1-5

# Every weekday at 8am and 6pm
0 8,18 * * 1-5

# Every Monday at 8:30am
30 8 * * 1

# Every Sunday at midnight
0 0 * * 0

# First day of every month at 6am
0 6 1 * *

# Every 2 hours
0 */2 * * *
```

---

## Full /loop examples

```bash
# Data refresh every morning before standup
/loop 0 6 * * * /fetch-api

# Monitor deployment every 5 minutes
/loop 5m check if staging deployment is healthy at localhost:8080/health

# Weekly PR review briefing
/loop 30 8 * * 1 review all open PRs and save a summary to reports/pr-briefing.md

# Daily data quality check
/loop 0 7 * * * scan the data/ folder for any files with zero rows and alert me

# Hourly cost monitoring
/loop 0 * * * * check API usage costs and log to logs/cost-tracking.log
```

---

## Managing jobs

```bash
# Delete a specific job (use the Job ID shown when creating)
/cron delete cron_abc123def456

# Disable ALL scheduled jobs (add to settings.json)
{
  "env": { "CLAUDE_DISABLE_CRON": "1" }
}

# Re-enable all jobs (remove the env var)
```

---

## Best practices

- **Use cron syntax** for production-like schedules — more explicit and portable
- **Use shorthand** for ad-hoc testing and development
- **Schedule skills** (`/loop 0 9 * * * /my-skill`) not raw prompts for repeating tasks — more reliable
- **Use Haiku** for frequent monitoring tasks (`--model claude-haiku-4-5`) to keep costs low
- **Log job IDs** — note them somewhere so you can cancel them later
- **Remember:** your machine must be on for jobs to fire
