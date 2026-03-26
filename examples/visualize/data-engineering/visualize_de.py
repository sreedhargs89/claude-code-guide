"""
visualize_de.py — Data Engineering KPI visualiser
==================================================
Generates warehouse-focused charts from dim/fact CSV files.
Knows about star schema conventions: joins dim tables to fact tables
to produce business-ready KPI charts.

Key charts produced:
  - Revenue over time          (fact_sales × dim_date)
  - Revenue by region          (fact_sales × dim_store)
  - Top products by revenue    (fact_sales × dim_product)
  - Return rate by product     (fact_returns × fact_sales × dim_product)

Usage:
    python visualize_de.py [--input data/latest]

Requirements:
    pip install pandas matplotlib seaborn pyarrow
"""

import logging
from datetime import datetime
from pathlib import Path
import argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ── Config ──────────────────────────────────────────────────────────────────────

CHART_DPI     = 150
SEABORN_STYLE = "whitegrid"
TOP_N         = 15   # top N items in bar charts

timestamp = datetime.now().strftime("%Y-%m-%d")
sns.set_style(SEABORN_STYLE)
palette = sns.color_palette("muted")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
log = logging.getLogger(__name__)


# ── Data loader ──────────────────────────────────────────────────────────────────

def load_tables(data_dir: Path) -> dict[str, pd.DataFrame]:
    """
    Load all CSV files in data_dir into a dict keyed by table name.
    Auto-discovers the most recent timestamped subfolder if needed.
    """
    csv_files: list[Path] = list(data_dir.glob("*.csv"))

    # If no CSVs at root, look for the most recent timestamped subfolder
    if not csv_files:
        subdirs = sorted([d for d in data_dir.iterdir() if d.is_dir()], reverse=True)
        for d in subdirs:
            found = list(d.glob("*.csv"))
            if found:
                csv_files = found
                log.info(f"Loading from: {d.name}")
                break

    if not csv_files:
        log.warning(f"No CSV files found under {data_dir}")
        return {}

    tables: dict[str, pd.DataFrame] = {}
    for f in csv_files:
        try:
            df = pd.read_csv(f)
            df.columns = [c.strip().lower() for c in df.columns]
            tables[f.stem] = df
            log.info(f"  Loaded {f.stem}: {len(df):,} rows × {len(df.columns)} cols")
        except Exception as e:
            log.error(f"  Failed to load {f.name}: {e}")

    return tables


# ── Chart helpers ─────────────────────────────────────────────────────────────────

def save(fig: plt.Figure, path: Path) -> None:
    plt.tight_layout()
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)
    log.info(f"  ✓ {path.name}")


# ── KPI charts ────────────────────────────────────────────────────────────────────

def chart_revenue_over_time(
    fact_sales: pd.DataFrame,
    dim_date: pd.DataFrame | None,
    out_dir: Path,
) -> tuple[Path, list[str]]:
    """Monthly revenue trend from fact_sales."""
    df = fact_sales.copy()

    # Try to join dim_date for a real date column
    if dim_date is not None and "date_id" in df.columns and "date_id" in dim_date.columns:
        date_cols = [c for c in dim_date.columns if "date" in c and c != "date_id"]
        if date_cols:
            df = df.merge(dim_date[["date_id", date_cols[0]]], on="date_id", how="left")
            df["period"] = pd.to_datetime(df[date_cols[0]], errors="coerce").dt.to_period("M")
    elif "date_id" in df.columns:
        df["period"] = df["date_id"]
    else:
        df["period"] = range(len(df))

    rev_col = next((c for c in df.columns if "revenue" in c or "amount" in c or "sales" in c), None)
    if rev_col is None:
        rev_col = df.select_dtypes(include="number").columns[0]

    monthly = df.groupby("period")[rev_col].sum().reset_index()

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(monthly["period"].astype(str), monthly[rev_col], marker="o", linewidth=2, color=palette[0])
    ax.fill_between(range(len(monthly)), monthly[rev_col], alpha=0.1, color=palette[0])
    ax.set_title("Revenue over time", fontsize=14)
    ax.set_xlabel("Period")
    ax.set_ylabel(rev_col.replace("_", " ").title())
    ax.tick_params(axis="x", rotation=45)

    path = out_dir / "revenue_over_time.png"
    save(fig, path)

    total = monthly[rev_col].sum()
    observations = [
        f"Total {rev_col}: {total:,.2f}",
        f"Peak period: {monthly.loc[monthly[rev_col].idxmax(), 'period']} "
        f"({monthly[rev_col].max():,.2f})",
        f"Periods shown: {len(monthly)}",
    ]
    return path, observations


