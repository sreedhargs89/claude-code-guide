# Example: Sub-agents

Demonstrates how to structure a Claude Code skill that delegates work to
sub-agents in parallel — the pattern used by `/readme-gen` on large codebases.

## The pattern

Instead of one agent loading all files into one context window:

```
One agent → loads 80 DAG files → context overflow / expensive
```

Use parallel sub-agents:

```
Parent agent
├── Sub-agent A → reviews DAGs 01–27
├── Sub-agent B → reviews DAGs 28–54
└── Sub-agent C → reviews DAGs 55–80
          ↓
Parent agent consolidates all three reports
```

## Skill that uses sub-agents

Here is a skill template that explicitly requests sub-agent parallelism:

```markdown
---
name: review-large-project
description: >
  Use this skill to review a project with many files by splitting work
  across parallel sub-agents. Use when reviewing >20 files at once.
---

## Steps

### Step 1 — List all target files
List all Python files in the src/ directory.
Group them into batches of ~15 files each.

### Step 2 — Spawn sub-agents in parallel
Use the agent tool to spawn one sub-agent per batch.
Pass each sub-agent:
- The list of files it should review
- The review criteria below

**Review criteria for each sub-agent:**
- Check for missing type hints
- Check for hardcoded credentials
- Check for functions longer than 30 lines
- Report the top 3 issues per file

### Step 3 — Wait for all sub-agents to complete
Collect the output from each sub-agent.

### Step 4 — Consolidate
Merge all sub-agent findings into a single report at:
  reports/project-review-YYYY-MM-DD.md

Deduplicate any repeated findings. Sort issues by severity.
```

## When Claude Code uses sub-agents automatically

You don't always need to ask explicitly. Claude Code will spawn sub-agents
when it detects a task that benefits from parallelism:

- "Review all 50 files in this repo"
- "Scan each DAG and explain what it does"
- "Check every script for security issues"

If you want to force parallel execution, add: "work in parallel where possible"
to your prompt.

## Memory across sub-agents

Sub-agents do NOT share context with each other or with the parent.
To pass information between them, use files:

```markdown
### Step 2 — Sub-agent instructions
Each sub-agent should:
1. Review its assigned files
2. Write its findings to: .claude/tmp/agent-{N}-findings.md
3. Report "done" when complete

### Step 3 — Parent reads all findings
Read all files matching .claude/tmp/agent-*-findings.md
and merge them into the final report.
```

## Cleanup

```markdown
### Step 5 — Cleanup
Delete all files in .claude/tmp/ after the final report is written.
```

## Cost consideration

Each sub-agent is a separate Claude Code session with its own token usage.
For 3 sub-agents, you're paying for 3× the LLM calls.

Use sub-agents when:
- The parallelism saves significant real time (>10 minutes of serial work)
- Context isolation is important (e.g., each agent needs a clean slate)
- The task genuinely can't fit in one context window

Don't use sub-agents for tasks that take <5 minutes total.
