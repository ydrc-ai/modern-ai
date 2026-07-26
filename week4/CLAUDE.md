# Week 4 — developer command center

FastAPI backend, static frontend, SQLite via SQLAlchemy. All commands run from **this directory** (`week4/`).

## Run & test

```bash
make run    # API + frontend at :8000, /docs for Swagger
make test   # pytest -q backend/tests
make seed   # load data/seed.sql if needed
```

## Where to edit

| Task type | Location |
|-----------|----------|
| New/changed routes | `backend/app/routers/` |
| Pydantic models | `backend/app/schemas.py` |
| SQLAlchemy models | `backend/app/models.py` |
| Business logic | `backend/app/services/` (e.g. `extract.py`) |
| Tests | `backend/tests/` |
| UI | `frontend/app.js` |

## Backlog

See `docs/TASKS.md` — pick one task at a time.

## Agent workflow

1. **test-agent** — failing test first
2. **code-agent** — minimal implementation
3. `/tests` — verify suite
4. `/docs-sync` — update `docs/API.md` after route changes

## Open Library MCP (optional)

Repo root has an Open Library MCP server. Use it to enrich notes (book titles, ISBN lookup) when building data-related features.
