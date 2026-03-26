# Example: Data Migration (Generic)

Format-agnostic CSV converter. Auto-selects output format based on row count.
No star schema assumptions — works with any CSV files.

## Quick start

```bash
cd examples/data-migration/generic

pip install pandas pyarrow

# Create test input
mkdir -p data/incoming
python -c "
import pandas as pd, numpy as np
pd.DataFrame({'id': range(1000), 'name': ['item']*1000, 'value': np.random.rand(1000)}).to_csv('data/incoming/sample.csv', index=False)
print('Sample created.')
"

python migrate_data.py
```

## Format decision logic

| Rows | Output format | Why |
|---|---|---|
| ≤ 50,000 | CSV | Human-readable, easy to inspect |
| 50,001–1,000,000 | Parquet | Columnar, fast analytical reads |
| > 1,000,000 | Parquet + snappy | Compression for large files |
| `--format` flag | Forced | Override the auto-decision |

## CLI options

```bash
python migrate_data.py                     # auto-decide format
python migrate_data.py --format parquet    # force Parquet
python migrate_data.py --format csv        # force CSV
python migrate_data.py --format json       # force JSON
```

## See also

- [Data engineering variant](../data-engineering/) — adds star schema format rules, schema validation per table
