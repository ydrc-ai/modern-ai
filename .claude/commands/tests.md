---
allowed-tools: Bash, Read, Grep, Glob
argument-hint: [pytest-path-or-marker]
description: Run Week 4 pytest suite; summarize failures and suggest fixes
---

Run the Week 4 test suite from the `week4/` directory.

## Arguments

Optional path or marker: `$ARGUMENTS`

If empty, run the full suite.

## Steps

1. `cd week4`
2. If `$ARGUMENTS` is non-empty:
   - `PYTHONPATH=. pytest -q $ARGUMENTS --maxfail=1 -x`
3. Else:
   - `make test` (fallback: `PYTHONPATH=. pytest -q backend/tests --maxfail=1 -x`)
4. If tests pass, report: **All tests passed** and list test files executed.
5. If tests fail:
   - Print the failing test name and assertion/error
   - Point to the most likely source file under `backend/app/`
   - Suggest the smallest fix (do not refactor unrelated code)
   - Offer to re-run only the failing test file

## Safety

- Do not delete the SQLite database in `week4/data/` unless a test explicitly requires a fresh seed.
- Do not run destructive git commands.
- Prefer read-only inspection before editing source.

## Context

Week 4 is a FastAPI + SQLite notes/action-items app. Tests live in `backend/tests/`. See `week4/docs/TASKS.md` for feature backlog.
