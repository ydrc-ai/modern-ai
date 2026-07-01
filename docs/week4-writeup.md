# Week 4 Write-up

Copy this file to `week4/writeup.md` if needed: `cp docs/week4-writeup.md week4/writeup.md`

Tip: Preview markdown — Mac: `⌘ + Shift + V` | Windows/Linux: `Ctrl + Shift + V`

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices), [SubAgents overview](https://docs.anthropic.com/en/docs/claude-code/sub-agents), Cursor Skills/Subagents docs, course `week4/assignment.md`

This assignment took me about **TODO** hours to do.

---

## YOUR RESPONSES

### Automation #1 — `/tests` Cursor Skill (Category A: slash command)

**a. Design inspiration**

Assignment Example 1 (“Test runner with coverage”) and Claude Code best practices: focused, repeatable, idempotent workflows. Implemented as a **Cursor Skill** at `.cursor/skills/tests/SKILL.md` (Cursor equivalent of `.claude/commands/tests.md`).

**b. Design (goals, inputs/outputs, steps)**

- **Goal:** One-command pytest for the Week 4 FastAPI starter without remembering `PYTHONPATH` or Makefile targets.
- **Inputs:** Optional pytest path or marker in the user’s message (e.g. `backend/tests/test_notes.py`).
- **Outputs:** Pass/fail summary; on failure — test name, likely file under `backend/app/`, suggested minimal fix.
- **Steps:** `conda activate moderndev` → `cd week4` → `PYTHONPATH=. pytest -q backend/tests --maxfail=1 -x` → structured report.

**c. How to run, expected outputs, rollback/safety**

- **Run:** Type `/tests` in **Cursor Agent** chat, or `/tests backend/tests/test_notes.py` for one file.
- **Manual verify:** `cd week4 && PYTHONPATH=. pytest -q backend/tests`
- **Expected (green):** `3 passed` — `test_notes.py`, `test_action_items.py`, `test_extract.py`.
- **Safety:** Does not delete SQLite DB or run destructive git. Rollback = revert any accidental edits made while fixing failures.

**d. Before vs. after**

| Before | After |
|--------|-------|
| Manually activate conda, cd to week4, run pytest, parse tracebacks | Single `/tests` skill returns structured pass/fail and fix hints |

**e. How you used the automation to enhance the starter application**

> TODO (Part II)

---

### Automation #2 — TestAgent + CodeAgent (Category C: SubAgents)

**a. Design inspiration**

Assignment Example 1 (TestAgent + CodeAgent) and [SubAgents overview](https://docs.anthropic.com/en/docs/claude-code/sub-agents). Implemented as **Cursor subagents** in `.cursor/agents/test-agent.md` and `.cursor/agents/code-agent.md`. Workflow guidance also in root `AGENTS.md` and `week4/AGENTS.md` (Category B).

**b. Design (goals, inputs/outputs, steps)**

- **Goal:** TDD workflow for Week 4 tasks in `docs/TASKS.md` — tests before implementation.
- **test-agent inputs:** Task number or description.
- **test-agent outputs:** New/updated failing tests + pytest output.
- **code-agent inputs:** Failing tests from test-agent.
- **code-agent outputs:** Router/service/schema/UI changes; green `make test`.
- **Flow:** User describes task → test-agent writes failing tests → code-agent implements → `/tests` verifies → optional `/docs-sync`.

**c. How to run, expected outputs, rollback/safety**

- **Run in Cursor Agent:**
  ```
  Use test-agent to add failing tests for Task 2 (notes search) from week4/docs/TASKS.md.
  Then use code-agent to implement until tests pass.
  ```
- **Verify:** `cd week4 && make test && make lint`
- **Expected:** New tests in `backend/tests/test_notes.py`; route in `backend/app/routers/`.
- **Safety:** Scoped to `week4/`; code-agent runs format/lint. Rollback: `git checkout -- week4/`.

**d. Before vs. after**

| Before | After |
|--------|-------|
| Mixed test + implementation in one agent pass; easy to skip edge cases | Explicit role split enforces failing-test-first and smaller diffs |

**e. How you used the automation to enhance the starter application**

> TODO (Part II)

---

### *(Optional) Automation #3 — `/docs-sync` + Open Library MCP

**a. Design inspiration**

Assignment Example 2 (Docs sync) and MCP category. Skill: `.cursor/skills/docs-sync/SKILL.md`. MCP: repo-root Open Library server in `.cursor/mcp.json`.

**b. Design (goals, inputs/outputs, steps)**

- **Goal:** Keep `week4/docs/API.md` aligned with `/openapi.json`; optional book lookup via MCP for data features.
- **Steps:** Start app → curl OpenAPI → update API.md → delta summary (added/changed/removed routes).

**c. How to run, expected outputs, rollback/safety**

- **Run:** `/docs-sync` in Agent chat (requires `make run` in week4).
- **MCP:** Enable **openlibrary** in Cursor Settings → MCP.
- **Safety:** Edits only `docs/API.md` by default.

**d. Before vs. after**

| Before | After |
|--------|-------|
| Task 7 marked “manual for now” | One skill regenerates endpoint docs and lists drift |

**e. How you used the automation to enhance the starter application**

> TODO (Part II)

---

## Cursor file map (Part I deliverables)

```
.cursor/skills/tests/SKILL.md       → /tests
.cursor/skills/docs-sync/SKILL.md   → /docs-sync
.cursor/agents/test-agent.md        → subagent
.cursor/agents/code-agent.md        → subagent
AGENTS.md                           → repo guidance (Cursor)
week4/AGENTS.md                     → week4 guidance
.cursor/mcp.json                    → Open Library MCP
```
