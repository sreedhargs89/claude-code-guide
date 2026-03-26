# Quiz Answers

→ [Back to questions](all-modules.md)

---

## Module 01

**A1.** Haiku (smallest — fast and cheap, good for simple tasks), Sonnet (balanced — the recommended default for developer work), Opus (largest — most capable, expensive, 1M token context).

**A2.** Claude.ai is a chat interface — you type questions and get text responses. Claude Code is a developer agent in your terminal — it can take actions like creating files, running scripts, and executing commands.

**A3.** Use Haiku (`claude-haiku-4-5`). It's the cheapest model (~$0.25/M input tokens vs $3/M for Sonnet), handles learning tasks well, and stretches $10 in credits much further.

**A4.** Opus can hold up to 1 million tokens of context in a single session. For data engineering this means loading hundreds of DAG files, large schemas, or entire codebases into a single conversation without losing earlier context.

**A5.** False. Claude Code requires API credits or a paid Pro/Team/Max subscription. The free Claude.ai tier does not include Claude Code.

---

## Module 02

**A1.** "Claude Code is an **agentic** graph that uses **Claude LLMs** under the hood."

**A2.** Any three from: Read (read files from disk), Write (create/modify files), Bash (execute shell commands), Glob (list files matching a pattern), Grep (search file contents), WebSearch (look things up online), Agent (spawn sub-agents for parallel work).

**A3.** Bash (create folder with `mkdir`), Write (create the script file), Bash (run the script), Write (create the log file). Order: Bash → Write → Bash → Write.

**A4.** Claude Code needs to execute commands on your operating system — create folders, run scripts, install packages. This requires terminal access. A browser extension runs in a sandboxed environment with no OS-level access.

**A5.** Claude Code sees the exception, reads the error message, attempts to diagnose the cause, modifies the code to fix the issue, and re-runs the script. It continues this loop until it succeeds or exhausts its retry strategy.

**A6.** Skill bodies can be large (detailed step-by-step instructions). If all skill bodies were always in context, they'd consume thousands of tokens every session even for sessions that don't use those skills. Loading only on invocation means you only pay for what you actually use.

---

## Module 03

**A1.** `npm install -g @anthropic-ai/claude-code` (or `brew install anthropic/tap/claude` with Homebrew).

**A2.** The installer adds Claude Code to the PATH for that system, but the current terminal session doesn't know about the updated PATH yet. Fix: add the Claude Code executable path to user environment variables (Win key → "environment variables" → User variables → Path → New → paste the path from the installer output), then open a new terminal.

**A3.** API credits: pay per token, no monthly commitment, good for learning or variable usage. Subscription: flat monthly fee, good for heavy daily use where you want predictable costs. Choose API for learning; switch to subscription when you're using Claude Code daily at work.

**A4.** `/cost` shows the number of tokens used and the dollar cost for the current session. Check it after each session when learning to understand which types of tasks are expensive and build cost awareness before moving to heavier use.

**A5.** `/model` — then use arrow keys to select from the available models.

**A6.** VS Code's integrated terminal is in the same process as your editor, so you can see code changes and Claude Code output side-by-side. You also get the Claude Code VS Code extension for native integration. A separate terminal requires window-switching, which is slower.

---

## Module 04

**A1.** `your-project/.claude/CLAUDE.md`

**A2.** Both are loaded. Claude Code reads the system-level CLAUDE.md (`~/.claude/CLAUDE.md`) first, then the project-level one. Both are injected into the context on startup.

**A3.** (1) Project overview — what it does, tech stack. (2) Standards and conventions — coding rules, library preferences, naming conventions. (3) Project structure — what lives in which folder. (4) Important constraints — hard rules, things to always check, things to never do.

**A4.** Most likely cause: CLAUDE.md has grown too large. Run `/context` and look at the "System prompt" token count. Audit CLAUDE.md and remove anything that isn't regularly needed — especially long explanations (use bullet points), unnecessary examples, and anything that belongs in a skill instead.

**A5.** A 30-step deployment process in CLAUDE.md would add hundreds of tokens to every single session, even sessions that have nothing to do with deployment. Those tokens cost money every time. Put the deployment process in a skill (e.g., `/deploy`). The skill body only loads when you invoke `/deploy`.

**A6.** False. CLAUDE.md is automatically injected at the start of every session, without any explicit request.

---

## Module 05

**A1.**
```
.claude/
└── skills/
    └── daily-report/
        └── skill.md
```

**A2.** The `description` is used for automatic skill detection — when you write a natural language prompt, Claude Code reads all skill descriptions to decide whether any skill is relevant. Good: `"Use this skill when generating, refreshing, or updating daily reports from the data warehouse. Invoke for requests about reporting, KPIs, or summaries."` Bad: `"Generates reports."` The good one answers when to invoke it; the bad one just names the output.

**A3.** `skill.md` (required — the skill definition). `scripts/` (optional — pre-written Python scripts the skill runs instead of generating code from scratch). `references/` (optional — supporting documentation, error catalogs, org-specific docs that Claude Code can consult when relevant).

**A4.** The YAML metadata block is missing or malformed. The `name` field in the YAML header must match the folder name exactly. Check for a `---` opening and closing, and verify the name field.

