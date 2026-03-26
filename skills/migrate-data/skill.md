---
name: migrate-data
description: >
  Use this skill when converting, transforming, or migrating data between
  file formats (CSV, Parquet, JSON, ORC). Handles schema inference,
  type casting, and large file processing. Invoke when asked to
  "convert files", "migrate data", or "transform format".
usage: /migrate-data
---

# Migrate Data skill

Converts data files between formats with schema validation and logging.
Supports CSV ↔ Parquet ↔ JSON ↔ ORC conversions.

## Pre-conditions
- Source files exist in the configured input directory
- Python environment available
- Required packages: pandas, pyarrow (install if missing)

## Steps

### Step 1 — Activate environment
Activate .venv if it exists. Otherwise use system Python.

### Step 2 — Install dependencies
```
pip install pandas pyarrow
```

### Step 3 — Scan input directory
Scan the `data/incoming/` directory for files to migrate.
List all files found, grouped by format.
If no files found, report and exit cleanly.

### Step 4 — Decide output format
**Decision rule for output format:**
- Under 50,000 rows → CSV (human-readable, easy to inspect)
- 50,000–1,000,000 rows → Parquet (columnar, fast reads)
- Over 1,000,000 rows → Parquet with snappy compression (storage-efficient)
- Explicit request overrides this rule

### Step 5 — Run migration script
A pre-built, tested script is available at:
  `.claude/skills/migrate-data/scripts/migrate_data.py`

Run it using the .venv Python environment:
  `.venv/bin/python .claude/skills/migrate-data/scripts/migrate_data.py`

Do NOT rewrite or regenerate this script. Use it as-is.
To force a specific output format: append `--format parquet` or `--format csv`.
The script reads from `data/incoming/` and writes to `data/migrated/YYYY-MM-DD_HH-MM-SS/`.

### Step 6 — Validate output
After conversion, read each output file back and verify:
- Row count matches source
- No data was silently dropped
- Schema matches expectations

### Step 7 — Log results
Write a migration report to `logs/migrate-data/YYYY-MM-DD/migration-report.log`:
- Source file → target file
- Source format → target format
- Row count (source vs output — must match)
- File size before and after
- Any schema warnings or type cast decisions
- Success/failure per file

## Format decision reference

| Source | Best target | When |
|---|---|---|
| CSV | Parquet | Large files, repeated reads |
| CSV | JSON | Need nested structure |
| Parquet | CSV | Need human-readable output |
| JSON | Parquet | Performance-critical pipeline |
| JSON | CSV | Flat structure, small dataset |

## Expected output
```
data/
└── migrated/
    └── 2025-03-15_09-30-00/
        ├── customers.parquet
        └── orders.parquet
logs/
└── migrate-data/
    └── 2025-03-15/
        └── migration-report.log
```
