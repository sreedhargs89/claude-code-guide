"""
migrate_data_de.py — Data Engineering CSV → Parquet migration
=============================================================
Data engineering variant: migrates dimensional and fact table CSV files
to Parquet format using pandas + PyArrow with schema validation.

Mirrors the pattern from the /migrate-data skill in a data warehouse context.
Handles dim_* and fact_* naming conventions, validates row counts, and
generates a migration report.

Usage:
    python migrate_data_de.py [--input data/incoming] [--format parquet]

Requirements:
    pip install pandas pyarrow

Note:
    In a production pipeline this logic would typically run inside a PySpark
    job or an Airflow operator. This standalone script is for local development
    and Claude Code skill usage where a full Spark cluster is not available.
"""

import argparse
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# ── Configuration ──────────────────────────────────────────────────────────────

# Expected table schemas — column names and pandas dtypes.
# Add or adjust per your actual warehouse schema.
EXPECTED_SCHEMAS: dict[str, dict[str, str]] = {
    "dim_customer": {
        "customer_id": "int64",
        "customer_name": "object",
        "email": "object",
        "country": "object",
        "created_date": "object",
    },
    "dim_date": {
        "date_id": "int64",
        "full_date": "object",
        "year": "int64",
        "quarter": "int64",
        "month": "int64",
        "day_of_week": "object",
    },
    "dim_store": {
        "store_id": "int64",
        "store_name": "object",
        "region": "object",
        "country": "object",
    },
    "dim_product": {
        "product_id": "int64",
        "product_name": "object",
        "category": "object",
        "unit_price": "float64",
    },
    "fact_sales": {
        "sale_id": "int64",
        "date_id": "int64",
        "customer_id": "int64",
        "store_id": "int64",
        "product_id": "int64",
        "quantity": "int64",
        "revenue": "float64",
    },
    "fact_returns": {
        "return_id": "int64",
        "sale_id": "int64",
        "date_id": "int64",
        "reason": "object",
        "refund_amount": "float64",
    },
}

# Row thresholds — dim tables are usually small, fact tables large
ROW_THRESHOLD_PARQUET = 50_000
ROW_THRESHOLD_SNAPPY  = 1_000_000

INPUT_DIR  = Path("data/incoming")
OUTPUT_DIR = Path("data/migrated")
LOG_DIR    = Path("logs/migrate-data")

# ── Setup ───────────────────────────────────────────────────────────────────────

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
run_out_dir = OUTPUT_DIR / timestamp
run_log_dir = LOG_DIR / timestamp[:10]

