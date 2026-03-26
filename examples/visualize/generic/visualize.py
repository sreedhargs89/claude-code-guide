"""
visualize.py — Generic data visualiser
=======================================
Discovers CSV files in data/, decides the best chart type for each,
generates PNG charts, and writes a summary markdown report.

Used by the /visualize skill.

Usage:
    python visualize.py [--input data/latest] [--output reports/charts]

Requirements:
    pip install pandas matplotlib seaborn pyarrow
"""

import argparse
import logging
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend — must be before pyplot import
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ── Config ──────────────────────────────────────────────────────────────────────

CHART_DPI     = 150
MAX_SCATTER   = 10_000   # sample down scatter plots above this
SEABORN_STYLE = "whitegrid"

timestamp = datetime.now().strftime("%Y-%m-%d")
sns.set_style(SEABORN_STYLE)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
log = logging.getLogger(__name__)


# ── Chart type decision ──────────────────────────────────────────────────────────

def pick_chart_type(df: pd.DataFrame) -> str:
    """Heuristic: infer best chart type from DataFrame columns."""
    cols      = df.columns.tolist()
    numeric   = df.select_dtypes(include="number").columns.tolist()
    date_hint = any(
        pd.api.types.is_datetime64_any_dtype(df[c]) or
        any(k in c.lower() for k in ("date", "time", "year", "month", "day"))
        for c in cols
    )
    cat_cols  = df.select_dtypes(include=["object", "category"]).columns.tolist()

    if date_hint and numeric:
        return "line"
    if cat_cols and numeric:
        return "bar"
    if len(numeric) >= 2:
        return "scatter"
    if numeric:
        return "histogram"
    return "bar"


# ── Chart generators ─────────────────────────────────────────────────────────────

def make_line_chart(df: pd.DataFrame, stem: str, out_dir: Path) -> tuple[Path, list[str]]:
    """Time-series line chart. Uses the first date-like column as x-axis."""
    date_col = next(
        (c for c in df.columns if any(k in c.lower() for k in ("date","time","year","month","day"))),
        df.columns[0]
    )
    # Parse dates if needed
    try:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)
    except Exception:
        pass

    numeric = df.select_dtypes(include="number").columns[:3]  # max 3 series
    fig, ax = plt.subplots(figsize=(10, 5))
    for col in numeric:
        ax.plot(df[date_col], df[col], label=col, linewidth=1.5)
    ax.set_title(stem.replace("_", " ").title(), fontsize=14)
    ax.set_xlabel(date_col)
    ax.legend()
    plt.tight_layout()
    path = out_dir / f"{stem}_line.png"
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)

    observations = [
        f"Line chart of {', '.join(numeric)} over {date_col}",
        f"Date range: {df[date_col].min()} → {df[date_col].max()}",
        f"Rows plotted: {len(df):,}",
    ]
    return path, observations


def make_bar_chart(df: pd.DataFrame, stem: str, out_dir: Path) -> tuple[Path, list[str]]:
    """Bar chart: top-20 values for first categorical vs first numeric column."""
    cat_col = df.select_dtypes(include=["object","category"]).columns[0]
    num_col = df.select_dtypes(include="number").columns[0]

    grouped = (
        df.groupby(cat_col)[num_col]
        .sum()
        .sort_values(ascending=False)
        .head(20)
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    grouped.plot(kind="bar", ax=ax, color=sns.color_palette("muted")[0])
    ax.set_title(f"{stem.replace('_',' ').title()}: {num_col} by {cat_col}", fontsize=14)
    ax.set_xlabel(cat_col)
    ax.set_ylabel(num_col)
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()

    path = out_dir / f"{stem}_bar.png"
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)

    observations = [
        f"Bar chart of {num_col} by {cat_col} (top {len(grouped)} categories)",
        f"Highest: {grouped.index[0]} = {grouped.iloc[0]:,.2f}",
        f"Lowest in top-20: {grouped.index[-1]} = {grouped.iloc[-1]:,.2f}",
    ]
    return path, observations


def make_scatter_chart(df: pd.DataFrame, stem: str, out_dir: Path) -> tuple[Path, list[str]]:
    """Scatter plot of first two numeric columns. Samples large datasets."""
    numerics = df.select_dtypes(include="number").columns
    x_col, y_col = numerics[0], numerics[1]

    plot_df = df if len(df) <= MAX_SCATTER else df.sample(MAX_SCATTER, random_state=42)
    sampled = len(df) > MAX_SCATTER

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(plot_df[x_col], plot_df[y_col], alpha=0.4, s=15,
               color=sns.color_palette("muted")[1])
    ax.set_title(f"{stem.replace('_',' ').title()}: {x_col} vs {y_col}", fontsize=14)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    if sampled:
        ax.set_title(ax.get_title() + f" (sample: {MAX_SCATTER:,} of {len(df):,})", fontsize=12)
    plt.tight_layout()

    path = out_dir / f"{stem}_scatter.png"
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)

    corr = plot_df[[x_col, y_col]].corr().iloc[0, 1]
    observations = [
        f"Scatter of {x_col} vs {y_col}",
        f"Pearson correlation: {corr:.3f}",
        f"Points plotted: {len(plot_df):,}" + (" (sampled)" if sampled else ""),
    ]
    return path, observations


