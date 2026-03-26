# Fetch API — Error Reference

This file is consulted by the `/fetch-api` skill when handling errors.
Claude Code reads it only when it encounters an error it needs to resolve.

---

## HTTP Errors

### 429 Too Many Requests
**Cause:** API rate limit hit.  
**Fix:** Wait 5–10 seconds, then retry the single failed endpoint. Do not retry all endpoints.  
**If persistent:** Check if the API has a daily quota that's been exhausted.

### 401 Unauthorized
**Cause:** Missing or expired auth token.  
**Fix:** Check that the `API_TOKEN` environment variable is set and not expired.  
**Do not:** Retry automatically — fix the credentials first.

### 403 Forbidden
**Cause:** Token exists but lacks permission for this endpoint.  
**Fix:** Check the API documentation for required scopes. Log the error and skip this endpoint.

### 404 Not Found
**Cause:** Endpoint URL is wrong or the resource was deleted.  
**Fix:** Log as a permanent failure for this endpoint. Do not retry.

### 500 / 502 / 503 / 504 Server Error
**Cause:** Upstream API is having issues.  
**Fix:** Wait 30 seconds, retry once. If still failing, log as failure and continue to next endpoint.

---

## Connection Errors

### `httpx.ConnectTimeout`
**Cause:** Request took longer than `TIMEOUT_SECONDS` to connect.  
**Fix:** Increase timeout to 120 seconds for this endpoint and retry once.

### `httpx.ReadTimeout`
**Cause:** Connected but response was too slow.  
**Fix:** Increase timeout. Consider if the API returns paginated data that needs chunked reading.

### `httpx.ConnectError`
**Cause:** DNS failure or network unreachable.  
**Fix:** Check network connectivity. Do not retry more than once — if the host is down, all retries will fail.

---

## Data Errors

### Response is empty (0 bytes)
**Cause:** API returned an empty body with a 200 status.  
**Fix:** Log as a warning (not failure). Save the empty file anyway to preserve the audit trail.

### Response is HTML instead of JSON/CSV
**Cause:** Redirected to a login page or error page.  
**Fix:** Check if the API requires authentication. Log the first 200 characters of the response for diagnosis.

### `csv.Error` on parse
**Cause:** Response is not valid CSV despite a 200 status.  
**Fix:** Save the raw response as `.txt` for manual inspection. Log as a warning.

---

## Environment Issues

### `ModuleNotFoundError: No module named 'httpx'`
**Fix:** Run `pip install httpx` (or `.venv/bin/pip install httpx` if using a virtual environment).

### `FileNotFoundError` on output directory
**Fix:** The output directory creation code should use `mkdir(parents=True, exist_ok=True)`.
Check that the path is correct and doesn't contain characters invalid for your OS.
