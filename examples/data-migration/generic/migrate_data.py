"""
migrate_data.py — Generic CSV → Parquet migration
==================================================
Converts CSV files in data/incoming/ to Parquet format in data/migrated/.
Applies the format-decision logic from the migrate-data skill.

Usage:
    python migrate_data.py [--format csv|parquet|json]

Requirements:
    pip install pandas pyarrow
"""

import argparse
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# ── Config ─────────────────────────────────────────────────────────────────────

INPUT_DIR  = Path("data/incoming")
OUTPUT_DIR = Path("data/migrated")
LOG_DIR    = Path("logs/migrate-data")

ROW_THRESHOLD_PARQUET = 50_000       # rows: use Parquet above this
ROW_THRESHOLD_COMPRESSED = 1_000_000 # rows: use snappy compression above this

# ── Setup ───────────────────────────────────────────────────────────────────────

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
run_out_dir = OUTPUT_DIR / timestamp
run_log_dir = LOG_DIR / timestamp[:10]  # daily log folder

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


# ── Format decision ─────────────────────────────────────────────────────────────

def decide_format(row_count: int, forced_format: str | None) -> tuple[str, str]:
    """
    Returns (format, reason).
    Forced format overrides the rule-based decision.
    """
    if forced_format:
        return forced_format, "user specified"
    if row_count > ROW_THRESHOLD_COMPRESSED:
        return "parquet_compressed", f">{ROW_THRESHOLD_COMPRESSED:,} rows → snappy Parquet"
    if row_count > ROW_THRESHOLD_PARQUET:
        return "parquet", f">{ROW_THRESHOLD_PARQUET:,} rows → Parquet"
    return "csv", f"<={ROW_THRESHOLD_PARQUET:,} rows → CSV"


# ── Migration ───────────────────────────────────────────────────────────────────

def migrate_file(
    src: Path,
    forced_format: str | None = None,
) -> dict:
    """Migrate one file. Returns a result dict."""
    log.info(f"Processing: {src.name}")

    try:
        # Read source
        df = pd.read_csv(src)
        src_rows = len(df)
        src_size_kb = src.stat().st_size / 1024

        # Check for obvious quality issues
        null_cols = [c for c in df.columns if df[c].isna().all()]
        if null_cols:
            log.warning(f"  Columns with all-null values: {null_cols}")

        # Decide output format
        fmt, reason = decide_format(src_rows, forced_format)
        log.info(f"  Rows: {src_rows:,} → Format: {fmt} ({reason})")

        # Write output
        stem = src.stem
        if fmt == "csv":
            out_path = run_out_dir / f"{stem}.csv"
            df.to_csv(out_path, index=False)
        elif fmt in ("parquet", "parquet_compressed"):
            out_path = run_out_dir / f"{stem}.parquet"
            compression = "snappy" if fmt == "parquet_compressed" else None
            table = pa.Table.from_pandas(df)
            pq.write_table(table, out_path, compression=compression)
        elif fmt == "json":
            out_path = run_out_dir / f"{stem}.json"
            df.to_json(out_path, orient="records", indent=2)
        else:
            raise ValueError(f"Unknown format: {fmt}")

        # Verify output
        out_size_kb = out_path.stat().st_size / 1024

        # Read back to verify row count
        if fmt == "csv":
            df_check = pd.read_csv(out_path)
        elif fmt in ("parquet", "parquet_compressed"):
            df_check = pd.read_parquet(out_path)
        else:
            df_check = pd.read_json(out_path)

        out_rows = len(df_check)
        if out_rows != src_rows:
            raise ValueError(f"Row count mismatch: source={src_rows}, output={out_rows}")

        compression_ratio = (1 - out_size_kb / src_size_kb) * 100
        log.info(
            f"  ✓ {src.name} → {out_path.name} "
            f"({src_size_kb:.1f} KB → {out_size_kb:.1f} KB, "
            f"{compression_ratio:+.0f}%)"
        )
        return {
            "source": src.name,
            "output": out_path.name,
            "format": fmt,
            "rows": src_rows,
            "src_kb": round(src_size_kb, 1),
            "out_kb": round(out_size_kb, 1),
            "success": True,
        }

    except Exception as e:
        log.error(f"  ✗ {src.name}: {e}")
        return {"source": src.name, "success": False, "error": str(e)}


# ── Main ────────────────────────────────────────────────────────────────────────

def main(forced_format: str | None = None) -> None:
    log.info(f"Migration run: {timestamp}")
    log.info(f"Input:  {INPUT_DIR}")
    log.info(f"Output: {run_out_dir}")

    # Find source files
    csv_files = sorted(INPUT_DIR.glob("*.csv"))
    if not csv_files:
        log.warning(f"No CSV files found in {INPUT_DIR}. Create the directory and add files.")
        return

    log.info(f"Files found: {len(csv_files)}")

    results = [migrate_file(f, forced_format) for f in csv_files]

    successes = [r for r in results if r["success"]]
    failures  = [r for r in results if not r["success"]]

    log.info("─" * 60)
    log.info(f"Complete: {len(successes)} migrated, {len(failures)} failed")
    if failures:
        for r in failures:
            log.error(f"  FAILED: {r['source']} — {r.get('error')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate CSV files to target format")
    parser.add_argument(
        "--format",
        choices=["csv", "parquet", "json"],
        help="Force a specific output format (overrides auto-decision)",
    )
    args = parser.parse_args()
    main(forced_format=args.format)
