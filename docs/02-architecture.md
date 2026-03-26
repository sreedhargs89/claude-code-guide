# Module 02 — Claude Code Architecture

**Prerequisites:** [Module 01](01-claude-models.md)  
**Time:** ~25 minutes  
**Next:** [Module 03 — Installation](03-installation.md)

---

## The one-line definition

> **Claude Code is an agentic graph that uses Claude LLMs under the hood.**

That's the whole thing. Everything else — skills, hooks, MCP, sub-agents — is just building on top of this foundation.

---

## What "agentic graph" means

A regular LLM call looks like this:

```
You → [prompt] → LLM → [text response] → You
```

An *agentic graph* adds a feedback loop and tools:

```
You → [prompt] → LLM → decides what to do
                          ↓
                    [tool call: write file]
                          ↓
                    [tool call: run script]
                          ↓
                    [tool call: check output]
                          ↓
                    LLM evaluates result
                          ↓
                    Done? → Response to You
                    Error? → Fix and retry
```

The LLM is still in the middle, but now it has *agency* — it can take multi-step actions, observe results, fix errors, and loop until the task is complete. You don't need to intervene.

---

## The built-in tools

Claude Code ships with tools that live on your local system. These are what give it the ability to act:

| Tool | What it does |
|---|---|
| `Read` | Reads files from disk |
| `Write` | Creates or modifies files |
| `Bash` | Executes shell commands |
| `Glob` | Lists files matching a pattern |
| `Grep` | Searches file contents |
| `TodoRead / TodoWrite` | Manages task state across a session |
| `WebSearch` | Looks up information online |
| `Agent` | Spawns a sub-agent for parallel work |

When Claude Code needs to create a folder, it uses `Bash` to run `mkdir`. When it needs to install a package, it runs `pip install`. These aren't magic — they're just system calls, the same ones you'd run yourself.

---

## Why it lives in the terminal

Claude Code cannot work as a browser extension or web app because it needs to run commands on your machine. The terminal is the control plane for your OS. When you open Claude Code in VS Code's integrated terminal, it has access to everything in that project directory — same as you do when you type commands manually.

This is also why it asks "do you trust this folder?" on startup. It's requesting permission to act on your behalf in that directory.

---

## The architecture stack

From bottom to top:

```
┌────────────────────────────────────────┐
│  Claude LLM (Haiku / Sonnet / Opus)    │  ← hosted on Anthropic's servers
│  The "brain" — generates all code,    │
│  plans steps, interprets results       │
├────────────────────────────────────────┤
│  Built-in tools                        │  ← lives on YOUR system
│  File system, bash, search, agent...   │
├────────────────────────────────────────┤
│  Custom skills (.claude/skills/)       │  ← you build these
│  Orchestration templates in plain text │
├────────────────────────────────────────┤
│  MCP servers (external)                │  ← connects to external tools
│  Gmail, GitHub, Slack, DBs, etc.       │
├────────────────────────────────────────┤
│  Your terminal / VS Code               │  ← where you interact
└────────────────────────────────────────┘
```

---

## How a request flows

Here's what happens when you type `/fetch-api` in Claude Code:

1. Claude Code reads your `CLAUDE.md` (project context)
2. It loads the metadata for your `fetch-api` skill (description + name only)
3. You confirm — Claude Code now loads the full `skill.md` body
4. The LLM reads the skill instructions and generates a plan
5. It makes tool calls: write a Python script, run it, check for errors
6. If errors occur, it fixes them and retries automatically
7. It logs results and reports back to you

The key insight: the skill body is only loaded **when the skill is invoked**. At all other times, only the metadata is in context. This is how Claude Code stays efficient with tokens.

---

## Building your own Claude Code (conceptually)

Claude Code is not a black box. The same pattern can be built with any LLM + tool framework (LangGraph, LlamaIndex agents, etc.):

```python
# Pseudocode — this is what Claude Code does under the hood
def run_agent(prompt, tools, context):
    while not done:
        response = llm.call(prompt, context, tools)
        if response.is_tool_call:
            result = execute_tool(response.tool, response.args)
            context.append(result)
        elif response.is_done:
            return response.text
        else:
            context.append(response)
```

Understanding this loop means you'll never be confused by Claude Code's behavior. If it keeps retrying something, it's in the feedback loop trying to resolve an error. If it seems to "think" for a while, it's making multiple sequential tool calls.

---

## What the learning curve actually looks like

The course instructor described it this way — and it's accurate:

> The learning graph for Claude Code is not a straight line. It starts, goes sideways, circles back, then jumps. You'll feel like you're not progressing and then suddenly things click.

The reason: Claude Code has many interacting components (skills, hooks, MCP, agents). Understanding each one in isolation is easy. Understanding how they compose is where the depth is. By the end of this guide, you'll have that composability mental model.

---

## Check your understanding

1. What is the difference between the LLM and the tools in Claude Code's architecture?
2. Why does Claude Code need to run in a terminal rather than a browser?
3. What happens in the feedback loop when Claude Code encounters an error?
4. Why is skill body content *not* loaded into context unless the skill is invoked?

→ Full quiz: [quizzes/module-02.md](../quizzes/module-02.md)

---

**Next:** [Module 03 — Installation & Setup →](03-installation.md)
