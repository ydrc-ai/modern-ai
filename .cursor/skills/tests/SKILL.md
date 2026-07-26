---
name: tests
description: Run Week 4 pytest suite, summarize failures, suggest fixes. Use when testing the FastAPI app or after code changes in week4/.
disable-model-invocation: true
---

# Week 4 test runner

Run pytest for the developer command-center app in `week4/`.

## Environment

Use conda env `moderndev` (or `cs146s` if available):

```bash
conda activate moderndev
cd week4
```

## Run

**Full suite** (default):

```bash
PYTHONPATH=. pytest -q backend/tests --maxfail=1 -x
```

**Single file** (if user passed a path in their message):

```bash
PYTHONPATH=. pytest -q backend/tests/test_notes.py --maxfail=1 -x
```

Fallback if `make` works: `make test`

## On success

Report **All tests passed** and list files under `backend/tests/` that ran.

## On failure

1. Print failing test name and assertion/error
2. Point to the likely source under `backend/app/` (routers, services, schemas)
3. Suggest the smallest fix — no unrelated refactors
4. Offer to re-run only the failing file

## Safety

- Do not delete `week4/data/*.db` unless a test requires a fresh seed
- No destructive git commands
- Inspect before editing

## Context

Backlog: `week4/docs/TASKS.md`. Tests: `backend/tests/test_notes.py`, `test_action_items.py`, `test_extract.py`.
