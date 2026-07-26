# Week 6

Minimal full‑stack starter for experimenting with Warp agentic workflows.

- FastAPI backend with SQLite (SQLAlchemy)
- Static frontend (no Node toolchain needed)
- Pytest suite + pre-commit (black + ruff)
- Warp Drive workflows, rules, and multi-agent playbook under `warp/`

## Quickstart

1) Activate your conda environment

```bash
conda activate moderndev
```

2) Run the app (from `week6/`)

```bash
cd week6 && make run
```

Open `http://localhost:8000` for the frontend and `http://localhost:8000/docs` for the API docs.

## Structure

```
backend/                # FastAPI app
frontend/               # Static UI served by FastAPI
data/                   # SQLite DB + seed
docs/                   # TASKS + generated API.md
warp/                   # Warp Drive workflows, prompts, multi-agent playbook
```

## Features (assignment tasks)

- Notes: list/create/update/delete, search with sort + pagination, extract hashtags/action items
- Action items: list with completed filter + pagination, complete, bulk-complete
- UI: search, pagination, optimistic note edits, filter toggles, bulk select

## Tests

```bash
cd week6 && make test
# or
./warp/scripts/run_tests.sh
```

## Formatting/Linting

```bash
cd week6 && make format && make lint
```

## Warp automations

See [`warp/README.md`](warp/README.md) for importable workflows, agent prompts, rules, and the multi-agent worktree playbook.

```bash
# Docs sync (server must be running)
python warp/scripts/docs_sync.py
```

## Configuration

Copy `.env.example` to `.env` (in `week6/`) to override defaults like the database path.
