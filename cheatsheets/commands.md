# Cheatsheet — Commands & Slash Commands

> Keep this open while you work. Everything you need in one place.

---

## Starting Claude Code

```bash
claude                              # start in current directory
claude --model claude-haiku-4-5     # start with specific model
claude --model claude-sonnet-4-6    # start with sonnet (default)
claude --print "your prompt"        # non-interactive one-shot
```

---

## Session commands (inside Claude Code)

### Navigation & info
```
/help                   list all available slash commands
/model                  view or change the active model
/cost                   token usage and cost for this session
/context                full context window breakdown
/status                 current session state
```

### Conversation control
```
/clear                  clear conversation history (keep context files)
/reset                  full reset — clears everything
/undo                   undo last action
/checkpoint             save a checkpoint to return to
/restore                restore to a previous checkpoint
```

### Task control
```
/todo                   view the current task list
/compact                compress conversation history to save tokens
\exit  (or Ctrl+C)      exit Claude Code
```

### Skills
```
/your-skill-name        invoke a skill by name
/plugins                browse and manage plugins
```

### Scheduling
```
/loop 5m your prompt    schedule a prompt every 5 minutes
/loop 0 9 * * * /fetch  schedule a skill at 9am daily
/cron delete JOB_ID     cancel a specific scheduled job
```

### Auth & billing
```
/login                  switch auth method (API vs subscription)
/logout                 sign out
```

---

## New commands (recently added)

### /btw — side question without polluting context
```
/btw what does this function return?
```
Ask a quick question without adding it to the main conversation history.
Runs even while Claude Code is processing another task. No tool access.
Single response only — not for back-and-forth.

### /voice — speak your prompts
```
/voice
```
Activates voice input mode. Speak your prompt instead of typing it.
Currently rolling out to Pro/Team/Enterprise users. Not available on API plan yet.

---

## Model reference

| Model | Use when | Approx cost (input/output per 1M tokens) |
|---|---|---|
| `claude-haiku-4-5` | Learning, testing, cheap monitoring | $0.25 / $1.25 |
| `claude-sonnet-4-6` | Daily work, default recommendation | $3 / $15 |
| `claude-opus-4-6` | Complex reasoning, 1M context window | $15 / $75 |

---

## Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `↑` / `↓` | Navigate command history |
| `Ctrl+C` | Cancel current operation / exit |
| `Ctrl+L` | Clear screen |
| `Tab` | Autocomplete slash commands |

---

## Windows-specific

```powershell
# Install (PowerShell)
iwr https://claude.ai/install | iex

# If 'claude' not found after install — add to PATH:
# Win key → "environment variables" → User variables → Path → New
# Paste the path shown at end of installer output

# Check version
claude --version
```

## macOS / Linux

```bash
# Install
npm install -g @anthropic-ai/claude-code

# Or Homebrew
brew install anthropic/tap/claude

# Verify
claude --version
```

---

## Disable all scheduled tasks
```bash
# In terminal session
export CLAUDE_DISABLE_CRON=1

# Or permanently in .claude/settings.json
{
  "env": { "CLAUDE_DISABLE_CRON": "1" }
}
```
