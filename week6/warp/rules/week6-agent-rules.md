# Week 6 Warp Agent Rules

Scope: only modify files under `week6/` unless the user explicitly asks otherwise.

## Commands (from `week6/`)

- Run app: `make run` → http://127.0.0.1:8000
- Tests: `make test` or `./warp/scripts/run_tests.sh`
- Format/lint: `make format && make lint`
- Docs sync (app running): `python warp/scripts/docs_sync.py`

## Layout

| Area | Path |
|------|------|
| Routes | `backend/app/routers/` |
| Schemas | `backend/app/schemas.py` |
| Models | `backend/app/models.py` |
| Extract | `backend/app/services/extract.py` |
| Tests | `backend/tests/` |
| UI | `frontend/` |
| Tasks | `docs/TASKS.md` |

## Safety

- Do not delete `week6/data/*.db` unless asked.
- No force-push, no `--no-verify` commits.
- Prefer TDD: failing tests first, then minimal implementation.
- Keep automations idempotent and non-interactive.
