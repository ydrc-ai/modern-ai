# Week 4 — Cursor agent context

FastAPI backend, static frontend, SQLite. **All commands from this directory.**

```bash
conda activate moderndev
make run && make test
```

## Edit map

| Change | File |
|--------|------|
| Routes | `backend/app/routers/` |
| Schemas | `backend/app/schemas.py` |
| Models / DB | `backend/app/models.py`, `db.py` |
| Logic | `backend/app/services/` |
| Tests | `backend/tests/` |
| UI | `frontend/app.js` |

## Agent workflow

1. `docs/TASKS.md` — pick one task
2. **test-agent** → failing tests
3. **code-agent** → implementation
4. `/tests` → verify
5. `/docs-sync` → update `docs/API.md`

See root `AGENTS.md` for full repo context.
