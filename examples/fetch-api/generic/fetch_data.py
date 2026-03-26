"""
fetch_data.py — Generic async API fetcher
==========================================
Fetches data from multiple REST API endpoints concurrently using httpx.
Saves responses to a timestamped directory. Logs all activity.

Usage:
    python fetch_data.py

Requirements:
    pip install httpx

Customise:
    - Update ENDPOINTS dict with your own URLs
    - Optionally add auth headers to get_client()
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path

import httpx

# ── Configuration ──────────────────────────────────────────────────────────────

ENDPOINTS: dict[str, str] = {
    "users":    "https://jsonplaceholder.typicode.com/users",
    "posts":    "https://jsonplaceholder.typicode.com/posts",
    "comments": "https://jsonplaceholder.typicode.com/comments",
}

TIMEOUT_SECONDS = 60
OUTPUT_DIR = Path("data")
LOG_DIR = Path("logs/fetch-api")

# ── Setup ───────────────────────────────────────────────────────────────────────

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
run_output_dir = OUTPUT_DIR / timestamp
run_log_dir = LOG_DIR / timestamp

run_output_dir.mkdir(parents=True, exist_ok=True)
run_log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.FileHandler(run_log_dir / "fetch-api.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


# ── Fetch ───────────────────────────────────────────────────────────────────────

def get_client() -> httpx.AsyncClient:
    """Return a configured httpx client. Add auth headers here if needed."""
    return httpx.AsyncClient(
        timeout=httpx.Timeout(TIMEOUT_SECONDS),
        headers={
            "Accept": "application/json",
            # "Authorization": f"Bearer {os.environ['API_TOKEN']}",
        },
    )


async def fetch_one(
    client: httpx.AsyncClient,
    name: str,
    url: str,
) -> tuple[str, bool, str]:
    """
    Fetch a single endpoint.
    Returns (name, success, message).
    """
    log.info(f"Fetching {name}: {url}")
    try:
        response = await client.get(url)
        response.raise_for_status()

        # Save to file
        out_path = run_output_dir / f"{name}.json"
        out_path.write_text(response.text, encoding="utf-8")

        size_kb = len(response.content) / 1024
        log.info(f"  ✓ {name}: HTTP {response.status_code}, {size_kb:.1f} KB → {out_path}")
        return (name, True, f"HTTP {response.status_code}, {size_kb:.1f} KB")

    except httpx.HTTPStatusError as e:
        msg = f"HTTP {e.response.status_code}: {e.response.text[:200]}"
        log.error(f"  ✗ {name}: {msg}")
        return (name, False, msg)

    except httpx.RequestError as e:
        msg = f"Request error: {e}"
        log.error(f"  ✗ {name}: {msg}")
        return (name, False, msg)


async def fetch_all() -> list[tuple[str, bool, str]]:
    """Fetch all endpoints concurrently."""
    async with get_client() as client:
        tasks = [
            fetch_one(client, name, url)
            for name, url in ENDPOINTS.items()
        ]
        return await asyncio.gather(*tasks)


# ── Main ────────────────────────────────────────────────────────────────────────

async def main() -> None:
    log.info(f"Starting fetch run — {timestamp}")
    log.info(f"Endpoints: {len(ENDPOINTS)}")
    log.info(f"Output directory: {run_output_dir}")

    results = await fetch_all()

    successes = [r for r in results if r[1]]
    failures  = [r for r in results if not r[1]]

    log.info("─" * 60)
    log.info(f"Complete. {len(successes)} succeeded, {len(failures)} failed.")

    if failures:
        log.warning("Failed endpoints:")
        for name, _, msg in failures:
            log.warning(f"  {name}: {msg}")

    if not successes:
        log.error("All endpoints failed. Check network / credentials.")
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
