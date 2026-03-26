---
name: fetch-api
description: >
  Use this skill when fetching, downloading, or refreshing data from
  external REST API endpoints. Handles async HTTP requests, saves
  responses to timestamped directories, and logs all results.
  Invoke when a user asks to "fetch data", "pull from API", or
  "refresh the dataset".
usage: /fetch-api
---

# Fetch API skill

Fetches data from configured REST API endpoints using asynchronous Python.
Saves responses to timestamped directories and logs all HTTP activity.

## Pre-conditions
- Python environment is available
- Required packages: httpx, asyncio (install if missing)

## Steps

### Step 1 — Activate environment
Activate the virtual environment if one exists in the project:
- Linux/Mac: `source .venv/bin/activate`
- Windows: `.venv\Scripts\activate`

If no virtual environment exists, use the system Python.

### Step 2 — Install dependencies
Ensure httpx is installed:
```
pip install httpx
```

### Step 3 — Run the fetch script
A pre-built, tested script is available at:
  `.claude/skills/fetch-api/scripts/fetch_data.py`

Run it using the .venv Python environment:
  `.venv/bin/python .claude/skills/fetch-api/scripts/fetch_data.py`

Do NOT rewrite or regenerate this script. Use it as-is.

If you need to fetch different endpoints, edit the `ENDPOINTS` dict at
the top of the script — do not rewrite the rest of the logic.

For errors during fetch, consult `.claude/skills/fetch-api/references/error-guide.md`.

### Step 4 — Save results
Save each response to:
```
data/YYYY-MM-DD_HH-MM-SS/
```
- Name each file after the endpoint path (e.g., `users.json`, `posts.json`)
- Create the directory if it doesn't exist
- Save raw JSON responses (do not transform yet)

### Step 5 — Log results
Create a log file at:
```
logs/fetch-api/YYYY-MM-DD_HH-MM-SS/fetch-api.log
```

The log must include:
- Start time and end time
- Each URL fetched
- HTTP status code for each request
- File size of each saved response
- Success/failure for each endpoint
- Any errors with full exception messages
- Summary: X successful, Y failed

## Error handling
- HTTP 429 (rate limited): wait 5 seconds, retry once
- HTTP 5xx (server error): log as failure, continue to next endpoint
- Connection error: log as failure, continue to next endpoint
- Do not crash the entire run if one endpoint fails

## Expected output
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
