# Example: Fetch API (Generic)

Demonstrates the pattern used in the `/fetch-api` skill — async concurrent
HTTP requests with structured logging and timestamped output.

## What it does

- Fetches multiple REST endpoints **concurrently** using `asyncio.gather()`
- Saves each response as a JSON file in a timestamped directory
- Logs all activity (status codes, file sizes, errors) to a structured log file
- Handles HTTP errors and connection errors gracefully (one failure doesn't crash the run)

## Quick start

```bash
cd examples/fetch-api/generic

pip install httpx

python fetch_data.py
```

## Output structure

```
data/
└── 2025-03-15_09-30-00/
    ├── users.json
    ├── posts.json
    └── comments.json
logs/
└── fetch-api/
    └── 2025-03-15_09-30-00/
        └── fetch-api.log
```

## Customising for your own APIs

Edit the `ENDPOINTS` dict in `fetch_data.py`:

```python
ENDPOINTS = {
    "customers": "https://api.yourservice.com/v1/customers",
    "products":  "https://api.yourservice.com/v1/products",
    "orders":    "https://api.yourservice.com/v1/orders",
}
```

To add authentication, update `get_client()`:

```python
def get_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        timeout=httpx.Timeout(60),
        headers={
            "Authorization": f"Bearer {os.environ['API_TOKEN']}",
        },
    )
```

## Using this with the skill

To use the pre-built script from the skill rather than generating code on each run,
add a `scripts/` folder to your skill and reference it:

```
.claude/skills/fetch-api/
├── skill.md
└── scripts/
    └── fetch_data.py   ← copy this file here
```

Then in your `skill.md`, tell Claude Code to use it:
```markdown
### Step 3 — Run the fetch script
Run the existing script at .claude/skills/fetch-api/scripts/fetch_data.py
Do not rewrite the script. Use it as-is.
```

## See also

- [Data engineering variant](../data-engineering/) — uses GitHub raw URLs as a
  proxy for real data warehouse APIs, with CSV output instead of JSON