def make_histogram(df: pd.DataFrame, stem: str, out_dir: Path) -> tuple[Path, list[str]]:
    """Histogram of the first numeric column."""
    num_col = df.select_dtypes(include="number").columns[0]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df[num_col].dropna(), bins=30, color=sns.color_palette("muted")[2], edgecolor="white")
    ax.set_title(f"{stem.replace('_',' ').title()}: distribution of {num_col}", fontsize=14)
    ax.set_xlabel(num_col)
    ax.set_ylabel("Count")
    plt.tight_layout()

    path = out_dir / f"{stem}_histogram.png"
    fig.savefig(path, dpi=CHART_DPI)
    plt.close(fig)

    observations = [
        f"Histogram of {num_col}",
        f"Mean: {df[num_col].mean():.2f}  |  Median: {df[num_col].median():.2f}  |  Std: {df[num_col].std():.2f}",
        f"Range: {df[num_col].min():.2f} → {df[num_col].max():.2f}",
    ]
    return path, observations


CHART_MAKERS = {
    "line":      make_line_chart,
    "bar":       make_bar_chart,
    "scatter":   make_scatter_chart,
    "histogram": make_histogram,
}


# ── Main ─────────────────────────────────────────────────────────────────────────

def visualize(input_dir: Path, output_dir: Path) -> None:
    run_out = output_dir / timestamp
    run_out.mkdir(parents=True, exist_ok=True)

    # Discover CSV files — use most recent timestamped subfolder if input_dir is data/
    csv_files: list[Path] = []
    if input_dir.name == "data" or not any(input_dir.glob("*.csv")):
        subdirs = sorted([d for d in input_dir.iterdir() if d.is_dir()], reverse=True)
        for d in subdirs:
            found = list(d.glob("*.csv"))
            if found:
                csv_files = found
                log.info(f"Using most recent data folder: {d.name}")
                break
    if not csv_files:
        csv_files = list(input_dir.glob("*.csv"))

    if not csv_files:
        log.warning(f"No CSV files found under {input_dir}. Run /fetch-api first.")
        return

    log.info(f"Files to visualize: {len(csv_files)}")

    summary_lines: list[str] = [
        f"# Visualisation summary — {timestamp}\n",
        f"Input: `{input_dir}`  \nOutput: `{run_out}`\n",
        f"Files processed: {len(csv_files)}\n\n---\n",
    ]
    charts_generated = 0

    for csv_path in csv_files:
        stem = csv_path.stem
        log.info(f"Processing: {stem}")
        try:
            df = pd.read_csv(csv_path)
            df.columns = [c.strip() for c in df.columns]   # clean whitespace
            log.info(f"  Rows: {len(df):,}  Cols: {list(df.columns)}")

            if df.empty:
                log.warning(f"  Skipping {stem}: zero rows")
                continue
            if not df.select_dtypes(include="number").columns.any():
                log.warning(f"  Skipping {stem}: no numeric columns")
                continue

            chart_type = pick_chart_type(df)
            log.info(f"  Chart type: {chart_type}")

            chart_path, observations = CHART_MAKERS[chart_type](df, stem, run_out)
            charts_generated += 1

            summary_lines += [
                f"## {stem.replace('_',' ').title()}\n",
                f"- Chart: `{chart_path.name}`  \n",
                f"- Type: {chart_type}  \n",
                f"- Rows: {len(df):,}\n\n",
                "**Observations:**\n",
            ] + [f"- {o}\n" for o in observations] + ["\n"]

            log.info(f"  ✓ Saved: {chart_path.name}")

        except Exception as e:
            log.error(f"  ✗ {stem}: {e}")
            summary_lines.append(f"## {stem}\n- ✗ Error: {e}\n\n")

    # Write summary report
    report_path = run_out / "visualisation-summary.md"
    report_path.write_text("".join(summary_lines), encoding="utf-8")

    log.info(f"Charts generated: {charts_generated}")
    log.info(f"Report: {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualise CSV data files")
    parser.add_argument("--input",  type=Path, default=Path("data"),          help="Input directory")
    parser.add_argument("--output", type=Path, default=Path("reports/charts"), help="Output directory")
    args = parser.parse_args()
    visualize(args.input, args.output)
