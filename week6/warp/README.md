# Week 6 — Warp automations

Importable Warp Drive workflows, agent prompts, rules, and a multi-agent playbook for this app.

All paths assume you run commands from `week6/`.

## Install into Warp Drive

1. Open Warp → Warp Drive panel.
2. **Import** each YAML under `workflows/` (or copy the command into a new Workflow).
3. Create **Prompts** from the markdown under `prompts/` (paste as Agent Mode prompts).
4. Add `rules/week6-agent-rules.md` as a Warp Rule (or paste into project rules).
5. For multi-agent work, follow `multi-agent/playbook.md` and run `multi-agent/worktree-setup.sh`.

## Automations in this folder

| ID | Category | Artifact |
|----|----------|----------|
| A1 | Warp Drive workflow | `workflows/week6-test-runner.yaml` |
| A2 | Warp Drive workflow + script | `workflows/week6-docs-sync.yaml`, `scripts/docs_sync.py` |
| A3 | Warp Drive rules | `rules/week6-agent-rules.md` |
| B1 | Multi-agent playbook | `multi-agent/playbook.md` + `prompts/` |

## Quick commands (without Warp UI)

```bash
cd week6
./warp/scripts/run_tests.sh
python warp/scripts/docs_sync.py   # app must be running on :8000
./warp/multi-agent/worktree-setup.sh
```
