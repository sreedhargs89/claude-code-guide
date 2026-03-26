# Cheatsheet — CLAUDE.md Template

> Copy this into `.claude/CLAUDE.md` in your project and fill in the blanks.

---

## Generic template

```markdown
# [Project Name]

## Project overview
[1–3 sentences: what this project does, why it exists, who uses it]

Tech stack: [list your main tools, languages, frameworks, versions]

## Standards and conventions
- [Code style rule — e.g., "All functions must have type hints"]
- [Naming convention — e.g., "Files use snake_case, classes use PascalCase"]
- [Library preference — e.g., "Use httpx for HTTP, not requests"]
- [Environment rule — e.g., "Always use .venv virtual environment"]
- [Credentials rule — e.g., "Never hardcode credentials — use .env"]

## Project structure
- [folder/]     [what lives here]
- [folder/]     [what lives here]
- [folder/]     [what lives here]

## Important
- [Critical constraint 1]
- [Critical constraint 2]
- [Anything Claude Code should always check before acting]
```

---

## Data engineering template

```markdown
# [Pipeline Name] — Data Engineering Project

## Project overview
[Data source] → [transformation] → [destination].
Runs on [schedule]. Owns [what datasets].

Tech stack: Python 3.11, PySpark 3.5, Apache Airflow 3.0, [destination DB]

## Standards
- All I/O must use async/await (httpx, aiofiles — not requests or open())
- Type hints required on all functions
- DAGs must pass `python -m py_compile` and Airflow DagBag validation
- Never hardcode credentials — use environment variables from .env
- Log all API responses with HTTP status codes and record counts
- Parquet preferred over CSV for large datasets (>100K rows)

## Project structure
- dags/          Airflow DAG definitions
- scripts/       Standalone Python scripts (fetch, transform, load)
- data/          Local data files (gitignored)
- logs/          Runtime logs (gitignored)
- tests/         pytest test suite
- .claude/       Claude Code config (skills, memory, settings)

## Environment
- Virtual environment: .venv/
- Activate: source .venv/bin/activate (Linux/Mac) or .venv\Scripts\activate (Windows)
- Always activate before running Python scripts

## Important
- Never delete files in data/ without asking
- Run tests before marking any task complete: python -m pytest tests/ -q
- Check Airflow DAG validation when modifying any file in dags/
```

---

## Software development template

```markdown
# [App Name]

## Project overview
[What the app does in 1–2 sentences]

Tech stack: [language], [framework], [database], [other key tools]

## Standards
- [Test coverage rule — e.g., "All new functions need a test"]
- [PR rule — e.g., "Never push directly to main"]
- [Error handling — e.g., "All exceptions must be logged, not silently swallowed"]
- [API rule — e.g., "All endpoints must return consistent error shapes"]

## Project structure
- src/           Application source code
- tests/         Test suite
- docs/          Documentation
- scripts/       Dev and deployment scripts

## Important
- Run `npm test` before marking any feature complete
- Check for TypeScript errors with `tsc --noEmit` after changes
- API keys and secrets in .env (never commit .env)
```

---

## Tips for writing CLAUDE.md

1. **Concise over complete.** Every line in CLAUDE.md costs tokens on every session. Cut ruthlessly.
2. **Rules over explanations.** "Use httpx not requests" > "We prefer httpx because it supports async which is important for..."
3. **Paths matter.** Always spell out exact paths for important locations (`data/incoming/`, not just "the data folder")
4. **Constraints > preferences.** State hard rules clearly. Soft preferences can go in your personal system-level CLAUDE.md.
5. **Run `/context` periodically.** If your system prompt creeps past 10K tokens, audit CLAUDE.md.
