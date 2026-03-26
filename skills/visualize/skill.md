---
name: visualize
description: >
  Use this skill to generate charts, plots, or visualizations from
  data files. Supports bar charts, line charts, scatter plots, and
  histograms. Invoke when asked to "visualize", "plot", "chart",
  "show trends", or "graph this data".
usage: /visualize
---

# Visualize skill

Generates charts and visualizations from CSV or Parquet data files.
Saves output as PNG images with a summary report.

## Pre-conditions
- Data files exist in `data/` directory
- Python environment available
- Required packages: pandas, matplotlib, seaborn (install if missing)

## Steps

### Step 1 — Activate environment
Activate .venv if it exists. Otherwise use system Python.

### Step 2 — Install dependencies
```
pip install pandas matplotlib seaborn pyarrow
```

### Step 3 — Discover data
Scan the `data/` directory for the most recent timestamped subfolder.
List available files and their schemas (column names and types).
Report what data is available before proceeding.

### Step 4 — Determine chart types
For each numeric column, decide the best chart type:

| Data type | Recommended chart |
|---|---|
| Time series (date column present) | Line chart |
| Categorical with counts | Bar chart |
| Two numeric columns | Scatter plot |
| Distribution of one numeric column | Histogram |
| Multiple categories over time | Multi-line chart |

Ask via the prompt if the best chart type is ambiguous.

### Step 5 — Run the visualise script
A pre-built, tested script is available at:
  `.claude/skills/visualize/scripts/visualize.py`

Run it using the .venv Python environment:
  `.venv/bin/python .claude/skills/visualize/scripts/visualize.py`

The script automatically finds the most recent data folder and picks the
best chart type for each CSV. Charts are saved to `reports/charts/YYYY-MM-DD/`.

Do NOT rewrite or regenerate this script. Use it as-is.

### Step 6 — Generate summary report
Create `reports/charts/YYYY-MM-DD/visualization-summary.md` containing:
- List of charts generated with file paths
- Key observations from each chart (2–3 bullet points per chart)
- Any data quality issues noticed (nulls, outliers, unexpected ranges)

### Step 7 — Log
Write to `logs/visualize/YYYY-MM-DD/visualize.log`:
- Files processed
- Charts generated
- Any errors or skipped columns

## Chart generation notes
- Use `plt.tight_layout()` before saving to prevent label clipping
- Set `dpi=150` for clear output on modern displays
- For large datasets (>100K rows), sample 10K rows for scatter plots
- Always close figures with `plt.close()` to free memory

## Expected output
```
reports/
└── charts/
    └── 2025-03-15/
        ├── sales_over_time.png
        ├── revenue_by_region.png
        └── visualization-summary.md
logs/
└── visualize/
    └── 2025-03-15/
        └── visualize.log
```
