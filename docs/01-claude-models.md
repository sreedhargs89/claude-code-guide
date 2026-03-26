# Module 01 — Claude Models & the Anthropic Ecosystem

**Prerequisites:** None  
**Time:** ~20 minutes  
**Next:** [Module 02 — Architecture](02-architecture.md)

---

## What is Anthropic?

Anthropic is an AI safety company that builds large language models (LLMs). Think of it like OpenAI — they make the models that power AI assistants. Where OpenAI has GPT-4 and GPT-5, Anthropic has the **Claude** family.

---

## The three Claude tiers

Every Claude model belongs to one of three categories. The naming has stayed consistent across releases:

| Tier | Name | Character |
|---|---|---|
| Smallest | **Haiku** | Fast, cheap, good for simple tasks |
| Balanced | **Sonnet** | The sweet spot — recommended for most developer work |
| Largest | **Opus** | Most capable, most expensive, 1M token context window |

The current release (as of this writing) is the **4.x** generation:
- `claude-haiku-4-5`
- `claude-sonnet-4-6` ← personal recommendation for Claude Code
- `claude-opus-4-6` ← most powerful, but expensive at ~$15/M input tokens

> **Tip:** When learning, use Haiku or the default Sonnet to keep costs low. Upgrade to Opus for production work where quality matters most.

---

## Claude vs Claude.ai vs Claude Code

These three names confuse everyone at first. Here's how they relate:

```
Anthropic (the company)
└── builds Claude (the model family)
    └── powers Claude.ai (the chat interface — like ChatGPT)
    └── powers Claude Code (the developer agent)
    └── accessible via API (for your own apps)
```

### Claude.ai
The chat interface. You ask questions, you get answers. Great for Q&A, writing, research. This is the free/Pro/Max subscription product.

**What it can do:** Generate code, answer questions, draft documents.  
**What it cannot do:** Create files, run scripts, interact with your filesystem.

### Claude Code
A developer agent that runs in your terminal. It can:
- Read and write files on your machine
- Execute bash commands and scripts
- Manage folders and project structure
- Make API calls through tools
- Run sub-agents in parallel

**The key difference:** Claude.ai gives you a text response. Claude Code *takes action*.

---

## Why Claude Code exists

Classic LLMs generate tokens — text, code snippets, answers. But they can't:
- Save a file to disk
- Run a script
- Create a folder if it doesn't exist
- Install a package

Claude Code solves this by connecting the LLM to a set of **tools** — file system access, bash execution, subprocess calls. When you ask "create a PySpark script and put it in the scripts folder," Claude Code:

1. Writes the code (LLM capability)
2. Creates the folder if missing (tool: file system)
3. Saves the file (tool: file system)
4. Confirms the result (LLM capability)

---

## Accessing Claude models

### Option 1: Subscription (Claude.ai)
Best if you want the chat interface plus pro features. Starts at ~$20–28/month depending on plan and region.

### Option 2: API (recommended for developers)
Pay per token. You add credits and use them throughout the year. Good for learning because you only pay for what you actually call.

**Getting started with the API:**
1. Go to `console.anthropic.com`
2. Add billing credits (start with $10)
3. Create an API key
4. You're ready

> **Cost reality check:** At Sonnet pricing ($3/M input tokens, $15/M output tokens), normal development use costs a few dollars a month. One million tokens is a *lot* of conversation.

---

## Check your understanding

Quick self-check before moving on:

1. What are the three Claude model tiers, and how do they differ?
2. What can Claude Code do that Claude.ai cannot?
3. If you're learning and want to keep costs low, which model should you use?
4. What does "1M token context window" mean in practical terms?

→ Full quiz: [quizzes/module-01.md](../quizzes/module-01.md)

---

**Next:** [Module 02 — Claude Code Architecture →](02-architecture.md)
