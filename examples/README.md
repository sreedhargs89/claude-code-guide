# Examples

Working code and configuration examples for every major Claude Code feature.
Each directory has a `README.md` with quick-start instructions.

---

## Structure

```
examples/
├── fetch-api/              Async REST API fetching
│   ├── generic/            Any JSON API → timestamped output
│   └── data-engineering/   Dim/fact table fetch → CSV
├── data-migration/         File format conversion
│   ├── generic/            CSV → auto-format (CSV/Parquet/JSON)
│   └── data-engineering/   Star schema CSV → Parquet with validation
├── visualize/              Chart generation
│   ├── generic/            Auto-chart any CSV data
│   └── data-engineering/   KPI charts from warehouse tables
├── sub-agents/             Parallel sub-agent patterns
├── hooks/                  settings.json hook configurations
├── scheduling/             /loop cron patterns
├── mcp-local/              Local MCP server setup (GitHub, Postgres, SQLite)
└── mcp-hosted/             Hosted MCP server setup (Notion, custom)
```

---

## The full data pipeline

The `fetch-api`, `data-migration`, and `visualize` examples form a complete pipeline:

```
fetch-api/data-engineering/fetch_data_de.py
        ↓  saves dim_*.csv + fact_*.csv to data/YYYY-MM-DD_HH-MM-SS/

data-migration/data-engineering/migrate_data_de.py
        ↓  converts to .parquet in data/migrated/YYYY-MM-DD_HH-MM-SS/

visualize/data-engineering/visualize_de.py
        ↓  generates KPI charts in reports/charts/YYYY-MM-DD/
```

Run the full pipeline:
```bash
# 1. Fetch
python examples/fetch-api/data-engineering/fetch_data_de.py

# 2. Migrate (optional — visualiser works with CSV too)
python examples/data-migration/data-engineering/migrate_data_de.py

# 3. Visualise
python examples/visualize/data-engineering/visualize_de.py
```

Or trigger the same pipeline via Claude Code skills:
```
/fetch-api
/migrate-data
/visualize
```

---

## Python requirements

```bash
pip install -r requirements.txt
```

Or per-example minimal installs:

| Example | Packages |
|---|---|
| fetch-api | `httpx` |
| data-migration | `pandas pyarrow` |
| visualize | `pandas matplotlib seaborn pyarrow` |
| All examples | see `requirements.txt` at repo root |

---

## Generic vs data-engineering variants

Every code example exists in two flavours:

| Variant | Best for | Assumptions |
|---|---|---|
| `generic/` | Any project, any domain | No domain knowledge — works with any CSV/API |
| `data-engineering/` | Data pipelines, warehouses | Knows about dim_*/fact_*, star schema, Parquet |

Start with `generic/` if you're new. Use `data-engineering/` if you work with warehouse pipelines.
