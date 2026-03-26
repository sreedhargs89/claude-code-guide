# Contributing

Contributions are welcome — especially new skill templates, additional examples, and corrections.

## What to contribute

- **New skills**: Add a folder to `skills/` with a `skill.md` following the template in `cheatsheets/skill-template.md`
- **New examples**: Add a folder to `examples/` — include both `generic/` and `data-engineering/` variants where relevant
- **Corrections**: Fix anything factually wrong in the docs — Claude Code evolves fast and docs go stale
- **New module docs**: If a significant feature is missing from the 10 modules, open an issue first to discuss

## Structure rules

- Every new doc in `docs/` must follow the existing format: prerequisites, time estimate, concept sections, check-your-understanding, link to quiz
- Every new skill must have a YAML header with `name` and `description`
- Every new example must have a `README.md` explaining what it does and how to run it
- Quiz questions must be answerable from the docs alone — no external knowledge required

## Pull request checklist

- [ ] Python files include type hints
- [ ] New examples tested locally (run them, verify output)
- [ ] Skill descriptions are written from the "when to invoke" perspective
- [ ] No hardcoded credentials anywhere
- [ ] README updated if a new section was added

## Reporting issues

Open a GitHub issue with:
- Which module/file is affected
- What is currently wrong
- What the correct content should be (with a source if possible)