run_out_dir.mkdir(parents=True, exist_ok=True)
run_log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.FileHandler(run_log_dir / "migration-report.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


# ── Schema validation ───────────────────────────────────────────────────────────

def validate_schema(df: pd.DataFrame, table_name: str) -> list[str]:
    """
    Validate that a DataFrame matches the expected schema for this table.
    Returns a list of warning messages (empty = all good).
    """
    warnings: list[str] = []
    expected = EXPECTED_SCHEMAS.get(table_name)
    if not expected:
        warnings.append(f"No expected schema defined for '{table_name}' — skipping validation")
        return warnings

    # Check for missing columns
    missing = set(expected.keys()) - set(df.columns)
    if missing:
        warnings.append(f"Missing expected columns: {sorted(missing)}")

    # Check for unexpected columns
    extra = set(df.columns) - set(expected.keys())
    if extra:
        warnings.append(f"Unexpected extra columns: {sorted(extra)}")

    # Check for completely empty columns
    null_cols = [c for c in df.columns if df[c].isna().all()]
    if null_cols:
        warnings.append(f"All-null columns: {null_cols}")

    return warnings


# ── Format decision ─────────────────────────────────────────────────────────────

def decide_format(table_name: str, row_count: int, forced: str | None) -> tuple[str, str]:
    """Returns (format_key, human_readable_reason)."""
    if forced:
        return forced, f"forced by user"

    # Dim tables: always Parquet (they're read repeatedly in star schema queries)
    if table_name.startswith("dim_"):
        return "parquet", "dimension table — Parquet for repeated reads"

    # Fact tables: size-based decision
    if row_count > ROW_THRESHOLD_SNAPPY:
        return "parquet_snappy", f"fact table >{ROW_THRESHOLD_SNAPPY:,} rows → snappy Parquet"
    if row_count > ROW_THRESHOLD_PARQUET:
        return "parquet", f"fact table >{ROW_THRESHOLD_PARQUET:,} rows → Parquet"

    return "csv", f"small table ({row_count:,} rows) → CSV"


# ── Migration ───────────────────────────────────────────────────────────────────

def migrate_table(src: Path, forced_format: str | None = None) -> dict:
    """Migrate one table file. Returns a result dict."""
    table_name = src.stem
    log.info(f"Migrating: {table_name}")

    try:
        # Read
        df = pd.read_csv(src)
        src_rows = len(df)
        src_size_kb = src.stat().st_size / 1024
        log.info(f"  Read {src_rows:,} rows, {src_size_kb:.1f} KB")

        # Validate schema
        schema_warnings = validate_schema(df, table_name)
        for w in schema_warnings:
            log.warning(f"  SCHEMA: {w}")

        # Decide format
        fmt, reason = decide_format(table_name, src_rows, forced_format)
        log.info(f"  Format: {fmt} ({reason})")

        # Write
        if fmt == "csv":
            out_path = run_out_dir / f"{table_name}.csv"
            df.to_csv(out_path, index=False)
        elif fmt in ("parquet", "parquet_snappy"):
            out_path = run_out_dir / f"{table_name}.parquet"
            table = pa.Table.from_pandas(df, preserve_index=False)
            compression = "snappy" if fmt == "parquet_snappy" else None
            pq.write_table(table, out_path, compression=compression)
        else:
            raise ValueError(f"Unknown format: {fmt}")

        # Verify readback
        if fmt == "csv":
            df_check = pd.read_csv(out_path)
        else:
            df_check = pd.read_parquet(out_path)

        out_rows = len(df_check)
        if out_rows != src_rows:
            raise ValueError(f"Row count mismatch! source={src_rows:,} output={out_rows:,}")

        out_size_kb = out_path.stat().st_size / 1024
        ratio = (1 - out_size_kb / src_size_kb) * 100 if src_size_kb > 0 else 0
        log.info(
            f"  ✓ → {out_path.name}  "
            f"({src_size_kb:.1f} KB → {out_size_kb:.1f} KB, {ratio:+.0f}%)"
        )

        return {
            "table": table_name,
            "success": True,
            "format": fmt,
            "src_rows": src_rows,
            "out_rows": out_rows,
            "src_kb": round(src_size_kb, 1),
            "out_kb": round(out_size_kb, 1),
            "schema_warnings": schema_warnings,
            "output_path": str(out_path),
        }

    except Exception as e:
        log.error(f"  ✗ {table_name}: {e}")
        return {"table": table_name, "success": False, "error": str(e)}


# ── Main ────────────────────────────────────────────────────────────────────────

def main(forced_format: str | None = None, input_dir: Path = INPUT_DIR) -> None:
    log.info("=" * 60)
    log.info(f"Data migration run: {timestamp}")
    log.info(f"Input:  {input_dir}")
    log.info(f"Output: {run_out_dir}")
    log.info("=" * 60)

    csv_files = sorted(input_dir.glob("*.csv"))
    if not csv_files:
        log.warning(f"No CSV files found in {input_dir}/")
        log.info("Create the directory and add CSV files to migrate.")
        return

    # Sort: dim_ tables first, fact_ tables second
    dim_files  = [f for f in csv_files if f.stem.startswith("dim_")]
    fact_files = [f for f in csv_files if f.stem.startswith("fact_")]
    other_files = [f for f in csv_files if f not in dim_files + fact_files]
    ordered_files = dim_files + fact_files + other_files

    log.info(f"Tables: {len(dim_files)} dim, {len(fact_files)} fact, {len(other_files)} other")

    results = [migrate_table(f, forced_format) for f in ordered_files]

    successes = [r for r in results if r["success"]]
    failures  = [r for r in results if not r["success"]]

    # Summary
    log.info("─" * 60)
    log.info(f"SUMMARY: {len(successes)} migrated, {len(failures)} failed")
    if successes:
        total_rows_in  = sum(r["src_rows"] for r in successes)
        total_rows_out = sum(r["out_rows"] for r in successes)
        total_kb_in    = sum(r["src_kb"]   for r in successes)
        total_kb_out   = sum(r["out_kb"]   for r in successes)
        overall_ratio  = (1 - total_kb_out / total_kb_in) * 100 if total_kb_in > 0 else 0
        log.info(f"  Total rows: {total_rows_in:,} → {total_rows_out:,}")
        log.info(f"  Total size: {total_kb_in:.1f} KB → {total_kb_out:.1f} KB ({overall_ratio:+.0f}%)")

    if failures:
        log.error("Failed tables:")
        for r in failures:
            log.error(f"  {r['table']}: {r.get('error')}")

    total_warnings = sum(len(r.get("schema_warnings", [])) for r in successes)
    if total_warnings:
        log.warning(f"Schema warnings: {total_warnings} (check log for details)")

    log.info(f"Report: {run_log_dir / 'migration-report.log'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate data warehouse tables to Parquet")
    parser.add_argument("--format", choices=["csv", "parquet"], help="Force output format")
    parser.add_argument("--input", type=Path, default=INPUT_DIR, help="Input directory")
    args = parser.parse_args()
    main(forced_format=args.format, input_dir=args.input)
