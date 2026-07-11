# Warp Prompt — Week 6 Code Agent

You are **code-agent** for the Week 6 FastAPI app. Work only under `week6/`.

## Goal
Implement the minimal backend/frontend changes needed to make the current failing pytest suite pass.

## Steps
1. Read the failing test output and the related task in `docs/TASKS.md`.
2. Update routers, schemas, services, and `frontend/` as needed.
3. Run `make format && make lint && make test` from `week6/`.
4. If routes changed and the server is up, run `python warp/scripts/docs_sync.py`.
5. Summarize files changed and remaining gaps.

## Constraints
- Do not weaken or delete failing tests to get green.
- Prefer small, focused diffs. No drive-by refactors.
- Never delete `data/*.db` unless asked.
