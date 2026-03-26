"""
fetch_data_de.py — Data Engineering async API fetcher
======================================================
Mirrors the exact pattern from the Claude Code masterclass transcript.

Fetches dimensional and fact table data from REST endpoints concurrently.
Saves each table as a CSV file in a timestamped directory.
Designed for data warehouse ingestion pipelines.

Usage:
    python fetch_data_de.py

Requirements:
    pip install httpx

Context:
    In a real pipeline these GitHub raw URLs would be replaced with your
    actual warehouse REST API endpoints, event hub URLs, or source system
    API endpoints (Oracle REST, SAP OData, Salesforce SOQL, etc.)
"""

import asyncio
import csv
import io
import logging
from datetime import datetime
from pathlib import Path

import httpx

# ── Configuration ──────────────────────────────────────────────────────────────
# Replace these with your actual data source endpoints.
# These GitHub raw CSV URLs simulate a REST API returning tabular data.

ENDPOINTS: dict[str, str] = {
    "dim_customer": (
        "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    ),
    "dim_date": (
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
        "csse_covid_19_data/csse_covid_19_time_series/"
        "time_series_covid19_confirmed_global.csv"
    ),
    "dim_store": (
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
    ),
    "dim_product": (
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv"
    ),
    "fact_sales": (
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv"
    ),
    "fact_returns": (
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    ),
}

TIMEOUT_SECONDS = 60
DATA_DIR = Path("data")
LOG_DIR = Path("logs/fetch-api")

# ── Setup ───────────────────────────────────────────────────────────────────────

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
run_data_dir = DATA_DIR / timestamp
run_log_dir = LOG_DIR / timestamp

run_data_dir.mkdir(parents=True, exist_ok=True)
run_log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.FileHandler(run_log_dir / "fetch-api.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


# ── Fetch ───────────────────────────────────────────────────────────────────────

async def fetch_table(
    client: httpx.AsyncClient,
    table_name: str,
    url: str,
) -> dict:
    """
    Fetch one table from a REST endpoint.
    Expects CSV response. Saves to data/{timestamp}/{table_name}.csv.
    Returns a result dict with success status and metadata.
    """
    log.info(f"Fetching {table_name} ...")

    try:
        response = await client.get(url)
        response.raise_for_status()

        # Parse to count rows (validate it's real CSV data)
        content = response.text
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        row_count = len(rows) - 1  # minus header

        # Save as CSV
        out_path = run_data_dir / f"{table_name}.csv"
        out_path.write_text(content, encoding="utf-8")

        size_kb = len(response.content) / 1024
        log.info(
            f"  ✓ {table_name}: "
            f"HTTP {response.status_code}, "
            f"{row_count} rows, "
            f"{size_kb:.1f} KB → {out_path.name}"
        )
        return {
            "table": table_name,
            "success": True,
            "status_code": response.status_code,
            "rows": row_count,
            "size_kb": round(size_kb, 1),
            "path": str(out_path),
        }

    except httpx.HTTPStatusError as e:
        msg = f"HTTP {e.response.status_code}"
        log.error(f"  ✗ {table_name}: {msg}")
        return {"table": table_name, "success": False, "error": msg}

    except httpx.RequestError as e:
        msg = f"Connection error: {type(e).__name__}"
        log.error(f"  ✗ {table_name}: {msg}")
        return {"table": table_name, "success": False, "error": msg}

    except csv.Error as e:
        msg = f"CSV parse error: {e}"
        log.error(f"  ✗ {table_name}: {msg}")
        return {"table": table_name, "success": False, "error": msg}


async def fetch_all_tables() -> list[dict]:
    """Fetch all tables concurrently."""
    async with httpx.AsyncClient(timeout=httpx.Timeout(TIMEOUT_SECONDS)) as client:
        tasks = [
            fetch_table(client, name, url)
            for name, url in ENDPOINTS.items()
        ]
        return await asyncio.gather(*tasks)


# ── Main ────────────────────────────────────────────────────────────────────────

async def main() -> None:
    log.info("=" * 60)
    log.info(f"Data fetch run started: {timestamp}")
    log.info(f"Tables to fetch: {len(ENDPOINTS)}")
    log.info(f"Output: {run_data_dir}")
    log.info("=" * 60)

    results = await fetch_all_tables()

    successes = [r for r in results if r["success"]]
    failures  = [r for r in results if not r["success"]]

    # Write summary log
    log.info("─" * 60)
    log.info("SUMMARY")
    log.info(f"  Total:      {len(results)}")
    log.info(f"  Successful: {len(successes)}")
    log.info(f"  Failed:     {len(failures)}")

    if successes:
        total_rows = sum(r.get("rows", 0) for r in successes)
        total_kb   = sum(r.get("size_kb", 0) for r in successes)
        log.info(f"  Total rows fetched: {total_rows:,}")
        log.info(f"  Total data size:    {total_kb:.1f} KB")

    if failures:
        log.warning("Failed tables:")
        for r in failures:
            log.warning(f"  {r['table']}: {r.get('error', 'unknown error')}")

    log.info(f"Data saved to: {run_data_dir}")
    log.info(f"Log saved to:  {run_log_dir / 'fetch-api.log'}")

    if not successes:
        raise SystemExit("All tables failed. Check connectivity and credentials.")


if __name__ == "__main__":
    asyncio.run(main())
