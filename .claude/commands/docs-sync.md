---
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
description: Sync week4/docs/API.md from the live OpenAPI schema
---

Keep API documentation in sync with the running FastAPI app.

## Steps

1. Confirm the app exposes OpenAPI at `/openapi.json` (see `week4/backend/app/main.py`).
2. If the server is not running, start it in the background from `week4/`:
   - `make run` (or `PYTHONPATH=. uvicorn backend.app.main:app --host 127.0.0.1 --port 8000`)
3. Fetch the schema:
   - `curl -s http://127.0.0.1:8000/openapi.json`
4. Read or create `week4/docs/API.md`.
5. Update `API.md` with:
   - A table of endpoints (method, path, summary)
   - Request/response body shapes for notes and action-items routes
   - Query params (e.g. `GET /notes/search?q=`)
6. Compare old vs new and output a **delta summary**:
   - Added routes
   - Removed routes
   - Changed request/response fields
7. If `week4/docs/TASKS.md` task 7 mentions drift, note any remaining manual gaps.

## Output format

```
## Docs sync summary
- Endpoints documented: N
- Added: ...
- Changed: ...
- Removed: ...
- TODOs: ...
```

## Safety

- Only edit `week4/docs/API.md` unless the user asked to update other docs.
- Do not change backend code in this command unless a schema bug is discovered; file a separate TODO instead.
