# Example: Visualise Data (Generic)

Auto-generates charts from any CSV data. Detects the best chart type per file
and produces a markdown summary report alongside the PNG images.

## What it does

- Scans `data/` for the most recent timestamped folder of CSV files
- For each CSV, picks the best chart type automatically:
  - date/time column + numeric → **line chart**
  - categorical + numeric → **bar chart** (top 20 by value)
  - two numeric columns → **scatter plot** (samples to 10K rows)
  - one numeric column → **histogram**
- Saves each chart as a PNG at `reports/charts/YYYY-MM-DD/`
- Writes `visualisation-summary.md` with observations per chart

## Quick start

```bash
cd examples/visualize/generic

pip install pandas matplotlib seaborn

# Run against data from the fetch-api example
python visualize.py --input ../../fetch-api/generic/data

# Or let it find the latest data/ folder automatically
python visualize.py
```

## Output

```
reports/charts/
└── 2025-03-15/
    ├── users_bar.png
    ├── posts_bar.png
    ├── comments_histogram.png
    └── visualisation-summary.md
```

## CLI options

```bash
python visualize.py                                    # auto-find latest data/
python visualize.py --input data/2025-03-15_09-30-00   # specific folder
python visualize.py --output reports/my-charts         # custom output location
```

## Chart type rules

| Data shape | Chart chosen | Why |
|---|---|---|
| Date/time column + numerics | Line | Shows trends over time |
| Categorical + numeric | Bar (top 20) | Compares categories |
| Two+ numeric columns | Scatter | Shows correlation |
| One numeric column | Histogram | Shows distribution |

## Connecting to the /visualize skill

Copy this script into the skill's `scripts/` folder:

```
.claude/skills/visualize/
├── skill.md
└── scripts/
    └── visualize.py
```

Reference it in `skill.md`:
```markdown
### Step 5 — Generate charts
Run .claude/skills/visualize/scripts/visualize.py
using the .venv Python environment.
Do NOT regenerate — use it as written.
```

## See also

- [Data engineering variant](../data-engineering/) — KPI-focused, star schema awareness
