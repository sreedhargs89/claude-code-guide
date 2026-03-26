# Example: Data Migration (Data Engineering)

Migrates dimensional and fact table CSV files to Parquet with schema validation.
Applies different format rules for dim vs fact tables and validates row counts.

## What it does

- Processes `dim_*` and `fact_*` tables separately (dims always → Parquet; facts use size rules)
- Validates each table against an expected schema (warns on missing columns, all-null columns)
- Reads back each output file to confirm row counts match
- Generates a detailed migration report with before/after sizes and compression ratios
- Logs schema warnings separately so you can audit data quality issues

## Quick start

```bash
cd examples/data-migration/data-engineering

pip install pandas pyarrow

# Create sample input data
mkdir -p data/incoming
python -c "
import pandas as pd
pd.DataFrame({'customer_id':[1,2,3],'customer_name':['Alice','Bob','Charlie'],'email':['a@x.com','b@x.com','c@x.com'],'country':['JP','US','AU'],'created_date':['2024-01-01','2024-02-01','2024-03-01']}).to_csv('data/incoming/dim_customer.csv', index=False)
pd.DataFrame({'sale_id':range(1,1001),'date_id':range(1,1001),'customer_id':[1,2,3]*(334)[:1000],'store_id':[1]*1000,'product_id':[1,2]*500,'quantity':[2]*1000,'revenue':[99.99]*1000}).to_csv('data/incoming/fact_sales.csv', index=False)
print('Sample data created.')
"

python migrate_data_de.py
```

## Output

```
data/
└── migrated/
    └── 2025-03-15_09-30-00/
        ├── dim_customer.parquet    ← always Parquet (dim rule)
        └── fact_sales.parquet      ← Parquet (>50K rows rule)
logs/
└── migrate-data/
    └── 2025-03-15/
        └── migration-report.log
```

## Format decision rules (data warehouse context)

| Table type | Rule | Output |
|---|---|---|
| `dim_*` | Always Parquet | Fast repeated reads in star schema joins |
| `fact_*` < 50K rows | CSV | Small enough to stay human-readable |
| `fact_*` 50K–1M rows | Parquet | Columnar for analytical queries |
| `fact_*` > 1M rows | Parquet + snappy | Compression for large fact tables |
| User `--format` flag | Overrides all | Force a specific output |

## Adapting the schema validation

Edit `EXPECTED_SCHEMAS` to match your actual warehouse:

```python
EXPECTED_SCHEMAS = {
    "dim_customer": {
        "customer_id": "int64",
        "customer_name": "object",
        # add your actual columns
    },
    "fact_sales": {
        "sale_id": "int64",
        "revenue": "float64",
        # add your actual columns
    },
}
```

## CLI options

```bash
python migrate_data_de.py --format parquet         # force all tables to Parquet
python migrate_data_de.py --input data/raw         # use a custom input directory
python migrate_data_de.py --format csv --input /tmp/tables
```

## Using with the /migrate-data skill

Copy this script into your skill's scripts folder:

```
.claude/skills/migrate-data/
├── skill.md
└── scripts/
    └── migrate_data_de.py
```

Then reference it in `skill.md`:
```markdown
### Step 3 — Run migration
Run .claude/skills/migrate-data/scripts/migrate_data_de.py
using the .venv Python environment.
Input directory: data/incoming/
```

## See also

- [Generic variant](../generic/) — format-agnostic, no star schema assumptions
