# Quizzes — All Modules

Self-test questions for all 10 modules. Try to answer before checking the answers file.

→ [Answers](answers.md)

---

## Module 01 — Claude Models & Ecosystem

**Q1.** Name the three Claude model tiers in order from smallest to largest, and describe each in one sentence.

**Q2.** What is the key difference between Claude.ai and Claude Code? (One sentence each.)

**Q3.** You're a developer learning Claude Code for the first time. You have $10 in API credits. Which model should you use to keep learning costs low, and why?

**Q4.** What does "1M token context window" mean for Opus, and why is it useful for data engineering work?

**Q5.** True or false: Claude Code is available for free with a Claude.ai account.

---

## Module 02 — Architecture

**Q1.** Complete this definition: "Claude Code is an __________ graph that uses __________ under the hood."

**Q2.** List three built-in tools Claude Code has access to, and explain what each one does.

**Q3.** A developer asks Claude Code: "Create a folder called output, write a Python script into it, run the script, and log the result." Which built-in tools would Claude Code need to use, in what order?

**Q4.** Why does Claude Code run in the terminal rather than as a browser extension?

**Q5.** What happens in the agentic feedback loop when a script that Claude Code generated throws a Python exception?

**Q6.** A skill's body is only loaded into context when the skill is invoked. Why does this matter for cost?

---

## Module 03 — Installation & Setup

**Q1.** What command installs Claude Code on macOS/Linux?

**Q2.** A Windows user installs Claude Code but gets `'claude' is not recognized as an internal or external command` when they type `claude`. What is the most likely cause and how do they fix it?

**Q3.** What is the difference between paying via API credits vs a subscription? When would you choose each?

**Q4.** What does the `/cost` command show, and why should you check it during a learning session?

**Q5.** What command do you run to change the active model inside Claude Code?

**Q6.** Why is it recommended to open Claude Code inside VS Code's integrated terminal rather than a separate terminal window?

---

## Module 04 — CLAUDE.md

**Q1.** Where do you put a project-level CLAUDE.md file?

**Q2.** You have a project-level CLAUDE.md and also a system-level CLAUDE.md. When you start Claude Code in your project folder, which one(s) are loaded?

**Q3.** List four categories of content that belong in a good CLAUDE.md.

**Q4.** You've noticed your `/context` output shows 18,000 tokens in the system prompt — much higher than usual. What is the most likely cause and what should you do?

**Q5.** A colleague suggests putting a 30-step deployment process into CLAUDE.md so Claude Code always knows how to deploy. Why is this a bad idea, and what should you do instead?

**Q6.** True or false: CLAUDE.md is injected into context only when you explicitly ask Claude Code to read it.

---

## Module 05 — Skills

**Q1.** What is the file path structure for a skill named `daily-report`?

**Q2.** What is the purpose of the `description` field in the skill YAML metadata? Give an example of a good description vs a bad one.

**Q3.** What are the three folders a skill directory can contain, and when would you use each?

**Q4.** You've created a skill but it doesn't appear when you type `/`. What is the most likely cause?

**Q5.** Explain the difference between invoking a skill with `/skill-name` vs using natural language. When is each approach preferable?

**Q6.** After running your `/fetch-api` skill twice, you notice it writes files to the wrong location. How do you fix this without completely rewriting the skill?

**Q7.** Why is the skill body *not* included in context unless the skill is invoked, while the skill metadata always is?

---

## Module 06 — Sub-agents & Memory

**Q1.** In what scenario would you use sub-agents instead of a single agent?

**Q2.** How does Claude Code achieve persistent memory between sessions (it has none by default)?

**Q3.** You've just spent an afternoon debugging a tricky async timeout issue in your pipeline. What should you add to your memory file before ending the session?

**Q4.** A new developer joins your team and runs `/readme-gen` on a project with 80 DAG files. What does Claude Code do, and what does the output look like?

---

## Module 07 — Hooks

**Q1.** What is the difference between a `PreToolUse` hook and a `PostToolUse` hook?

**Q2.** You want to run `ruff check --fix` every time Claude Code writes a Python file. Write the settings.json configuration for this hook.

**Q3.** Which environment variable gives you the path to the project root directory inside a hook command?

**Q4.** Your PostToolUse hook runs the full test suite on every file write. Claude Code is now very slow. What are two ways to fix this?

**Q5.** Design a hook that would be specifically useful for a data engineering project (not one of the examples from the module).

---

## Module 08 — Scheduling

**Q1.** What Claude Code version is required for scheduling? How do you check your version?

**Q2.** Write a /loop command to run the `/fetch-api` skill every weekday at 6:30am.

**Q3.** Write a cron expression for "every Monday and Thursday at 9:00am".

**Q4.** You created a scheduled job three days ago. It stopped running. Why, and how do you fix it?

**Q5.** How do you cancel a specific scheduled job without stopping all other scheduled jobs?

**Q6.** You want to use scheduling for production work but your laptop is often closed. What is the fundamental limitation of Claude Code's scheduler, and what would you use instead for true production scheduling?

---

## Module 09 — MCP Servers

**Q1.** What does MCP stand for, and who created the standard?

**Q2.** Explain the USB-C analogy for MCP in your own words.

**Q3.** What is the difference between a local MCP server and a hosted MCP server? Which type is more common today?

**Q4.** You've added a GitHub MCP server to your settings.json. After restarting Claude Code, how do you verify it loaded correctly?

**Q5.** Write the settings.json configuration for a local PostgreSQL MCP server connecting to a database called `sales_db` on localhost.

**Q6.** What is one important security practice when configuring MCP servers with credentials?

---

## Module 10 — Plugins & Marketplace

**Q1.** What is the difference between a skill you build yourself and a plugin from the marketplace?

**Q2.** Name two community registries where you can find Claude Code plugins and MCP servers.

**Q3.** What slash command opens the plugin browser?

**Q4.** Name the three built-in skills that ship with Claude Code (no installation needed).

**Q5.** You want to share a skill you've built with the community. What file structure does a minimal shareable plugin need?
