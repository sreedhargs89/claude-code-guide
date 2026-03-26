# Code Review — Common Issues Reference

Consulted by the `/code-review` skill when analysing code.
Provides severity ratings and suggested fixes for common patterns.

---

## Critical issues (always flag)

### Hardcoded credentials
```python
# BAD
API_KEY = "sk-abc123xyz"
password = "mypassword123"

# GOOD
import os
API_KEY = os.environ["API_KEY"]
```
**Severity:** Critical  
**Reason:** Credentials committed to version control are a major security incident.

---

### Silent exception swallowing
```python
# BAD
try:
    process_data()
except Exception:
    pass

# GOOD
try:
    process_data()
except Exception as e:
    log.error(f"process_data failed: {e}", exc_info=True)
    raise
```
**Severity:** Critical  
**Reason:** Hides failures, makes debugging impossible.

---

### Mutable default argument
```python
# BAD — shared across all calls
def append_item(item, lst=[]):
    lst.append(item)
    return lst

# GOOD
def append_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```
**Severity:** Critical  
**Reason:** Classic Python bug — the default list is created once and reused.

---

## Warnings (should fix)

### Missing type hints
```python
# BAD
def fetch_data(url, timeout):
    ...

# GOOD
def fetch_data(url: str, timeout: int = 60) -> dict:
    ...
```
**Severity:** Warning

---

### requests library instead of httpx for async code
```python
# BAD in async context
import requests
response = requests.get(url)

# GOOD
import httpx
async with httpx.AsyncClient() as client:
    response = await client.get(url)
```
**Severity:** Warning — `requests` blocks the event loop in async code.

---

### No retry logic on external API calls
```python
# BAD
response = await client.get(url)

# GOOD — minimum viable retry
for attempt in range(3):
    try:
        response = await client.get(url)
        response.raise_for_status()
        break
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            await asyncio.sleep(5 * (attempt + 1))
        else:
            raise
```
**Severity:** Warning for production code.

---

### Pandas `iterrows()` on large DataFrames
```python
# BAD — very slow
for index, row in df.iterrows():
    process(row['value'])

# GOOD — vectorised
df['result'] = df['value'].apply(process)
# or even better: use vectorised pandas operations directly
```
**Severity:** Warning for DataFrames > 10K rows.

---

### `SELECT *` in production queries
```python
# BAD
query = "SELECT * FROM fact_sales"

# GOOD
query = "SELECT sale_id, date_id, customer_id, revenue FROM fact_sales"
```
**Severity:** Warning — fetches unnecessary columns, breaks if schema changes.

---

## Suggestions (consider fixing)

### Function longer than 30 lines
Split into smaller functions with single responsibilities.

### Deeply nested conditionals (3+ levels)
Consider early returns or extracting conditions into named boolean variables.

### Magic numbers
```python
# BAD
if len(records) > 50000:

# GOOD
PARQUET_THRESHOLD = 50_000
if len(records) > PARQUET_THRESHOLD:
```

### Missing docstrings on public functions
All public functions (no leading underscore) should have at least a one-line docstring.

---

## Data Engineering specific

### DAG without retry policy
```python
# BAD
@task
def fetch():
    ...

# GOOD
@task(retries=3, retry_delay=timedelta(minutes=5))
def fetch():
    ...
```
**Severity:** Warning for production DAGs.

### Hardcoded dates in DAGs
```python
# BAD
start_date = datetime(2024, 1, 1)

# GOOD
from datetime import datetime, timedelta
start_date = datetime.now() - timedelta(days=1)
```