def chart_revenue_by_region(
    fact_sales: pd.DataFrame,
    dim_store: pd.DataFrame | None,
    out_dir: Path,
) -> tuple[Path, list[str]]:
    """Revenue by store region from fact_sales × dim_store."""
    df = fact_sales.copy()
    region_col = None

    if dim_store is not None and "store_id" in df.columns and "store_id" in dim_store.columns:
        region_cols = [c for c in dim_store.columns if "region" in c or "country" in c]
        if region_cols:
            region_col = region_cols[0]
            df = df.merge(dim_store[["store_id", region_col]], on="store_id", how="left")

    if region_col is None:
        cat_cols = df.select_dtypes(include=["object", "category"]).columns
        region_col = cat_cols[0] if len(cat_cols) else "store_id"

    rev_col = next((c for c in df.columns if "revenue" in c or "amount" in c), None)
    if rev_col is None:
        rev_col = df.select_dtypes(include="number").columns[0]

    by_region = (
        df.groupby(region_col)[rev_col]
        .sum()
        .sort_values(ascending=False)
        .head(TOP_N)
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    by_region.plot(kind="bar", ax=ax, color=palette[1], edgecolor="white")
    ax.set_title(f"Revenue by {region_col.replace('_',' ')}", fontsize=14)
    ax.set_xlabel(region_col.replace("_", " ").title())
    ax.set_ylabel(rev_col.replace("_", " ").title())
    ax.tick_params(axis="x", rotation=45)

    path = out_dir / "revenue_by_region.png"
    save(fig, path)

    observations = [
        f"Top region: {by_region.index[0]} ({by_region.iloc[0]:,.2f})",
        f"Regions shown: {len(by_region)}",
        f"Total across all regions: {by_region.sum():,.2f}",
    ]
    return path, observations


def chart_top_products(
    fact_sales: pd.DataFrame,
    dim_product: pd.DataFrame | None,
    out_dir: Path,
) -> tuple[Path, list[str]]:
    """Top N products by revenue."""
    df = fact_sales.copy()
    name_col = "product_id"

    if dim_product is not None and "product_id" in df.columns and "product_id" in dim_product.columns:
        name_cols = [c for c in dim_product.columns if "name" in c or "desc" in c]
        if name_cols:
            name_col = name_cols[0]
            df = df.merge(dim_product[["product_id", name_col]], on="product_id", how="left")

    rev_col = next((c for c in df.columns if "revenue" in c or "amount" in c), None)
    if rev_col is None:
        rev_col = df.select_dtypes(include="number").columns[0]

    top = (
        df.groupby(name_col)[rev_col]
        .sum()
        .sort_values(ascending=True)   # ascending for horizontal bar
        .tail(TOP_N)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    top.plot(kind="barh", ax=ax, color=palette[2], edgecolor="white")
    ax.set_title(f"Top {TOP_N} products by {rev_col.replace('_',' ')}", fontsize=14)
    ax.set_xlabel(rev_col.replace("_", " ").title())

    path = out_dir / "top_products.png"
    save(fig, path)

    observations = [
        f"Top product: {top.index[-1]} ({top.iloc[-1]:,.2f})",
        f"Products shown: {len(top)}",
        f"Top {TOP_N} account for {top.sum() / df[rev_col].sum() * 100:.1f}% of total revenue",
    ]
    return path, observations


def chart_return_rate(
    fact_returns: pd.DataFrame,
    fact_sales: pd.DataFrame,
    dim_product: pd.DataFrame | None,
    out_dir: Path,
) -> tuple[Path, list[str]]:
    """Return rate (returns / sales) by product."""
    returns_count = fact_returns.groupby("product_id").size().rename("returns")
    sales_count   = fact_sales.groupby("product_id").size().rename("sales")
    rate_df = pd.concat([returns_count, sales_count], axis=1).fillna(0)
    rate_df["return_rate_pct"] = (rate_df["returns"] / rate_df["sales"].replace(0, 1)) * 100

    if dim_product is not None and "product_id" in dim_product.columns:
        name_cols = [c for c in dim_product.columns if "name" in c or "desc" in c]
        if name_cols:
            rate_df = rate_df.merge(
                dim_product[["product_id", name_cols[0]]].set_index("product_id"),
                left_index=True, right_index=True, how="left"
            )
            rate_df.index = rate_df[name_cols[0]].fillna(rate_df.index.astype(str))

    top_returns = rate_df["return_rate_pct"].sort_values(ascending=True).tail(TOP_N)

    fig, ax = plt.subplots(figsize=(10, 6))
    top_returns.plot(kind="barh", ax=ax, color=palette[3], edgecolor="white")
    ax.set_title(f"Return rate by product (top {TOP_N})", fontsize=14)
    ax.set_xlabel("Return rate (%)")
    ax.axvline(x=top_returns.mean(), color="gray", linestyle="--", linewidth=1, label=f"Avg: {top_returns.mean():.1f}%")
    ax.legend()

    path = out_dir / "return_rate_by_product.png"
    save(fig, path)

    observations = [
        f"Highest return rate: {top_returns.index[-1]} ({top_returns.iloc[-1]:.1f}%)",
        f"Average return rate (top {TOP_N}): {top_returns.mean():.1f}%",
        f"Total returns: {int(fact_returns.shape[0]):,}  |  Total sales: {int(fact_sales.shape[0]):,}",
    ]
    return path, observations


# ── Main ──────────────────────────────────────────────────────────────────────────

def main(data_dir: Path) -> None:
    out_dir = Path("reports/charts") / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Output: {out_dir}")

    tables = load_tables(data_dir)
    if not tables:
        log.error("No tables loaded. Run /fetch-api first to populate data/.")
        return

    summary: list[str] = [
        f"# KPI Dashboard — {timestamp}\n\n",
        f"Tables loaded: {', '.join(tables.keys())}\n\n---\n\n",
    ]

    # Chart 1: Revenue over time
    if "fact_sales" in tables:
        log.info("Chart: revenue over time")
        path, obs = chart_revenue_over_time(
            tables["fact_sales"], tables.get("dim_date"), out_dir
        )
        summary += [f"## Revenue over time\n![]({path.name})\n"] + [f"- {o}\n" for o in obs] + ["\n"]

    # Chart 2: Revenue by region
    if "fact_sales" in tables:
        log.info("Chart: revenue by region")
        path, obs = chart_revenue_by_region(
            tables["fact_sales"], tables.get("dim_store"), out_dir
        )
        summary += [f"## Revenue by region\n![]({path.name})\n"] + [f"- {o}\n" for o in obs] + ["\n"]

    # Chart 3: Top products
    if "fact_sales" in tables:
        log.info("Chart: top products")
        path, obs = chart_top_products(
            tables["fact_sales"], tables.get("dim_product"), out_dir
        )
        summary += [f"## Top products\n![]({path.name})\n"] + [f"- {o}\n" for o in obs] + ["\n"]

    # Chart 4: Return rate
    if "fact_returns" in tables and "fact_sales" in tables:
        log.info("Chart: return rate by product")
        path, obs = chart_return_rate(
            tables["fact_returns"], tables["fact_sales"], tables.get("dim_product"), out_dir
        )
        summary += [f"## Return rate by product\n![]({path.name})\n"] + [f"- {o}\n" for o in obs] + ["\n"]

    # Fallback: any unrecognised table
    known = {"fact_sales","fact_returns","dim_date","dim_store","dim_product","dim_customer"}
    for name, df in tables.items():
        if name in known:
            continue
        log.info(f"Chart: generic bar for {name}")
        num_cols = df.select_dtypes(include="number").columns
        cat_cols = df.select_dtypes(include=["object","category"]).columns
        if len(num_cols) and len(cat_cols):
            grouped = df.groupby(cat_cols[0])[num_cols[0]].sum().sort_values(ascending=False).head(TOP_N)
            fig, ax = plt.subplots(figsize=(10, 5))
            grouped.plot(kind="bar", ax=ax, color=palette[4], edgecolor="white")
            ax.set_title(name.replace("_"," ").title(), fontsize=14)
            plt.tight_layout()
            p = out_dir / f"{name}_bar.png"
            fig.savefig(p, dpi=CHART_DPI); plt.close(fig)
            summary += [f"## {name.replace('_',' ').title()}\n![]({p.name})\n\n"]
            log.info(f"  ✓ {p.name}")

    report = out_dir / "kpi-summary.md"
    report.write_text("".join(summary), encoding="utf-8")
    log.info(f"Report: {report}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate KPI charts from warehouse tables")
    parser.add_argument("--input", type=Path, default=Path("data"), help="Input data directory")
    args = parser.parse_args()
    main(args.input)
