# Module 06 — Sub-agents & Agent Memory

**Prerequisites:** [Module 05](05-skills.md)  
**Time:** ~25 minutes  
**Next:** [Module 07 — Hooks](07-hooks.md)

---

## What sub-agents are

Claude Code can delegate work to sub-agents — separate Claude Code instances running in parallel or in sequence. Each sub-agent has its own context window, its own tools, and its own task. The parent agent coordinates them.

**When to use sub-agents:**
- A task has multiple independent parts that can run in parallel
- You want to isolate context (each sub-agent starts fresh)
- A task is too large for one context window

**Example:** Scanning a project with 50 DAG files. Instead of loading all 50 into one context:
- Parent agent: "Review these 50 files for issues"
- Sub-agent 1: reviews files 1–17
- Sub-agent 2: reviews files 18–34
- Sub-agent 3: reviews files 35–50
- Parent agent: aggregates and summarizes

---

## Invoking sub-agents

You don't invoke sub-agents directly. Claude Code decides when to use them based on task complexity. You can suggest parallelism in your prompt:

```
Review all the DAG files in dags/ and give me a summary of each.
Work in parallel where possible.
```

Or set up a skill that explicitly uses agents:

```markdown
## Steps
### Step 1 — Scan files
Use the agent tool to spawn parallel sub-agents:
- Agent A: analyze all fetch DAGs
- Agent B: analyze all transform DAGs
- Agent C: analyze all load DAGs

### Step 2 — Consolidate
Wait for all agents to complete, then merge their findings into
a single report at reports/dag-review.md
```

---

## Agent memory

Claude Code has no memory between sessions by default — each session starts fresh. But you can give it persistent memory through **memory files**.

A memory file is any markdown file Claude Code can read and write. You reference it in CLAUDE.md:

```markdown
## Memory
Read .claude/memory.md at the start of each session.
Update it with any important context discovered during this session.
```

The memory file itself might look like:

```markdown
# Project memory

## Last session (2025-03-15)
- Fixed the async timeout issue in fetch_customers.py — root cause was
  10s timeout too short for large datasets, increased to 60s
- Discovered that the dim_store table has duplicate store_ids for
  closed stores (keep this in mind when joining)

## Known issues
- fact_sales API sometimes returns 429 — backoff logic needed
- dim_date API has no pagination, always returns full table (3MB)
```

On the next session, Claude Code reads this memory file and carries that context forward. Over time it builds up a working knowledge of your project that would take a human weeks to accumulate.

---

## The readme-gen skill in practice

One powerful application of sub-agents + memory is automated README generation. The skill:

1. Scans your entire project structure
2. Reads key files (main scripts, config, existing docs)
3. Understands what each component does
4. Generates a professional README.md

This is genuinely useful at onboarding. A developer joining a project with 100 DAGs can run `/readme-gen` and get a plain-language explanation of the entire codebase in 2 minutes.

See [skills/readme-gen/](../skills/readme-gen/) for the ready-to-use template.

---

## Check your understanding

1. In what scenario would you use sub-agents instead of a single agent?
2. How does Claude Code achieve persistent memory across sessions?
3. What would you put in a project memory file after a debugging session?

→ Full quiz: [quizzes/module-06.md](../quizzes/module-06.md)

---

**Next:** [Module 07 — Hooks →](07-hooks.md)
