# modern-ai — Cursor agent instructions

Equivalent to `CLAUDE.md` for this repo. Cursor Agent reads this file for project context.

## Repo layout

| Path | What |
|------|------|
| `src/` | Open Library MCP server (TypeScript) |
| `week4/` | Week 4 FastAPI + SQLite command-center starter |
| `.cursor/skills/` | Project slash workflows (`/tests`, `/docs-sync`) |
| `.cursor/agents/` | Subagents: `test-agent`, `code-agent` |
| `.cursor/mcp.json` | Open Library MCP config |

## Week 4 commands

Run from `week4/` with `conda activate moderndev`:

```bash
make run    # http://localhost:8000
make test   # pytest
make format && make lint
make seed
```

| Code | Location |
|------|----------|
| FastAPI entry | `backend/app/main.py` |
| Routes | `backend/app/routers/` |
| Tests | `backend/tests/` |
| UI | `frontend/app.js` |
| Backlog | `docs/TASKS.md` |

## Automations (Cursor)

| Workflow | How to run |
|----------|------------|
| Test runner | `/tests` in Agent chat |
| API docs sync | `/docs-sync` (app must be running) |
| TDD | Invoke **test-agent** → **code-agent** |

## Default workflow for new endpoints

1. Pick a task in `week4/docs/TASKS.md`
2. **test-agent** — write failing tests
3. **code-agent** — implement until `make test` passes
4. `/docs-sync` if routes changed
5. `make format && make lint`

## Style and safety

- Run `make test` before finishing Week 4 changes
- Safe: pytest, black, ruff, `npm test` at repo root
- Avoid: deleting `week4/data/*.db`, force push, editing `node_modules/`

## MCP (Open Library)

Enable **openlibrary** in Cursor Settings → MCP. Tools: `search_books`, `lookup_isbn`, `get_work`, `get_author`, `search_by_subject`, `get_edition`. Build: `npm run build && npm test`.
