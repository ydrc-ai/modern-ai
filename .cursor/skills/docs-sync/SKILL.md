---
name: docs-sync
description: Sync week4/docs/API.md from the live OpenAPI schema at /openapi.json. Use after adding or changing API routes.
disable-model-invocation: true
---

# Week 4 API docs sync

Keep `week4/docs/API.md` aligned with the running FastAPI app.

## Prerequisites

App must be running from `week4/`:

```bash
conda activate moderndev
cd week4
make run
```

## Steps

1. Fetch schema: `curl -s http://127.0.0.1:8000/openapi.json`
2. Read or create `week4/docs/API.md`
3. Update with:
   - Endpoint table (method, path, summary)
   - Request/response shapes for notes and action-items routes
   - Query params (e.g. `GET /notes/search?q=`)
4. Output a delta summary:
   - **Added** routes
   - **Changed** fields
   - **Removed** routes
   - **TODOs** for manual gaps

## Output format

```markdown
## Docs sync summary
- Endpoints documented: N
- Added: ...
- Changed: ...
- Removed: ...
- TODOs: ...
```

## Safety

- Only edit `week4/docs/API.md` unless asked otherwise
- Do not change backend code in this workflow unless a schema bug is found — file a TODO instead

## Related

Task 7 in `week4/docs/TASKS.md`. Cross-check with `/docs` Swagger UI.
