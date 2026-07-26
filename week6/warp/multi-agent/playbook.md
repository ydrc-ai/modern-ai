# Multi-agent playbook (Warp tabs + git worktrees)

Run independent `docs/TASKS.md` items in parallel Warp Agent tabs without clobbering each other.

## Roles

| Tab / Agent | Role | Prompt | Typical task |
|-------------|------|--------|--------------|
| Tab A | test-agent | `prompts/week6-test-agent.md` | Write failing tests for Task N |
| Tab B | code-agent | `prompts/week6-code-agent.md` | Implement until green for Task M |
| Tab C | docs / QA | Workflow `week6-docs-sync` + `week6-test-runner` | Sync API.md + verify suite |

Challenge: open as many concurrent agents as your machine allows; isolate each with a worktree.

## Setup

From repo root (or `week6/`):

```bash
./week6/warp/multi-agent/worktree-setup.sh
```

This creates sibling worktrees:

- `../modern-ai-wt-task-a` on branch `week6/agent-a`
- `../modern-ai-wt-task-b` on branch `week6/agent-b`

Open each worktree path as the cwd in a separate Warp tab, paste the matching prompt, and assign different TASKS.md items.

## Coordination

1. Pick disjoint tasks (e.g. Task 3 notes CRUD vs Task 4 action-item filters).
2. Each agent commits only on its branch inside its worktree.
3. After both are green, merge sequentially into your main week6 branch and re-run `make test`.
4. Resolve conflicts in `schemas.py` / `frontend/app.js` carefully — those files are shared hotspots.

## Wins / risks

- **Win:** wall-clock time drops when tasks touch different routers.
- **Risk:** both agents editing `schemas.py` or `frontend/app.js` → merge conflicts.
- **Mitigation:** assign one agent “API-only” and another “UI-only”, or serialize shared files.
