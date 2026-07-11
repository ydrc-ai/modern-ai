# Week 6 — agent context (Warp + local)

FastAPI + SQLite command center. **All commands from this directory.**

```bash
conda activate moderndev
make run && make test
```

## Warp automations

See `warp/README.md`:

- Workflows: `warp/workflows/*.yaml`
- Rules: `warp/rules/week6-agent-rules.md`
- Multi-agent: `warp/multi-agent/playbook.md`

## Edit map

| Change | File |
|--------|------|
| Routes | `backend/app/routers/` |
| Schemas | `backend/app/schemas.py` |
| Models / DB | `backend/app/models.py`, `db.py` |
| Logic | `backend/app/services/` |
| Tests | `backend/tests/` |
| UI | `frontend/` |

## Suggested TDD flow

1. Pick a task in `docs/TASKS.md`
2. Warp tab A → test-agent prompt
3. Warp tab B → code-agent prompt (or same tab after tests fail)
4. `./warp/scripts/run_tests.sh`
5. `python warp/scripts/docs_sync.py` if routes changed
