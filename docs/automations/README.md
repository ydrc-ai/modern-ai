# Cursor automations (Week 4 assignment)

Part I deliverables for **Cursor** (no Claude Code required).

## Quick start

| Automation | Type | Run in Cursor Agent |
|------------|------|---------------------|
| Test runner | Skill (slash command) | `/tests` |
| API docs sync | Skill | `/docs-sync` |
| TDD workflow | Subagents | “Use **test-agent** then **code-agent** for Task N” |
| Project context | AGENTS.md | Auto-loaded; or `@AGENTS.md` |
| Book lookup | MCP | Settings → MCP → openlibrary |

## Part I vs Part II

- **Part I (done):** Files below + `week4/writeup.md` sections a–d
- **Part II (you):** Fill section **e** in `week4/writeup.md` after using automations on a TASKS.md item

## Suggested Part II task

Pick **Task 2** (`GET /notes/search?q=...`) from `week4/docs/TASKS.md`:

1. `/tests` — baseline (3 passed)
2. test-agent → code-agent — implement search
3. `/tests` — verify new tests green
4. `/docs-sync` — update API.md
5. Document in writeup section **e**
