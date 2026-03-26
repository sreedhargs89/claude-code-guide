# Module 07 — Hooks

**Prerequisites:** [Module 06](06-agents.md)  
**Time:** ~20 minutes  
**Next:** [Module 08 — Scheduling](08-scheduling.md)

---

## What hooks are

Hooks are automation triggers that fire at specific points in Claude Code's lifecycle. They let you run code *around* Claude Code's actions — before a task starts, after a file is written, when Claude Code exits, and so on.

Think of them like Git hooks (`pre-commit`, `post-merge`) but for your AI agent.

---

## Hook types

| Hook | When it fires |
|---|---|
| `PreToolUse` | Before Claude Code uses any tool |
| `PostToolUse` | After Claude Code uses a tool |
| `Stop` | When Claude Code finishes a task |
| `Notification` | When Claude Code sends a notification |

The most useful are `PostToolUse` (run something after Claude edits a file) and `Stop` (run cleanup or validation after a task completes).

---

## Configuring hooks

Hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "cd $CLAUDE_REPO_ROOT && python -m pytest tests/ -q --tb=short"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd $CLAUDE_REPO_ROOT && ruff check . --fix"
          }
        ]
      }
    ]
  }
}
```

This configuration:
- Runs your test suite every time Claude Code writes a file
- Runs the linter when Claude Code finishes a session

---

## Environment variables available in hooks

Claude Code injects context into every hook command:

| Variable | Value |
|---|---|
| `$CLAUDE_REPO_ROOT` | The project root directory |
| `$CLAUDE_TOOL_NAME` | Name of the tool that fired the hook |
| `$CLAUDE_TOOL_INPUT` | The input passed to the tool (JSON) |
| `$CLAUDE_TOOL_OUTPUT` | The output from the tool (JSON) |
| `$CLAUDE_SESSION_ID` | Current session ID |

---

## Practical hook patterns

### Auto-lint on file write
```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "command",
      "command": "ruff check $CLAUDE_TOOL_INPUT_PATH --fix"
    }]
  }]
}
```

### Auto-test after changes
```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "command",
      "command": "cd $CLAUDE_REPO_ROOT && python -m pytest tests/ -x -q"
    }]
  }]
}
```

### Log all tool usage
```json
{
  "PostToolUse": [{
    "matcher": "*",
    "hooks": [{
      "type": "command",
      "command": "echo \"$(date): $CLAUDE_TOOL_NAME\" >> $CLAUDE_REPO_ROOT/logs/tool-usage.log"
    }]
  }]
}
```

### Notify on task completion (macOS)
```json
{
  "Stop": [{
    "hooks": [{
      "type": "command",
      "command": "osascript -e 'display notification \"Claude Code task complete\" with title \"Claude Code\"'"
    }]
  }]
}
```

---

## Data engineering patterns

### Validate data files after write
```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "command",
      "command": "python $CLAUDE_REPO_ROOT/scripts/validate_output.py $CLAUDE_TOOL_INPUT_PATH"
    }]
  }]
}
```

### Run Airflow DAG validation after any DAG file changes
```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "command",
      "command": "python -c \"from airflow.models import DagBag; b = DagBag('$CLAUDE_REPO_ROOT/dags'); print('DAG errors:', b.import_errors or 'None')\""
    }]
  }]
}
```

---

## Important notes

- **Hooks run synchronously** by default — Claude Code waits for the hook to finish before continuing.
- **Non-zero exit codes** from hooks are reported to Claude Code, which may adjust its behavior.
- **Keep hooks fast.** A 30-second test run on every file write will make your sessions painful.
- **Use `--tb=short` and `-q`** on pytest to keep hook output readable.

---

## Check your understanding

1. What is the difference between `PreToolUse` and `PostToolUse` hooks?
2. What environment variable gives you the project root directory?
3. Why should hooks be kept fast?
4. Design a hook that would be useful for a data engineering project.

→ Full quiz: [quizzes/module-07.md](../quizzes/module-07.md)

---

**Next:** [Module 08 — Scheduling →](08-scheduling.md)