**A5.** `/skill-name` (direct invocation) is faster, more reliable, and always runs the exact skill steps. Natural language invocation is useful when you forget the skill name or want Claude Code to choose the best skill for a vague prompt. Prefer direct for repeating tasks; use natural language for exploration.

**A6.** Edit the `skill.md` file — find the step that specifies the output location and correct the path. Re-run the skill. Skills are meant to be iterated on: run → observe → fix → re-run until the behavior matches your intent.

**A7.** Token economy. The skill metadata (name + description) is small (~50 tokens) and tells Claude Code what skills exist. The skill body may be hundreds of tokens of detailed instructions. Loading all skill bodies at all times would bloat every session. Only the invoked skill's body needs to be in context.

---

## Module 06

**A1.** When a task has multiple independent parts that can run in parallel, when context isolation is needed (each agent starts fresh), or when the total work exceeds one context window.

**A2.** Through memory files — markdown files that Claude Code reads at the start of a session (configured via CLAUDE.md) and updates during/after the session. On the next session it reads the updated file, carrying knowledge forward.

**A3.** The root cause (async timeout too short for large datasets), the fix applied (increased from 10s to 60s), and any related caveats discovered (e.g., which specific endpoint is slowest). Future sessions can use this without re-debugging.

**A4.** Claude Code scans the project structure, reads up to ~10 key files, understands what each DAG does, and generates a `README.md` with project overview, architecture, DAG-by-DAG descriptions, data flow, dependencies, and how to run it. A developer new to the project gets a plain-English explanation of 80 DAGs in ~2 minutes.

---

## Module 07

**A1.** `PreToolUse` fires *before* Claude Code executes a tool — useful for validation or blocking certain actions. `PostToolUse` fires *after* a tool executes — useful for running checks, linting, or logging in response to what just happened.

**A2.**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "command",
        "command": "ruff check $CLAUDE_TOOL_INPUT_PATH --fix"
      }]
    }]
  }
}
```

**A3.** `$CLAUDE_REPO_ROOT`

**A4.** (1) Switch to a lighter test command — run only the test file related to what changed, or use `-x` to stop at first failure and `-q` for quiet output. (2) Move the test hook to a `Stop` hook instead of `PostToolUse` — this runs tests once at the end of the session rather than after every single file write.

**A5.** Example: A hook that validates Airflow DAG syntax after any file in `dags/` is written:
```json
{
  "PostToolUse": [{
    "matcher": "Write",
    "hooks": [{
      "type": "command",
      "command": "python -c \"from airflow.models import DagBag; b=DagBag('$CLAUDE_REPO_ROOT/dags'); print('Errors:', b.import_errors or 'None')\""
    }]
  }]
}
```

---

## Module 08

**A1.** Version 2.1.72 or later. Check with: `claude --version`

**A2.** `/loop 30 6 * * 1-5 /fetch-api`

**A3.** `0 9 * * 1,4`

**A4.** Scheduled jobs auto-expire after 3 days by default. To fix: recreate the job with `/loop <cron> <prompt>` again, and note the new Job ID.

**A5.** `/cron delete <JOB_ID>` — using the specific Job ID shown when the job was created.

**A6.** Claude Code's scheduler requires the local machine to be on and Claude Code to be running. If the machine is off or asleep, no jobs fire. For true production scheduling (cloud, 24/7, reliable), use Apache Airflow, AWS EventBridge, GitHub Actions scheduled workflows, or a cron job on a always-on server.

---

## Module 09

**A1.** Model Context Protocol. Created by Anthropic.

**A2.** MCP is a universal connector standard (like USB-C) that lets Claude Code plug into external tools. Each tool is a different "device" (Gmail, GitHub, Snowflake). The JSON config file is the "cable." The same config works with any MCP-compatible client, just like a USB-C cable works with any USB-C device.

**A3.** Local: the server code runs on your machine, executed via `uvx` or `npx`. Hosted: the server runs in the cloud, Claude Code connects via HTTP. Local servers are more common today because the hosted (streamable HTTP) standard is newer and most providers haven't migrated yet.

**A4.** Run `/context` inside Claude Code and look for the server name listed under "MCP tools". If it doesn't appear, check: the package is installed, env vars are set, JSON syntax is valid, and you fully restarted Claude Code.

**A5.**
```json
{
  "mcpServers": {
    "postgres": {
      "command": "uvx",
      "args": ["mcp-server-postgres", "postgresql://localhost/sales_db"]
    }
  }
}
```

**A6.** Never hardcode credentials directly in settings.json. Use `${ENV_VAR_NAME}` syntax to pull from environment variables, which keeps secrets out of version control.

---

## Module 10

**A1.** A skill you build yourself lives in your `.claude/skills/` folder and is specific to your project. A marketplace plugin is a pre-packaged skill or MCP integration created by Anthropic, a vendor, or the community — installable with `/plugins install name` and usable by anyone.

**A2.** smithery.ai and skills.mp (GitHub is also acceptable).

**A3.** `/plugins`

**A4.** `/simplify`, `/debug`, `/badge`

**A5.**
```
my-skill/
├── skill.md
├── README.md
└── package.json
```
With `package.json` containing name, version, description, and a `claudeCode` field specifying type and command.
