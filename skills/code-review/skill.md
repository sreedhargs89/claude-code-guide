---
name: code-review
description: >
  Use this skill to review recently changed or newly written code files.
  Checks for bugs, style violations, security issues, and improvements.
  Invoke when asked to "review code", "check my changes", "audit this file",
  or "find issues in the code".
usage: /code-review
---

# Code Review skill

Reviews code files for issues, improvements, and standards compliance.
Generates a structured report with actionable findings.

## Steps

### Step 1 — Identify files to review
Determine which files to review:

**Option A — Recent git changes (preferred)**
```bash
git diff --name-only HEAD~1 HEAD
```
Review all changed files from the last commit.

**Option B — Specific files**
If the user specified files in their prompt, review those files.

**Option C — All source files**
If no git history and no specific files, scan the main source directory
and review up to 10 files (prioritize by file size, largest first).

### Step 2 — Read each file
Read each file completely. Note:
- File size and complexity
- Language and framework
- Purpose (inferred from name, imports, function signatures)

### Step 3 — Review each file
For each file, check these categories:

**Bugs and correctness**
- Logic errors or off-by-one mistakes
- Unhandled edge cases (null values, empty lists, zero division)
- Error handling that silently swallows exceptions
- Race conditions or async/await misuse
- Incorrect type usage

**Security**
- Hardcoded credentials, tokens, or secrets
- SQL or command injection vulnerabilities
- Unsafe deserialization
- Missing input validation

**Performance**
- N+1 query patterns
- Unnecessary re-computation in loops
- Missing indexes (if SQL)
- Large data loaded into memory unnecessarily

**Code quality**
- Functions doing too many things (>30 lines = consider splitting)
- Missing or incorrect type hints (for Python)
- Unclear variable or function names
- Duplicated code that could be extracted
- Missing docstrings on public functions

**Standards compliance**
- Matches conventions in CLAUDE.md (if present)
- Follows project patterns (check other files for context)

### Step 4 — Generate review report
Write the report to `reports/code-review/YYYY-MM-DD_HH-MM-SS-review.md`:

```markdown
# Code Review — [Date]

## Summary
Reviewed X files. Found Y issues (Z critical, W warnings, V suggestions).

## Files reviewed
- [file1.py] — [brief description]
- [file2.py] — [brief description]

## Critical issues (fix before merging)
### [filename]:[line number]
**Issue:** [what's wrong]
**Fix:** [specific suggested fix or code snippet]

## Warnings (should fix)
### [filename]:[line number]
**Issue:** [what's wrong]
**Suggestion:** [what to do]

## Suggestions (consider fixing)
[Lower priority improvements]

## Positives
[What the code does well — always include at least one]
```

### Step 5 — Print summary
After writing the report, print a brief summary to the console:
- Total issues found by severity
- The single most important issue to fix first
- Path to the full report

## Severity guide
- **Critical**: data loss risk, security vulnerability, crash potential
- **Warning**: bug that affects correctness but won't crash
- **Suggestion**: style, readability, performance improvements

## Notes
- Focus on actionable, specific feedback — not vague "improve this"
- For every critical issue, provide a concrete fix
- Don't flag style issues as critical
- Be constructive — note what works well alongside what doesn't
