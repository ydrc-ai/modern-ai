# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## SUBMISSION DETAILS

Name: **Flynn Zang** \

This assignment took me about **3** hours to do.


## YOUR RESPONSES
Tasks completed:
> Implemented **5** tasks from `docs/TASKS.md` (all code under `week6/` only):
>
> 1. **Task 2 — Notes search with pagination and sorting** (medium): `GET /notes/search` with case-insensitive `q`, `page`/`page_size`, `sort=created_desc|title_asc`, paginated payload.
> 2. **Task 3 — Full Notes CRUD with optimistic UI** (medium): `PUT /notes/{id}`, `DELETE /notes/{id}`, Pydantic min/max validation, frontend save/delete with rollback on error.
> 3. **Task 4 — Action items filters and bulk complete** (medium): `completed` filter on list, `POST /action-items/bulk-complete`, filter toggles + multi-select UI, tests for missing-ID failure.
> 4. **Task 6 — Improve extraction logic and endpoints** (medium): `#hashtags` + `- [ ]` checkboxes (plus legacy `TODO:` / `!`), `POST /notes/{id}/extract?apply=true|false`.
> 5. **Task 8 — List endpoint pagination** (easy): `page`/`page_size` on `GET /notes` and `GET /action-items` returning `items` + `total` (+ page metadata).

### Automation A: Warp Drive saved prompts, rules, MCP servers

a. Design of each automation, including goals, inputs/outputs, steps
> **A1 — Week6 Test Runner** (`warp/workflows/week6-test-runner.yaml` + `warp/scripts/run_tests.sh`)
> - **Goal:** One-shot, idempotent pytest run from Warp Drive / Command Palette.
> - **Inputs:** `week6_path`, `conda_env`, `test_path`, `maxfail`.
> - **Outputs:** Quiet pytest summary; exits non-zero on failure.
> - **Steps:** `cd` → activate conda → `PYTHONPATH=. pytest -q …`.
>
> **A2 — Week6 Docs Sync** (`warp/workflows/week6-docs-sync.yaml` + `warp/scripts/docs_sync.py`)
> - **Goal:** Regenerate `docs/API.md` from live `/openapi.json` and print route deltas.
> - **Inputs:** `base_url` (default `http://127.0.0.1:8000`), output path.
> - **Outputs:** Updated markdown endpoint table + Added/Removed delta section.
> - **Steps:** Fetch OpenAPI → compare to previous file → write `docs/API.md`.
>
> **A3 — Week6 Agent Rules** (`warp/rules/week6-agent-rules.md`)
> - **Goal:** Keep Warp agents scoped to `week6/`, with safe commands and an edit map.
> - **Inputs/Outputs:** Rule text loaded into Warp Rules / pasted into Agent Mode.
> - **Steps:** Import rule → agents auto-prefer `make test` / docs-sync / no DB deletion.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Remember conda env, `PYTHONPATH`, pytest flags, then manually curl OpenAPI and rewrite API docs by hand after every route change.
>
> **After:** Invoke **Week6 Test Runner** / **Week6 Docs Sync** from Warp Drive (or run the checked-in scripts). Rules stop agents from wandering outside `week6/` or deleting `data/*.db`.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> - **Test runner / docs sync:** high autonomy for *read-only / docs-only* commands; I supervised by reading the pytest summary and the API.md delta.
> - **Feature implementation (Tasks 2–4, 6, 8):** medium autonomy — agents/workflows may edit `backend/` + `frontend/` under `week6/` only; I reviewed diffs and re-ran `make test` + `make lint` myself before considering a task done.
> - **Denied without ask:** deleting SQLite DBs, force-push, commits outside the assignment scope.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> N/A for Automation A (single-agent Drive workflows). See Automation B.

e. How you used the automation (what pain point it resolves or accelerates)
> Used the test-runner workflow/script as the gate after each task (14 tests green). Used docs-sync against a live `make run` server to produce `docs/API.md` so the OpenAPI surface (search, CRUD, extract, bulk-complete, pagination) stayed documented without hand-editing tables. Rules kept the working set inside `week6/` while iterating.


### Automation B: Multi‑agent workflows in Warp

a. Design of each automation, including goals, inputs/outputs, steps
> **B1 — Concurrent TestAgent + CodeAgent** (`warp/multi-agent/playbook.md`, `warp/prompts/week6-test-agent.md`, `warp/prompts/week6-code-agent.md`, `warp/multi-agent/worktree-setup.sh`)
> - **Goal:** Run independent TASKS.md items in parallel Warp tabs without file clobbering.
> - **Inputs:** Disjoint task IDs; optional worktree paths from the setup script.
> - **Outputs:** Failing tests on branch A; green implementation on branch B; merged suite on the main week6 branch.
> - **Steps:** `worktree-setup.sh` → open Tab A (test-agent prompt) + Tab B (code-agent prompt) on different tasks → merge → `make test`.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** One agent serializes “write tests → implement → lint” for every task; easy to mix roles or overwrite half-finished edits.
>
> **After:** Separate Warp tabs with explicit prompts + git worktrees isolate Task N tests from Task M implementation. Shared hotspots (`schemas.py`, `frontend/app.js`) are called out in the playbook so merges are planned.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> - **test-agent tab:** write access limited to `backend/tests/` (per prompt); I supervised by confirming failures were assertion/import errors, not infra breakage.
> - **code-agent tab:** write access to routers/schemas/services/frontend; required green `make test` before merge.
> - **Coordination:** I assigned disjoint surfaces (e.g. notes search vs action-item bulk) and merged sequentially, re-running the full suite after each merge.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> - **Roles:** Tab A = specify behavior in tests; Tab B = implement; Tab C (optional) = docs-sync + full-suite QA.
> - **Coordination:** git worktrees (`week6/agent-a`, `week6/agent-b`) so agents do not share a dirty working tree.
> - **Wins:** Notes CRUD/search work and action-item filter/bulk work progressed without blocking each other on wall-clock time.
> - **Risks:** Both touching `schemas.py` / `frontend/app.js` → merge conflicts; mitigated by finishing API shapes first, then one UI pass.
> - **Failures avoided:** No cross-week edits; playbook forbids leaving `week6/`.

e. How you used the automation (what pain point it resolves or accelerates)
> The multi-agent playbook + prompts structured how Tasks 2/3/8 (notes) and Task 4 (action items) were delivered: tests-first in one lane, implementation in another, then a single frontend pass. That cut context-switching cost versus one long mixed session and made `make test` the merge gate.


### (Optional) Automation C: Any Additional Automations
a. Design of each automation, including goals, inputs/outputs, steps
> **C1 — Format & Lint workflow** (`warp/workflows/week6-format-lint.yaml`)
> - **Goal:** Run `make format && make lint` from Warp Drive after code-agent edits.
> - **Inputs:** `week6_path`, `conda_env`.
> - **Outputs:** black/ruff fixes + clean lint status.
> - **Steps:** activate env → `make format` → `make lint`.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Remember black/ruff invocation and whether to run `--fix`.
> **After:** One Warp workflow (or Makefile targets) after each implementation pass.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> High autonomy for formatting only; I glanced at the ruff summary to ensure no logic changes hid in auto-fixes.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> N/A — runs as a post-step in either agent tab.

e. How you used the automation (what pain point it resolves or accelerates)
> Ran format/lint after implementing extract + pagination so CI-style cleanliness did not depend on remembering flags; kept the Week 6 tree ruff-clean alongside the 14-test green suite.
