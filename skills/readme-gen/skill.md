---
name: readme-gen
description: >
  Use this skill to automatically generate or update a README.md for
  any project. Scans project structure, reads key source files, and
  writes a professional README. Invoke when asked to "generate a README",
  "document this project", or "create project documentation".
usage: /readme-gen
---

# README Generator skill

Scans a project and generates a comprehensive, professional README.md.
Uses the actual code and structure to produce accurate documentation.

## Steps

### Step 1 — Scan project structure
List all files and directories at the project root (2 levels deep).
Identify the project type from the structure:
- Python project: look for setup.py, pyproject.toml, requirements.txt
- Node project: look for package.json
- Data pipeline: look for dags/, airflow, spark, dbt
- General: use file extensions to determine

### Step 2 — Read key files
Read the following files if they exist (in this priority order):
1. Any existing README.md (to understand what's already documented)
2. Main config files (pyproject.toml, package.json, setup.cfg)
3. Main entry point (main.py, app.py, index.js, __init__.py)
4. Up to 3 of the largest/most complex source files
5. Any existing docs/ folder contents

Limit: read no more than 10 files total to stay within context budget.

### Step 3 — Understand the project
From what you've read, identify:
- What the project does (1 sentence)
- Who uses it
- The core workflow or pipeline
- Key components and what each does
- Dependencies and requirements
- How to run or deploy it

### Step 4 — Generate README.md
Write a README.md to the project root with these sections:

```markdown
# [Project Name]

> [One-sentence description]

## Overview
[2-3 paragraphs: what it does, why it exists, who uses it]

## Architecture
[Description of main components and how they connect]
Include a simple ASCII diagram if the architecture is non-trivial.

## Getting started

### Prerequisites
[List all dependencies with versions]

### Installation
[Step-by-step setup instructions]

### Configuration
[Key config files and environment variables needed]

## Usage
[How to run the main workflow — concrete commands]

## Project structure
[Tree of key directories with one-line descriptions]

## Key components
[One section per major component — what it does, key files]

## Development
[How to run tests, lint, add new components]

## Contributing
[Brief contributing guidelines]
```

### Step 5 — Review and refine
After generating, re-read the README and verify:
- No hallucinated features or file paths that don't exist
- All code examples actually work (match the real structure)
- Installation steps are accurate for the detected project type
- The overview accurately reflects what the codebase does

If you find inaccuracies, fix them before finishing.

### Step 6 — Report
Summarize what was documented:
- Sections written
- Files read to generate the documentation
- Any gaps found (things you couldn't document due to missing information)

## Notes
- Do not invent features. Only document what you actually see in the code.
- If a section would be empty or speculative, omit it rather than padding with guesses.
- Use the project's own terminology — don't replace domain terms with generic ones.
- For data engineering projects: always include a data flow section showing source → transform → destination.
