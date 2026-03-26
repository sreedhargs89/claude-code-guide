# Example: Hooks

Working `settings.json` configurations for common hook patterns.
Each section is a drop-in config block you can copy into `.claude/settings.json`.

---

## Template: Complete settings.json

```json
{
  "hooks": {
    "PreToolUse": [],
    "PostToolUse": [],
    "Stop": [],
    "Notification": []
  },
  "mcpServers": {},
  "env": {}
}
```

---

## Pattern 1: Auto-lint Python on write

Runs `ruff` every time Claude Code writes any Python file.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_TOOL_INPUT_PATH\" | grep -q '\\.py$'; then ruff check \"$CLAUDE_TOOL_INPUT_PATH\" --fix --quiet; fi"
          }
        ]
      }
    ]
  }
}
```

---

## Pattern 2: Run tests after write (lightweight)

Runs only tests related to the changed file — not the full suite.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "cd $CLAUDE_REPO_ROOT && python -m pytest tests/ -x -q --tb=short 2>&1 | tail -5"
          }
        ]
      }
    ]
  }
}
```

> Tip: `tail -5` keeps hook output short. Remove it if you need full output.

---

## Pattern 3: Full quality gate on session end

Runs the complete quality pipeline once when Claude Code finishes — not on every write.
This is less disruptive than per-write hooks.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd $CLAUDE_REPO_ROOT && echo '--- Quality gate ---' && ruff check . --fix -q && python -m pytest tests/ -q --tb=short && echo 'All checks passed.'"
          }
        ]
      }
    ]
  }
}
```

---

## Pattern 4: Log all tool usage (audit trail)

Creates a plain-text log of every tool Claude Code uses.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date '+%Y-%m-%d %H:%M:%S')  $CLAUDE_TOOL_NAME  $CLAUDE_TOOL_INPUT_PATH\" >> $CLAUDE_REPO_ROOT/logs/tool-usage.log"
          }
        ]
      }
    ]
  }
}
```

---

## Pattern 5: Data engineering — validate Airflow DAGs

Runs Airflow DagBag validation every time a DAG file is written.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_TOOL_INPUT_PATH\" | grep -q 'dags/'; then python -c \"from airflow.models import DagBag; b=DagBag('$CLAUDE_REPO_ROOT/dags'); errors=b.import_errors; print('DAG errors:', errors if errors else 'None')\"; fi"
          }
        ]
      }
    ]
  }
}
```

---

## Pattern 6: Data engineering — validate output CSVs

Checks that any CSV written to the `data/` directory has rows and a valid header.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_TOOL_INPUT_PATH\" | grep -q 'data/.*\\.csv$'; then python -c \"import pandas as pd, sys; df=pd.read_csv('$CLAUDE_TOOL_INPUT_PATH'); print(f'CSV OK: {len(df)} rows, {len(df.columns)} cols'); sys.exit(0 if len(df) > 0 else 1)\"; fi"
          }
        ]
      }
    ]
  }
}
```

---

## Pattern 7: Desktop notification on task complete (macOS)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Task complete\" with title \"Claude Code\" sound name \"Glass\"'"
          }
        ]
      }
    ]
  }
}
```

For Linux (requires `notify-send`):
```json
{
  "type": "command",
  "command": "notify-send 'Claude Code' 'Task complete'"
}
```

---

## Combining multiple hooks

All hook types can be combined in one `settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$CLAUDE_TOOL_INPUT_PATH\" | grep -q '\\.py$'; then ruff check \"$CLAUDE_TOOL_INPUT_PATH\" --fix -q; fi"
          },
          {
            "type": "command",
            "command": "echo \"$(date '+%H:%M:%S')  wrote: $CLAUDE_TOOL_INPUT_PATH\" >> $CLAUDE_REPO_ROOT/logs/writes.log"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd $CLAUDE_REPO_ROOT && python -m pytest tests/ -q --tb=short 2>&1 | tail -10"
          }
        ]
      }
    ]
  }
}
```

---

## Environment variables in hooks

| Variable | Value |
|---|---|
| `$CLAUDE_REPO_ROOT` | Project root directory |
| `$CLAUDE_TOOL_NAME` | Tool that fired the hook (`Write`, `Bash`, etc.) |
| `$CLAUDE_TOOL_INPUT_PATH` | Path of file written (Write hook only) |
| `$CLAUDE_SESSION_ID` | Current session ID |

---

## See also

- [Docs: Module 07 — Hooks](../../docs/07-hooks.md)
