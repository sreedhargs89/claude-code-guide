# Example: Fetch API (Data Engineering)

The data engineering variant of the `/fetch-api` skill — dimensional + fact table
fetching, CSV output, row-count validation.

## What it does

- Fetches 6 tables (dim_customer, dim_date, dim_store, dim_product, fact_sales, fact_returns)
- Runs all fetches **concurrently** with `asyncio.gather()`
- Validates each response is parseable CSV and counts rows
- Saves as `.csv` files in a timestamped directory
- Logs per-table: HTTP status, row count, file size, success/failure
- Logs a run summary: total tables, rows, data size

## Quick start

```bash
cd examples/fetch-api/data-engineering

pip install httpx

python fetch_data_de.py
```

## Output

```
data/
└── 2025-03-15_09-30-00/
    ├── dim_customer.csv
    ├── dim_date.csv
    ├── dim_store.csv
    ├── dim_product.csv
    ├── fact_sales.csv
    └── fact_returns.csv
logs/
└── fetch-api/
    └── 2025-03-15_09-30-00/
        └── fetch-api.log
```

## Adapting for real data sources

Replace the `ENDPOINTS` dict URLs with your actual sources:

```python
# Oracle REST API
"dim_customer": "https://db.internal.corp/ords/schema/dim_customer",

# SAP OData
"dim_product": "https://sap.internal.corp/sap/opu/odata/sap/PRODUCT_SRV/Products",

# Azure Event Hub checkpoint
"fact_sales": "https://eventhub.servicebus.windows.net/sales/messages",

# Snowflake REST API
"fact_returns": "https://account.snowflakecomputing.com/api/v2/statements",
```

Add auth headers in the `httpx.AsyncClient` constructor:

```python
async with httpx.AsyncClient(
    timeout=httpx.Timeout(60),
    headers={"Authorization": f"Bearer {os.environ['WAREHOUSE_TOKEN']}"},
) as client:
```

## Connecting to the skill

Copy this script into your skill's `scripts/` folder and reference it:

```
.claude/skills/fetch-api/
├── skill.md
└── scripts/
    └── fetch_data_de.py
```

In `skill.md`:
```markdown
### Step 2 — Run the fetch script
Run .claude/skills/fetch-api/scripts/fetch_data_de.py
using the project's .venv Python environment.
Do NOT regenerate this script — use it as written.
```

## Scheduling this with /loop

```bash
# Fetch data every morning at 6am before standup
/loop 0 6 * * * /fetch-api

# Or schedule the script directly
/loop 0 6 * * * run the fetch_data_de.py script in examples/fetch-api/data-engineering/
```
