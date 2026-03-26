# Example: Visualise Data (Data Engineering)

KPI-focused visualiser for star schema data. Automatically joins fact and dimension
tables to produce business-ready charts — revenue trends, regional breakdowns,
top products, and return rates.

## What it does

Loads dim_* and fact_* CSV files, joins them intelligently, and produces:

| Chart | Tables used | What it shows |
|---|---|---|
| Revenue over time | fact_sales + dim_date | Monthly revenue trend |
| Revenue by region | fact_sales + dim_store | Sales by store region |
| Top products | fact_sales + dim_product | Top 15 products by revenue |
| Return rate | fact_returns + fact_sales + dim_product | Return % by product |

Any unrecognised table gets a generic bar chart automatically.

## Quick start

```bash
cd examples/visualize/data-engineering

pip install pandas matplotlib seaborn

# Run against the data-engineering fetch example output
python visualize_de.py --input ../../fetch-api/data-engineering/data

# Or let it find the latest data/ folder
python visualize_de.py
```

## Output

```
reports/charts/
└── 2025-03-15/
    ├── revenue_over_time.png
    ├── revenue_by_region.png
    ├── top_products.png
    ├── return_rate_by_product.png
    └── kpi-summary.md
```

## Full pipeline (fetch → migrate → visualise)

```bash
# 1. Fetch
cd ../../fetch-api/data-engineering && python fetch_data_de.py

# 2. (Optional) Migrate to Parquet
cd ../../data-migration/data-engineering && python migrate_data_de.py

# 3. Visualise
cd ../../visualize/data-engineering && python visualize_de.py --input ../../fetch-api/data-engineering/data
```

## Skill integration

```
.claude/skills/visualize/scripts/visualize_de.py
```

Reference in `skill.md`:
```markdown
### Step 5 — Generate KPI charts
Run .claude/skills/visualize/scripts/visualize_de.py
with --input pointing to the most recent data/ folder.
```

## See also

- [Generic variant](../generic/) — format-agnostic, works with any CSV
