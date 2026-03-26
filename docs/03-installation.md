# Module 03 — Installation & Setup

**Prerequisites:** [Module 02](02-architecture.md)  
**Time:** ~30 minutes (including actual install)  
**Next:** [Module 04 — CLAUDE.md](04-claude-md.md)

---

## Before you start

You need:
- Python (basic install — any recent version)
- A terminal (PowerShell on Windows, Terminal on macOS/Linux)
- An Anthropic account

You do **not** need:
- Node.js (the installer handles this)
- Prior LLM experience
- A paid subscription to start (API credits work fine)

---

## Step 1: Get API access or a subscription

### Option A: API credits (recommended for learners)
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign in (use the same account as Claude.ai if you have one)
3. Click **Billing** → Add credits (start with $10 — enough to learn the entire course)
4. Click **API Keys** → **Create Key**
5. Name it `claude-code-learning` (or anything)
6. Copy and save the key — you only see it once

> **Note:** When you install Claude Code, it automatically creates a key in your console called `claude-code-key`. So you may not need to create one manually.

### Option B: Subscription
Go to claude.ai → Account → Upgrade Plan. The Pro/Max plans include Claude Code with a monthly message allowance. Good if you'll be a heavy daily user.

---

## Step 2: Install Claude Code

### Windows (PowerShell — recommended)

Open PowerShell (not cmd) and run:

```powershell
iwr https://claude.ai/install | iex
```

If you only have cmd, use:

```cmd
curl -L https://claude.ai/install -o install.ps1 && powershell -File install.ps1
```

> **Common issue — "claude is not recognized":**  
> The installer adds Claude Code to your PATH, but the current terminal session doesn't know about it yet. Fix:
> 1. Win key → search "environment variables" → Edit system environment variables
> 2. Click **Environment Variables**
> 3. Under **User variables**, find **Path** → Edit → New
> 4. Paste the path shown at the end of the installer output (usually `%LOCALAPPDATA%\Programs\claude`)
> 5. Click OK → close terminal → open a new one
> 6. Run `claude` — it should work now

### macOS / Linux

```bash
npm install -g @anthropic-ai/claude-code
```

Or with Homebrew:

```bash
brew install anthropic/tap/claude
```

Or with WSL on Windows:

```bash
npm install -g @anthropic-ai/claude-code
```

---

## Step 3: Verify the install

Open a fresh terminal and run:

```bash
claude --version
```

You should see something like `2.1.74`. If you see an error, re-check the PATH step above.

---

## Step 4: First launch

Navigate to a project folder (or just your home directory to start):

```bash
cd ~/my-project
claude
```

On first launch, Claude Code will ask:
1. **Dark mode or light mode** — use arrow keys, hit Enter
2. **How do you want to connect?** — choose "Anthropic console (API)" if you have credits, or "Subscription" if you have Pro/Max

It will then open your browser to authenticate. After login, it creates the `claude-code-key` in your console automatically.

Once you see the Claude Code prompt in your terminal, you're in.

---

## Step 5: Open in VS Code (recommended)

The best way to work with Claude Code as a developer is inside VS Code's integrated terminal. This gives you:
- Side-by-side view of code and Claude Code output
- Direct access to project files
- The Claude Code VS Code extension (optional but useful)

```bash
cd your-project
code .          # opens VS Code
# then open the integrated terminal: Ctrl+` (backtick)
claude          # start Claude Code in that terminal
```

---

## Useful first commands

Once Claude Code is running, try these:

```
/model                    # see and change the active model
/cost                     # see token usage for this session
/context                  # see what's in the current context window
/help                     # list all slash commands
\exit                     # exit Claude Code
```

Change model at startup:

```bash
claude --model claude-haiku-4-5    # cheaper for learning
claude --model claude-sonnet-4-6   # default recommended
```

---

## Managing cost

While learning, keep costs low:
- Use Haiku (`claude-haiku-4-5`) for experimenting — ~$0.25/M input tokens
- Use Sonnet for real work — ~$3/M input tokens
- Run `/cost` after sessions to track usage
- $10 in credits will last weeks of learning at normal usage

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `claude: command not found` | Check PATH (see Step 2 notes) |
| Browser doesn't open for auth | Run `claude login` manually |
| API key error | Check billing has credits at console.anthropic.com |
| Python scripts fail | Make sure Python is in your PATH: `python --version` |
| Wrong model selected | Use `/model` to switch |

---

## Check your understanding

1. What is the difference between using the API and using a subscription?
2. Why does `claude` sometimes fail immediately after install on a fresh machine?
3. What does `/cost` show you, and why is it useful?
4. Why is it recommended to open Claude Code inside VS Code's terminal rather than a standalone terminal?

→ Full quiz: [quizzes/module-03.md](../quizzes/module-03.md)  
→ Cheatsheet: [cheatsheets/commands.md](../cheatsheets/commands.md)

---

**Next:** [Module 04 — CLAUDE.md →](04-claude-md.md)
