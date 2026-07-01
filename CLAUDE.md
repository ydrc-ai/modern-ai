# modern-ai — agent guidance

This repo has two main parts:

1. **Open Library MCP server** (repo root) — TypeScript STDIO MCP in `src/`, tests via `npm test`
2. **Week 4 starter app** (`week4/`) — FastAPI + SQLite notes/action-items command center

## Week 4 quick reference

```bash
cd week4
conda activate cs146s   # if using course env
make run              # http://localhost:8000
make test             # pytest
make format && make lint
make seed             # apply SQLite seed if needed
```

| Path | Purpose |
|------|---------|
| `week4/backend/app/main.py` | FastAPI entry |
| `week4/backend/app/routers/` | API routes |
| `week4/backend/tests/` | pytest |
| `week4/frontend/app.js` | Static UI |
| `week4/docs/TASKS.md` | Feature backlog for agent workflows |
| `week4/data/` | SQLite DB + seed |

## Custom automations

**Cursor (primary):** see `AGENTS.md`, `.cursor/skills/`, `.cursor/agents/`

| Automation | How to run |
|------------|------------|
| Test runner | `/tests` in Cursor Agent |
| API docs sync | `/docs-sync` |
| TDD pair | **test-agent** → **code-agent** in Cursor Agent |

**Claude Code (legacy mirrors):** `.claude/commands/`, `.claude/agents/`

## MCP (Open Library)

The **openlibrary** MCP server is configured in `.cursor/mcp.json`. In Claude Code, add the same server to your MCP config if you want book search during Week 4 extensions (e.g. lookup reading lists for notes).

Tools: `search_books`, `lookup_isbn`, `get_work`, `get_author`, `search_by_subject`, `get_edition`.

Build MCP server: `npm run build && npm test` from repo root.

## Workflow defaults

When adding a Week 4 API endpoint:

1. Read the matching item in `week4/docs/TASKS.md`
2. Delegate to **test-agent** → write failing tests
3. Delegate to **code-agent** → implement until green
4. Run `/docs-sync` if routes changed
5. Run `make format && make lint` in `week4/`

## Safety

- Safe: `make test`, `make format`, `make lint`, `npm test`, read-only git
- Avoid: deleting `week4/data/*.db` without reason, force push, editing `node_modules/`
